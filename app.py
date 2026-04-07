import tkinter as tk
import threading
import queue
import pyperclip
import pytesseract
from PIL import ImageGrab, Image, ImageDraw
import pystray
import keyboard
import winreg
import sys
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

task_queue = queue.Queue()


def make_tray_image():
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([4, 4, 60, 60], radius=12, fill='#89b4fa')
    d.rounded_rectangle([12, 14, 52, 44], radius=4, fill='white')
    d.rectangle([28, 44, 36, 50], fill='white')
    d.rectangle([22, 50, 42, 53], fill='white')
    return img


class ScreenSelector(tk.Toplevel):
    def __init__(self, root, callback):
        super().__init__(root)
        self.callback = callback
        self.start_x = self.start_y = 0
        self.rect = None

        self.attributes('-fullscreen', True)
        self.attributes('-alpha', 0.25)
        self.attributes('-topmost', True)
        self.configure(bg='black', cursor='cross')

        self.canvas = tk.Canvas(self, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.canvas, text='Alan seçmek için sürükle  •  İptal: ESC',
                 bg='black', fg='white', font=('Segoe UI', 13)
                 ).place(relx=0.5, rely=0.05, anchor='center')

        self.canvas.bind('<ButtonPress-1>', self.on_press)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        self.bind('<Escape>', lambda e: self.destroy())

    def on_press(self, e):
        self.start_x, self.start_y = e.x, e.y
        if self.rect:
            self.canvas.delete(self.rect)

    def on_drag(self, e):
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, e.x, e.y,
            outline='#00ff88', width=2, fill='')

    def on_release(self, e):
        x1 = min(self.start_x, e.x)
        y1 = min(self.start_y, e.y)
        x2 = max(self.start_x, e.x)
        y2 = max(self.start_y, e.y)
        self.destroy()
        if abs(x2 - x1) > 5 and abs(y2 - y1) > 5:
            self.callback(x1, y1, x2, y2)


def show_toast(root, msg, color='#a6e3a1'):
    """Sağ alt köşede 2 saniyelik bildirim"""
    toast = tk.Toplevel(root)
    toast.overrideredirect(True)
    toast.attributes('-topmost', True)
    toast.attributes('-alpha', 0.92)
    toast.configure(bg='#1e1e2e')

    tk.Label(toast, text=msg, font=('Segoe UI', 10),
             bg='#1e1e2e', fg=color, padx=16, pady=10).pack()

    toast.update_idletasks()
    w = toast.winfo_width()
    h = toast.winfo_height()
    sw = toast.winfo_screenwidth()
    sh = toast.winfo_screenheight()
    toast.geometry(f'+{sw - w - 24}+{sh - h - 60}')

    toast.after(2200, toast.destroy)


def process_area(root, x1, y1, x2, y2):
    def run():
        try:
            img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
            img = img.convert('L')
            text = pytesseract.image_to_string(img, lang='tur+eng', config='--psm 3').strip()

            if text:
                pyperclip.copy(text)
                preview = text[:50] + ('...' if len(text) > 50 else '')
                root.after(0, lambda: show_toast(root, f'Kopyalandı: {preview}'))
            else:
                root.after(0, lambda: show_toast(root, 'Metin bulunamadı', '#f38ba8'))
        except Exception as ex:
            root.after(0, lambda: show_toast(root, f'Hata: {ex}', '#f38ba8'))

    threading.Thread(target=run, daemon=True).start()


def poll(root, icon_ref):
    try:
        task = task_queue.get_nowait()
        if task == 'capture':
            sel = ScreenSelector(root, lambda x1, y1, x2, y2: process_area(root, x1, y1, x2, y2))
            sel.focus_force()
        elif task == 'quit':
            icon_ref[0].stop()
            root.quit()
    except Exception:
        pass
    root.after(100, lambda: poll(root, icon_ref))


REG_PATH = r'Software\Microsoft\Windows\CurrentVersion\Run'
APP_NAME = 'SS Kopyala'


def get_exe_path():
    return sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)


def is_startup_enabled():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
        winreg.QueryValueEx(key, APP_NAME)
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False


def toggle_startup(icon_ref, root):
    if is_startup_enabled():
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, APP_NAME)
        winreg.CloseKey(key)
        root.after(0, lambda: show_toast(root, 'Başlangıçtan kaldırıldı', '#f9e2af'))
    else:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{get_exe_path()}"')
        winreg.CloseKey(key)
        root.after(0, lambda: show_toast(root, 'Başlangıca eklendi!'))
    # Menüyü güncelle
    icon_ref[0].menu = build_menu(icon_ref, root)
    icon_ref[0].update_menu()


def build_menu(icon_ref, root):
    startup_label = 'Başlangıçtan Kaldır' if is_startup_enabled() else 'Başlangıca Ekle'
    return pystray.Menu(
        pystray.MenuItem('Alan Seç  (Ctrl+Y)', lambda: task_queue.put('capture')),
        pystray.MenuItem(startup_label, lambda: toggle_startup(icon_ref, root)),
        pystray.MenuItem('Çıkış', lambda: task_queue.put('quit')),
    )


def main():
    root = tk.Tk()
    root.withdraw()

    icon_ref = [None]

    icon = pystray.Icon('SS Kopyala', make_tray_image(), 'SS Kopyala  |  Ctrl+Y')
    icon.menu = build_menu(icon_ref, root)
    icon_ref[0] = icon

    threading.Thread(target=icon.run, daemon=True).start()
    keyboard.add_hotkey('ctrl+y', lambda: task_queue.put('capture'))

    poll(root, icon_ref)
    root.mainloop()


if __name__ == '__main__':
    main()
