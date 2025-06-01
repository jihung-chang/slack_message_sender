#!/usr/bin/env python3
"""
Setup script for Slack Message Sender
This script helps users get started with the Slack Message Sender by:
1. Installing dependencies
2. Providing instructions
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import requests
        print("✅ Required dependencies are already installed.")
        return True
    except ImportError:
        print("📦 Installing required dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencies installed successfully.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}", file=sys.stderr)
            return False

def setup():
    """Run the setup process."""
    print("=" * 50)
    print("Welcome to Slack Message Sender Setup")
    print("=" * 50)
    print()
    
    # Step 1: Check dependencies
    if not check_dependencies():
        return False
    
    print()
    
    # Step 2: Show instructions
    print("=" * 50)
    print("Setup Complete!")
    print("=" * 50)
    print()
    print("Here's how to use Slack Message Sender:")
    print()
    print("1. Create or edit messages.txt file with your scheduled messages")
    print("   Format: YYYY-MM-DD HH:MM")
    print('   "Your message text here"')
    print()
    print("2. Run the script to send the messages:")
    print("   python main.py --schedule  # For scheduled messages")
    print()
    print("For more options, see README.md or run:")
    print("   python main.py --help")
    
    return True

if __name__ == "__main__":
    setup()
