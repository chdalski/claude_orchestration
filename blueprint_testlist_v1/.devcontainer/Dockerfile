FROM node:20

ARG TZ
ENV TZ="$TZ"

ARG CLAUDE_CODE_VERSION=latest
ARG USER_UID=1000
ARG USER_GID=1000

# Install basic development tools and iptables/ipset
RUN apt-get update && apt-get install -y --no-install-recommends \
    less \
    git \
    procps \
    sudo \
    fzf \
    zsh \
    man-db \
    unzip \
    gnupg2 \
    gh \
    iptables \
    ipset \
    iproute2 \
    dnsutils \
    aggregate \
    jq \
    nano \
    vim \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Remap the node user's UID/GID to match the host user. This ensures
# bind-mounted files from the host are readable and writable inside
# the container without permission mismatches. The node:20 base image
# ships with node:node at 1000:1000 — if the host user differs, we
# need to remap. Handle collisions where the target GID/UID is already
# taken by a different system user/group.
RUN if [ "$USER_GID" != "$(id -g node)" ]; then \
        if getent group "$USER_GID" > /dev/null 2>&1; then \
            CONFLICTING_GROUP=$(getent group "$USER_GID" | cut -d: -f1); \
            groupmod -g 99999 "$CONFLICTING_GROUP"; \
        fi; \
        groupmod -g "$USER_GID" node; \
    fi && \
    if [ "$USER_UID" != "$(id -u node)" ]; then \
        if getent passwd "$USER_UID" > /dev/null 2>&1; then \
            CONFLICTING_USER=$(getent passwd "$USER_UID" | cut -d: -f1); \
            usermod -u 99999 "$CONFLICTING_USER"; \
        fi; \
        usermod -u "$USER_UID" node; \
    fi && \
    chown -R node:node /home/node

# Ensure default node user has access to /usr/local/share
RUN mkdir -p /usr/local/share/npm-global && \
    chown -R node:node /usr/local/share

ARG USERNAME=node

# Persist bash history.
RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    && mkdir /commandhistory \
    && touch /commandhistory/.bash_history \
    && chown -R $USERNAME /commandhistory

# Set `DEVCONTAINER` environment variable to help with orientation
ENV DEVCONTAINER=true

# Create workspace directory and set permissions
RUN mkdir -p /workspace && \
    chown -R node:node /workspace

WORKDIR /workspace

ARG GIT_DELTA_VERSION=0.18.2
RUN ARCH=$(dpkg --print-architecture) && \
    wget "https://github.com/dandavison/delta/releases/download/${GIT_DELTA_VERSION}/git-delta_${GIT_DELTA_VERSION}_${ARCH}.deb" && \
    sudo dpkg -i "git-delta_${GIT_DELTA_VERSION}_${ARCH}.deb" && \
    rm "git-delta_${GIT_DELTA_VERSION}_${ARCH}.deb"

# Set up non-root user
USER node

# Install global packages
ENV NPM_CONFIG_PREFIX=/usr/local/share/npm-global
ENV PATH=$PATH:/usr/local/share/npm-global/bin

# Set the default shell to zsh rather than sh
ENV SHELL=/bin/zsh

# Set the default editor and visual
ENV EDITOR=nano
ENV VISUAL=nano

# Default powerline10k theme
ARG ZSH_IN_DOCKER_VERSION=1.2.0
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v${ZSH_IN_DOCKER_VERSION}/zsh-in-docker.sh)" -- \
    -p git \
    -p fzf \
    -a "source /usr/share/doc/fzf/examples/key-bindings.zsh" \
    -a "source /usr/share/doc/fzf/examples/completion.zsh" \
    -a "export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    -x

# Install Claude
RUN npm install -g @anthropic-ai/claude-code@${CLAUDE_CODE_VERSION}


# Copy firewall script (allowed-domains.conf is bind-mounted at
# runtime so changes take effect on container restart without rebuild)
COPY init-firewall.sh /usr/local/bin/
USER root
RUN chmod +x /usr/local/bin/init-firewall.sh && \
    echo "node ALL=(root) NOPASSWD: /usr/local/bin/init-firewall.sh" > /etc/sudoers.d/node-firewall && \
    chmod 0440 /etc/sudoers.d/node-firewall
USER node
