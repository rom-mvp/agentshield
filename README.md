# AgentShield Proxy

A minimal PII-safe proxy on AWS (API Gateway + Lambda) using the Serverless Framework.  
It redacts emails & SSNs from request bodies and (optionally) tests Postgres connectivity.

## ✨ Features

- 🔒 **PII redaction**: emails → `[REDACTED_EMAIL]`, SSNs → `[REDACTED_SSN]`
- 🐘 **Optional DB check**: `SELECT 1` via `psycopg2` when `PG_DSN` is set
- 🔑 **API key required in prod** (via API Gateway usage plan)
- 🧱 **Tiny bundles**: deps live in an AWS Lambda Layer; function zip stays small
- 🛡️ **Security blocks**: Automatic blocking of admin DELETE operations

---

## 🚀 Quick Start

### Prerequisites

- Node 18+ and `npx`
- AWS CLI configured with deploy permissions
- Python 3.9 (only for building the psycopg2 layer)

### 1️⃣ Build the psycopg2 Layer

```bash
chmod +x build-psycopg2-layer.sh
./build-psycopg2-layer.sh
```

### 2️⃣ Deploy to AWS

```bash
# Install Serverless Framework globally
npm install -g serverless

# Deploy to development stage
serverless deploy --stage dev
```

### 3️⃣ Get Your API Key

```bash
# Make the script executable
chmod +x print-api-key.sh

# Get API key for development
./print-api-key.sh dev
```

### 4️⃣ Test Your Deployment

```bash
# Update the curl-test.sh with your actual API Gateway URL
# Replace <your-gateway-id> in the BASE URL

# Make executable and test
chmod +x curl-test.sh
export API_KEY="your-api-key-from-step-3"
./curl-test.sh dev
```

---

## 🧪 Example Request

```bash
curl -X POST "https://your-api.execute-api.us-east-2.amazonaws.com/dev/proxy/test" \
  -H "Content-Type: application/json" \
  -H "X-Agent-ID: test-agent" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "email": "user@example.com",
    "ssn": "123-45-6789", 
    "name": "John Doe"
  }'
```

### Example Response

```json
{
  "status": "processed",
  "agent_id": "test-agent", 
  "redacted": true,
  "body": {
    "email": "[REDACTED_EMAIL]",
    "ssn": "[REDACTED_SSN]",
    "name": "John Doe"
  }
}
```

---

## 🏗️ Architecture

```
API Gateway → Lambda Function → (Optional) PostgreSQL
     │              │
     │              └── PII Redaction
     │              └── Security Guards  
     │              └── DB Health Checks
     │
     └── API Key Validation
     └── CORS Handling
```

---

## 🔧 Configuration

### Environment Variables

- `PG_DSN`: PostgreSQL connection string (stored in AWS SSM)

### API Endpoints

- `POST /proxy/test` - Main proxy endpoint with optional DB check
- `DELETE /proxy/admin/drop` - Blocked endpoint (security demo)

---

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`) 
5. Open a Pull Request

---

## ⭐ Support AgentShield

If this project helped you, please give it a star on GitHub! ⭐

**Why starring matters:**
- Helps more developers discover AgentShield
- Shows appreciation for open-source work
- Motivates further development and features

### 📢 Share Your Experience

Tested AgentShield? We'd love to hear from you!
- **Open an issue** with feedback or feature requests
- **Share on social media** and tag #AgentShield
- **Tell your colleagues** about secure API proxying

---

## 🆘 Need Help?

- 📖 **Documentation**: Check this README
- 🐛 **Issues**: Open a GitHub issue
- 💬 **Discussions**: Start a GitHub discussion

---

**Ready to secure your APIs? Deploy AgentShield Proxy today! 🚀**

*Give us a star ⭐ if this project helps you build more secure applications!*
