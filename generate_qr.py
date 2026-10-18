import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
import socket

# Paths
ASSETS_DIR = "assets"
LOGO_PATH = os.path.join(ASSETS_DIR, "logo.jpg")
COVER_PATH = os.path.join(ASSETS_DIR, "cover.jpg")

# Official Links
FB_URL = "https://www.facebook.com/profile.php?id=61595401193073"
IG_URL = "https://www.instagram.com/maison.evora07"
YT_URL = "https://www.youtube.com/@maison.evora07"
TT_URL = "https://www.tiktok.com/@maison.evora6"

# Live GitHub Pages URL
LIVE_HUB_URL = "https://britsync07-prog.github.io/maison-evora/"

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

LOCAL_IP = get_local_ip()
LOCAL_TEST_URL = f"http://{LOCAL_IP}:8000"

def create_styled_qr(data_url, output_path, with_logo=True, fill_color=(3, 38, 18), back_color=(255, 255, 255)):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H, # 30% error correction allows center logo
        box_size=15,
        border=4,
    )
    qr.add_data(data_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGBA')

    if with_logo and os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH).convert('RGBA')
        
        qr_width, qr_height = img.size
        logo_size = int(qr_width * 0.23)
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        # Circular mask
        mask = Image.new('L', (logo_size, logo_size), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, logo_size, logo_size), fill=255)
        
        # Gold framed circular plate
        plate_size = logo_size + 16
        plate = Image.new('RGBA', (plate_size, plate_size), (255, 255, 255, 255))
        draw_plate = ImageDraw.Draw(plate)
        draw_plate.ellipse((2, 2, plate_size - 2, plate_size - 2), fill=(255, 255, 255, 255), outline=(212, 175, 55, 255), width=4)
        
        plate.paste(logo, (8, 8), mask)
        
        pos = ((qr_width - plate_size) // 2, (qr_height - plate_size) // 2)
        img.paste(plate, pos, plate)
        
    img.save(output_path, "PNG")
    print(f"Generated QR: {output_path} ({img.size[0]}x{img.size[1]}) -> {data_url}")
    return img

def create_luxury_flyer(qr_source_path="maison_evora_qr_with_logo.png", output_path="maison_evora_flyer.png"):
    width = 1200
    height = 1800
    canvas = Image.new('RGB', (width, height), (3, 26, 12))
    draw = ImageDraw.Draw(canvas)

    # 1. Cover Banner at top
    if os.path.exists(COVER_PATH):
        cover = Image.open(COVER_PATH).convert('RGB')
        cover = cover.resize((width, int(width * 540 / 960)), Image.Resampling.LANCZOS)
        canvas.paste(cover, (0, 0))
        
        # Smooth gradient overlay to dark green
        gradient_h = 240
        gradient_y = cover.height - gradient_h
        for y in range(gradient_h):
            ratio = y / gradient_h
            r = int(3 * ratio)
            g = int(26 * ratio)
            b = int(12 * ratio)
            draw.line([(0, gradient_y + y), (width, gradient_y + y)], fill=(3, 26, 12))

    # 2. Golden borders
    gold = (212, 175, 55)
    champagne = (255, 220, 140)
    draw.rectangle([(24, 24), (width - 24, height - 24)], outline=gold, width=3)
    draw.rectangle([(34, 34), (width - 34, height - 34)], outline=gold, width=1)

    # 3. Logo circle badge
    if os.path.exists(LOGO_PATH):
        logo_size = 200
        logo = Image.open(LOGO_PATH).convert('RGBA')
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        mask = Image.new('L', (logo_size, logo_size), 0)
        draw_m = ImageDraw.Draw(mask)
        draw_m.ellipse((0, 0, logo_size, logo_size), fill=255)
        
        logo_x = (width - logo_size) // 2
        logo_y = 510
        
        draw.ellipse((logo_x - 10, logo_y - 10, logo_x + logo_size + 10, logo_y + logo_size + 10), fill=(255, 255, 255), outline=gold, width=6)
        canvas.paste(logo, (logo_x, logo_y), mask)

    # 4. Typography
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 62)
        font_sub = ImageFont.truetype("arial.ttf", 30)
        font_scan = ImageFont.truetype("arialbd.ttf", 36)
        font_links = ImageFont.truetype("arial.ttf", 26)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_scan = ImageFont.load_default()
        font_links = ImageFont.load_default()

    draw.text((width // 2, 755), "MAISON EVORA", fill=champagne, font=font_title, anchor="mm")
    draw.text((width // 2, 805), "LUXURY &bull; ELEGANCE &bull; LIFESTYLE", fill=(210, 230, 220), font=font_sub, anchor="mm")

    # 5. Paste QR Code
    if os.path.exists(qr_source_path):
        qr_img = Image.open(qr_source_path).convert('RGBA')
    else:
        qr_img = create_styled_qr(LIVE_HUB_URL, qr_source_path, with_logo=True)

    qr_display_size = 480
    qr_resized = qr_img.resize((qr_display_size, qr_display_size), Image.Resampling.LANCZOS)
    
    card_pad = 32
    card_x = (width - qr_display_size) // 2
    card_y = 865
    draw.rounded_rectangle(
        [(card_x - card_pad, card_y - card_pad), 
         (card_x + qr_display_size + card_pad, card_y + qr_display_size + card_pad + 54)],
        radius=24,
        fill=(255, 255, 255),
        outline=gold,
        width=4
    )
    
    canvas.paste(qr_resized, (card_x, card_y), qr_resized)
    draw.text((width // 2, card_y + qr_display_size + 24), "SCAN TO CONNECT WITH US", fill=(3, 38, 18), font=font_scan, anchor="mm")

    # 6. Bottom Social Channels
    social_y = 1500
    draw.text((width // 2, social_y), "FOLLOW US ACROSS ALL CHANNELS", fill=gold, font=font_scan, anchor="mm")
    draw.text((width // 2, social_y + 55), "Facebook  |  Instagram  |  YouTube  |  TikTok", fill=(245, 245, 245), font=font_sub, anchor="mm")
    draw.text((width // 2, social_y + 105), "@maison.evora07  &bull;  @maison.evora6", fill=(180, 200, 190), font=font_links, anchor="mm")
    
    canvas.save(output_path, "PNG")
    print(f"Generated printable flyer: {output_path}")

if __name__ == "__main__":
    # 1. Main branded QR code with logo -> Live GitHub Pages Multi-Link Hub URL!
    create_styled_qr(LIVE_HUB_URL, "maison_evora_qr_with_logo.png", with_logo=True)
    
    # 2. Classic B&W QR code -> Live GitHub Pages Multi-Link Hub URL
    create_styled_qr(LIVE_HUB_URL, "maison_evora_qr_classic.png", with_logo=False, fill_color=(0, 0, 0))
    
    # 3. Direct QR for Facebook Page
    create_styled_qr(FB_URL, "maison_evora_facebook_qr.png", with_logo=True)
    
    # 4. Printable Luxury Flyer (with the Multi-Link Hub QR code)
    create_luxury_flyer("maison_evora_qr_with_logo.png", "maison_evora_flyer.png")
