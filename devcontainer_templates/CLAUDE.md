# Devcontainer Template

`.devcontainer/` is the single devcontainer template. The
repo's root `.devcontainer` is a symlink to it, so every
change here also changes this repo's own devcontainer.

PulseAudio passthrough lives in `docker-compose.audio.yml`,
loaded by default from `devcontainer.json`. Keep audio-only
settings in that file so that removing its
`dockerComposeFile` entry turns audio off completely. The
audio packages in the Dockerfile are the one exception —
they are inert without the overlay.

## Invariants

- **Read-only host binds go in `docker-compose.yml`, never
  in `devcontainer.json` `mounts`.** On the Compose path the
  devcontainer CLI drops `readonly` from `mounts` entries —
  the bind silently becomes writable and exposes the host's
  `~/.claude` to the sandbox.
- **Named volumes in `mounts` are named
  `<purpose>-${devcontainerId}`.** Compose already prefixes
  the project name (`<folder>_devcontainer_`); adding the
  folder name again doubles it.
- **No `name:` or `container_name:` in
  `docker-compose.yml`.** A fixed name makes every checkout
  of a project share one container.
- **Never add `.env.credentials` to `env_file`.** The CLI
  prints the resolved Compose config, env_file values
  included, in its start log. Only fish reads that file.
- **No secrets and no `$` in `.env.defaults`.** Its values
  appear in the start log, and Compose expands `$VAR` in
  them from the host environment.
- **Unattended plugin installs stay limited to
  `claude-plugins-official`** (`setup_plugins` in
  `post-start.sh`) — whoever can write the project's
  `settings.json` decides what that step installs.

## Documentation

Changes to files, env keys, volumes, or mounts must also
update `.devcontainer/README.md` and the Devcontainer
Templates section of the root `README.md`.
