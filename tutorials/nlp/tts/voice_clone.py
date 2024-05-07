import os
import argparse
import torch
from TTS.api import TTS

#https://huggingface.co/coqui/XTTS-v2

class VoiceClone:
    def __init__(self, text, speaker_wav, output_wav, lang='en'):
        self.model = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=torch.cuda.is_available())
        self.speaker_wav = speaker_wav
        self.output_wav = output_wav
        self.text = text
        self.lang = lang

    def text_to_speech(self):
        self.model.tts_to_file(text=self.text,
                               file_path=self.output_wav,
                               speaker_wav=self.speaker_wav,
                               language=self.lang)
        

def main():
    parser = argparse.ArgumentParser(description="Voice Clone TTS")
    parser.add_argument = ("-t", "--text", type=str, help="Text to transform into speech.")
    parser.add_argument = ("-s", "--speaker_wav", type=str, help="Speaker WAV filepath for use in voice cloning task.")
    parser.add_argument = ("-o", "--output_wav", type=str, help="Output WAV filepath.")
    parser.add_argument = ("-l", "--lang", type=str, default="en", help="Language (e.g., en)")
    
    args = parser.parse_args()
    
    tts = VoiceClone(args.text, args.speaker_wav, args.output_wav, args.lang)
    tts.text_to_speech()
    print("\nTask Complete!\n")
    
if __name__ == "__main__":
    main()
