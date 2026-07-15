"""
YouTube Upload Service for Fact Fusion Automation

Uploads videos to YouTube via OAuth2 API.
Supports Shorts and long-form, scheduling, and custom thumbnails.

Usage:
    from app.services.youtube import upload_to_youtube
    result = upload_to_youtube("video.mp4", metadata)
"""

import os
import pickle
from datetime import datetime
from pathlib import Path
from typing import Optional

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

from loguru import logger

# OAuth2 scopes
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
]

# Token paths
TOKEN_DIR = Path.home() / ".config" / "google"
TOKEN_FILE = TOKEN_DIR / "youtube_token.pickle"
CREDENTIALS_FILE = TOKEN_DIR / "client_secret.json"


def authenticate():
    """Authenticate with YouTube API and return credentials."""
    creds = None
    
    # Load existing token
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)
    
    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("🔄 Refreshing OAuth token...")
            creds.refresh(Request())
        else:
            logger.info("🔐 Starting OAuth flow...")
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save token
        TOKEN_DIR.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)
        logger.info("✅ Token saved")
    
    return creds


def upload_to_youtube(video_path, metadata):
    """
    Upload video to YouTube.
    
    Args:
        video_path: Path to video file
        metadata: Dict with title, description, tags, privacy, schedule
    
    Returns:
        Dict with success status, video URL, video ID
    """
    try:
        creds = authenticate()
        youtube = build("youtube", "v3", credentials=creds)
        
        # Prepare metadata
        title = metadata.get("title", "Fact Fusion Video")
        description = metadata.get("description", "")
        tags = metadata.get("tags", ["facts", "trivia", "shorts"])
        privacy = metadata.get("privacy", "public")
        schedule = metadata.get("schedule")
        
        privacy_map = {
            "public": "public",
            "private": "private",
            "unlisted": "unlisted",
        }
        
        # Build request body
        body = {
            "snippet": {
                "title": title[:100],
                "description": description[:5000],
                "tags": tags,
                "categoryId": "22",  # People & Blogs
            },
            "status": {
                "privacyStatus": privacy_map.get(privacy, "public"),
                "selfDeclaredMadeForKids": False,
            },
        }
        
        # Add schedule if provided
        if schedule:
            body["status"]["publishAt"] = schedule
        
        # Upload video
        logger.info(f"📤 Uploading {video_path} to YouTube...")
        media = MediaFileUpload(video_path, chunksize=100*1024*1024, resumable=True)
        
        request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                logger.info(f"⏳ Uploaded {int(status.progress() * 100)}%")
        
        video_id = response["id"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        logger.info(f"✅ YouTube upload successful: {video_url}")
        
        return {
            "success": True,
            "video_id": video_id,
            "url": video_url,
        }
        
    except HttpError as e:
        logger.error(f"❌ YouTube upload failed: {e}")
        return {"success": False, "error": str(e)}
    """Authenticate with YouTube API and return credentials."""
    creds = None
    
    # Load existing token
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)
    
    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("🔄 Refreshing OAuth token...")
            creds.refresh(Request())
        else:
            logger.info("🔐 Starting OAuth flow...")
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save token
        TOKEN_DIR.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)
        logger.info("✅ Token saved")
    
    return creds