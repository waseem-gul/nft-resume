from PIL import Image, ImageDraw, ImageFont
import streamlit as st

def create_card(name, wallet, image_path, traits):
    width, height = 600, 400
    card = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(card)
    
    title_font = ImageFont.truetype("assets/fonts/arial.ttf", 20)
    body_font = ImageFont.truetype("assets/fonts/arial.ttf", 15)
    
    draw.text((10, 10), name, font=title_font, fill="black")
    draw.text((10, 40), wallet, font=body_font, fill="gray")

    user_image = Image.open(image_path).resize((50, 50))
    card.paste(user_image, (width-60, 10))

    y_offset = 90
    for trait, value in traits.items():
        draw.text((10, y_offset), f"{trait}: {value}%", font=body_font, fill="black")
        bar_width = width - 80
        progress_width = int(bar_width * (value / 100))
        color = (255 * (1 - (value / 100)), 255 * (value / 100), 0)
        if value > 75:
            color = (int(255 - 2 * value), int(2 * value), 0)
        elif value > 50:
            color = (255, int(2 * value), 0)
        else:
            color = (255, int(5.1 * value), 0)
        draw.rectangle([10, y_offset + 20, 10 + int(progress_width), y_offset + 30], fill=color)
        y_offset += 50

    st.image(card)

def create_card_v1(name, wallet, image_path, traits):
    width, height = 600, 400
    card = Image.new("RGB", (width, height), "#F5F5F5")  # Changed to a light gray for a subtle background
    draw = ImageDraw.Draw(card)
    
    title_font = ImageFont.truetype("assets/fonts/arial.ttf", 25)
    body_font = ImageFont.truetype("assets/fonts/arial.ttf", 18)
    
    draw.text((20, 20), name, font=title_font, fill="#333333")
    draw.text((20, 60), wallet, font=body_font, fill="#777777")  # Slightly darker gray for better contrast

    user_image = Image.open(image_path).resize((70, 70))  # Increased size for better visibility
    card.paste(user_image, (width-90, 15))

    y_offset = 130  # Increase initial offset for a more spaced layout
    for trait, value in traits.items():
        draw.text((20, y_offset), f"{trait}:", font=body_font, fill="#333333")
        bar_width = width - 140  # Reduced bar width for better padding
        progress_width = int(bar_width * (value / 100))
        color = (255 * (1 - (value / 100)), 255 * (value / 100), 0)
        # Color gradient adjustments as per the original code
        if value > 75:
            color = (int(255 - 2 * value), int(2 * value), 0)
        elif value > 50:
            color = (255, int(2 * value), 0)
        else:
            color = (255, int(5.1 * value), 0)
        draw.rectangle([20, y_offset + 25, 20 + int(progress_width), y_offset + 35], fill=color)
        y_offset += 60  # Increased spacing for traits

    st.image(card)

def create_rounded_rectangle(width, height, corner_radius):
    """Helper function to create a mask for rounded rectangles"""
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle([corner_radius, 0, width - corner_radius, height], fill=255)
    draw.rectangle([0, corner_radius, width, height - corner_radius], fill=255)
    draw.pieslice([0, 0, 2*corner_radius, 2*corner_radius], 180, 270, fill=255)
    draw.pieslice([width - 2*corner_radius, 0, width, 2*corner_radius], 270, 360, fill=255)
    draw.pieslice([0, height - 2*corner_radius, 2*corner_radius, height], 90, 180, fill=255)
    draw.pieslice([width - 2*corner_radius, height - 2*corner_radius, width, height], 0, 90, fill=255)
    return mask

def create_card_v2(name, wallet, image_path, traits):
    width, height = 600, 440
    card = Image.new("RGB", (width, height), "#EAEAEA")  # Light gray background
    draw = ImageDraw.Draw(card)
    
    title_font = ImageFont.truetype("assets/fonts/arial.ttf", 25)
    body_font = ImageFont.truetype("assets/fonts/arial.ttf", 18)
    
    draw.text((20, 20), name, font=title_font, fill="#333333")
    draw.text((20, 60), wallet, font=body_font, fill="#777777")

    # Rounded image
    user_image = Image.open(image_path).resize((80, 80))
    mask = Image.new("L", user_image.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0) + user_image.size, fill=255)
    card.paste(user_image, (width-90, 15), mask)

    y_offset = 130
    for trait, value in traits.items():
        draw.text((20, y_offset), f"{trait}: {value}%", font=body_font, fill="#333333")
        bar_width = width - 140
        progress_width = int(bar_width * (value / 100))
        color = (255 * (1 - (value / 100)), 255 * (value / 100), 0)
        if value > 75:
            color = (int(255 - 2 * value), int(2 * value), 0)
        elif value > 50:
            color = (255, int(2 * value), 0)
        else:
            color = (255, int(5.1 * value), 0)
        draw.rectangle([20, y_offset + 25, 20 + int(progress_width), y_offset + 35], fill=color)
        y_offset += 60

    # Apply rounded rectangle for card itself
    rounded_card = Image.new("RGB", (width, height), "black")
    rounded_card.paste(card, (0, 0), create_rounded_rectangle(width, height, 20))
    st.image(rounded_card)
    return rounded_card


