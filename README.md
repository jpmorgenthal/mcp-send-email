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

## Configuration with Claude Code

To use this MCP server with Claude Code, add it to your MCP configuration:

### 1. Add to Claude Code Settings

Add the following to your Claude Code MCP configuration file (typically `~/.config/claude-code/mcp_servers.json`):

```json
{
  "mcpServers": {
    "email": {
      "command": "python",
      "args": ["/path/to/your/email_mcp.py"],
      "env": {
        "SMTP_HOST": "smtp.gmail.com",
        "SMTP_PORT": "587",
        "SMTP_USERNAME": "your-email@gmail.com",
        "SMTP_PASSWORD": "your-app-password"
      }
    }
  }
}
```

### 2. Using .env file (Recommended)

If you have a `.env` file in the same directory as `email_mcp.py`, use this simpler configuration:

```json
{
  "mcpServers": {
    "email": {
      "command": "python",
      "args": ["/path/to/your/email_mcp.py"]
    }
  }
}
```

The app will automatically load settings from your `.env` file.

### 3. Alternative: Global Environment Variables

Set environment variables globally and use the same simple configuration:

```bash
# Add to your shell profile (.bashrc, .zshrc, etc.)
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USERNAME="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
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