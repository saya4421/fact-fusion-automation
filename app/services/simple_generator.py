#!/usr/bin/env python3
"""
Simple Video Generator - High-level wrapper
Generates complete video from topic in one call
"""

import os
import tempfile
from pathlib import Path
from loguru import logger

from app.config import config
from app.models.schema import VideoParams, VideoAspect
from app.services.llm import generate_script
from app.services.tts_manager import generate_voiceover
from app.services.material import download_videos
from app.services.video import generate_video
from app.utils.logger import get_logger

logger = get_logger(__name__)


def generate_video_from_topic(
    topic: str,
    duration: int = 30,
    orientation: str = "9:16",
    output_dir: str = None
):
    """Generate complete video from topic string."""
    
    output_dir = output_dir or "~/Projects/fact-fusion-automation/storage/output"
    output_dir = os.path.expanduser(output_dir)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    logger.info(f"🎬 Generating video: {topic}")
    
    # Step 1: Generate script
    logger.info("📝 Generating script...")
    script = generate_script(
        video_subject=topic,
        paragraph_number=1,
        language="en"
    )
    if not script:
        logger.error("❌ Failed to generate script")
        return None
    logger.info(f"✅ Script generated: {len(script)} chars")
    
    # Step 2: Generate voiceover
    logger.info("🎙️ Generating voiceover...")
    voice_name = config.get('tts', {}).get('voice', 'en-US-GuyNeural')
    audio_path, subtitle_path = generate_voiceover(
        text=script,
        voice=voice_name
    )
    if not audio_path:
        logger.error("❌ Failed to generate voiceover")
        return None
    logger.info(f"✅ Voiceover generated: {audio_path}")
    
    # Step 3: Download stock footage
    logger.info("📹 Downloading stock footage...")
    video_source = config.get('app', {}).get('video_source', 'pexels')
    pexels_api_key = config.get('app', {}).get('pexels_api_keys', [''])[0]
    
    materials = download_videos(
        search_term=topic,
        source=video_source,
        api_key=pexels_api_key,
        video_aspect=orientation,
        total_duration=duration,
        clip_duration=5
    )
    if not materials:
        logger.error("❌ Failed to download materials")
        return None
    logger.info(f"✅ Downloaded {len(materials)} clips")
    
    # Step 4: Create temp video file from clips
    # For now, use first clip as placeholder
    # TODO: Properly concatenate clips
    video_path = materials[0].url if materials else None
    if not video_path:
        logger.error("❌ No video clips available")
        return None
    
    # Step 5: Generate final video
    logger.info("🎞️ Generating final video...")
    params = VideoParams(
        video_subject=topic,
        video_script=script,
        video_aspect=orientation,
        voice_name=voice_name,
        video_clip_duration=5,
        video_count=1,
        subtitle_enabled=True,
        video_language='en',
        video_source=video_source
    )
    
    output_file = os.path.join(output_dir, f"{topic.replace(' ', '_')}.mp4")
    
    success = generate_video(
        video_path=video_path,
        audio_path=audio_path,
        subtitle_path=subtitle_path or "",
        output_file=output_file,
        params=params
    )
    
    if success:
        logger.info(f"✅ Video generated: {output_file}")
        return output_file
    else:
        logger.error(f"❌ Failed to generate video")
        return None


if __name__ == "__main__":
    # Test
    output = generate_video_from_topic("Amazing Facts About Space", duration=30)
    print(f"Output: {output}")