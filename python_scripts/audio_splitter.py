# TLDR
# Use this script to split an MP3 file into chunks of random length between 2 and 10 seconds.

from pydub import AudioSegment
import math
import os
import random
import sys

if len(sys.argv) != 2:
    print("Usage: python audiosplitter.py <file_name>")
    sys.exit(1)

file_name = sys.argv[1]


def get_random_chunk_length():
    """Generate a random chunk length between 2 and 10 seconds"""
    return random.randint(2, 10)

def split_audio(input_file, output_dir="chunks", chunk_length_sec=10):
    """
    Split an MP3 file into chunks of specified length, as of now we set the chunk length between 2 and 10 seconds
    """

    # Validate chunk length
    if not 1 <= chunk_length_sec <= 10:
        raise ValueError("Chunk length must be between 1 and 10 seconds")
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Load the audio file
    audio = AudioSegment.from_mp3(input_file)
    
    # Get the duration in milliseconds
    duration = len(audio)
    chunk_length_ms = chunk_length_sec * 1000
    chunks = math.ceil(duration / chunk_length_ms)
    
    # Split the audio file into chunks
    for i in range(chunks):
        start_time = i * chunk_length_ms
        end_time = min((i + 1) * chunk_length_ms, duration)
        
        # Extract the chunk
        chunk = audio[start_time:end_time]
        
        # Generate output filename
        filename = os.path.splitext(os.path.basename(input_file))[0]
        chunk_name = f"{filename}_chunk_{i+1}.mp3"
        chunk_path = os.path.join(output_dir, chunk_name)
        
        # Export the chunk
        chunk.export(chunk_path, format="mp3")


output_dir = "chunks"  # Directory to save chunks
split_audio(file_name, output_dir, chunk_length_sec=get_random_chunk_length()) 