---
paths:
  - "**/Cargo.toml"
---

# Required Clippy Lints for Rust Crates

When creating or modifying a `Cargo.toml`, first determine
whether it is a **workspace** root or a **crate** manifest.
A workspace root contains `[workspace]`; a crate manifest
contains `[package]`. The lint configuration syntax differs
between the two — using the wrong one is a silent error
that Cargo ignores without warning.

## Crate `Cargo.toml` (has `[package]`)

Add these lints under `[lints.clippy]`:

```toml
[lints.clippy]
indexing_slicing = "deny"       # panics on out-of-bounds — use .get() instead
fallible_impl_from = "deny"     # From impls that can panic — use TryFrom
wildcard_enum_match_arm = "deny" # silently ignores new variants when enum grows
unneeded_field_pattern = "deny" # dead pattern arms that hide refactoring bugs
fn_params_excessive_bools = "deny" # boolean params are easy to swap — use enums
must_use_candidate = "deny"     # functions whose return value should not be ignored
```

If the crate inherits lints from the workspace
(`lints.workspace = true`), do not add a `[lints.clippy]`
section — the workspace already defines the lints.

## Workspace `Cargo.toml` (has `[workspace]`)

Add these lints under `[workspace.lints.clippy]`:

```toml
[workspace.lints.clippy]
indexing_slicing = "deny"
fallible_impl_from = "deny"
wildcard_enum_match_arm = "deny"
unneeded_field_pattern = "deny"
fn_params_excessive_bools = "deny"
must_use_candidate = "deny"
```

Member crates inherit these by adding `lints.workspace =
true` to their own `Cargo.toml`. Prefer workspace-level
lints in multi-crate projects — they enforce consistency
and avoid duplicating config across crates.

## Merging

If the file already has a lints section, merge these
entries into it. If any lint conflicts with an existing
entry, keep the stricter setting (`"deny"` over `"warn"`
over `"allow"`).

This is an example of a conditional rule — it only activates
when an agent reads or writes a file matching the `paths`
glob. Projects should add similar rules for their own
conventions (e.g., required ESLint config, Python linter
settings, Go build tags).
