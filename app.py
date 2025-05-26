from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import os

app = Flask(__name__)

# Banner configuration
BANNER_TEMPLATE = "banner_template.png"
FONT1_PATH = "orbitron_regular.ttf"
FONT2_PATH = "quick_sand.ttf"

TEXT1 = {"position": (582, 190), "size": 116, "color": (255, 255, 255)}  # white
TEXT2 = {"position": (582, 165), "size": 40, "color": (255, 255, 255)}  # white


@app.route("/", methods=["GET", "POST"])
def index():
    image_data = None

    if request.method == "POST":
        text1 = request.form.get("text1", "")
        text2 = request.form.get("text2", "")
        print(f"[INFO] Generating banner with text1: '{text1}', text2: '{text2}'")

        try:
            img = generate_banner(text1, text2)
            img_io = io.BytesIO()
            img.save(img_io, "PNG")
            img_io.seek(0)

            image_data = base64.b64encode(img_io.getvalue()).decode("utf-8")
            print("[INFO] Banner generated successfully")

        except Exception as e:
            print(f"[ERROR] Failed to generate banner: {e}")

    return render_template("index.html", image_data=image_data)


def generate_banner(text1, text2):
    try:
        print(f"[INFO] Opening template: {BANNER_TEMPLATE}")
        img = Image.open(BANNER_TEMPLATE).convert("RGBA")
    except Exception as e:
        print(f"[ERROR] Cannot open template: {e}")
        raise FileNotFoundError(f"Cannot open template: {e}")

    draw = ImageDraw.Draw(img)

    try:
        print(f"[INFO] Loading fonts: {FONT1_PATH}, {FONT2_PATH}")
        font1 = ImageFont.truetype(FONT1_PATH, TEXT1["size"])
        font2 = ImageFont.truetype(FONT2_PATH, TEXT2["size"])
    except Exception as e:
        print(f"[ERROR] Font loading issue: {e}")
        font1 = font2 = ImageFont.load_default()

    if text1.strip():
        # Calculate text width for centering
        text1_width = draw.textlength(text1, font=font1)
        # Center the text horizontally while keeping Y position
        text1_x = (img.width - text1_width) // 2
        text1_position = (text1_x, TEXT1["position"][1])
        print(f"[INFO] Drawing text1 at position: {text1_position}")
        draw.text(text1_position, text1, font=font1, fill=TEXT1["color"])

        # Align TEXT2 to the left edge of TEXT1
        if text2.strip():
            text2_position = (text1_x, TEXT2["position"][1])
            print(f"[INFO] Drawing text2 at position: {text2_position}")
            draw.text(text2_position, text2, font=font2, fill=TEXT2["color"])
    elif text2.strip():
        # If only TEXT2 is present, use its original position
        print(f"[INFO] Drawing text2 at original position: {TEXT2['position']}")
        draw.text(TEXT2["position"], text2, font=font2, fill=TEXT2["color"])

    return img


if __name__ == "__main__":
    app.run(debug=True)
