"""Uygulama ikonu oluşturur"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    sizes = [16, 32,48, 64, 128, 256]
    images = []

    for size in sizes:
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Arka plan - yuvarlak köşeli dikdörtgen
        margin = size // 10
        draw.rounded_rectangle(
            [margin, margin, size - margin, size - margin],
            radius=size // 5,
            fill='#89b4fa'
        )

        # Kamera / ekran ikonu — beyaz dikdörtgen (ekran sembolü)
        m = size // 4
        draw.rounded_rectangle(
            [m, m + size//12, size - m, size - m - size//8],
            radius=size // 12,
            fill='white'
        )

        # Alt stand
        cx = size // 2
        stand_w = size // 5
        stand_h = size // 10
        draw.rectangle(
            [cx - stand_w//2, size - m - size//8,
             cx + stand_w//2, size - m - size//8 + stand_h],
            fill='white'
        )
        draw.rectangle(
            [cx - stand_w, size - m - size//8 + stand_h - 2,
             cx + stand_w, size - m - size//8 + stand_h + 2],
            fill='white'
        )

        images.append(img)

    images[0].save(
        'icon.ico',
        format='ICO',
        sizes=[(s, s) for s in sizes],
        append_images=images[1:]
    )
    print("icon.ico olusturuldu.")

if __name__ == '__main__':
    create_icon()
