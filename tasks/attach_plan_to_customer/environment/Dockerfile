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
LABEL Description="Autumn attach_plan_to_customer task: Node.js project with autumn-js for parallel customer onboarding."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    cat >package.json <<'EOF'
{
  "name": "myproject",
  "version": "1.0.0",
  "type": "module",
  "description": "Autumn plan attachment demo"
}
EOF

RUN cd /home/user/myproject && npm install autumn-js

ENV AUTUMN_SECRET_KEY="am_sk_test_placeholder"

# Container contents:
#   - Node.js v24 runtime
#   - /home/user/myproject — Node.js ES module project
#   - autumn-js npm package installed
#   - AUTUMN_SECRET_KEY env variable (placeholder, override at runtime)

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
