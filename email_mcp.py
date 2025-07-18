#!/usr/bin/env python3
"""
Email MCP Server - A tool for sending emails via SMTP with TLS support
"""
import asyncio
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Any, Dict, List, Optional
import json
import os
from dotenv import load_dotenv

import mcp.types as types
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio


class EmailMCPServer:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        self.server = Server("email-mcp")
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[types.Tool]:
            """List available tools"""
            return [
                types.Tool(
                    name="send_email",
                    description="Send an email via SMTP with TLS encryption",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "to": {
                                "type": "string",
                                "description": "Recipient email address"
                            },
                            "cc": {
                                "type": "string",
                                "description": "CC email address (optional)"
                            },
                            "subject": {
                                "type": "string",
                                "description": "Email subject line"
                            },
                            "message": {
                                "type": "string",
                                "description": "Email message body"
                            }
                        },
                        "required": ["to", "subject", "message"]
                    }
                )
            ]

        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict[str, Any]
        ) -> list[types.TextContent]:
            """Handle tool calls"""
            if name == "send_email":
                return await self._send_email(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")

    async def _send_email(self, args: Dict[str, Any]) -> List[types.TextContent]:
        """Send an email with the provided arguments"""
        try:
            # Validate required arguments
            if not self.smtp_username or not self.smtp_password:
                return [types.TextContent(
                    type="text",
                    text="Error: SMTP credentials not configured. Please set SMTP_USERNAME and SMTP_PASSWORD in environment variables or .env file."
                )]

            to_email = args.get("to")
            cc_email = args.get("cc", "")
            subject = args.get("subject")
            message = args.get("message")

            if not to_email or not subject or not message:
                return [types.TextContent(
                    type="text",
                    text="Error: Missing required parameters. 'to', 'subject', and 'message' are required."
                )]

            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = to_email
            if cc_email:
                msg['Cc'] = cc_email
            msg['Subject'] = subject

            # Attach message body
            msg.attach(MIMEText(message, 'plain'))

            # Create SMTP connection with TLS
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.smtp_username, self.smtp_password)
                
                # Send email
                recipients = [to_email]
                if cc_email:
                    recipients.append(cc_email)
                
                server.sendmail(self.smtp_username, recipients, msg.as_string())

            return [types.TextContent(
                type="text",
                text=f"Email sent successfully to {to_email}" + (f" (CC: {cc_email})" if cc_email else "")
            )]

        except smtplib.SMTPAuthenticationError:
            return [types.TextContent(
                type="text",
                text="Error: SMTP authentication failed. Please check your username and password."
            )]
        except smtplib.SMTPException as e:
            return [types.TextContent(
                type="text",
                text=f"Error: SMTP error occurred: {str(e)}"
            )]
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error: An unexpected error occurred: {str(e)}"
            )]

    async def run(self):
        """Run the MCP server"""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="email-mcp",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=None,
                        experimental_capabilities=None,
                    ),
                ),
            )


def main():
    """Main entry point"""
    server = EmailMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()