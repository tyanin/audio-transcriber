# vosk_transcriber.py
import os
import argparse
import json
import wave
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment

def transcribe_audio(file_path, output_path=None):
    """
    Transcribe an MP3 audio file to text using Vosk
    
    Args:
        file_path (str): Path to the MP3 file
        output_path (str, optional): Path to save the transcript. If None, prints to console.
        
    Returns:
        str: The transcribed text
    """
    print(f"Processing {file_path}...")
    
    # Download model if it doesn't exist
    model_path = "vosk-model-small-en-us-0.15"
    if not os.path.exists(model_path):
        print("Downloading the model...")
        import urllib.request
        import zipfile
        
        url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
        zip_path = "vosk-model-small-en-us-0.15.zip"
        urllib.request.urlretrieve(url, zip_path)
        
        print("Extracting the model...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(".")
        os.remove(zip_path)
    
    # Convert MP3 to WAV
    print("Converting MP3 to WAV format...")
    audio = AudioSegment.from_mp3(file_path)
    wav_path = file_path.replace('.mp3', '.wav')
    audio.export(wav_path, format="wav")
    
    # Load the model and process the audio
    print("Transcribing audio...")
    model = Model(model_path)
    
    wf = wave.open(wav_path, "rb")
    
    # Check if the WAV file has the correct format
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        return ""
    
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    
    transcript = ""
    last_speaker = 1
    
    # Process audio in chunks
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            if result.get("text", ""):
                # Simple speaker alternation based on pauses
                current_speaker = 2 if last_speaker == 1 else 1
                last_speaker = current_speaker
                
                transcript += f"Speaker {current_speaker}: {result['text']}\n\n"
    
    # Get the final part
    result = json.loads(rec.FinalResult())
    if result.get("text", ""):
        current_speaker = 2 if last_speaker == 1 else 1
        transcript += f"Speaker {current_speaker}: {result['text']}\n\n"
    
    # Clean up
    wf.close()
    if os.path.exists(wav_path):
        os.remove(wav_path)
    
    print("Transcription complete!")
    
    # Save or print transcript
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(transcript)
        print(f"Transcript saved to {output_path}")
    else:
        print("\nTranscript:")
        print(transcript)
    
    return transcript

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Transcribe MP3 audio files to text')
    parser.add_argument('file', help='Path to the MP3 file')
    parser.add_argument('--output', '-o', help='Path to save the transcript (txt file)')
    args = parser.parse_args()
    
    # Ensure output is a txt file if not specified
    output_path = args.output
    if output_path and not output_path.endswith('.txt'):
        output_path += '.txt'
    
    # Transcribe the file
    transcribe_audio(args.file, output_path)

if __name__ == "__main__":
    main()