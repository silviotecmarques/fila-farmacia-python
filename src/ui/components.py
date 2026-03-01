# src/ui/components.py
import tkinter as tk
from .styles import COLORS, FONTS

class CardFrame(tk.Frame):
    def __init__(self, master, width=None, height=None, bg=COLORS["card_bg"], shadow=True, **kwargs):
        p_bg = master.cget("bg") if master.cget("bg") else COLORS["bg_end"]
        super().__init__(master, bg=p_bg, **kwargs)
        if shadow:
            self.shadow = tk.Frame(self, bg="#e0e0e0", width=width, height=height)
            self.shadow.place(x=4, y=4)
        self.card = tk.Frame(self, bg=bg, width=width, height=height)
        self.card.place(x=0, y=0)
        if width and height:
            self.card.pack_propagate(False); self.config(width=width+8, height=height+8)
    def body(self): return self.card

class RoundedButton(tk.Canvas):
    def __init__(self, master, text="", command=None, bg_color=COLORS["accent"], 
                 fg_color="white", width=160, height=45, radius=22, image=None, **kwargs):
        p_bg = master.cget("bg") if master.cget("bg") else COLORS["bg_end"]
        super().__init__(master, width=width, height=height, bg=p_bg, highlightthickness=0, **kwargs)
        
        self.command = command
        r = radius
        p = [r, 0, width-r, 0, width, 0, width, r, width, height-r, width, height, width-r, height, r, height, 0, height, 0, height-r, 0, r, 0, 0]
        self.create_polygon(p, fill=bg_color, smooth=True, tags="bg")
        
        # Proporção ajustada: ícone e texto mais próximos e centralizados
        if image:
            img_x = width * 0.22 if text else width // 2
            self.create_image(img_x, height // 2, image=image, tags="content")
            if text:
                self.create_text(width * 0.60, height // 2, text=text, fill=fg_color, font=FONTS["button"], tags="content")
        else:
            self.create_text(width // 2, height // 2, text=text, fill=fg_color, font=FONTS["button"], tags="content")
            
        self.bind("<Button-1>", lambda e: self.on_press())
        self.bind("<ButtonRelease-1>", lambda e: self.on_release())
        self.config(cursor="hand2")

    def on_press(self): self.move("all", 1, 1)
    def on_release(self):
        self.move("all", -1, -1)
        if self.command: self.command()