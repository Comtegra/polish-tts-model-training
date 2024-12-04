# Polish TTS Model Training 

## Introduction
The goal of this project is to fine-tune a Text-to-Speech (TTS) model for the Polish language, enhancing accessibility and usability for Polish speakers. The goal is to fine-tune a pre-trained model on a diverse dataset of Polish speech, preferably the one from ["inteligentne rozmowy" Podcast](https://www.youtube.com/@inteligentnerozmowy). For potential training and tests we gathered and used various datasets, which will be described below.

## Objectives 
- Develop a high-quality TTS model for Polish language.
- Evaluate the model's performance against existing benchmarks and models.
- Ensure the model can handle various accents and dialects within the Polish language.

## What have we tried so far?
### suno-ai/bark
Bark gives a great TTS output, however it's not necessarily easily accessible for training. The repo itself doesn't have a training recipe. Training the model using HuggingFace trainer.train() function was tricky since bark doesn't have a direct processor and we couldn't get it to work. There's a possibly useful repository: [barkify](https://github.com/anyvoiceai/Barkify), yet it requires a lot of additional work to be fully functional. **Please note that this repository has been archived by the owner on May 27, 2024. It is now read-only.** As of November 19th, 2024, the repo is no longer actively maintained, which makes it hard to use.

### SpeechT5
After some struggles with suno-ai/bark we decided to try a different model called "SpeechT5". After finding a [Fine-tuning tutorial](https://huggingface.co/learn/audio-course/chapter6/fine-tuning) on Hugging Face, we decided to use a pre-trained model called "SpeechT5" for fine-tuning. The model was trained, a few different times on a diverse datasets of Polish speech, including our own dataset based on ["inteligentne rozmowy" Podcast](https://www.youtube.com/@inteligentnerozmowy).

At first we tried training the model using Facebook's VoxPopuli dataset. The training process was quite fast, taking only a few hours to complete. The model was able to generate polish speech from text, though the quality was not as good as we hoped for.

Models trained on different datasets:
First training (Part of VoxPopuli dataset):
https://huggingface.co/d190305/speecht5_finetuned_voxpopuli_pl

Second training (Full VoxPopuli dataset):
https://huggingface.co/d190305/speecht5_finetuned_voxpopuli_pl_full_dataset

Third training (Inteligentne rozmowy Podcast - first 1000 audio files):
https://huggingface.co/d190305/speecht5_finetuned_voxpopuli_pl_inteligentne

Fourth training (Inteligentne rozmowy Podcast - Full dataset):
https://huggingface.co/d190305/speecht5_finetuned_pl_inteligentne_full

#### Observations and results
Within the first training (with just a part of the VoxPopuli dataset) the difference is noticeable, the model is able to generate speech with a more natural sounding light polish accent. It's no longer a robotic voice with absolutely no polish accent and pronunciation.

Within the second training (with full VoxPopuli dataset) the quality of the voice is similar to the first training, though the accent seems to be slightly better. The problem though is that the model is not always able to pronounce words correctly, sometimes repeating them multiple times, pronouncing them with a wrong accent, cutting them off or not generating them at all.

Within the third training (with first 1000 audio chunks from inteligentne rozmowy podcast dataset) the model gets a really slight polish accent, though it's unable to pronounce words correctly. In majority of the cases the words are cut off, repeated multiple times, stuck on the first word (not continuing further into the sentence) or not generated at all. The effects are significantly worse than those observed in the first two trainings on the VoxPopuli dataset.

Within the fourth training (with full inteligentne rozmowy podcast dataset) the model is not able to generate speech at all. Which is a bit surprising since the first three trainings were able to at least generate some speech. Possible reasons for this could be that the dataset could have potential errors, changing sampling rate from 48kHz to 16kHz might have went wrong or loading arrays into the dataset went wrong.

## Datasets
- **Datasets Used**:
    - **[VoxPopuli](https://huggingface.co/datasets/facebook/voxpopuli/viewer/pl)**: A large dataset for general speech patterns. It's an ASR (Automatic Speech Recognition) dataset, not a TTS one, which is why the quality of the audio is not the best.
    - **[inteligentne rozmowy podcast](https://www.youtube.com/@inteligentnerozmowy)**: High quality dataset of Polish speech based on a Podcast.

### Other polish datasets
- **[Nemo](https://csi.amu.edu.pl/datasets/nemo-dataset-of-emotional-speech-in-polish)**
- **[Pelcraparl](https://www.kaggle.com/datasets/jimregan/pelcraparl)**
- **[Luna](https://www.kaggle.com/datasets/czyzi0/luna-speech-dataset)**
- **[The MC Speech Dataset](https://www.kaggle.com/datasets/czyzi0/the-mc-speech-dataset)**
- **[Mozilla Polish Commonvoice](https://commonvoice.mozilla.org/pl/datasets)**
- **[Facebook Multilingual Librispeech](https://huggingface.co/datasets/facebook/multilingual_librispeech/viewer/polish)**


## What might be interesting to try next?
- Experiment with different models, especially the ones with an easier fine-tuning recipe than Bark.
- Incorporate more diverse datasets to improve model robustness.
- Retrain already trained models on different datasets to see how they perform and improve.

## Problems we are facing
- **Data Quality**: Some datasets contain noise or inconsistencies that affect training. E.g. The VoxPopuli dataset is made to train ASR models, not TTS so the quality of the audio is not the best, which can be heard in the generated speech on a trained model. The audio seems to be of lower quality and has a lot of background noise.
- **Speaker/Accent Variability**: Difficulty in capturing the nuances of different Polish accents and speakers. Preparing a dataset with a diverse set of accents and speakers is a challenging task, which takes a lot of time and effort.
- **Model Complexity**: Some models are just not suitable for fine-tuning because they don't come with a direct fine-tuning recipe. Bark is a great example of a really good model that is really hard to fine-tune. Check this issue for further details: [How to train this model #37 ](https://github.com/suno-ai/bark/issues/37).


## Future Work and key insights
- Explore different models, maybe some that are easier to fine-tune.
- All TTS with sampling rate < 32k kHz are awful, I'd recommend not using them at all.
- The more high quality data you have the better.

## References
- [Hugging Face Fine-tuning Audio Course](https://huggingface.co/learn/audio-course/chapter6/fine-tuning)
- [Barkify](https://github.com/anyvoiceai/Barkify)

### Files attached in the python_scripts folder and their purpose:
- **arrow_creator.py**: Create Arrow file dataset from your own files for training a TTS model (arrow is the file format used by 🤗 Datasets under the hood, therefore it's recommended to use).
- **audio_splitter.py**: Split audio files into chunks
- **audio_transcribe.py**: Transcribe audio files using whisper-large-v3-turbo model.
- **counter.py**: Simple counter and duration calculator for MP3 files in the specified directory to check the size of the dataset.
- **json_creator.py**: Create a JSON file dataset for training a TTS model (Technically you can use this script to create a JSON file dataset for training a TTS model. However, Arrow is the file format used by 🤗 Datasets under the hood, therefore it's recommended to use).
- **samplerate_convert.py**: Convert audio files sample rate from 48kHz to 16kHz. Might be unnecessary depending on the model you're using (SpeechT5 expects audio data to have a sampling rate of 16 kHz).

## How to train a model?
After gathering an audio you want to chunk and train perform the following steps:
1. Split into chunks using audio_splitter.py
2. Transcribe audio files using audio_transcribe.py
3. Convert sample rate (if needed) using samplerate_convert.py
4. Optionally you can use counter.py to check the size of the dataset.
5. Create an Arrow file dataset using arrow_creator.py
6. Install all necessary dependencies using softstack.ipynb
7. Fine-tune the model using huggingface trainer.train() function. For reference check the notebooks provided in this repository.

Trained on A5000 GPU. Average training time: 2-4 hours. Dependent on dataset.


