# Use this script to transcribe audio files using whisper-large-v3-turbo model in the chunks directory.

import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import os

directory = "chunks"  # Specify your input directory
audio_data = None

for file_name in os.listdir(directory):
    if file_name.endswith(".mp3"):
        try:
            file_path = os.path.join(directory, file_name)
            with open(file_path, "rb") as uploaded_file:
                audio_data = uploaded_file.read()
                print(f"Processing file: {file_name}")
        except FileNotFoundError:
            print(f"Error: {file_name} file not found")
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            continue


    if audio_data:

        # Whisper model (you can use other models as well, turbo is the fastest one)
        model_id = "openai/whisper-large-v3-turbo"

        # Set polish language as default
        audio_language = "polish"

        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, 
            torch_dtype=torch_dtype, 
            low_cpu_mem_usage=True, 
            use_safetensors=True,
            device_map="auto"
        )

        processor = AutoProcessor.from_pretrained(model_id)

        pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            torch_dtype=torch_dtype,
            device_map="auto"
        )

        result = pipe(audio_data, generate_kwargs={"language": "polish"})

        # Write text to a file
        output_filename = file_name.replace('.mp3', '.txt')
        f = open(f"chunks/{output_filename}", "w")
        f.write(result["text"])
        f.close()