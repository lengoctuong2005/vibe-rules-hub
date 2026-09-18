---
name: fal-ai
description: |
  Comprehensive fal.ai generative AI media suite covering Image Generation (Flux, SDXL, Ideogram, Nano Banana), Image Editing & Inpainting, Video Generation (Kling O3, Seedance, Veo 3), Video Editing, Generative Audio/Speech (CSM-1B, ThinkSound), 3D Asset Generation, Lip Sync & Avatars, Super-Resolution Upscaling, Image Restoration, Custom LoRA Training, Virtual Try-On, Realtime Streaming, and Computer Vision.
triggers:
  - "fal ai"
  - "fal generate"
  - "fal image"
  - "fal video"
  - "fal 3d"
  - "fal audio"
  - "kling video"
  - "seedance"
  - "flux image"
  - "lip sync"
  - "upscale image"
  - "virtual tryon"
  - "inpaint"
license: MIT
od:
  mode: media
  category: generative-ai
  upstream: "https://github.com/fal-ai-community/skills"
metadata:
  origin: ECC
---

# fal.ai Generative Media Suite

Production-grade guide for generating, transforming, and analyzing multimodal media (images, video, audio, 3D, vision) using fal.ai hosted models and MCP tools.

---

## 1. MCP Configuration & Tooling

To use fal.ai via MCP, configure your client settings (`~/.claude.json` or equivalent):

```json
{
  "mcpServers": {
    "fal-ai": {
      "command": "npx",
      "args": ["-y", "fal-ai-mcp-server"],
      "env": { "FAL_KEY": "YOUR_FAL_API_KEY" }
    }
  }
}
```

### Core MCP Tools
- `search(query)`: Discover current model endpoints by keyword.
- `find(endpoint_ids)`: Retrieve model parameters, schema, and pricing.
- `generate(app_id, input_data)`: Run inference synchronously or enqueue job.
- `result(request_id)`: Retrieve async job output.
- `status(request_id)`: Check execution status.
- `cancel(request_id)`: Abort a running inference task.
- `estimate_cost(estimate_type, endpoints)`: Calculate run cost before execution.
- `upload(file_path)`: Upload local images/videos for inference.

---

## 2. Image Generation & Diffusion Models

Supports Flux, SDXL, Ideogram, and Nano Banana pipelines.

### Nano Banana 2 (Drafts & Rapid Iterations)
```javascript
generate({
  app_id: "fal-ai/nano-banana-2",
  input_data: {
    prompt: "cyberpunk street market at dusk, neon lighting, highly detailed",
    image_size: "landscape_16_9",
    num_images: 1,
    seed: 42
  }
});
```

### Production Quality (Flux / Nano Banana Pro / Ideogram)
```javascript
generate({
  app_id: "fal-ai/nano-banana-pro",
  input_data: {
    prompt: "studio product shot of luxury wristwatch on black slate, dramatic rim light",
    image_size: "square",
    guidance_scale: 7.5,
    num_images: 1
  }
});
```

### Realtime Streaming Image Generation (`fal-realtime`)
For interactive UI canvases, live sketching, and instant moodboards:
```javascript
generate({
  app_id: "fal-ai/fast-sdxl/realtime",
  input_data: {
    prompt: "minimalist architectural interior, natural light",
    sync_mode: true
  }
});
```

---

## 3. Image Editing, Inpainting & Virtual Try-On

### Inpainting & Object Removal
```javascript
// 1. Upload source asset and mask
const image = await upload({ file_path: "./assets/scene.png" });
const mask = await upload({ file_path: "./assets/mask.png" });

// 2. Inpaint / Edit
generate({
  app_id: "fal-ai/flux-inpaint",
  input_data: {
    prompt: "modern ergonomic wooden chair",
    image_url: image.url,
    mask_url: mask.url
  }
});
```

### Virtual Try-On (`fal-tryon`)
Fit garments onto human models for ecommerce and lookbooks:
```javascript
generate({
  app_id: "fal-ai/idm-vton",
  input_data: {
    human_img: "<model_photo_url>",
    garm_img: "<clothing_item_url>",
    description: "casual linen summer shirt"
  }
});
```

---

## 4. Video Generation & Editing

### Kling Video v3 & Kling O3 (`fal-kling-o3`)
State-of-the-art text-to-video and image-to-video with synchronized audio:
```javascript
generate({
  app_id: "fal-ai/kling-video/v3/pro",
  input_data: {
    prompt: "Cinematic drone shot flying through a misty Nordic pine forest at sunrise",
    duration: "5s",
    aspect_ratio: "16:9",
    cfg_scale: 0.5
  }
});
```

### ByteDance Seedance 1.0 Pro
High dynamic motion and smooth physics:
```javascript
generate({
  app_id: "fal-ai/seedance-1-0-pro",
  input_data: {
    prompt: "High speed rally car drifting on gravel corner, dust clouds",
    image_url: "<optional_starter_frame_url>",
    duration: "5s",
    aspect_ratio: "16:9"
  }
});
```

### Google DeepMind Veo 3
```javascript
generate({
  app_id: "fal-ai/veo-3",
  input_data: {
    prompt: "Time-lapse of blooming cherry blossoms in Kyoto garden, ambient breeze",
    aspect_ratio: "16:9"
  }
});
```

### Video Style Transfer & Remixing (`fal-video-edit`)
```javascript
generate({
  app_id: "fal-ai/video-to-video/remix",
  input_data: {
    video_url: "<input_video_url>",
    prompt: "oil painting animation style, vibrant brush strokes"
  }
});
```

---

## 5. Audio, Speech & Lip Sync

### CSM-1B Conversational Text-to-Speech
```javascript
generate({
  app_id: "fal-ai/csm-1b",
  input_data: {
    text: "Welcome to the product overview. Let's walk through the architecture.",
    speaker_id: 0
  }
});
```

### ThinkSound (Video-to-Audio Foley)
Generates ambient audio and sound effects synchronized with video frames:
```javascript
generate({
  app_id: "fal-ai/thinksound",
  input_data: {
    video_url: "<video_url>",
    prompt: "gentle rain on window with distant soft thunder"
  }
});
```

### Lip Sync & Talking Heads (`fal-lip-sync`)
Syncs character or portrait video with recorded audio speech tracks:
```javascript
generate({
  app_id: "fal-ai/latentsync",
  input_data: {
    video_url: "<speaker_video_url>",
    audio_url: "<voiceover_audio_url>"
  }
});
```

---

## 6. 3D Asset Generation (`fal-3d`)

Transform text descriptions or 2D image concepts into textured 3D mesh assets (GLB/OBJ):
```javascript
generate({
  app_id: "fal-ai/trellis-3d",
  input_data: {
    image_url: "<concept_art_url>",
    texture_size: 1024,
    mesh_simplify: 0.95
  }
});
```

---

## 7. Restoration, Super-Resolution & Upscaling

### Super-Resolution 4K (`fal-upscale`)
```javascript
generate({
  app_id: "fal-ai/creative-upscaler",
  input_data: {
    image_url: "<low_res_url>",
    scale: 4,
    creativity: 0.35,
    prompt: "masterpiece, sharp textures, high resolution"
  }
});
```

### Face Restoration & Document Fixes (`fal-restore`)
```javascript
generate({
  app_id: "fal-ai/face-restore",
  input_data: {
    image_url: "<blurred_photo_url>",
    fidelity: 0.8
  }
});
```

---

## 8. Custom LoRA Model Training (`fal-train`)

Fine-tune custom styles, characters, or brand identity models on fal:
```javascript
generate({
  app_id: "fal-ai/flux-lora-training",
  input_data: {
    images_data_url: "<zip_archive_of_training_images>",
    trigger_word: "MYBRAND_STYLE",
    steps: 1000,
    learning_rate: 0.0004
  }
});
```

---

## 9. Computer Vision & Visual QA (`fal-vision`)

Extract data, run OCR, segment objects, and inspect images:
```javascript
generate({
  app_id: "fal-ai/florence-2-large",
  input_data: {
    image_url: "<document_or_diagram_url>",
    task_prompt: "<OCR_WITH_REGION>"
  }
});
```

---

## 10. Cost Estimation & Operational Tips

1. **Pre-flight Budget Check**:
   ```javascript
   estimate_cost({
     estimate_type: "unit_price",
     endpoints: { "fal-ai/kling-video/v3/pro": { unit_quantity: 1 } }
   });
   ```
2. **Seed Pinning**: Always pin `seed` when iterating on prompt variations.
3. **Draft to Final Pipeline**: Use fast models (Nano Banana 2 / SDXL Realtime) to lock composition before dispatching 4K upscale or high-tier video pipelines (Veo 3 / Kling).
