FROM ubuntu:20.04

WORKDIR /playground

# Ignore installation prompts
ENV DEBIAN_FRONTEND=noninteractive

# Verify system packages are updated
RUN apt-get update -y && apt-get upgrade -y

# Remove unnecessary packages
RUN apt-get autoclean -y && apt-get autoremove -y

# INSTALL BACKEND REQUIREMENTS
# ==================================
RUN apt-get install -y \
  python3 \
  pip \
  curl

COPY src/server/requirements.txt src/server/requirements.txt
RUN pip install -r src/server/requirements.txt

# Install httpie
RUN curl -SsL https://packages.httpie.io/deb/KEY.gpg | gpg --dearmor -o /usr/share/keyrings/httpie.gpg
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/httpie.gpg] https://packages.httpie.io/deb ./" > /etc/apt/sources.list.d/httpie.list
RUN apt-get update -y && apt-get install -y httpie

# INSTALL FRONTEND REQUIREMENTS
# ==================================
RUN apt install -y \
  ca-certificates \
  gnupg

# Install latest version of node
RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
RUN NODE_MAJOR=20 && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list
RUN apt update -y && apt install -y nodejs

COPY src/client/package.json src/client/package.json
RUN cd src/client && npm install

COPY . .