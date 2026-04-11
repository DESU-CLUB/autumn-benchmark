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
LABEL Description="Autumn usage_quota_hard_limit task: Express.js project with autumn-js for API metering."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    cat >package.json <<'EOF'
{
  "name": "myproject",
  "version": "1.0.0",
  "type": "module",
  "description": "Autumn API quota demo"
}
EOF

RUN cd /home/user/myproject && npm install autumn-js express

RUN cat >/home/user/myproject/index.js <<'EOF'
import express from 'express';

const app = express();
app.use(express.json());

app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
EOF

ENV AUTUMN_SECRET_KEY="am_sk_test_placeholder"

# Container contents:
#   - Node.js v24 runtime
#   - /home/user/myproject — Express.js project with health route
#   - autumn-js and express installed
#   - AUTUMN_SECRET_KEY env variable (placeholder, override at runtime)

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
