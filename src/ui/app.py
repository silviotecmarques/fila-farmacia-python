# src/ui/app.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw
import os
import math
import winsound 
from .styles import COLORS, FONTS
from .components import CardFrame, RoundedButton

class FarmaciaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PHARMA FLOW PRO 2026")
        self.root.state('zoomed')
        
        self.bg_canvas = tk.Canvas(self.root, highlightthickness=0)
        self.bg_canvas.place(relwidth=1, relheight=1)
        
        from src.database import Database
        from src.engine import FilaEngine
        self.db = Database(); self.engine = FilaEngine(self.db)
        
        self.icons = {}; self.main_cache = []; self.select_cache = []
        self.foto_escolhida = ""

        self.carregar_icones()
        self.main_container = tk.Frame(self.root, bg=COLORS["bg_end"])
        self.main_container.pack(expand=True, fill="both")

        self.screen_main = tk.Frame(self.main_container, bg=COLORS["bg_end"])
        self.screen_select = tk.Frame(self.main_container, bg=COLORS["bg_end"])
        
        # Escudo Opaco para o Modal
        self.overlay = tk.Frame(self.root, bg="#dcdde1") 
        
        self.setup_main_ui()
        self.setup_select_ui()
        
        self.root.bind("<Configure>", self.on_resize)
        self.show_screen(self.screen_main)
        self.root.after(100, self.refresh_ui)

    def carregar_icones(self):
        self.icons['atendir'] = self.load_img("icons/check.png", (24, 24), circular=False)
        self.icons['central'] = self.load_img("icons/group_add.png", (24, 24), circular=False)
        self.icons['adicionar'] = self.load_img("icons/person_add.png", (24, 24), circular=False)
        self.icons['back'] = self.load_img("icons/back.png", (24, 24), circular=False)
        self.icons['delete'] = self.load_img("icons/delete.png", (14, 14), circular=False)
        self.icons['salvar'] = self.load_img("icons/salve.png", (24, 24), circular=False)
        self.icons['cancelar'] = self.load_img("icons/close.png", (24, 24), circular=False)

    def tocar_ding(self):
        winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS | winsound.SND_ASYNC)

    def load_img(self, rel_path, size, circular=True, grayscale=False):
        full_path = os.path.join("assets", rel_path)
        if not os.path.exists(full_path): return None
        try:
            img = Image.open(full_path).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
            if grayscale:
                alpha = img.getchannel('A')
                img = img.convert('L').convert('RGBA')
                img.putalpha(alpha)
            if circular:
                mask = Image.new('L', size, 0); draw = ImageDraw.Draw(mask)
                draw.ellipse((2, 2, size[0]-3, size[1]-3), fill=255)
                output = Image.new('RGBA', size, (0, 0, 0, 0)); output.paste(img, (0, 0), mask=mask)
                img = output
            return ImageTk.PhotoImage(img)
        except: return None

    def show_screen(self, screen):
        for s in [self.screen_main, self.screen_select]: s.pack_forget()
        screen.pack(expand=True, fill="both")
        if screen == self.screen_select: self.refresh_select_ui()
        self.refresh_ui()

    def setup_main_ui(self):
        tk.Frame(self.screen_main, bg=COLORS["accent_dark"], height=5).pack(fill="x")
        tk.Label(self.screen_main, text="VEZ DE ATENDIMENTO", font=FONTS["title"], bg=COLORS["accent"], fg="white").pack(pady=(15, 0), fill="x")
        footer = tk.Frame(self.screen_main, bg=COLORS["bg_end"])
        footer.pack(side="bottom", fill="x", pady=25)
        btn_ctx = tk.Frame(footer, bg=COLORS["bg_end"]); btn_ctx.pack(expand=True)
        RoundedButton(btn_ctx, image=self.icons.get('atendir'), bg_color=COLORS["success"], command=lambda: [self.engine.proximo(), self.refresh_ui(), self.tocar_ding()], width=80, height=55).pack(side="left", padx=15)
        RoundedButton(btn_ctx, image=self.icons.get('central'), bg_color=COLORS["accent"], command=lambda: self.show_screen(self.screen_select), width=80, height=55).pack(side="left", padx=15)
        self.hero_card = CardFrame(self.screen_main, width=580, height=680)
        self.hero_card.pack(pady=10, expand=True)
        c = self.hero_card.body()
        self.halo = tk.Frame(c, bg="white"); self.halo.pack(pady=15); self.halo.pack_propagate(False)
        self.main_img_lbl = tk.Label(self.halo, bg="white", bd=0); self.main_img_lbl.place(relx=0.5, rely=0.5, anchor="center")
        self.main_name_lbl = tk.Label(c, text="", font=FONTS["name"], bg="white", fg=COLORS["text"]); self.main_name_lbl.pack()
        tk.Frame(c, bg="#f1f2f6", height=2).pack(fill="x", padx=60, pady=30)
        tk.Label(c, text="PRÓXIMOS DA FILA", font=("Segoe UI", 9, "bold"), bg="white", fg="#95a5a6").pack()
        self.next_slots_frame = tk.Frame(c, bg="white"); self.next_slots_frame.pack(pady=15); self.next_slots = []
        for i in range(3):
            f = tk.Frame(self.next_slots_frame, bg="white"); f.pack(side="left", padx=20)
            img = tk.Label(f, bg="white", bd=0); img.pack(pady=5)
            nm = tk.Label(f, text="", font=FONTS["info_small"], bg="white"); nm.pack(); self.next_slots.append({"img": img, "name": nm})

    def setup_select_ui(self):
        tk.Label(self.screen_select, text="CENTRAL EQUIPE", font=FONTS["title"], bg=COLORS["accent"], fg="white").pack(pady=15, fill="x")
        self.scroll_canvas = tk.Canvas(self.screen_select, bg=COLORS["bg_end"], highlightthickness=0)
        self.scroll_bar = ttk.Scrollbar(self.screen_select, orient="vertical", command=self.scroll_canvas.yview)
        self.grid_container = tk.Frame(self.scroll_canvas, bg=COLORS["bg_end"])
        screen_w = self.root.winfo_screenwidth()
        self.scroll_canvas.create_window((screen_w//2, 20), window=self.grid_container, anchor="n")
        self.scroll_canvas.configure(yscrollcommand=self.scroll_bar.set)
        self.scroll_canvas.pack(side="left", fill="both", expand=True); self.scroll_bar.pack(side="right", fill="y")
        self.grid_container.bind("<Configure>", lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")))
        f_bot = tk.Frame(self.screen_select, bg=COLORS["bg_end"], pady=20); f_bot.pack(side="bottom", fill="x")
        ctx = tk.Frame(f_bot, bg=COLORS["bg_end"]); ctx.pack(expand=True)
        RoundedButton(ctx, image=self.icons.get('adicionar'), bg_color=COLORS["success"], command=self.open_modal, width=70, height=50).pack(side="left", padx=10)
        RoundedButton(ctx, image=self.icons.get('back'), bg_color=COLORS["neutral"], command=lambda: self.show_screen(self.screen_main), width=70, height=50).pack(side="left", padx=10)
        self.modal_card = None

    def refresh_select_ui(self):
        for w in self.grid_container.winfo_children(): w.destroy()
        self.select_cache = []
        if not self.engine.cadastro: return
        num_cols = 4 
        for i, b in enumerate(self.engine.cadastro):
            pos_na_fila = next((idx + 1 for idx, f in enumerate(self.engine.fila) if f['id'] == b['id']), None)
            is_active = pos_na_fila is not None
            bg_color = COLORS["bg_form"] if is_active else "#e1e4e8" 
            row, col = i // num_cols, i % num_cols
            card = CardFrame(self.grid_container, width=190, height=220, bg=bg_color)
            card.grid(row=row, column=col, padx=12, pady=12)
            body = card.body()
            def handle_click(event, c_id=b['id']): self.toggle_user(c_id)
            body.bind("<Button-1>", handle_click)
            btn_del = tk.Button(body, image=self.icons.get('delete'), bg=COLORS["danger"], relief="flat", bd=0, command=lambda id=b['id']: self.confirmar_delecao(id), cursor="hand2")
            btn_del.place(x=165, y=5, width=20, height=20)
            p = self.load_img(f"avatares/{b['foto']}", (90, 90), circular=True, grayscale=not is_active)
            if p:
                self.select_cache.append(p)
                img_lbl = tk.Label(body, image=p, bg=bg_color); img_lbl.pack(pady=(15, 5)); img_lbl.bind("<Button-1>", handle_click)
            name_lbl = tk.Label(body, text=b['nome'], font=("Segoe UI", 10, "bold"), bg=bg_color, fg=COLORS["text"]); name_lbl.pack(); name_lbl.bind("<Button-1>", handle_click)
            pos_text = f"{pos_na_fila}° NA FILA" if is_active else "FORA DA FILA"
            pos_lbl = tk.Label(body, text=pos_text, font=("Segoe UI", 10, "bold"), bg=bg_color, fg=COLORS["accent_dark"] if is_active else "#7f8c8d")
            pos_lbl.pack(pady=(2, 0)); pos_lbl.bind("<Button-1>", handle_click)

    # --- TELA 3: MODAL DESIGN REFORMULADO ---
    def open_modal(self):
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1); self.overlay.lift()
        w, h = int(self.root.winfo_width() * 0.65), int(self.root.winfo_height() * 0.70)
        self.modal_card = CardFrame(self.root, width=w, height=h, bg="white", shadow=True)
        self.modal_card.place(relx=0.5, rely=0.5, anchor="center"); self.modal_card.lift()
        self.setup_modal_content(w, h)
        self.refresh_avatar_gallery()

    def close_modal(self):
        if self.modal_card: self.modal_card.destroy(); self.modal_card = None
        self.overlay.place_forget(); self.foto_escolhida = ""

    def setup_modal_content(self, w, h):
        m = self.modal_card.body(); m.config(bg="white")
        # Header Minimalista
        header = tk.Frame(m, bg="#f8f9fa", height=50); header.pack(fill="x")
        tk.Label(header, text="NOVA IDENTIDADE TÁTICA", font=("Segoe UI", 10, "bold"), bg="#f8f9fa", fg="#7f8c8d").pack(pady=15)
        
        content = tk.Frame(m, bg="white"); content.pack(expand=True, fill="both", padx=40, pady=20)
        
        # Coluna ESQUERDA: O "Crachá" (Profile ID)
        profile_col = tk.Frame(content, bg="white", width=int(w*0.35))
        profile_col.pack(side="left", fill="both"); profile_col.pack_propagate(False)
        
        # Container do Avatar Preview
        self.p_card = tk.Frame(profile_col, bg="white", highlightbackground="#f1f2f6", highlightthickness=2)
        self.p_card.pack(pady=(0, 20), fill="x", ipady=20)
        
        self.preview_img_lbl = tk.Label(self.p_card, bg="white", text="AGUARDANDO\nAVATAR", font=("Segoe UI", 8), fg="#bdc3c7")
        self.preview_img_lbl.pack(pady=20)
        
        # Input Estilizado
        tk.Label(profile_col, text="NOME DO COLABORADOR", font=("Segoe UI", 8, "bold"), bg="white", fg="#95a5a6").pack(anchor="w")
        input_bg = tk.Frame(profile_col, bg="#f1f2f6", padx=15, pady=10)
        input_bg.pack(fill="x", pady=5)
        self.ent_nome = tk.Entry(input_bg, font=("Segoe UI", 12), bg="#f1f2f6", relief="flat", justify="center")
        self.ent_nome.pack(fill="x"); self.ent_nome.focus_set()

        # Coluna DIREITA: Galeria de Seleção
        gallery_col = tk.Frame(content, bg="white")
        gallery_col.pack(side="right", expand=True, fill="both", padx=(40, 0))
        
        tk.Label(gallery_col, text="BIBLIOTECA DE AVATARES", font=("Segoe UI", 8, "bold"), bg="white", fg="#95a5a6").pack(anchor="w")
        
        gal_container = tk.Frame(gallery_col, bg="#f8f9fa", padx=5, pady=5)
        gal_container.pack(expand=True, fill="both", pady=10)
        
        self.canvas_gal = tk.Canvas(gal_container, bg="#f8f9fa", highlightthickness=0)
        sc = ttk.Scrollbar(gal_container, orient="vertical", command=self.canvas_gal.yview)
        self.scroll_frame_gal = tk.Frame(self.canvas_gal, bg="#f8f9fa")
        
        self.canvas_gal.create_window((0, 0), window=self.scroll_frame_gal, anchor="nw")
        self.canvas_gal.configure(yscrollcommand=sc.set); self.canvas_gal.pack(side="left", fill="both", expand=True); sc.pack(side="right", fill="y")
        self.scroll_frame_gal.bind("<Configure>", lambda e: self.canvas_gal.configure(scrollregion=self.canvas_gal.bbox("all")))
        
        # Footer de Ações
        footer = tk.Frame(m, bg="white", height=80); footer.pack(side="bottom", fill="x")
        f_ctx = tk.Frame(footer, bg="white"); f_ctx.pack(expand=True)
        
        RoundedButton(f_ctx, image=self.icons.get('salvar'), bg_color=COLORS["success"], command=self.save_new, width=65, height=50).pack(side="left", padx=15)
        RoundedButton(f_ctx, image=self.icons.get('cancelar'), bg_color=COLORS["danger"], command=self.close_modal, width=65, height=50).pack(side="left", padx=15)

    def refresh_avatar_gallery(self):
        for w in self.scroll_frame_gal.winfo_children(): w.destroy()
        r, c = 0, 0
        for i in range(1, 41):
            fn = f"{i}.png"; im = self.load_img(f"avatares/{fn}", (70, 70), circular=True)
            if im:
                # Botão de avatar como um "tile" limpo
                btn = tk.Button(self.scroll_frame_gal, image=im, bg="#f8f9fa", relief="flat", activebackground="#e1e4e8", command=lambda f=fn: self.select_avatar(f), cursor="hand2")
                btn.image = im; btn.grid(row=r, column=c, padx=8, pady=8); c += 1
                if c >= 4: c = 0; r += 1

    def select_avatar(self, f):
        self.foto_escolhida = f; p = self.load_img(f"avatares/{f}", (160, 160), circular=True)
        if p:
            self.preview_img_lbl.config(image=p, text=""); self.preview_img_lbl.image = p
            self.p_card.config(highlightbackground=COLORS["success"]) # Feedback visual de seleção

    def save_new(self):
        nome = self.ent_nome.get().strip().title()
        if nome and self.foto_escolhida:
            self.engine.cadastrar_novo(nome, self.foto_escolhida); self.close_modal(); self.refresh_select_ui()
        else: messagebox.showwarning("Aviso", "Identidade incompleta! Nome e Avatar são obrigatórios.")

    def toggle_user(self, b_id): self.engine.alternar_na_fila(b_id); self.refresh_select_ui(); self.refresh_ui()
    def confirmar_delecao(self, b_id):
        if messagebox.askyesno("Confirmar", "Deseja excluir permanentemente?"): self.engine.deletar_membro(b_id); self.refresh_select_ui(); self.refresh_ui()

    def refresh_ui(self):
        win_h = self.root.winfo_height()
        if win_h < 100: return
        hero_sz, next_sz = int(win_h * 0.30), int(win_h * 0.13); self.main_cache = []
        self.halo.config(width=hero_sz + 10, height=hero_sz + 10)
        if self.engine.fila:
            at = self.engine.fila[0]; p = self.load_img(f"avatares/{at['foto']}", (hero_sz, hero_sz), circular=True)
            self.main_name_lbl.config(text=at['nome'].upper())
            if p: self.main_img_lbl.config(image=p); self.main_cache.append(p)
            for i in range(3):
                idx, slot = i + 1, self.next_slots[i]
                if idx < len(self.engine.fila):
                    nx = self.engine.fila[idx]; p_nx = self.load_img(f"avatares/{nx['foto']}", (next_sz, next_sz), circular=True)
                    if p_nx: slot["img"].config(image=p_nx); self.main_cache.append(p_nx)
                    slot["name"].config(text=nx['nome'].split()[0])
                else: slot["img"].config(image=""); slot["name"].config(text="")
        else:
            p_sem = self.load_img("icons/sem-atendimento.png", (hero_sz, hero_sz), circular=False)
            if p_sem: self.main_img_lbl.config(image=p_sem); self.main_cache.append(p_sem)
            self.main_name_lbl.config(text="AGUARDANDO EQUIPE...")
            for slot in self.next_slots: slot["img"].config(image=""); slot["name"].config(text="")

    def on_resize(self, event):
        if event.widget == self.root: self.draw_gradient(); self.refresh_ui()

    def draw_gradient(self):
        self.bg_canvas.delete("grad")
        w, h = self.root.winfo_width(), self.root.winfo_height()
        if w < 10 or h < 10: return
        start, end = (41, 128, 185), (242, 245, 248)
        for i in range(h):
            r = int(start[0] + (end[0]-start[0]) * i/h); g = int(start[1] + (end[1]-start[1]) * i/h); b = int(start[2] + (end[2]-start[2]) * i/h)
            self.bg_canvas.create_line(0, i, w, i, fill=f"#{r:02x}{g:02x}{b:02x}", tags="grad")
        self.bg_canvas.lower()