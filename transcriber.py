# transcriber.py
# Author: Tyanin Opdahl
# Date Started: 04/01/2025; Date Finished: N/A
# Audio transcription tool with speaker diarization
# Acknowledgements: I used help from Claude AI (Anthropic) to develop this

import os
import argparse
import openai
import tempfile
import pydub
import AudioSegment

def transcribe_audio_with_speakers (file_path, output_path=None, api_key=None)
