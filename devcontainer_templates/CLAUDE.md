# Devcontainer Templates

This directory contains two devcontainer templates:

- `.devcontainer/` — base template (cross-platform)
- `.devcontainer_audio/` — audio variant with PulseAudio
  passthrough (Linux only)

## Keeping Templates in Sync

`.devcontainer_audio/` is a superset of `.devcontainer/`.
When editing shared files (Dockerfile, devcontainer.json,
post-create.sh, post-start.sh, init-env, init-env.cmd),
apply the same change to both templates. The only
differences in the audio variant should be audio-specific:

- **Dockerfile**: `pulseaudio-utils`, `alsa-utils`,
  `libasound2-plugins` packages and the ALSA-to-PulseAudio
  `/etc/asound.conf` config
- **devcontainer.json**: PulseAudio socket bind mounts and
  `PULSE_SERVER` container env var

Everything else must stay identical. If the templates drift
on non-audio changes, one of them has a bug.
