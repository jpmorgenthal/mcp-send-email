# Email MCP Server

A Model Context Protocol (MCP) server for sending emails via SMTP with TLS encryption.

## Features

- Send emails with `to`, `cc`, `subject`, and `message` parameters
- Configurable SMTP server settings
- TLS encryption for secure email transmission
- Comprehensive error handling and validation

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure SMTP settings using one of these methods:

### Option A: Using .env file (Recommended)
Copy the example environment file and edit it:
```bash
cp .env.example .env
```

Edit `.env` with your SMTP configuration:
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Option B: Using environment variables
```bash
export SMTP_HOST="smtp.gmail.com"        # Default: smtp.gmail.com
export SMTP_PORT="587"                   # Default: 587
export SMTP_USERNAME="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
```

## Running the Server

1. Start the MCP server:
```bash
python email_mcp.py
```

The server will start on `http://127.0.0.1:8000` using SSE (Server-Sent Events) transport.

## Configuration with Claude Code

To use this remote MCP server with Claude Code, you need to configure it as a remote server:

### 1. Add to Claude Code Settings

Add the following to your Claude Code MCP configuration file (typically `~/.config/claude-code/mcp_servers.json`):

```json
{
  "mcpServers": {
    "email": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-everything",
        "mcp-remote",
        "http://127.0.0.1:8000"
      ]
    }
  }
}
```

### 2. Alternative: Using MCP CLI

You can also use the MCP CLI to connect to the remote server:

```bash
npx @modelcontextprotocol/cli mcp-remote http://127.0.0.1:8000
```

### 3. Docker Configuration (Optional)

For containerized deployment, you can use Docker:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "email_mcp.py"]
```

Build and run:
```bash
docker build -t email-mcp .
docker run -p 8000:8000 --env-file .env email-mcp
```

## Usage

Once configured, you can use the email tool in Claude Code:

```
Send an email to john@example.com with subject "Hello" and message "This is a test email"
```

The tool supports:
- **to**: Recipient email address (required)
- **cc**: CC email address (optional)
- **subject**: Email subject line (required)
- **message**: Email message body (required)

## SMTP Configuration

### Gmail Setup
1. Enable 2-factor authentication
2. Generate an app password
3. Use the app password as `SMTP_PASSWORD`

### Other SMTP Providers
- **Outlook**: `smtp-mail.outlook.com:587`
- **Yahoo**: `smtp.mail.yahoo.com:587`
- **Custom SMTP**: Configure `SMTP_HOST` and `SMTP_PORT` accordingly

## Security

- Uses TLS encryption for all email transmission
- Credentials are stored as environment variables
- No sensitive data is logged or exposed

## Error Handling

The server provides detailed error messages for:
- Missing SMTP credentials
- Authentication failures
- Invalid email addresses
- Network connectivity issues
- SMTP server errors