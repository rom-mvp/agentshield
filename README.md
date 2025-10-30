# AgentShield Proxy

A minimal PII-safe proxy on AWS (API Gateway + Lambda) using the Serverless Framework.  
It redacts emails & SSNs from request bodies and (optionally) tests Postgres connectivity.

## ✨ Features
- 🔒 **PII redaction**: emails → `[REDACTED_EMAIL]`, SSNs → `[REDACTED_SSN]`
- 🐘 **Optional DB check**: `SELECT 1` via `psycopg2` when `PG_DSN` is set
- 🔑 **API key** required in **prod** (via API Gateway usage plan)
- 🧱 **Tiny bundles**: deps live in an AWS Lambda Layer; function zip stays small

---

## 🚀 Quick start

### Prereqs
- Node 18+ and `npx`
- AWS CLI configured with deploy permissions
- Python 3.9 (only for building the psycopg2 layer)

### 1️⃣ Build the psycopg2 layer
```bash
./build-psycopg2-layer.sh
# Add to your README.md:

## Quick Deploy
```bash
npm install -g serverless
./build-psycopg2-layer.sh
serverless deploy --stage dev
