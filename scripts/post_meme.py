#!/usr/bin/env python3
import os
import requests
import datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# ── Config ───────────────────────────────────────────────────────────────────
HF_TOKEN    = os.getenv("HF_TOKEN")
TEXT_MODEL  = "distilgpt2"                    # small, hosted GPT-2 variant
IMAGE_MODEL = "stabilityai/stable-diffusion-2" # your chosen text2img model

# ── Caption generation ───────────────────────────────────────────────────────
def generate_caption() -> str:
    url = (
        "https://api-inference.huggingface.co/pipeline/text-generation"
        f"?model={TEXT_MODEL}"
    )
    payload = {
        "inputs": "One short, nostalgic 90s meme caption",
        "options": {"wait_for_model": True}
    }
    resp = requests.post(
        url,
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json=payload
    )
    resp.raise_for_status()
    # pipeline returns [{ "generated_text": "..." }]
    text = resp.json()[0]["generated_text"]
    return text.strip().split("\n")[0]

# ── Image generation ─────────────────────────────────────────────────────────
def generate_image(prompt: str) -> Image.Image:
    resp = requests.post(
        f"https://api-inference.huggingface.co/models/{IMAGE_MODEL}",
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json={"inputs": prompt}
    )
    resp.raise_for_status()
    return Image.open(BytesIO(resp.content))

# ── Overlay the caption at bottom of image ──────────────────────────────────
def overlay_caption(img: Image.Image, caption: str) -> Image.Image:
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    w, h = draw.textsize(caption, font=font)
    x = (img.width - w) // 2
    y = img.height - h - 10
    # semi‐transparent box behind text
    draw.rectangle((x-5, y-5, x+w+5, y+h+5), fill=(0,0,0,180))
    draw.text((x, y), caption, font=font, fill=(255,255,255))
    return img

# ── Main: generate, save, commit-ready ───────────────────────────────────────
def main():
    caption = generate_caption()
    img     = generate_image(caption)
    meme    = overlay_caption(img, caption)
    ts      = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H%M%S")
    os.makedirs("memes", exist_ok=True)
    path    = f"memes/{ts}.png"
    meme.save(path)
    print("Saved", path)

if __name__ == "__main__":
    main()
