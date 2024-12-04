# TLDR
# Simple counter and duration calculator for MP3 files in the specified directory.

import os
from mutagen.mp3 import MP3

def count_mp3_files(directory_path):
    mp3_count = len([file for file in os.listdir(directory_path) 
                     if file.lower().endswith('.mp3')])
    return mp3_count

def get_total_duration(directory_path):
    total_seconds = 0
    
    # Iterate through all MP3 files
    for file in os.listdir(directory_path):
        if file.lower().endswith('.mp3'):
            try:
                file_path = os.path.join(directory_path, file)
                audio = MP3(file_path)
                total_seconds += audio.info.length # Add duration in seconds to the total
            except Exception as e:
                print(f"Error reading {file}: {str(e)}")
    
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    
    return {
        'total_seconds': total_seconds,
        'formatted': f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    }

# Example usage
directory = "datasets/inteligentne_rozmowy/chunks"  # Replace with your directory path
mp3_files = count_mp3_files(directory)
duration = get_total_duration(directory)

print(f"Number of MP3 files: {mp3_files}")
print(f"Total duration: {duration['formatted']} (HH:MM:SS)")
print(f"Total seconds: {duration['total_seconds']:.2f}")
