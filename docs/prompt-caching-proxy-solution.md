# Prompt Caching Proxy Solution for Claude Code

## Problem Statement

Claude Code does not expose `cache_control` parameters for enabling Anthropic's prompt caching feature when spawning agents. This means multi-agent orchestration workflows cannot take advantage of ~90% cost savings on repeated context tokens.

## Background: How Prompt Caching Works

Prompt caching requires modifying API requests to include:

### 1. Required Header

```bash
anthropic-beta: prompt-caching-2024-07-31
```

### 2. Request Body Modifications

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "system": [
    {
      "type": "text",
      "text": "Large system prompt here...",
      "cache_control": {"type": "ephemeral"}
    }
  ],
  "messages": [...]
}
```

### Cache Requirements

- **TTL**: 5 minutes (fixed)
- **Minimum size**:
  - Sonnet/Opus: 1,024 tokens
  - Haiku: 2,048 tokens
- **Savings**: ~90% cost reduction on cached tokens

## Solution: HTTP Proxy Interceptor

Create a local proxy that sits between Claude Code and your API gateway (e.g., Portkey), intercepting requests to inject `cache_control` parameters.

### Architecture

```
Claude Code → Local Proxy (localhost:3000) → Portkey → Anthropic
              ↑
         Injects cache_control
         Adds anthropic-beta header
```

## Implementation Options

### Option 1: Express + http-proxy-middleware (Recommended)

**File: `cache-proxy.js`**

```javascript
import express from 'express'
import { createProxyMiddleware } from 'http-proxy-middleware'

const app = express()

app.use('/v1/messages', express.json(), (req, res, next) => {
  // Inject cache_control into system messages
  if (req.body.system) {
    req.body.system = req.body.system.map(block => {
      // Only cache text blocks > 1024 characters (rough token estimate)
      if (block.type === 'text' && block.text.length > 1024) {
        return {
          ...block,
          cache_control: { type: 'ephemeral' }
        }
      }
      return block
    })
  }

  // Add required header
  req.headers['anthropic-beta'] = 'prompt-caching-2024-07-31'

  next()
}, createProxyMiddleware({
  target: 'https://api.portkey.ai',
  changeOrigin: true,
  onProxyReq: (proxyReq, req) => {
    if (req.body) {
      const bodyData = JSON.stringify(req.body)
      proxyReq.setHeader('Content-Length', Buffer.byteLength(bodyData))
      proxyReq.write(bodyData)
    }
  }
}))

app.listen(3000, () => {
  console.log('Cache proxy running on http://localhost:3000')
})
```

**Installation:**

```bash
npm install express http-proxy-middleware
node cache-proxy.js
```

### Option 2: mitmproxy (Most Powerful)

**File: `cache_injector.py`**

```python
from mitmproxy import http
import json

def request(flow: http.HTTPFlow) -> None:
    if "api.portkey.ai" in flow.request.pretty_host:
        if flow.request.path.startswith("/v1/messages"):
            # Parse request body
            body = json.loads(flow.request.content)

            # Inject cache_control
            if "system" in body:
                for block in body["system"]:
                    if block.get("type") == "text":
                        # Only cache blocks > 1024 chars
                        if len(block.get("text", "")) > 1024:
                            block["cache_control"] = {"type": "ephemeral"}

            # Update request
            flow.request.content = json.dumps(body).encode()
            flow.request.headers["anthropic-beta"] = "prompt-caching-2024-07-31"
```

**Usage:**

```bash
pip install mitmproxy
mitmproxy -s cache_injector.py --listen-port 8080
```

## Claude Code Configuration

Update `~/.claude/settings.json` to point at your proxy:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:3000",
    "ANTHROPIC_AUTH_TOKEN": "dummy",
    "ANTHROPIC_CUSTOM_HEADERS": "x-portkey-api-key: YOUR_PORTKEY_KEY"
  }
}
```

**Note**: If using mitmproxy on port 8080, change `localhost:3000` to `localhost:8080`.

## Smart Caching Strategies

### Strategy 1: Cache Only Large System Prompts

```javascript
if (req.body.system) {
  // Cache only the last system block (Anthropic's recommendation)
  const lastBlock = req.body.system[req.body.system.length - 1]
  if (lastBlock.text.length > 1024) {
    lastBlock.cache_control = { type: 'ephemeral' }
  }
}
```

### Strategy 2: Cache All System Messages Above Threshold

```javascript
if (req.body.system) {
  req.body.system = req.body.system.map(block => {
    if (block.type === 'text' && block.text.length > 1024) {
      return { ...block, cache_control: { type: 'ephemeral' } }
    }
    return block
  })
}
```

### Strategy 3: Cache User Messages Too

```javascript
// Cache large user messages (e.g., pasted code)
if (req.body.messages) {
  req.body.messages = req.body.messages.map(msg => {
    if (msg.content && Array.isArray(msg.content)) {
      msg.content = msg.content.map(block => {
        if (block.type === 'text' && block.text.length > 2048) {
          return { ...block, cache_control: { type: 'ephemeral' } }
        }
        return block
      })
    }
    return msg
  })
}
```

## Monitoring Cache Performance

### With Portkey

Portkey's dashboard shows:

- `cache_creation_input_tokens`: New cache entries written
- `cache_read_input_tokens`: Cached tokens retrieved

### With Custom Logging

Add logging to your proxy:

```javascript
app.use((req, res, next) => {
  const originalSend = res.send
  res.send = function(data) {
    try {
      const body = JSON.parse(data)
      if (body.usage) {
        console.log('Cache stats:', {
          cache_creation_tokens: body.usage.cache_creation_input_tokens || 0,
          cache_read_tokens: body.usage.cache_read_input_tokens || 0,
          total_tokens: body.usage.input_tokens
        })
      }
    } catch (e) {}
    originalSend.call(this, data)
  }
  next()
})
```

## Considerations

### Pros

- ✅ No changes to Claude Code needed
- ✅ Works with existing Portkey setup
- ✅ Easy to test and iterate
- ✅ Low latency overhead (~1-5ms)
- ✅ Can be customized for specific use cases

### Cons

- ❌ Character count is imprecise for token estimation
- ❌ Requires running a separate process
- ❌ Needs maintenance if Anthropic changes the API
- ❌ Another point of failure in the chain

### Security

- Local proxy is safe (no external exposure)
- Don't log sensitive request/response data
- Consider using environment variables for API keys

## Testing

### 1. Start the Proxy

```bash
node cache-proxy.js
```

### 2. Test with Claude Code

```bash
cd /path/to/test-project
claude
# Spawn agents and verify caching is working
```

### 3. Monitor Cache Hits

Check Portkey dashboard or proxy logs for cache statistics.

## Why This Is Needed for Multi-Agent Orchestration

In the Claude Orchestration Kit blueprints:

- Each agent has large system prompts (knowledge base + practices + agent definitions)
- System prompts are **identical across turns** for the same agent
- Agents are spawned multiple times in a session
- 5-minute cache TTL covers typical session duration

**Potential savings**: 90% reduction on system prompt tokens across all agent turns.

## References

- [Anthropic Prompt Caching Documentation](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [Portkey Prompt Caching Support](https://portkey.ai/docs/integrations/llms/anthropic/prompt-caching)
- [mitmproxy Documentation](https://docs.mitmproxy.org/)
- [http-proxy-middleware GitHub](https://github.com/chimurai/http-proxy-middleware)

## Future Improvements

1. **Token-accurate counting**: Use Anthropic's tokenizer for precise 1024-token threshold
2. **Automatic cache detection**: Analyze response headers to verify caching is working
3. **Cost tracking**: Calculate actual savings from cache hits
4. **Configuration file**: Make caching strategy configurable
5. **Request Claude Code feature**: Submit feature request to Anthropic for native support

---

**Last Updated**: 2026-02-26
