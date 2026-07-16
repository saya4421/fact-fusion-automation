#!/usr/bin/env python3
"""
Hybrid TTS Manager - Piper + Edge + Paid Fallback

Priority:
1. Piper (FREE, offline, best quality)
2. Edge TTS (FREE, online, good quality)
3. Azure/Google (paid, last resort)

Usage:
    from app.services.tts_manager import generate_voiceover
    
    # Auto-fallback
    audio_path, subtitle_path = generate_voiceover(
        text="Hello world",
        voice="en-US-JennyNeural",
        provider="auto"  # Will try Piper → Edge → Paid
    )
"""

import os
import tempfile
from pathlib import Path
from typing import Optional, Tuple
from loguru import logger

try:
    from app.config import config
    # Use dict access for config (settings.toml structure)
    tts_config = config.get('tts', {})
    PIPER_URL = tts_config.get('piper_url', "http://localhost:5002")
    EDGE_ENABLED = True  # Re-enabled with CLI mode (more reliable)
    GTTS_ENABLED = True  # gTTS as fallback (simple, reliable)
    ESPEAK_ENABLED = True  # espeak-ng: offline, guaranteed, robotic but works
    AZURE_ENABLED = tts_config.get('azure_enabled', False)
    GOOGLE_ENABLED = tts_config.get('google_enabled', False)
    AZURE_KEY = tts_config.get('azure_key', None)
    AZURE_REGION = tts_config.get('azure_region', 'eastus')
except ImportError:
    # Fallback for standalone usage
    PIPER_URL = "http://localhost:5002"
    EDGE_ENABLED = True
    AZURE_ENABLED = False
    GOOGLE_ENABLED = False
    AZURE_KEY = None
    AZURE_REGION = "eastus"


class HybridTTSManager:
    """Manages multiple TTS providers with automatic fallback."""
    
    def __init__(self):
        self.piper_url = PIPER_URL
        self.edge_enabled = EDGE_ENABLED
        self.gtts_enabled = GTTS_ENABLED
        self.espeak_enabled = ESPEAK_ENABLED
        self.azure_enabled = AZURE_ENABLED
        self.google_enabled = GOOGLE_ENABLED
        
    def generate(
        self,
        text: str,
        voice: str,
        output_path: str,
        provider: str = "auto"
    ) -> Tuple[str, Optional[str]]:
        """
        Generate voiceover with automatic fallback.
        
        Args:
            text: Text to synthesize
            voice: Voice name (e.g., "en-US-JennyNeural")
            output_path: Output audio file path
            provider: "auto", "piper", "edge", "azure", "google"
            
        Returns:
            Tuple of (audio_path, subtitle_path)
            
        Raises:
            RuntimeError: If all providers fail
        """
        providers_to_try = self._get_provider_order(provider)
        last_error = None
        
        for provider_name in providers_to_try:
            try:
                logger.info(f"Trying TTS provider: {provider_name}")
                
                if provider_name == "piper":
                    return self._generate_piper(text, voice, output_path)
                elif provider_name == "edge":
                    return self._generate_edge(text, voice, output_path)
                elif provider_name == "gtts":
                    return self._generate_gtts(text, voice, output_path)
                elif provider_name == "espeak":
                    return self._generate_espeak(text, voice, output_path)
                elif provider_name == "azure":
                    return self._generate_azure(text, voice, output_path)
                elif provider_name == "google":
                    return self._generate_google(text, voice, output_path)
                    
            except Exception as e:
                logger.warning(f"{provider_name} TTS failed: {e}")
                last_error = e
                continue
        
        # All providers failed
        raise RuntimeError(
            f"All TTS providers failed. Last error: {last_error}"
        )
    
    def _get_provider_order(self, provider: str) -> list:
        """Get list of providers to try in order."""
        if provider != "auto":
            return [provider]
        
        # Auto mode: try in priority order
        order = []
        
        # 1. Piper (if available)
        if self._is_piper_available():
            order.append("piper")
        
        # 2. Edge (always available, FREE)
        if self.edge_enabled:
            order.append("edge")
        
        # 3. gTTS (simple fallback)
        if self.gtts_enabled:
            order.append("gtts")
        
        # 4. espeak-ng (offline, guaranteed - last resort)
        if self.espeak_enabled:
            order.append("espeak")
        
        # 4. Paid providers
        if self.azure_enabled:
            order.append("azure")
        if self.google_enabled:
            order.append("google")
        
        # Fallback to gTTS if nothing else (most reliable)
        if not order:
            order.append("gtts")
        
        return order
    
    def _is_piper_available(self) -> bool:
        """Check if Piper TTS service is running."""
        import requests
        try:
            response = requests.get(f"{self.piper_url}/api/voices", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def _generate_piper(
        self,
        text: str,
        voice: str,
        output_path: str
    ) -> Tuple[str, Optional[str]]:
        """Generate using Piper TTS (FREE, offline)."""
        import requests
        
        # Parse voice name to get Piper voice key
        # Format: "piper:<voice_key>" or just use default
        voice_key = voice.replace("piper:", "") if voice.startswith("piper:") else ""
        
        response = requests.post(
            f"{self.piper_url}/api/tts",
            json={
                "text": text,
                "voice_key": voice_key,
                "speaker_language": voice.split("-")[0] if "-" in voice else "en"
            },
            timeout=60
        )
        
        if response.status_code != 200:
            raise RuntimeError(f"Piper API error: {response.text}")
        
        # Save audio
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        # Piper doesn't return subtitles, generate dummy
        subtitle_path = self._generate_dummy_subtitle(output_path, text)
        
        return output_path, subtitle_path
    
    def _generate_edge(
        self,
        text: str,
        voice: str,
        output_path: str
    ) -> Tuple[str, Optional[str]]:
        """Generate using Edge TTS CLI (FREE, online) - more reliable than WebSocket."""
        import subprocess
        
        # Edge TTS voice format: "en-US-JennyNeural"
        if not voice or voice == "auto":
            voice = "en-US-GuyNeural"
        
        # Use edge-tts CLI directly (more reliable)
        mp3_path = output_path.replace(".wav", ".mp3")
        subtitle_path = mp3_path.replace(".mp3", ".srt")
        
        try:
            # Generate audio + subtitles with CLI
            result = subprocess.run(
                [
                    "edge-tts",
                    "--text", text,
                    "--voice", voice,
                    "--write-media", mp3_path,
                    "--write-subtitles", subtitle_path
                ],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"edge-tts CLI failed: {result.stderr}")
            
            # Convert MP3 to WAV for compatibility
            if os.path.exists(mp3_path):
                subprocess.run(
                    ["ffmpeg", "-y", "-i", mp3_path, output_path],
                    capture_output=True,
                    check=True
                )
                os.remove(mp3_path)
            
            if not os.path.exists(output_path):
                raise RuntimeError("Failed to generate audio file")
            
            logger.info(f"Edge TTS generated: {output_path}")
            return output_path, (subtitle_path if os.path.exists(subtitle_path) else None)
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("Edge TTS timeout - network issue")
        except FileNotFoundError:
            raise RuntimeError("edge-tts CLI not found - run: pip install edge-tts")
        except Exception as e:
            raise RuntimeError(f"Edge TTS error: {str(e)}")
    
    def _generate_gtts(
        self,
        text: str,
        voice: str,
        output_path: str
    ) -> Tuple[str, Optional[str]]:
        """Generate using gTTS (Google TTS - FREE, simple HTTP API)."""
        try:
            from gtts import gTTS
            
            # gTTS doesn't support voice selection, uses auto-detect
            lang = "en"
            if voice and "-" in voice:
                # Extract language from voice code (e.g., "en-US-GuyNeural" -> "en")
                lang = voice.split("-")[0]
            
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(output_path)
            
            if not os.path.exists(output_path):
                raise RuntimeError("gTTS failed to generate audio file")
            
            logger.info(f"gTTS generated: {output_path}")
            return output_path, None  # No subtitles
            
        except ImportError:
            raise RuntimeError("gTTS not installed - run: pip install gtts")
        except Exception as e:
            raise RuntimeError(f"gTTS error: {str(e)}")
    
    def _generate_espeak(
        self,
        text: str,
        voice: str,
        output_path: str
    ) -> Tuple[str, Optional[str]]:
        """Generate using espeak-ng (OFFLINE, guaranteed to work)."""
        import subprocess
        
        # Map voice to espeak language
        # Default: English US
        lang = "en-us"
        if voice and "-" in voice:
            lang_map = {
                "en": "en-us", "en-US": "en-us", "en-GB": "en-gb",
                "id": "id", "id-ID": "id",
                "ja": "ja", "zh": "cmn", "ko": "ko",
                "fr": "fr", "de": "de", "es": "es",
            }
            base = voice.split("-")[0].lower()
            lang = lang_map.get(base, "en-us")
        
        # espeak-ng outputs WAV directly
        try:
            result = subprocess.run(
                [
                    "espeak-ng",
                    "-v", lang,
                    "-w", output_path,
                    "--stdin"
                ],
                input=text,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0 and not os.path.exists(output_path):
                raise RuntimeError(f"espeak-ng failed: {result.stderr}")
            
            # espeak might output WAV with .wav extension already
            if not os.path.exists(output_path):
                # Try without .wav extension handling
                raise RuntimeError("espeak-ng did not produce output file")
            
            logger.info(f"espeak-ng generated: {output_path}")
            return output_path, None  # No subtitles
            
        except FileNotFoundError:
            raise RuntimeError("espeak-ng not installed - run: sudo dnf install espeak-ng")
        except Exception as e:
            raise RuntimeError(f"espeak-ng error: {str(e)}")
    
    def _generate_azure(
        self,
        text: str,
        voice: str,
        output_path: str
    ) -> Tuple[str, Optional[str]]:
        """Generate using Azure TTS (paid)."""
        try:
            from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer
        except ImportError:
            raise RuntimeError("Azure Speech SDK not installed. Run: pip install azure-cognitiveservices-speech")
        
        api_key = AZURE_KEY
        region = AZURE_REGION
        
        if not api_key:
            raise RuntimeError("Azure API key not configured")
        
        speech_config = SpeechConfig(subscription=api_key, region=region)
        speech_config.speech_synthesis_voice_name = voice
        
        synthesizer = SpeechSynthesizer(speech_config=speech_config)
        result = synthesizer.speak_text_async(text).get()
        
        if result.reason == result.Reason.SynthesizingAudioCompleted:
            with open(output_path, "wb") as f:
                f.write(result.audio_data)
            return output_path, None
        else:
            raise RuntimeError(f"Azure TTS error: {result.error_details}")
    
    def _generate_google(
        self,
        text: str,
        voice: str,
        output_path: str
    ) -> Tuple[str, Optional[str]]:
        """Generate using Google TTS (paid)."""
        try:
            from google.cloud import texttospeech
        except ImportError:
            raise RuntimeError("Google Cloud TTS SDK not installed. Run: pip install google-cloud-texttospeech")
        
        client = texttospeech.TextToSpeechClient()
        
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        voice_obj = texttospeech.VoiceSelectionParams(
            language_code=voice.split("-")[0] if "-" in voice else "en-US",
            name=voice,
        )
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice_obj,
            audio_config=audio_config
        )
        
        with open(output_path, "wb") as f:
            f.write(response.audio_content)
        
        return output_path, None
    
    def _generate_dummy_subtitle(
        self,
        audio_path: str,
        text: str
    ) -> str:
        """Generate dummy subtitle when TTS doesn't provide timing."""
        subtitle_path = audio_path.replace(".wav", ".srt").replace(".mp3", ".srt")
        
        # Estimate duration (rough: 150 words per minute)
        word_count = len(text.split())
        duration_seconds = (word_count / 150) * 60
        
        # Simple SRT format
        srt_content = f"""1
00:00:00,000 --> 00:00:{int(duration_seconds):02d},000
{text}
"""
        
        with open(subtitle_path, "w", encoding="utf-8") as f:
            f.write(srt_content)
        
        return subtitle_path


# Singleton instance
_tts_manager = None

def get_tts_manager() -> HybridTTSManager:
    """Get singleton TTS manager instance."""
    global _tts_manager
    if _tts_manager is None:
        _tts_manager = HybridTTSManager()
    return _tts_manager


def generate_voiceover(
    text: str,
    voice: str = "auto",
    provider: str = "auto",
    output_dir: Optional[str] = None
) -> Tuple[str, Optional[str]]:
    """
    Convenience function to generate voiceover.
    
    Args:
        text: Text to synthesize
        voice: Voice name (auto = best available)
        provider: "auto", "piper", "edge", "azure", "google"
        output_dir: Output directory (default: temp dir)
        
    Returns:
        Tuple of (audio_path, subtitle_path)
    """
    if output_dir is None:
        output_dir = tempfile.gettempdir()
    
    output_path = os.path.join(
        output_dir,
        f"tts_{hash(text) % 10000}.wav"
    )
    
    manager = get_tts_manager()
    return manager.generate(text, voice, output_path, provider)


if __name__ == "__main__":
    # Test
    audio_path, subtitle_path = generate_voiceover(
        text="Hello! This is a test of the hybrid TTS system.",
        voice="auto",
        provider="auto"
    )
    print(f"Audio: {audio_path}")
    print(f"Subtitles: {subtitle_path}")