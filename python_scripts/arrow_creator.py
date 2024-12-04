# TLDR
# Use this script to create an Arrow file dataset for training a TTS model. 
# Arrow is the file format used by 🤗 Datasets under the hood, therefore it's recommended to use.
# For more information visit: https://huggingface.co/docs/datasets/loading


import os
import pyarrow as pa
import librosa

# Sampling rate of the audio files in the dataset (for Inteligentne Rozmowy Podcast it's 48kHz)
sr = 48000

# Create schema for the Arrow table (Array will be handled later by loading the dataset)
schema = pa.schema([
    pa.field('audio_id', pa.string()),
    pa.field('audio', pa.struct([
        pa.field('path', pa.string()),
        pa.field('sampling_rate', pa.int32())
    ]), nullable=False),
    pa.field('text', pa.string()),
    pa.field('speaker_id', pa.int64()),
    pa.field('gender', pa.string())
])

# Create output directory if it doesn't exist
os.makedirs("arrow_train_data", exist_ok=True)

# Create writer
output_file = os.path.join("arrow_train_data", 'dataset.arrow')
sink = pa.OSFile(output_file, 'wb')
writer = pa.RecordBatchFileWriter(sink, schema)

for file in os.listdir("chunks/converted"):
    if file.endswith(".wav"):
        try:
            print(f"Processing file: {file}")
            
            audio_path = os.path.join("chunks/converted", file)
            audio_id = file.replace(".wav", "")
            
            # Load and process audio file
            _, sr = librosa.load(audio_path, sr=sr, mono=True)
            
            text_file = file.replace(".wav", ".txt")
            with open(os.path.join("chunks", text_file), "r", encoding='utf-8') as t:
                text = t.read()

            # Create the entry based on the schema we set earlier
            entry = {
                "audio_id": audio_id,
                "audio": {
                    "path": os.path.abspath(audio_path),
                    "sampling_rate": sr
                },
                "text": text,
                "speaker_id": 1, # TODO: Add speaker_id to dataset, as of now it's set to 1 because we didn't differentiate between speakers
                "gender": "male"
            }
            
            # Write single entry
            batch = pa.RecordBatch.from_pylist([entry], schema=schema)
            writer.write_batch(batch)
            
            # Clear memory in order to avoid memory error
            del entry
            del batch
            
            print(f"Successfully processed: {file}")
            
        except Exception as e:
            print(f"Error processing {file}: {str(e)}")
            continue

writer.close()
sink.close()
