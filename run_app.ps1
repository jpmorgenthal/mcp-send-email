# PowerShell script to activate virtual environment and run Python app

# Get the script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path

# Activate the virtual environment
& "$scriptPath\mcp\Scripts\Activate.ps1"

# Run the Python application
# Change 'email_mcp.py' to whichever Python file you want to run
python "$scriptPath\email_mcp.py"

# Keep the window open after execution (optional)
# Remove this line if you want the window to close automatically
Read-Host -Prompt "Press Enter to exit"