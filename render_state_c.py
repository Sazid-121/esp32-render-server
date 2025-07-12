from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

def render_state_c(topic_text, speaker_name, image_url, abstract_text, width=640, height=480):
    # === Style ===
    background_color = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    margin = 30
    photo_size = (220, 220)
    max_font_size = 36
    min_font_size = 14

    canvas = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(canvas)

    # === Load speaker photo ===
    try:
        if "drive.google.com/open?id=" in image_url:
            image_url = image_url.replace("open?id=", "uc?id=")

        response = requests.get(image_url)
        response.raise_for_status()
        speaker_img = Image.open(BytesIO(response.content)).convert("RGB").resize(photo_size)
        canvas.paste(speaker_img, (width - photo_size[0] - margin, margin))
    except Exception as e:
        print(f"[Warning] Could not load speaker image: {e}")

    # === Font loader ===
    def get_font(name, size):
        try:
            return ImageFont.truetype(name, size)
        except:
            return ImageFont.load_default()

    # === Word wrapping ===
    def wrap_text(text, font, max_width):
        words = text.split()
        lines = []
        line = ""
        for word in words:
            test_line = f"{line} {word}".strip()
            if draw.textlength(test_line, font=font) <= max_width:
                line = test_line
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        return lines

    # === Topic title (top-left, centered before speaker photo) ===
    topic_area_width = width - photo_size[0] - 3 * margin
    topic_area_height = photo_size[1]

    for size in range(max_font_size, min_font_size - 1, -2):
        topic_font = get_font("arialbd.ttf", size)
        topic_lines = wrap_text(topic_text, topic_font, topic_area_width)
        topic_height = sum([draw.textbbox((0, 0), line, font=topic_font)[3] + 5 for line in topic_lines])
        if topic_height <= topic_area_height:
            break

    y = margin + 5
    for line in topic_lines:
        text_width = draw.textlength(line, font=topic_font)
        x = margin + (topic_area_width - text_width) // 2
        draw.text((x, y), line, font=topic_font, fill=red)
        y += draw.textbbox((0, 0), line, font=topic_font)[3] + 5

    topic_bottom_y = y

    # === Speaker Name (centered before speaker photo) ===
    speaker_text = f"Speaker: {speaker_name}"
    speaker_area_width = width - photo_size[0] - 2 * margin

    for size in range(24, 10, -1):
        speaker_font = get_font("arialbd.ttf", size)
        if draw.textlength(speaker_text, font=speaker_font) <= speaker_area_width:
            break

    speaker_x = margin + (speaker_area_width - draw.textlength(speaker_text, font=speaker_font)) // 2
    speaker_y = (topic_bottom_y + height // 2 - margin) // 2
    draw.text((speaker_x, speaker_y), speaker_text, font=speaker_font, fill=green)

    # === Abstract (bottom half) ===
    abstract_top = height // 2 + margin
    abstract_width = width - 2 * margin
    abstract_height = height // 2 - 2 * margin
    paragraphs = [p.strip() for p in abstract_text.strip().split("\n") if p.strip()]

    for size in range(22, min_font_size - 1, -2):
        abstract_font = get_font("arial.ttf", size)
        wrapped_paragraphs = [wrap_text(p, abstract_font, abstract_width) for p in paragraphs]
        total_height = sum([len(para) * (draw.textbbox((0, 0), line, font=abstract_font)[3] + 4)
                            for para in wrapped_paragraphs]) + 10 * len(paragraphs)
        if total_height <= abstract_height:
            break

    y = abstract_top + (abstract_height - total_height) // 2
    for para in wrapped_paragraphs:
        for line in para:
            draw.text((margin, y), line, font=abstract_font, fill=white)
            y += draw.textbbox((0, 0), line, font=abstract_font)[3] + 4
        y += 10

    return canvas
