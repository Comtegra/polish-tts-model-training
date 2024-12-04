import librosa
import soundfile as sf
import os
from pathlib import Path
from tqdm import tqdm

def convert_sample_rate(input_file, output_file, target_sr=16000):
    """
    Convert audio file sample rate from 48kHz to 16kHz (SpeechT5 expects audio data to have a sampling rate of 16 kHz)
    """
    # Load the audio file
    audio, sr = librosa.load(input_file, sr=None) # sr=None to get the original sample rate
    
    # Resample audio
    if sr != target_sr:
        audio_resampled = librosa.resample(y=audio, orig_sr=sr, target_sr=target_sr)
    else:
        audio_resampled = audio
    
    # Save the resampled audio
    sf.write(output_file, audio_resampled, target_sr)

def process_folder(folder_path="chunks"):
    """Process all MP3 files in the specified folder"""
    # Create folder for converted files
    output_folder = Path(folder_path) / "converted"
    output_folder.mkdir(exist_ok=True)
    
    # Get all MP3 files
    mp3_files = list(Path(folder_path).glob("*.mp3"))
    converted_files = []  # Track converted files
    
    # Process each file with a progress bar
    for mp3_file in tqdm(mp3_files, desc="Converting files"):
        output_file = output_folder / mp3_file.name
        # Convert to WAV as soundfile doesn't support MP3 output
        output_file = output_file.with_suffix('.wav')
        convert_sample_rate(str(mp3_file), str(output_file))
        converted_files.append(output_file.name)

    # Print summary of converted files
    print("\nConverted files:")
    for file in converted_files:
        print(f"- {file}")

if __name__ == "__main__":
    process_folder()
    print("Conversion complete! Check the 'chunks/converted' folder for the results.")
