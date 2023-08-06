# retico-speechbraintts

Local speechbrain speech synthesis for retico.

## Installation and requirements

You can install the module via pip:

```bash
$ pip install retico-speechbraintts
```

For this, PyTorch has to be installed:

```bash
$ pip install torch
```

## Example

```python
from retico_core import *
import retico_wav2vecasr
import retico_speechbraintts

microphone = audio.MicrophoneModule()
asr = retico_wav2vecasr.Wav2VecASRModule("en")
tts = retico_speechbraintts.SpeechBrainTTSModule("en")
speaker = audio.SpeakerModule(rate=22050)

microphone.subscribe(asr)
asr.subscribe(tts)
tts.subscribe(speaker)

network.run(asr)

print("Running the TTS. Press enter to exit")
input()

network.stop(asr)
```