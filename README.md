# Slack Message Sender

A simple Python utility to send messages to Slack channels. This project allows you to schedule messages to be sent at specific times through Slack.

## Repository

This project is hosted on GitHub: https://github.com/jihung-chang/slack_message_sender

## Quick Start

Run the setup script to quickly get started:

```bash
python setup.py
```

This will:
1. Install required dependencies
2. Help you create a message file
3. Provide usage instructions

## Manual Setup

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

The default Slack channel and username are set as global variables in `slack_messenger.py`:
- Default channel: `#richard-test-channel`
- Default username: `richard_slack_bot`

You can edit these values directly in the `slack_messenger.py` file.

## Message Content

By default, the message content is read from a file called `messages.txt`. You can edit this file to change the message that gets sent to Slack.

### Scheduled Messages Format

The scheduled messages file should follow this format:

```
YYYY-MM-DD HH:MM
"This is a multi-line message
line2
line3
line4"

YYYY-MM-DD HH:MM
"This is a single line message"
```

To send scheduled messages:

```bash
python main.py --schedule
```

This will read the scheduled messages from the default `messages.txt` file and send them at the specified times.

## Usage

You can use the script in several ways:

### 1. Using main.py with Test Flag

```bash
python main.py --test
```

This will send a predefined test message to the Slack channel.

### 2. Using main.py to Send Message from File

```bash
python main.py
```

This will read the message from `messages.txt` and send it to the default Slack channel.

```bash
python main.py --file custom_message.txt
```

This will read the message from a custom file and send it to the default Slack channel.

### 3. Using main.py with Text Parameter

```bash
python main.py --text "Your message"
```

This will send the specified text to the default Slack channel.

### 4. Using main.py with Scheduled Messages

```bash
python main.py --schedule
```

This will read scheduled messages from `messages.txt` and send them at the specified times.

```bash
python main.py --schedule --file scheduled_messages.txt
```

This will read scheduled messages from a custom file and send them at the specified times.

**Arguments:**
- `--channel`: The Slack channel to send the message to (optional, defaults to `#richard-test-channel`)
- `--text`: The message text to send (optional if using --file)
- `--username`: The bot username that will appear in Slack (optional, defaults to `richard_slack_bot`)
- `--file`: Path to a file containing the message to send (optional, defaults to `messages.txt`)
- `--username`: The bot username that will appear in Slack (optional, defaults to `richard_slack_bot`)
- `--file`: Path to a file containing the message to send (optional, defaults to `messages.txt`)

### 4. Import as a Module

You can also import the function in your own Python code:

```python
from slack_messenger import send_slack_message

# Using defaults
response = send_slack_message(
    text="Your message"
)

# Or specifying all parameters
response = send_slack_message(
    text="Your message",
    channel="#your-channel",
    username="your_bot_name"
)

if response and response.get("ok"):
    print("Message sent successfully!")
else:
    print(f"Failed to send message: {response}")
```

## Examples

```bash
# Send a message from messages.txt
python main.py

# Send a test message
python main.py --test

# Send a message from a custom file
python main.py --file my_message.txt

# Send a message with custom text
python main.py --text "Hello from Slack Messenger!"

# Send a message to a different channel
python main.py --channel "#another-channel" --text "Hello from Slack Messenger!"

# Send scheduled messages
python main.py --schedule
```
