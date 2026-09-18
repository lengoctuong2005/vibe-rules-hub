---
name: venice-ai-media
description: |
  Comprehensive Generative AI Media Suite powered by Venice.ai API. Unifies text-to-video generation & transcription, AI music composition & background scoring, high-fidelity text-to-speech voice synthesis, image editing/inpainting/upscaling, and text-to-image prompt engineering.
triggers:
  - "venice ai"
  - "venice video"
  - "venice music"
  - "venice tts"
  - "venice speech"
  - "venice image"
  - "ai media"
license: MIT
metadata:
  origin: ECC
---

# Venice AI Generative Media Suite

Enterprise orchestration for programmatic multi-modal generation covering video generation, music composition, speech synthesis, and image synthesis via Venice.ai.

---

## 1. Text-to-Video Generation & Transcription

Create cinematic video clips and transcribe spoken audio using high-throughput GPU pipelines:

```python
# ponytail: Venice Video Generation Request - standard JSON payload
import os
import requests

VENICE_API_KEY = os.getenv("VENICE_API_KEY")

def generate_ai_video(prompt: str, duration_sec: int = 5, aspect_ratio: str = "16:9") -> str:
    url = "https://api.venice.ai/api/v1/video/generate"
    headers = {
        "Authorization": f"Bearer {VENICE_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "venice-video-ultra",
        "prompt": prompt,
        "duration": duration_sec,
        "aspect_ratio": aspect_ratio,
        "motion_bucket_id": 127,
    }
    res = requests.post(url, json=payload, headers=headers, timeout=60)
    res.raise_for_status()
    return res.json().get("video_url")
```

---

## 2. AI Music Composition & Audio Scoring

Generate customized background scores, jingles, and ambient soundscapes with controlled tempo and key:

- **Prompt Structure**: `[Genre] + [Mood] + [BPM/Tempo] + [Instrumentation] + [Arrangement]`
- **Example**: `"Cyberpunk synthwave, dark brooding bassline, 118 BPM, analog Moog synth, cinematic trailer climax"`

---

## 3. High-Fidelity Speech & Voice Synthesis (TTS)

Convert script dialog into natural speech with emotional modulation:

```python
# ponytail: Venice Text-to-Speech Streaming Generator
def synthesize_speech(text: str, voice_id: str = "narrator-british-male", speed: float = 1.0) -> bytes:
    url = "https://api.venice.ai/api/v1/audio/speech"
    headers = {"Authorization": f"Bearer {VENICE_API_KEY}"}
    payload = {
        "model": "venice-tts-v2",
        "input": text,
        "voice": voice_id,
        "response_format": "mp3",
        "speed": speed,
    }
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.content
```

---

## 4. Image Generation, Inpainting & Super-Resolution

- **Text-to-Image**: High-resolution generation with strict negative prompt filtering to remove artifacts.
- **Inpainting & Masking**: Modify local regions without changing surrounding composition.
- **4x Super-Resolution Upscaling**: Enhance clarity for production print and high-DPI displays.

```python
def generate_image(prompt: str, style_preset: str = "photographic") -> str:
    url = "https://api.venice.ai/api/v1/image/generate"
    headers = {"Authorization": f"Bearer {VENICE_API_KEY}"}
    payload = {
        "model": "venice-image-v3",
        "prompt": prompt,
        "negative_prompt": "blurry, low quality, distorted, extra limbs, watermark",
        "width": 1024,
        "height": 1024,
        "steps": 30,
        "style_preset": style_preset,
    }
    response = requests.post(url, json=payload, headers=headers, timeout=45)
    response.raise_for_status()
    return response.json()["images"][0]["url"]
```
