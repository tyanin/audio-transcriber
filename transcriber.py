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

def transcribe_audio_with_speakers (file_path, output_path=None, api_key=None):
    """
    Transcribe an MP3 audio file to text with speaker diarization
    
    Args:
        file_path (str): Path to the MP3 file
        output_path (str, optional): Path to save the transcript. If None, prints to console.
        api_key (str, optional): OpenAI API key. If None, tries to use environment variable.
        
    Returns:
        str: The transcribed text with speaker labels
    """
    print(f"Processing {file_path}...")
    
    # Set OpenAI API key
    if api_key:
        openai.api_key = api_key
    else:
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OpenAI API key is required. Set it as an environment variable OPENAI_API_KEY or pass it as a parameter.")
    
    # Convert MP3 to WAV
    print("Converting MP3 to WAV format...")
    audio = AudioSegment.from_mp3(file_path)
    
    # Save to a temporary file
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
        wav_path = temp_wav.name
        audio.export(wav_path, format="wav")
    
    # Transcribe with speaker diarization using Whisper API
    print("Transcribing audio with speaker diarization... This may take a while for longer files.")
    try:
        with open(wav_path, "rb") as audio_file:
            response = openai.Audio.transcribe(
                file=audio_file,
                model="whisper-1",
                response_format="verbose_json",
                language="en"
            )
        
        # Process the response to identify speakers
        transcript = process_whisper_response(response)
        print("Transcription complete!")
    except Exception as e:
        transcript = f"Error during transcription: {str(e)}"
        print(transcript)
    finally:
        # Clean up temporary file
        if os.path.exists(wav_path):
            os.remove(wav_path)
    
    # Save or print transcript
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(transcript)
        print(f"Transcript saved to {output_path}")
    else:
        print("\nTranscript:")
        print(transcript)
    
    return transcript

def process_whisper_response(response):
    """
    Process the Whisper API response to format it with speaker labels
    
    Args:
        response: The Whisper API response object
        
    Returns:
        str: Formatted transcript with speaker labels
    """
    # This is a simplified approach - more advanced speaker diarization would require
    # additional processing or a different API
    segments = response.get("segments", [])
    
    # Simple speaker detection based on pauses and other heuristics
    current_speaker = 1
    formatted_transcript = ""
    last_end_time = 0
    
    for segment in segments:
        text = segment.get("text", "").strip()
        start_time = segment.get("start", 0)
        
        # Change speaker if there's a significant pause (>1 second)
        if start_time - last_end_time > 1.0:
            current_speaker = 2 if current_speaker == 1 else 1
        
        formatted_transcript += f"Speaker {current_speaker}: {text}\n\n"
        last_end_time = segment.get("end", 0)
    
    return formatted_transcript

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Transcribe MP3 audio files to text with speaker diarization')
    parser.add_argument('file', help='Path to the MP3 file')
    parser.add_argument('--output', '-o', help='Path to save the transcript (txt file)')
    parser.add_argument('--api-key', help='OpenAI API key (optional if set as environment variable)')
    args = parser.parse_args()
    
    # Ensure output is a txt file if not specified
    output_path = args.output
    if output_path and not output_path.endswith('.txt'):
        output_path += '.txt'
    
    # Transcribe the file
    transcribe_audio_with_speakers(args.file, output_path, args.api_key)

if __name__ == "__main__":
    main()