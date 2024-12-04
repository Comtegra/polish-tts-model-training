# TLDR
# Technically you can use this script to create a JSON file dataset for training a TTS model. 
# However, it's not recommended to use it for training, since it's not efficient and takes a lot of time.
# Arrow is the file format used by 🤗 Datasets under the hood, therefore it's recommended to use it instead.
# For more information visit: https://huggingface.co/docs/datasets/loading

import os
import json

with open("data.json", "w") as f:
    f.write("[\n")
    
    # Made this to avoid writing a comma before the first item
    first_item = True
    for file in os.listdir("chunks"):
        if file.endswith(".mp3"):
            try:
                print(f"Processing file: {file}")
                
                audio_path = os.path.join("chunks", file)
                audio_id = file.replace(".mp3", "")
                sr = 16000
                
                text_file = file.replace(".mp3", ".txt")
                with open(os.path.join("chunks", text_file), "r", encoding='utf-8') as t:
                    text = t.read()

                entry = {
                    "audio_id": audio_id,
                    "audio": {
                        "path": os.path.abspath(audio_path),
                        "sampling_rate": sr
                    },
                    "text": text,
                    "speaker_id": 1,
                    "gender": "male"
                }
                
                if not first_item:
                    f.write(",\n")
                json.dump(entry, f, indent=2)
                f.flush()
                
                del entry # Clear the entry data from memory not to raise memory error
                
                first_item = False
                print(f"Successfully processed: {file}")
                
            except Exception as e:
                print(f"Error processing {file}: {str(e)}")
                continue
    
    f.write("\n]")