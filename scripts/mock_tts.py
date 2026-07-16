#!/usr/bin/env python3
"""
Mock TTS generator for testing - creates silent WAV file
"""
import wave
import struct
import sys

def create_silent_wav(output_path, duration_sec=10, sample_rate=22050):
    """Create a silent WAV file for testing"""
    num_samples = int(duration_sec * sample_rate)
    
    with wave.open(output_path, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        # Write silent frames
        for _ in range(num_samples):
            wav_file.writeframes(struct.pack('<h', 0))  # Silent sample
    
    print(f"Created silent WAV: {output_path} ({duration_sec}s)")
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: mock_tts.py <output.wav> [duration_sec]")
        sys.exit(1)
    
    output = sys.argv[1]
    duration = int(float(sys.argv[2]) if len(sys.argv) > 2 else 10)
    create_silent_wav(output, duration)