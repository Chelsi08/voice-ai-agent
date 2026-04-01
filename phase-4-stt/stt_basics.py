import whisper
import sounddevice as sd
import numpy as np

# Load the whisper model 
model = whisper.load_model("base")

print("🎤 Recording... Speak now! (5 seconds)")

# Record the audio through microphone
sample_rate = 16000  # whisper wants 16000hz
duration = 5  # seconds

audio = sd.rec(
    int(duration * sample_rate),    # total samples = duration x sample_rate
    samplerate=sample_rate,
    channels=1,   # mono audio - one channel 
    dtype=np.float32   #Whisper wants float32
)
sd.wait()  # wait once the recording is over

print("Recording done! Transcribing...")

# converting the speech to text
audio_squeezed = np.squeeze(audio)  # fix shape
result = model.transcribe(audio_squeezed)

print(f"You said: {result['text']}")