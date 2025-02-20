import os
import re
import google.auth
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import time

# Set up authentication
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
CLIENT_SECRET_FILE = "client_secret_229023094739-49h2l7r1ok79qq4vqu15k0sco4o9ao8u.apps.googleusercontent.com.json"  # Replace with your OAuth 2.0 credentials

# Authenticate with OAuth 2.0
def authenticate_youtube():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    return build("youtube", "v3", credentials=credentials)

youtube = authenticate_youtube()

# Function to extract Live Chat ID from a live stream URL
def get_live_chat_id_from_url(live_stream_url):
    video_id_match = re.search(r"v=([a-zA-Z0-9_-]+)", live_stream_url)
    if not video_id_match:
        print("Invalid YouTube live stream URL.")
        return None
    video_id = video_id_match.group(1)
    
    request = youtube.videos().list(
        part="liveStreamingDetails",
        id=video_id
    )
    response = request.execute()
    
    if response.get("items") and "liveStreamingDetails" in response["items"][0]:
        return response["items"][0]["liveStreamingDetails"].get("activeLiveChatId")
    return None

# Ask for the live stream URL
live_stream_url = input("Enter YouTube live stream URL: ")
live_chat_id = get_live_chat_id_from_url(live_stream_url)
if not live_chat_id:
    print("No active live chat found for this stream.")
    exit()

# Function to check and delete spam messages
def is_suspicious_message(message):
    spam_patterns = [
        r"http[s]?://",  # Detects links
        r"(?:\W*\w+\W*){10,}",  # Detects very long messages
        r"[^a-zA-Z0-9 ]{5,}",  # Detects excessive special characters
        r"(.)\1{5,}",  # Detects repeated characters
    ]
    return any(re.search(pattern, message) for pattern in spam_patterns)

# Function to check if a user is a bot (based on account creation date and activity)
def is_bot(author_details):
    try:
        if not author_details.get("isChatModerator") and not author_details.get("isChatOwner"):
            account_age_days = (time.time() - int(author_details.get("publishedAt", "0"))) / 86400
            return account_age_days < 30  # Flag accounts less than 30 days old as potential bots
    except Exception:
        return True
    return False

# Function to monitor and moderate chat
def moderate_chat():
    user_message_count = {}
    
    while True:
        request = youtube.liveChatMessages().list(
            liveChatId=live_chat_id,
            part="snippet,authorDetails"
        )
        response = request.execute()
        
        for item in response.get("items", []):
            message = item["snippet"]["displayMessage"].lower()
            author_id = item["authorDetails"]["channelId"]
            message_id = item["id"]
            author_details = item["authorDetails"]
            
            # Track user message frequency
            user_message_count[author_id] = user_message_count.get(author_id, 0) + 1
            
            # Detect spam messages
            if is_suspicious_message(message) or is_bot(author_details) or user_message_count[author_id] > 5:
                print(f"Deleting message from {author_id}: {message}")
                youtube.liveChatMessages().delete(id=message_id).execute()
                
                if user_message_count[author_id] > 10:
                    print(f"User {author_id} is spamming. Taking action.")
                    # Here you can implement a timeout or report action if needed
            
        time.sleep(5)  # Poll every 5 seconds

# Run the bot
moderate_chat()
