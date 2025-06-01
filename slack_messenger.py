#!/usr/bin/env python3
"""
Slack Message Sender
A simple script to send messages to Slack channels using the Slack API.
"""

import argparse
import requests
import json
import sys
import os
import re
import datetime

# Global variables
DEFAULT_CHANNEL = "#richard-test-channel"
DEFAULT_USERNAME = "richard_slack_bot"


def read_scheduled_messages(file_path="messages.txt"):
    """
    Read scheduled messages from a file.
    
    The file format should be:
    ```
    YYYY-MM-DD HH:MM
    "Message content
    can span multiple lines
    within quotes"
    
    YYYY-MM-DD HH:MM
    "Another message"
    ```
    
    Args:
        file_path (str): Path to the file containing scheduled messages
        
    Returns:
        list: A list of tuples (datetime_obj, message_text)
    """
    try:
        if not os.path.exists(file_path):
            print(f"Message file not found: {file_path}", file=sys.stderr)
            return None
            
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Regular expression to match timestamp and quoted message
        # This pattern looks for:
        # 1. A date in YYYY-MM-DD format
        # 2. Followed by a time in HH:MM format
        # 3. Followed by a quoted string that can contain multiple lines
        pattern = r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})\s*\n\s*"((?:[^"]|"[^"])*?)"'
        
        matches = re.findall(pattern, content, re.DOTALL)
        
        if not matches:
            print(f"No properly formatted scheduled messages found in {file_path}", file=sys.stderr)
            print("Format should be: YYYY-MM-DD HH:MM followed by a message in quotes", file=sys.stderr)
            return None
        
        scheduled_messages = []
        for timestamp_str, message in matches:
            try:
                timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M')
                scheduled_messages.append((timestamp, message))
            except ValueError as e:
                print(f"Error parsing timestamp '{timestamp_str}': {e}", file=sys.stderr)
                
        return scheduled_messages
    except Exception as e:
        print(f"Error reading scheduled messages file: {e}", file=sys.stderr)
        return None


def read_message_from_file(file_path="messages.txt"):
    """
    Read a message from a text file.
    
    Args:
        file_path (str): Path to the file containing the message
        
    Returns:
        str: The message text read from the file, or None if the file doesn't exist
    """
    try:
        if not os.path.exists(file_path):
            print(f"Message file not found: {file_path}", file=sys.stderr)
            return None
            
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading message file: {e}", file=sys.stderr)
        return None


def send_slack_message(text, channel=DEFAULT_CHANNEL, username=DEFAULT_USERNAME):
    """
    Send a message to a Slack channel using the Slack API.
    
    Args:
        text (str): The message text to send
        channel (str, optional): The channel to send the message to (e.g., "#channel-name")
        username (str, optional): The bot username that will appear in Slack
        
    Returns:
        dict: The API response
    """
    url = "https://slack-api-proxy-group-all.linecorp.com/api/chat.postMessage"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "channel": channel,
        "text": text,
        "username": username
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for 4XX/5XX responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending Slack message: {e}", file=sys.stderr)
        return None