from dotenv import load_dotenv
import os
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Load environment variables from .env
load_dotenv()


class SlackConnector:
    def __init__(self, bot_token):
        self.client = WebClient(token=bot_token)

    def get_channels(self):
        """Fetch all public and private channels."""
        channels = []
        next_cursor = None

        while True:
            try:
                response = self.client.conversations_list(
                    types="public_channel,private_channel",
                    cursor=next_cursor,
                    limit=100,
                )
                channels.extend(response["channels"])
                next_cursor = response.get("response_metadata", {}).get("next_cursor")
                if not next_cursor:
                    break
            except SlackApiError as e:
                print(f"Error fetching channels: {e.response['error']}")
                break

        return channels

    def get_messages(self, channel_id, channel_name):
        """Fetch all messages from a given channel and extract only the text."""
        messages = []
        next_cursor = None

        while True:
            try:
                response = self.client.conversations_history(
                    channel=channel_id, cursor=next_cursor, limit=200
                )

                # Check if the request was successful
                if not response.get("ok"):
                    print(f"Error fetching messages for {channel_id}: {response.get('error')}")
                    break

                # Extract only the text field and channel name
                for message in response.get("messages", []):
                    if "text" in message:  # Ensure text exists
                        messages.append({
                            "text": message["text"],
                            "channel": channel_name
                        })

                # Ensure response_metadata exists before accessing it
                next_cursor = response.get("response_metadata", {}).get("next_cursor")

                if not next_cursor:
                    break  # No more pages left

            except SlackApiError as e:
                print(f"Error fetching messages for {channel_id}: {e.response['error']}")
                break

        return messages

    def fetch_all_messages(self):
        """Fetch only the text from all messages across all channels."""
        all_messages = []

        # Get public and private channels only (no DMs)
        channels = self.get_channels()
        for channel in channels:
            channel_name = channel["name"]
            channel_id = channel["id"]
            print(f"Fetching messages from #{channel_name}...")
            messages = self.get_messages(channel_id, channel_name)
            all_messages.extend(messages)  # Append messages to a single array

        return all_messages


if __name__ == "__main__":
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

    if not SLACK_BOT_TOKEN:
        raise ValueError("SLACK_BOT_TOKEN not found. Please set it in the .env file.")

    slack_connector = SlackConnector(SLACK_BOT_TOKEN)
    all_messages = slack_connector.fetch_all_messages()

    with open("slack_messages.json", "w", encoding="utf-8") as f:
        json.dump(all_messages, f, indent=4)

    print(f"Saved {len(all_messages)} messages to slack_messages.json.")
