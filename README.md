# audio-transcriber
Personal audio transcriber for my research (I have hours upon hours of audio to transcribe and dont have the time to do it manually)
Wrote out the readme before completion of project, just as a roadmap for me:

## Acknowledgments

- This project was developed with assistance from Claude AI (Anthropic).

# Audio Transcriber

A Python tool to transcribe MP3 audio files to text with speaker diarization.

## Features

- Transcribe MP3 files to text
- Distinguish between different speakers
- Command-line interface for easy use
- Save transcripts to text files or view them in the console

## Installation

1. Clone repo:
   ```
   git clone https://github.com/yourusername/audio-transcriber.git
   cd audio-transcriber
   ```

2. Create virtual environment/activate it:
   ```
   python -m venv venv
   
   # On Windows
   .\venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```
python transcriber.py path/to/your/audiofile.mp3 --api-key YOUR_OPENAI_API_KEY
```

### Save Output to File

```
python transcriber.py path/to/your/audiofile.mp3 -o output_transcript.txt --api-key YOUR_OPENAI_API_KEY
```

### Using Environment Variable for API Key

You can set your OpenAI API key as an environment variable to avoid passing it each time:

```bash
# On Windows
set OPENAI_API_KEY=your-api-key-here

# On macOS/Linux
export OPENAI_API_KEY=your-api-key-here
```

Then run:
```
python transcriber.py path/to/your/audiofile.mp3 -o output_transcript.txt
```

## How It Works

1. The tool converts MP3 to WAV format using pydub
2. It uses OpenAI's Whisper API to perform the transcription
3. The code processes the response to identify different speakers
4. The transcript with speaker labels is displayed in the console or saved to a text file

## Speaker Detection

This implementation uses a simple heuristic to detect speaker changes based on pauses in speech. If there's a significant pause (>1 second), it assumes a different person is speaking.

## Goal Output (still in progress)
```
Speaker 1: Hello everyone, welcome to today's meeting about the quarterly results.

Speaker 2: Thanks for having us. I'm excited to share the data from Q3.

Speaker 1: Before we dive in, did everyone receive the slide deck I sent yesterday?

Speaker 2: Yes, I've reviewed it and have a few questions about the marketing spend on page 12.

Speaker 1: Great point. The increase in marketing was due to our new product launch in August.

Speaker 2: That makes sense. I see the ROI numbers are quite strong compared to previous campaigns.

Speaker 1: Exactly. We're seeing a 24% improvement in conversion rates across all channels.
```

## Future Improvements

- Support for more audio formats
- More accurate speaker identification
- Batch processing for multiple files
- A simple graphical user interface

## License

This project is licensed under the MIT License - see the LICENSE file for details.