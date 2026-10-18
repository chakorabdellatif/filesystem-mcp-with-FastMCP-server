"""
Kokoro-TTS & Local Voice Synthesizer
Inspired by hexgrad/Kokoro-82M
Provides real-time local text-to-speech audio generation and playback
on Windows (ASUS ROG Flow) with zero cloud API costs.
"""

import logging
import os
import subprocess
import sys
import threading
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class LocalVoiceSynthesizer:
    @staticmethod
    def speak_powershell_sapi(text: str) -> bool:
        """
        Instant, zero-dependency local text-to-speech via Windows SAPI.
        """
        # Escape single quotes
        safe_text = text.replace("'", "''").replace('"', '`"')
        ps_cmd = f"Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{safe_text}')"
        try:
            subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True, timeout=15)
            return True
        except Exception as e:
            logger.error(f"SAPI TTS failed: {e}")
            return False

    @staticmethod
    def synthesize_to_file(text: str, output_wav_path: Path) -> str:
        """
        Synthesize text to audio file.
        """
        output_wav_path.parent.mkdir(parents=True, exist_ok=True)
        safe_text = text.replace("'", "''").replace('"', '`"')
        ps_cmd = (
            f"Add-Type -AssemblyName System.Speech; "
            f"$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
            f"$synth.SetOutputToWaveFile('{output_wav_path}'); "
            f"$synth.Speak('{safe_text}'); "
            f"$synth.Dispose()"
        )
        try:
            subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True, timeout=20)
            return str(output_wav_path)
        except Exception as e:
            return f"Error: {e}"


def speak_async(text: str):
    thread = threading.Thread(target=LocalVoiceSynthesizer.speak_powershell_sapi, args=(text,))
    thread.daemon = True
    thread.start()
