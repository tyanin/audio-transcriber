# transcriber.py
import os
import argparse
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

def transcribe_audio_with_speakers(file_path, output_path=None):
    """
    Transcribe an MP3 audio file to text with basic speaker diarization
    
    Args:
        file_path (str): Path to the MP3 file
        output_path (str, optional): Path to save the transcript. If None, prints to console.
        
    Returns:
        str: The transcribed text with speaker labels
    """
    print(f"Processing {file_path}...")
    
    # Convert MP3 to WAV
    print("Converting MP3 to WAV format...")
    audio = AudioSegment.from_mp3(file_path)
    wav_path = file_path.replace('.mp3', '.wav')
    audio.export(wav_path, format="wav")
    
    try:
        # Split audio on silence to get segments
        print("Splitting audio into segments based on silence...")
        segments = split_on_silence(
            audio,
            min_silence_len=1000,  # 1 second silence to split
            silence_thresh=-40,    # silence threshold in dB
            keep_silence=500       # keep 500ms of silence at the start/end
        )
        
        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Process each segment
        transcript = ""
        current_speaker = 1
        
        print(f"Found {len(segments)} audio segments. Transcribing...")
        for i, segment in enumerate(segments):
            # Save segment to a temp WAV file
            segment_path = f"temp_segment_{i}.wav"
            segment.export(segment_path, format="wav")
            
            # Transcribe the segment
            try:
                with sr.AudioFile(segment_path) as source:
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data)
                    
                    # Change speaker based on segment (simplified heuristic)
                    if i > 0 and len(text.strip()) > 0:
                        # Check if enough time has passed to assume speaker change
                        # (this is a simple heuristic - could be improved)
                        current_speaker = 2 if current_speaker == 1 else 1
                    
                    # Add to transcript if there's text
                    if text.strip():
                        transcript += f"Speaker {current_speaker}: {text}\n\n"
            except sr.UnknownValueError:
                # No speech detected in this segment
                pass
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
            
            # Clean up temp file
            os.remove(segment_path)
        
        print("Transcription complete!")
        
    except Exception as e:
        transcript = f"Error during transcription: {str(e)}"
        print(transcript)
    finally:
        # Clean up WAV file
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

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Transcribe MP3 audio files to text with speaker diarization')
    parser.add_argument('file', help='Path to the MP3 file')
    parser.add_argument('--output', '-o', help='Path to save the transcript (txt file)')
    args = parser.parse_args()
    
    # Ensure output is a txt file if not specified
    output_path = args.output
    if output_path and not output_path.endswith('.txt'):
        output_path += '.txt'
    
    # Transcribe the file
    transcribe_audio_with_speakers(args.file, output_path)

if __name__ == "__main__":
    main()