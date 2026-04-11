FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Autumn get_or_create_customer task: Node.js project with autumn-js installed."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    cat >package.json <<'EOF'
{
  "name": "myproject",
  "version": "1.0.0",
  "type": "module",
  "description": "Autumn billing SDK demo",
  "main": "index.js"
}
EOF

RUN cd /home/user/myproject && npm install autumn-js

ENV AUTUMN_SECRET_KEY="am_sk_test_placeholder"

# Container contents:
#   - Node.js v24 runtime
#   - /home/user/myproject — Node.js project with type=module
#   - autumn-js npm package installed
#   - AUTUMN_SECRET_KEY env variable set (placeholder, should be overridden at runtime)

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
