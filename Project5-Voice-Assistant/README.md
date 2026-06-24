# Voice-Controlled Browser Assistant

A simple Python voice assistant that listens to voice commands and opens websites automatically using speech recognition and text-to-speech.

## Features
- Voice-activated commands using Google Speech Recognition
- Opens YouTube, LinkedIn, GitHub, or Google based on spoken command
- Text-to-speech feedback using pyttsx3
- Exit anytime by saying "bye"

## Tech Stack
- Python
- SpeechRecognition
- pyttsx3 (text-to-speech)
- webbrowser (built-in)

## How It Works
1. The assistant listens through the microphone
2. Converts speech to text using Google's speech recognition API
3. Matches the recognized command against known keywords
4. Opens the corresponding website, or asks the user to repeat if unrecognized

## How to Run

```bash
pip install -r requirements.txt
python main.py
```

Then speak one of: "YouTube", "LinkedIn", "GitHub", "Google", or "bye" to exit.

## Example Commands
- "Open YouTube" → launches youtube.com
- "GitHub" → launches github.com
- "bye" → exits the assistant