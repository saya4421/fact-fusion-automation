#!/usr/bin/env python3
"""
Fact Fusion Automation - Multi-Platform Uploader

Upload videos to:
- YouTube (Shorts + Long-form)
- TikTok
- Instagram Reels

Usage:
    python scripts/auto_upload.py --video video.mp4 --platforms all
    python scripts/auto_upload.py --video video.mp4 --platforms youtube,tiktok
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.youtube import upload_to_youtube
from app.services.tiktok import upload_to_tiktok
from app.services.instagram import upload_to_instagram
from app.utils.logger import get_logger

logger = get_logger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="Multi-platform video uploader")
    
    parser.add_argument(
        "--video",
        type=str,
        required=True,
        help="Path to video file"
    )
    
    parser.add_argument(
        "--platforms",
        type=str,
        default="all",
        help="Platforms to upload: all, youtube, tiktok, instagram, or comma-separated"
    )
    
    parser.add_argument(
        "--title",
        type=str,
        default=None,
        help="Video title (auto-generate if not provided)"
    )
    
    parser.add_argument(
        "--description",
        type=str,
        default=None,
        help="Video description (auto-generate if not provided)"
    )
    
    parser.add_argument(
        "--tags",
        type=str,
        nargs="+",
        default=None,
        help="Video tags (auto-generate if not provided)"
    )
    
    parser.add_argument(
        "--schedule",
        type=str,
        default=None,
        help="Schedule upload (ISO 8601 format, e.g., 2026-07-15T09:00:00)"
    )
    
    parser.add_argument(
        "--privacy",
        type=str,
        choices=["public", "private", "unlisted"],
        default="public",
        help="Video privacy status"
    )
    
    return parser.parse_args()


def upload_to_all(video_path, metadata):
    """Upload to all platforms"""
    
    results = {
        "youtube": None,
        "tiktok": None,
        "instagram": None
    }
    
    # YouTube Upload
    try:
        logger.info("📤 Uploading to YouTube...")
        results["youtube"] = upload_to_youtube(video_path, metadata)
        logger.info(f"✅ YouTube upload successful: {results['youtube']['url']}")
    except Exception as e:
        logger.error(f"❌ YouTube upload failed: {str(e)}")
    
    # TikTok Upload
    try:
        logger.info("📤 Uploading to TikTok...")
        results["tiktok"] = upload_to_tiktok(video_path, metadata)
        logger.info(f"✅ TikTok upload successful: {results['tiktok']['url']}")
    except Exception as e:
        logger.error(f"❌ TikTok upload failed: {str(e)}")
    
    # Instagram Reels Upload
    try:
        logger.info("📤 Uploading to Instagram Reels...")
        results["instagram"] = upload_to_instagram(video_path, metadata)
        logger.info(f"✅ Instagram upload successful: {results['instagram']['url']}")
    except Exception as e:
        logger.error(f"❌ Instagram upload failed: {str(e)}")
    
    return results


def main():
    args = parse_args()
    
    # Parse platforms
    if args.platforms == "all":
        platforms = ["youtube", "tiktok", "instagram"]
    else:
        platforms = [p.strip() for p in args.platforms.split(",")]
    
    # Prepare metadata
    metadata = {
        "title": args.title,
        "description": args.description,
        "tags": args.tags,
        "schedule": args.schedule,
        "privacy": args.privacy
    }
    
    # Validate video file
    video_path = Path(args.video)
    if not video_path.exists():
        logger.error(f"❌ Video file not found: {video_path}")
        sys.exit(1)
    
    logger.info("=" * 50)
    logger.info(f"🚀 Multi-Platform Upload")
    logger.info(f"📹 Video: {video_path.name}")
    logger.info(f"📱 Platforms: {', '.join(platforms)}")
    logger.info(f"📝 Title: {metadata['title'] or 'Auto-generate'}")
    logger.info("=" * 50)
    
    # Upload to selected platforms
    results = {}
    
    if "youtube" in platforms:
        try:
            results["youtube"] = upload_to_youtube(video_path, metadata)
            logger.info(f"✅ YouTube: {results['youtube']['url']}")
        except Exception as e:
            logger.error(f"❌ YouTube failed: {str(e)}")
    
    if "tiktok" in platforms:
        try:
            results["tiktok"] = upload_to_tiktok(video_path, metadata)
            logger.info(f"✅ TikTok: {results['tiktok']['url']}")
        except Exception as e:
            logger.error(f"❌ TikTok failed: {str(e)}")
    
    if "instagram" in platforms:
        try:
            results["instagram"] = upload_to_instagram(video_path, metadata)
            logger.info(f"✅ Instagram: {results['instagram']['url']}")
        except Exception as e:
            logger.error(f"❌ Instagram failed: {str(e)}")
    
    # Summary
    logger.info("=" * 50)
    logger.info("📊 Upload Summary:")
    logger.info(f"✅ Successful: {sum(1 for v in results.values() if v)}")
    logger.info(f"❌ Failed: {sum(1 for v in results.values() if not v)}")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()