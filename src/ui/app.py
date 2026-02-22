import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageEnhance, ImageDraw
import os
from .styles import COLORS, FONTS

# --- CLASSE PARA BOTÕES ARREDONDADOS CUSTOMIZADOS ---
class RoundedButton(tk.Canvas):
    def __init__(self, master, text="", command=None, bg_color="#2980b9", fg_color="white", 
                 image=None, width=180, height=50, radius=25, **kwargs):
        super().__init__(master, width=width, height=height, bg=master["bg"], highlightthickness=0, **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.radius = radius
        
        # Desenho do botão
        self.rect = self.create_round_rect(0, 0, width, height, radius, fill=bg_color, tags="button_bg")
        
        # Texto e Ícone
        if image:
            self.create_image(width//2 - 40 if text else width//2, height//2, image=image, tags="button_content")
        if text:
            self.create_text(width//2 + 20 if image else width//2, height//2, text=text, 
                             fill=fg_color, font=FONTS["button"], tags="button_content")

        self.bind("<Button-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)

    def create_round_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)

    def on_press(self, event):
        self.move("button_bg", 2, 2)
        self.move("button_content", 2, 2)

    def on_release(self, event):
        self.move("button_bg", -2, -2)
        self.move("button_content", -2, -2)
        if self.command: self.command()

# --- CLASSE PRINCIPAL ---
class FarmaciaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PHARMA FLOW - PRO")
        self.root.state('zoomed')
        self.root.configure(bg=COLORS["bg"])
        
        from src.database import Database
        from src.engine import FilaEngine
        self.db = Database()
        self.engine = FilaEngine(self.db)
        
        self.icons = {}
        self.main_cache = []; self.select_cache = []; self.add_cache = []
        self.foto_escolhida = ""

        self.screen_main = tk.Frame(self.root, bg=COLORS["bg"])
        self.screen_select = tk.Frame(self.root, bg=COLORS["bg"])
        self.screen_add = tk.Frame(self.root, bg=COLORS["bg"])
        
        self.setup_main_ui()
        self.setup_select_ui()
        self.setup_add_ui()
        
        self.root.bind("<Configure>", self.on_resize)
        self.show_screen(self.screen_main)
        self.update_loop()

    def load_img(self, rel_path, size, subtle_gray=False, circular=True):
        full_path = os.path.join("assets", rel_path)
        if not os.path.exists(full_path): return None
        img = Image.open(full_path).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
        if subtle_gray:
            img = ImageEnhance.Color(img).enhance(0.15)
            img = ImageEnhance.Brightness(img).enhance(1.1)
        if circular:
            mask = Image.new('L', size, 0); draw = ImageDraw.Draw(mask); draw.ellipse((0, 0) + size, fill=255)
            output = Image.new('RGBA', size, (0, 0, 0, 0)); output.paste(img, (0, 0), mask=mask); img = output
        return ImageTk.PhotoImage(img)

    def on_resize(self, event):
        if event.widget == self.root: self.refresh_ui()

    def show_screen(self, screen):
        for s in [self.screen_main, self.screen_select, self.screen_add]: s.pack_forget()
        if screen == self.screen_select: self.refresh_select_ui()
        if screen == self.screen_add: self.refresh_avatar_gallery()
        screen.pack(expand=True, fill="both")

    def setup_main_ui(self):
        tk.Label(self.screen_main, text="ATENDIMENTO ATUAL", font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["accent"]).pack(pady=(40, 5))
        self.content_container = tk.Frame(self.screen_main, bg=COLORS["bg"])
        self.content_container.pack(expand=True, fill="both", pady=(60, 0))
        self.main_img_lbl = tk.Label(self.content_container, bg=COLORS["bg"]); self.main_img_lbl.pack()
        self.main_name_lbl = tk.Label(self.content_container, text="", font=FONTS["name"], bg=COLORS["bg"], fg=COLORS["text"]); self.main_name_lbl.pack()
        self.lbl_timer = tk.Label(self.content_container, text="00:00", font=FONTS["timer"], bg=COLORS["bg"], fg=COLORS["timer"]); self.lbl_timer.pack()
        self.next_slots_frame = tk.Frame(self.content_container, bg=COLORS["bg"]); self.next_slots_frame.pack(pady=10)
        self.next_slots = []
        for i in range(3):
            f = tk.Frame(self.next_slots_frame, bg=COLORS["bg"]); f.pack(side="left", padx=25)
            img_lbl = tk.Label(f, bg=COLORS["bg"]); img_lbl.pack()
            name_lbl = tk.Label(f, text="", font=FONTS["info"], bg=COLORS["bg"]); name_lbl.pack()
            self.next_slots.append({"img": img_lbl, "name": name_lbl})
        
        self.footer = tk.Frame(self.screen_main, bg=COLORS["bg"], pady=40); self.footer.pack(side="bottom", fill="x")
        self.btn_ctx = tk.Frame(self.footer, bg=COLORS["bg"]); self.btn_ctx.pack(expand=True)
        self.icons['atendi'] = self.load_img("icons/atendi.png", (24, 24), circular=False)
        self.icons['pular'] = self.load_img("icons/pular.png", (24, 24), circular=False)
        self.icons['fila'] = self.load_img("icons/fila.png", (24, 24), circular=False)
        
        RoundedButton(self.btn_ctx, text="ATENDI", image=self.icons['atendi'], bg_color=COLORS["success"], command=self.engine.atender).pack(side="left", padx=10)
        RoundedButton(self.btn_ctx, text="PULAR", image=self.icons['pular'], bg_color=COLORS["warning"], command=self.engine.pular).pack(side="left", padx=10)
        RoundedButton(self.btn_ctx, text="FILA", image=self.icons['fila'], bg_color=COLORS["accent"], command=lambda: self.show_screen(self.screen_select)).pack(side="left", padx=10)

    def setup_select_ui(self):
        tk.Label(self.screen_select, text="GERENCIAR FILA", font=FONTS["title"], bg=COLORS["bg"], fg=COLORS["accent"]).pack(pady=20)
        self.grid_frame = tk.Frame(self.screen_select, bg=COLORS["bg"]); self.grid_frame.pack(expand=True, fill="both")
        self.sel_footer = tk.Frame(self.screen_select, bg=COLORS["bg"], pady=30); self.sel_footer.pack(side="bottom", fill="x")
        self.sel_ctx = tk.Frame(self.sel_footer, bg=COLORS["bg"]); self.sel_ctx.pack(expand=True)
        self.icons['voltar'] = self.load_img("icons/voltar.png", (24, 24), circular=False)
        RoundedButton(self.sel_ctx, text="VOLTAR", image=self.icons['voltar'], bg_color="#7f8c8d", command=lambda: self.show_screen(self.screen_main)).pack(side="left", padx=10)
        RoundedButton(self.sel_ctx, text="NOVO CADASTRO", bg_color=COLORS["accent"], command=lambda: self.show_screen(self.screen_add), width=220).pack(side="left", padx=10)

    def refresh_select_ui(self):
        for w in self.grid_frame.winfo_children(): w.destroy()
        self.select_cache = []
        if self.engine.cadastro:
            inner = tk.Frame(self.grid_frame, bg=COLORS["bg"]); inner.place(relx=0.5, rely=0.5, anchor="center")
            r, c = 0, 0
            for b in self.engine.cadastro:
                pos = next((i + 1 for i, item in enumerate(self.engine.fila) if item['id'] == b['id']), None)
                p = self.load_img(f"avatares/{b['foto']}", (120, 120), subtle_gray=(not pos))
                if p:
                    self.select_cache.append(p)
                    card = tk.Frame(inner, bg="#ffc973" if pos else "white", padx=10, pady=10, highlightthickness=1, highlightbackground="#ccc")
                    card.grid(row=r, column=c, padx=15, pady=15)
                    tk.Button(card, image=p, relief="flat", bg="#ffc973" if pos else "white", command=lambda id=b['id']: self.toggle_user(id)).pack()
                    tk.Label(card, text=b['nome'], font=FONTS["info"], bg="#ffc973" if pos else "white").pack()
                    c += 1
                    if c > 2: # FIX: SyntaxError resolvido aqui
                        c = 0
                        r += 1

    def toggle_user(self, b_id): self.engine.alternar_na_fila(b_id); self.refresh_select_ui()

    def setup_add_ui(self):
        # AQUI FOI APLICADA A COR LARANJA (#ffc973) NO FUNDO
        self.screen_add.configure(bg="#ffc973")
        tk.Label(self.screen_add, text="NOVO CADASTRO", font=FONTS["title"], bg="#ffc973", fg="black").pack(pady=20)
        content = tk.Frame(self.screen_add, bg="#ffc973"); content.pack(expand=True, fill="both", padx=50)
        form = tk.Frame(content, bg="#ffc973", padx=20, pady=20); form.pack(side="left", fill="y")
        tk.Label(form, text="NOME:", font=FONTS["button"], bg="#ffc973").pack(anchor="w")
        self.ent_nome = tk.Entry(form, font=("Arial", 14), width=20); self.ent_nome.pack(pady=10)
        self.cb_sexo = ttk.Combobox(form, values=["Masculino", "Feminino"], state="readonly"); self.cb_sexo.pack(fill="x", pady=5); self.cb_sexo.current(0)
        self.cb_funcao = ttk.Combobox(form, values=["Balconista", "Farmacêutico(a)"], state="readonly"); self.cb_funcao.pack(fill="x", pady=5); self.cb_funcao.current(0)
        self.lbl_foto = tk.Label(form, text="FOTO: Nenhuma", font=("Arial", 9), bg="#ffc973"); self.lbl_foto.pack(pady=5)
        gallery = tk.Frame(content, bg="white", relief="solid", bd=1); gallery.pack(side="right", fill="both", expand=True)
        self.canvas = tk.Canvas(gallery, bg="white", highlightthickness=0); self.scrollbar = ttk.Scrollbar(gallery, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg="white"); self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set); self.canvas.pack(side="left", fill="both", expand=True); self.scrollbar.pack(side="right", fill="y")
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.add_footer = tk.Frame(self.screen_add, bg="#ffc973", pady=20); self.add_footer.pack(side="bottom")
        RoundedButton(self.add_footer, text="SALVAR", bg_color=COLORS["success"], command=self.save_new).pack(side="left", padx=10)
        RoundedButton(self.add_footer, text="CANCELAR", bg_color="#e74c3c", command=lambda: self.show_screen(self.screen_select)).pack(side="left", padx=10)

    def refresh_avatar_gallery(self):
        for w in self.scroll_frame.winfo_children(): w.destroy()
        self.add_cache = []
        r, c = 0, 0
        for i in range(1, 41):
            f = f"{i}.png"; p = self.load_img(f"avatares/{f}", (70, 70), circular=True)
            if p:
                self.add_cache.append(p)
                tk.Button(self.scroll_frame, image=p, relief="flat", bg="white", command=lambda f=f: self.select_avatar(f)).grid(row=r, column=c, padx=5, pady=5)
                c += 1
                if c > 4: # FIX: SyntaxError resolvido aqui
                    c = 0
                    r += 1

    def select_avatar(self, f): self.foto_escolhida = f; self.lbl_foto.config(text=f"FOTO: {f}")

    def save_new(self):
        n_raw = self.ent_nome.get().strip()
        if n_raw and self.foto_escolhida:
            n_final = (("Dr. " if self.cb_sexo.get() == "Masculino" else "Dra. ") + n_raw.title()) if "Farmacêutico" in self.cb_funcao.get() else n_raw.title()
            self.engine.cadastrar_novo(n_final, self.cb_funcao.get(), self.foto_escolhida)
            self.ent_nome.delete(0, tk.END); self.show_screen(self.screen_select)
        else: messagebox.showwarning("Aviso", "Nome e foto obrigatórios!")

    def refresh_ui(self):
        win_w, win_h = self.root.winfo_width(), self.root.winfo_height()
        if win_w < 100 or win_h < 100: return
        hero_size = int(win_h * 0.35) if win_w > win_h else int(win_h * 0.25)
        next_size = int(win_h * 0.15)
        self.main_cache = []
        if self.engine.fila:
            foto_path = f"avatares/{self.engine.fila[0]['foto']}"; is_circ = True; nome_txt = self.engine.fila[0]['nome'].upper()
        else:
            foto_path = "icons/sem-atendimento.png"; is_circ = False; nome_txt = "AGUARDANDO..."
        p = self.load_img(foto_path, (hero_size, hero_size), circular=is_circ)
        if p: self.main_img_lbl.config(image=p); self.main_cache.append(p)
        self.main_name_lbl.config(text=nome_txt)
        for i in range(3):
            idx, slot = i + 1, self.next_slots[i]
            if idx < len(self.engine.fila):
                b = self.engine.fila[idx]
                p_next = self.load_img(f"avatares/{b['foto']}", (next_size, next_size), circular=True)
                if p_next: slot["img"].config(image=p_next); self.main_cache.append(p_next)
                pts = b["nome"].split(); slot["name"].config(text=" ".join(pts[:2]) if pts[0] in ["Dr.", "Dra."] else pts[0])
            else: slot["img"].config(image=""); slot["name"].config(text="")
        if self.engine.fila:
            m, s = divmod(self.engine.fila[0]["tempo_atual"], 60); self.lbl_timer.config(text=f"{m:02d}:{s:02d}")
        else: self.lbl_timer.config(text="00:00")

    def update_loop(self):
        self.engine.tick(); self.refresh_ui(); self.root.after(1000, self.update_loop)