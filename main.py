#!/usr/bin/env python3
"""
Slack Message Sender

A script to send messages to Slack channels.
This is the main entry point for the application.
Supports sending messages at scheduled times.
"""

import argparse
import sys
import time
import datetime
from slack_messenger import (
    send_slack_message, 
    read_message_from_file, 
    read_scheduled_messages,
    DEFAULT_CHANNEL, 
    DEFAULT_USERNAME
)


def send_test_message():
    """Send a test message to the Slack channel."""
    print("Sending test message...")
    response = send_slack_message(
        text="Test message from Slack Messenger script!"
    )
    
    if response and response.get("ok"):
        print(f"Test message sent successfully to {DEFAULT_CHANNEL}")
        return True
    else:
        print(f"Failed to send test message: {response}", file=sys.stderr)
        return False


def main():
    """Main function to parse arguments and execute commands."""
    parser = argparse.ArgumentParser(description="Send messages to Slack channels")
    parser.add_argument("--test", action="store_true", help="Send a test message to the Slack channel")
    parser.add_argument("--channel", default=DEFAULT_CHANNEL, help="The Slack channel to send the message to (e.g., #channel-name)")
    parser.add_argument("--text", help="The message text to send")
    parser.add_argument("--username", default=DEFAULT_USERNAME, help="The bot username that will appear in Slack")
    parser.add_argument("--file", default="messages.txt", help="Path to a file containing the message to send")
    parser.add_argument("--schedule", action="store_true", help="Read scheduled messages from file and send them at the specified times")
    
    args = parser.parse_args()
    
    if args.test:
        send_test_message()
        return
        
    if args.schedule:
        # Read scheduled messages from file
        scheduled_messages = read_scheduled_messages(args.file)
        if not scheduled_messages:
            print(f"No valid scheduled messages found in {args.file}")
            sys.exit(1)
            
        # Sort messages by timestamp
        scheduled_messages.sort(key=lambda x: x[0])
        
        print(f"Found {len(scheduled_messages)} scheduled messages in {args.file}")
        
        # Display the scheduled messages
        for timestamp, message in scheduled_messages:
            print(f"• {timestamp.strftime('%Y-%m-%d %H:%M')} - {message[:30]}{'...' if len(message) > 30 else ''}")
        
        print("\nWaiting to send messages at scheduled times...")
        print("Press Ctrl+C to exit")
        
        try:
            # Process messages
            for timestamp, message in scheduled_messages:
                # Skip messages scheduled in the past
                now = datetime.datetime.now()
                if timestamp < now:
                    print(f"Skipping message scheduled for {timestamp.strftime('%Y-%m-%d %H:%M')} (in the past)")
                    continue
                
                # Wait until the scheduled time
                wait_seconds = (timestamp - now).total_seconds()
                if wait_seconds > 0:
                    print(f"Waiting until {timestamp.strftime('%Y-%m-%d %H:%M')} to send message ({int(wait_seconds)} seconds)...")
                    time.sleep(wait_seconds)
                
                # Send the message
                print(f"Sending scheduled message at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
                response = send_slack_message(
                    text=message,
                    channel=args.channel,
                    username=args.username
                )
                
                if response and response.get("ok"):
                    print(f"Message sent successfully to {args.channel}")
                else:
                    print(f"Failed to send message: {response}", file=sys.stderr)
            
            print("All scheduled messages have been sent!")
        except KeyboardInterrupt:
            print("\nMessage scheduler stopped by user")
            sys.exit(0)
        
        return
    
    # Determine the message text to send
    text = args.text
    if not text:
        text = read_message_from_file(args.file)
        if not text:
            print("Error: No message text provided. Use --text or --file or create a messages.txt file.", file=sys.stderr)
            sys.exit(1)
    
    # Send the message
    response = send_slack_message(
        text=text,
        channel=args.channel,
        username=args.username
    )
    
    if response and response.get("ok"):
        print(f"Message sent successfully to {args.channel}")
    else:
        print(f"Failed to send message: {response}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
