#!/usr/bin/env python3
"""
Prompt Caching Proxy for Claude API
Uses mitmproxy to inject cache_control blocks into system messages
"""

import json
import os
import sys
from datetime import datetime

from mitmproxy import http
from mitmproxy.tools.main import mitmdump


# Configuration from environment
TARGET_URL = os.getenv("TARGET_URL", "https://api.portkey.ai")
MIN_CACHE_CHARS = int(os.getenv("MIN_CACHE_CHARS", "1024"))
PROXY_PORT = int(os.getenv("PROXY_PORT", "3000"))


def log(message: str, prefix: str = "INFO"):
    """Log with timestamp to stdout"""
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] {prefix}: {message}", flush=True)


def log_cache_injection(system_blocks: int, cached_count: int):
    """Log cache injection statistics"""
    log("Cache injection:")
    log(f"  - Total system blocks: {system_blocks}")
    log(f"  - Blocks marked for caching: {cached_count}")


def log_cache_stats(usage: dict):
    """Log cache usage statistics from API response"""
    if not usage:
        return

    cache_creation = usage.get("cache_creation_input_tokens", 0)
    cache_read = usage.get("cache_read_input_tokens", 0)
    total_input = usage.get("input_tokens", 0)

    if cache_creation > 0 or cache_read > 0:
        log("Cache stats:")
        log(f"  - Cache creation tokens: {cache_creation}")
        log(f"  - Cache read tokens: {cache_read}")
        log(f"  - Total input tokens: {total_input}")

        if cache_read > 0 and total_input > 0:
            savings = round((cache_read * 0.9 / total_input) * 100)
            log(f"  - Estimated savings: ~{savings}% on cached tokens")


class PromptCachingAddon:
    """Mitmproxy addon that injects cache_control into Claude API requests"""

    def __init__(self):
        self.target_host = (
            TARGET_URL.replace("https://", "").replace("http://", "").split("/")[0]
        )

    def request(self, flow: http.HTTPFlow) -> None:
        """Intercept requests to /v1/messages and inject cache_control"""

        log(f"Received request: {flow.request.method} {flow.request.path}")

        # Match messages endpoint (handles /v1/messages, /messages, etc.)
        if "messages" not in flow.request.path:
            log("  - Skipping (not a messages endpoint)")
            return

        log("Processing messages request")

        try:
            # Parse request body
            body = json.loads(flow.request.content)

            cached_block_count = 0

            # Strip parameters not supported by Bedrock
            unsupported_params = ["output_config", "thinking"]
            stripped = []
            for param in unsupported_params:
                if param in body:
                    stripped.append(param)
                    del body[param]
            if stripped:
                log(f"  - Stripped Bedrock-unsupported params: {stripped}")

            # Inject cache_control into system messages
            if "system" in body and isinstance(body["system"], list):
                modified_system = []

                for index, block in enumerate(body["system"]):
                    # Only cache text blocks above minimum size
                    if (
                        block.get("type") == "text"
                        and "text" in block
                        and len(block["text"]) > MIN_CACHE_CHARS
                    ):
                        cached_block_count += 1
                        log(
                            f"  - Caching system block {index + 1} ({len(block['text'])} chars)"
                        )

                        modified_block = {
                            **block,
                            "cache_control": {"type": "ephemeral"},
                        }
                        modified_system.append(modified_block)
                    else:
                        modified_system.append(block)

                body["system"] = modified_system
                log_cache_injection(len(body["system"]), cached_block_count)

            # Add required header for prompt caching
            flow.request.headers["anthropic-beta"] = "prompt-caching-2024-07-31"

            # Update request body
            flow.request.content = json.dumps(body).encode("utf-8")
            flow.request.headers["content-length"] = str(len(flow.request.content))

        except json.JSONDecodeError as e:
            log(f"Failed to parse request JSON: {e}", "ERROR")
        except Exception as e:
            log(f"Error processing request: {e}", "ERROR")

    def response(self, flow: http.HTTPFlow) -> None:
        """Log cache statistics from API responses"""

        # Only process messages endpoint
        if "messages" not in flow.request.path:
            return

        try:
            body = json.loads(flow.response.content)
            if "usage" in body:
                log_cache_stats(body["usage"])
        except json.JSONDecodeError:
            # Not JSON or streaming response - ignore
            pass
        except Exception as e:
            log(f"Error processing response: {e}", "ERROR")

    def error(self, flow: http.HTTPFlow) -> None:
        """Handle proxy errors"""
        if flow.error:
            log(f"Proxy error: {flow.error.msg}", "ERROR")


def start_proxy():
    """Start the mitmproxy server"""
    log("=" * 60)
    log("Prompt Caching Proxy Started")
    log("=" * 60)
    log(f"Listening on: http://0.0.0.0:{PROXY_PORT}")
    log(f"Proxying to: {TARGET_URL}")
    log(f"Min cache size: {MIN_CACHE_CHARS} characters")
    log("=" * 60)

    # Start mitmdump with our addon
    sys.argv = [
        "mitmdump",
        "--mode",
        f"reverse:{TARGET_URL}",
        "--listen-host",
        "0.0.0.0",
        "--listen-port",
        str(PROXY_PORT),
        "--set",
        "connection_strategy=lazy",
        "--set",
        "stream_large_bodies=1m",
        "--set",
        "websocket=false",
        "--ssl-insecure",
        "-s",
        __file__,
    ]

    mitmdump()


addons = [PromptCachingAddon()]


if __name__ == "__main__":
    start_proxy()
