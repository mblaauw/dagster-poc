FROM ubuntu:22.04

# Prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Install base system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    git \
    vim \
    nano \
    tmux \
    htop \
    jq \
    python3 \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    postgresql-client \
    libpq-dev \
    s3fs \
    fuse \
    openssh-client \
    sudo \
    apt-transport-https \
    gnupg \
    lsb-release \
    netcat \
    unzip \
    iputils-ping \
    dnsutils \
    && rm -rf /var/lib/apt/lists/*

# Install Docker CLI (no daemon, just client tools)
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list \
    && apt-get update && apt-get install -y docker-ce-cli \
    && rm -rf /var/lib/apt/lists/*

# Install kubectl directly
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl" \
    && chmod +x kubectl \
    && mv kubectl /usr/local/bin/

# Install Helm
RUN curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash

# Install MinIO client
RUN wget https://dl.min.io/client/mc/release/linux-amd64/mc -O /usr/local/bin/mc \
    && chmod +x /usr/local/bin/mc

# Set up Python environment
RUN pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir \
    ipython \
    jupyter \
    notebook \
    pytest \
    black \
    isort \
    flake8 \
    pylint \
    mypy \
    dagster \
    dagster-graphql \
    dagster-webserver \
    polars \
    pyarrow \
    pandas \
    numpy \
    scipy \
    matplotlib \
    seaborn \
    scikit-learn \
    duckdb \
    duckdb-engine \
    deltalake \
    mlflow \
    psycopg2-binary \
    sqlalchemy \
    httpie \
    boto3 \
    s3fs

# Install code-server
RUN curl -fsSL https://code-server.dev/install.sh | sh

# Install Node.js and React development tools
RUN npm install -g create-react-app typescript eslint prettier
RUN useradd -m -s /bin/bash -G sudo coder \
    && echo "coder ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Set up pre-commit hooks configuration
RUN mkdir -p /etc/skel/.git-templates/hooks \
    && echo '#!/bin/sh\n\npython3 -m black --check .\npython3 -m isort --check .\npython3 -m flake8 .\n' > /etc/skel/.git-templates/hooks/pre-commit \
    && chmod +x /etc/skel/.git-templates/hooks/pre-commit

# Copy default configuration files and templates
# Create minimal default configuration rather than copying
RUN echo 'alias k="kubectl"' > /etc/skel/.bashrc
RUN echo 'alias mc="mc --insecure"' >> /etc/skel/.bashrc
RUN mkdir -p /etc/skel/templates
RUN mkdir -p /etc/skel/.vscode-server/data/Machine

# Create default settings.json for VSCode
RUN echo '{\n  "editor.formatOnSave": true,\n  "python.linting.enabled": true,\n  "python.formatting.provider": "black"\n}' > /etc/skel/.vscode-server/data/Machine/settings.json

# Create required directories with proper permissions
RUN mkdir -p /home/coder/.local/share/code-server/{extensions,User,Machine,logs,User/globalStorage,User/History} && \
    mkdir -p /home/coder/.config && \
    chown -R coder:coder /home/coder/.local && \
    chown -R coder:coder /home/coder/.config
RUN echo "#!/bin/bash\n\
# Install VS Code extensions at runtime\n\
code-server --install-extension ms-python.python\n\
code-server --install-extension ms-toolsai.jupyter\n\
code-server --install-extension eamodio.gitlens\n\
code-server --install-extension njpwerner.autodocstring\n\
code-server --install-extension ms-python.vscode-pylance\n\
exec \"\$@\"\n" > /usr/local/bin/entrypoint.sh && chmod +x /usr/local/bin/entrypoint.sh

# Setup workspace directory
RUN mkdir -p /home/coder/workspace
WORKDIR /home/coder/workspace

USER root
# Set up environment variables
ENV PATH="/home/coder/.local/bin:${PATH}"
ENV PYTHONPATH="/home/coder/workspace"

USER coder

# Expose default code-server port
EXPOSE 8080

# Use our entrypoint script to install extensions at runtime
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Command to start code-server
CMD ["code-server", "--auth", "none", "--bind-addr", "0.0.0.0:8080", "."]