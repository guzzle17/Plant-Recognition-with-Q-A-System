# PlantBot Backend API

An AI-powered plant care assistant API built with FastAPI and AWS Bedrock (Claude models).

## 🌱 Features

- **AI-Powered Plant Advice**: Get expert plant care recommendations using Claude AI
- **Streaming Support**: Real-time streaming responses for better UX
- **Clean Architecture**: Modular, scalable, and maintainable codebase
- **Production-Ready**: Comprehensive error handling, logging, and retry logic
- **AWS Bedrock Integration**: Leverages Claude 3 models via AWS Bedrock
- **CORS Enabled**: Ready for frontend integration

## 📋 Prerequisites

- Python 3.9 or higher
- AWS Account with Bedrock access
- AWS credentials with Bedrock permissions

## 🚀 Quick Start

### 1. Clone and Setup

```bash
cd plantbot-backend
python -m venv .venv
```

### 2. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy `.env.example` to `.env` and fill in your AWS credentials:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
BEDROCK_MODEL_ID=anthropic.claude-3-haiku-20240307-v1:0
```

### 5. Run the Server

```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## 📚 API Documentation

Once the server is running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 API Endpoints

### Health Check
```http
GET /api/v1/health
```

Returns API health status and version information.

### Chat (Standard)
```http
POST /api/v1/chat
Content-Type: application/json

{
  "message": "How do I care for a succulent?",
  "stream": false
}
```

### Chat (Streaming)
```http
POST /api/v1/chat
Content-Type: application/json

{
  "message": "How do I care for a succulent?",
  "stream": true
}
```

## 🏗️ Project Structure

```
plantbot-backend/
├── app/
│   ├── api/              # API layer
│   │   ├── dependencies.py
│   │   └── v1/
│   │       ├── router.py
│   │       └── endpoints/
│   │           ├── health.py
│   │           └── chat.py
│   ├── core/             # Core configuration
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   ├── logging.py
│   │   └── prompts.py
│   ├── models/           # Pydantic models
│   │   ├── chat.py
│   │   └── health.py
│   ├── services/         # Business logic
│   │   └── chat_service.py  # Uses langchain_aws
│   └── utils/            # Utilities
│       └── aws.py
├── tests/                # Test suite
├── main.py               # Entry point
└── requirements.txt
```

## 🧪 Testing

Use the provided `test_main.http` file with tools like:
- VS Code REST Client extension
- JetBrains HTTP Client
- Or any HTTP client (curl, Postman, etc.)

## ⚙️ Configuration

All configuration is managed through environment variables. See `.env.example` for all options.

### Key Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `AWS_REGION` | AWS region for Bedrock | Required |
| `AWS_ACCESS_KEY_ID` | AWS access key | Required |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | Required |
| `BEDROCK_MODEL_ID` | Claude model ID | claude-3-haiku |
| `BEDROCK_MAX_TOKENS` | Max tokens per response | 3000 |
| `LOG_LEVEL` | Logging level | INFO |
| `CORS_ORIGINS` | Allowed CORS origins | localhost:3000 |

## 🔒 Security Best Practices

1. **Never commit `.env` file** - Keep credentials secure
2. **Use IAM roles** in production instead of access keys
3. **Rotate credentials** regularly
4. **Limit CORS origins** to trusted domains
5. **Enable rate limiting** for production use

## 📈 Performance Tips

1. **Streaming responses** for better user experience with long responses
2. **Automatic retry logic** handles transient AWS failures
3. **Connection pooling** via boto3 for efficient AWS API calls
4. **Dependency caching** via `@lru_cache` decorators

## 🐛 Troubleshooting

### "500 Internal Server Error"
- Check `.env` file exists and has valid AWS credentials
- Verify AWS Bedrock access in your region
- Check logs for detailed error messages

### "Service unavailable"
- AWS Bedrock might be experiencing issues
- Check your AWS region configuration
- Verify network connectivity to AWS

### Import Errors
```bash
pip install -r requirements.txt --force-reinstall
```

## 📝 License

[Your License Here]

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.

## 📧 Support

For issues or questions, please open a GitHub issue.

