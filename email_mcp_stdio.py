#!/usr/bin/env python3
"""
Email MCP Server - A tool for sending emails via SMTP with TLS support
Stdio version for Claude Desktop
"""
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables from .env file
load_dotenv()

# Initialize SMTP configuration
smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
smtp_port = int(os.getenv("SMTP_PORT", "587"))
smtp_username = os.getenv("SMTP_USERNAME")
smtp_password = os.getenv("SMTP_PASSWORD")

# Create FastMCP instance
mcp = FastMCP("email-mcp")

@mcp.tool()
def send_email(to: str, subject: str, message: str, cc: str = "") -> str:
    """Send an email via SMTP with TLS encryption
    
    Args:
        to: Recipient email address
        subject: Email subject line
        message: Email message body
        cc: CC email address (optional)
    
    Returns:
        Success or error message
    """
    try:
        # Validate required credentials
        if not smtp_username or not smtp_password:
            return "Error: SMTP credentials not configured. Please set SMTP_USERNAME and SMTP_PASSWORD in environment variables or .env file."

        # Create message
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = to
        msg['Subject'] = subject
        
        # Add CC if provided
        if cc:
            msg['Cc'] = cc
            recipients = [to, cc]
        else:
            recipients = [to]
        
        # Add message body
        msg.attach(MIMEText(message, 'plain'))
        
        # Create SSL context
        context = ssl.create_default_context()
        
        # Send email
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls(context=context)
            server.login(smtp_username, smtp_password)
            server.send_message(msg, to_addrs=recipients)
        
        return f"Email successfully sent to {to}" + (f" and cc'd to {cc}" if cc else "")
        
    except smtplib.SMTPAuthenticationError:
        return "Error: SMTP authentication failed. Please check your username and password."
    except smtplib.SMTPException as e:
        return f"Error: SMTP error occurred: {str(e)}"
    except Exception as e:
        return f"Error: An unexpected error occurred: {str(e)}"


if __name__ == "__main__":
    # Run in stdio mode for Claude Desktop
    mcp.run()