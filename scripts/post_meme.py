#!/usr/bin/env python3
import os, requests, datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

HF_TOKEN    = os.getenv("HF_TOKEN")
TEXT_MODEL  = "gpt2"
IMAGE_MODEL = "stabilityai/stable-diffusion-2"

def generate_caption():
    resp = requests.post(
        f"https://api-inference.huggingface.co/models/{TEXT_MODEL}",
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json={"inputs": "One short, nostalgic 90s meme caption"}
    )
    resp.raise_for_status()
    return resp.json()[0]["generated_text"].split("\n")[0]

def generate_image(prompt):
    resp = requests.post(
        f"https://api-inference.huggingface.co/models/{IMAGE_MODEL}",
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json={"inputs": prompt}
    )
    resp.raise_for_status()
    return Image.open(BytesIO(resp.content))

def overlay_caption(img, caption):
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    w, h = draw.textsize(caption, font=font)
    x, y = (img.width - w)//2, img.height - h - 10
    draw.rectangle((x-5,y-5,x+w+5,y+h+5), fill=(0,0,0,180))
    draw.text((x,y), caption, font=font, fill=(255,255,255))
    return img

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
