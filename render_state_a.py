from PIL import Image, ImageDraw, ImageFont

def render_state_a(width=640, height=480):
    text = "No\nUpcoming\nMeeting"
    background_color = (0, 0, 0)
    text_color = (255, 255, 255)
    line_spacing = 10  # pixels between lines

    # Create image
    img = Image.new("RGB", (width, height), color=background_color)
    draw = ImageDraw.Draw(img)

    # Load font
    try:
        font = ImageFont.truetype("arialbd.ttf", 120)
    except:
        font = ImageFont.load_default()

    # Split and measure text
    lines = text.split('\n')
    line_heights = []
    line_widths = []

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]
        line_widths.append(line_width)
        line_heights.append(line_height)

    total_text_height = sum(line_heights) + line_spacing * (len(lines) - 1)
    current_y = (height - total_text_height) // 2

    # Draw each line centered
    for i, line in enumerate(lines):
        x = (width - line_widths[i]) // 2
        draw.text((x, current_y), line, font=font, fill=text_color)
        current_y += line_heights[i] + line_spacing

    return img  # PIL.Image object
