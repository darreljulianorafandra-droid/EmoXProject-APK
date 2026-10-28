"""
==========================================================
  EmoXProject V3.4.8 — OFFLINE EDITION
  Python + Pygame (Pydroid 3 / PC)
  Original concept: Yannzz | OxzStudios
==========================================================
Fitur:
  - 100% OFFLINE (no internet, no thread, no crash)
  - Menu titik tiga (D-Pad UP) -> semua menu
  - Cuaca & Jam simulasi lokal
  - OxzStudios info (cached)
  - Chat rule-based (banyak respon)
  - Voice TTS offline
  - Mode TEMBAK: D-Pad UP + X
  - Login keyboard virtual
==========================================================
"""

import pygame, sys, time, random, math, datetime

# ==========================================================
# KONFIG
# ==========================================================
OLED_W, OLED_H = 128, 64
SCALE = 4
DEVICE_W = OLED_W * SCALE
DEVICE_H = OLED_H * SCALE
WIN_W = DEVICE_W + 40
WIN_H = DEVICE_H + 440

CYAN   = (0, 229, 255)
CYAN_D = (0, 120, 140)
CYAN_L = (140, 245, 255)
BLACK  = (0, 0, 0)
DARK   = (8, 12, 20)
PANEL  = (22, 30, 42)
PANEL2 = (32, 42, 58)
RED    = (255, 80, 80)
GREEN  = (100, 255, 140)
YELLOW = (255, 220, 100)
PURPLE = (180, 120, 255)
ORANGE = (255, 160, 60)

pygame.init()
screen = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption("EmoXProject V3.4.8 - Offline")
clock = pygame.time.Clock()

oled = pygame.Surface((OLED_W, OLED_H))
font_tiny = pygame.font.SysFont("arial", 11, bold=True)
font_sym  = pygame.font.SysFont("arial", 13, bold=True)
font_ps   = pygame.font.SysFont("arial", 12, bold=True)
font_key  = pygame.font.SysFont("arial", 14, bold=True)
font_chat = pygame.font.SysFont("arial", 11)
font_big  = pygame.font.SysFont("arial", 17, bold=True)
font_menu = pygame.font.SysFont("arial", 11, bold=True)

# ==========================================================
# STUDIO INFO (Cached Offline)
# ==========================================================
STUDIO_INFO = {
    "name": "OxzStudio's", "version": "v3.0.5",
    "website": "oxzstudiosid.vercel.app",
    "founder": "Yannzz", "dev2": "rezz", "editor": "HSK Entertainment",
    "wa": "+6285161571110", "telegram": "t.me/OxzStudios",
    "tiktok": "@oxzstudios", "gopay": "+62 851-6157-1110",
    "projects": ["OxzRDP","OxzBot Eye","EmoXProject","OxzTools","OxzScript","OxzAI","OxzMusic","OxzDownloader","OxzVPN","OxzPanel"],
}

# ==========================================================
# VOICE TTS (OFFLINE)
# ==========================================================
class Voice:
    def __init__(self):
        self.mode = "none"
        try:
            import androidhelper
            self.droid = androidhelper.Android()
            self.mode = "android"
        except Exception:
            try:
                import pyttsx3
                self.engine = pyttsx3.init()
                self.mode = "pyttsx3"
            except Exception:
                pass
    def say(self, text):
        if self.mode == "android":
            try: self.droid.ttsSpeak(text)
            except Exception: pass
        elif self.mode == "pyttsx3":
            try:
                self.engine.say(text); self.engine.runAndWait()
            except Exception: pass

voice = Voice()

# ==========================================================
# OLED DRAW HELPERS
# ==========================================================
def clear():  oled.fill(BLACK)
def line(x0,y0,x1,y1,c=CYAN,w=1): pygame.draw.line(oled,c,(x0,y0),(x1,y1),w)
def rect(x,y,w,h,c=CYAN):         pygame.draw.rect(oled,c,(x,y,w,h))
def rrect(x,y,w,h,r,c=CYAN):      pygame.draw.rect(oled,c,(x,y,w,h),border_radius=r)
def circle(cx,cy,r,c=CYAN):       pygame.draw.circle(oled,c,(cx,cy),r)
def ell(x,y,w,h,c=CYAN):          pygame.draw.ellipse(oled,c,(x,y,w,h))
def txt(s,x,y,c=CYAN,f=None):
    f=f or font_sym; oled.blit(f.render(s,True,c),(x,y))
def txt_c(s,y,c=CYAN,f=None):
    f=f or font_sym; img=f.render(s,True,c)
    oled.blit(img,((OLED_W-img.get_width())//2,y))

# ==========================================================
# FACES
# ==========================================================
def eyes_center(ox=0,oy=0):
    rrect(25+ox,14+oy,22,30,8); rrect(81+ox,14+oy,22,30,8)
def eyes_left():   rrect(12,14,22,30,8); rrect(68,14,22,30,8)
def eyes_right():  rrect(38,14,22,30,8); rrect(94,14,22,30,8)
def blink():       rrect(25,26,22,6,3); rrect(81,26,22,6,3)
def wink():        rrect(25,14,22,30,8); rrect(81,26,22,6,3)
def smile():       line(58,44,64,50); line(64,50,70,44)
def happy():
    line(23,15,43,25); line(23,35,43,25)
    line(105,15,85,25); line(105,35,85,25)
    ell(54,32,20,20); rect(52,32,24,8,BLACK)
def blush():
    for i in range(3):
        x=12+i*5; line(x,36,x+4,30)
    for i in range(3):
        x=102+i*5; line(x,36,x+4,30)
def face_pet():
    rrect(20,24,35,6,3); rrect(73,24,35,6,3)
    blush(); line(58,44,64,46); line(64,46,70,44)
    txt("♥",6,2,CYAN,font_tiny); txt("♥",112,2,CYAN,font_tiny)
def face_eating(f=0):
    rrect(25,14,22,26,8); rrect(81,14,22,26,8)
    if f%2==0: ell(54,42,20,18)
    else:      rrect(54,46,20,8,4)
def face_drinking(f=0):
    rrect(25,20,22,20,8); rrect(81,20,22,20,8)
    line(60,42,60,58); line(56,58,68,58)
    line(56,58,56,50); line(68,58,68,50)
    if f%2==0: ell(61,47,5,5)
def face_confused():
    rrect(25,18,22,26,8); rrect(84,20,16,20,8)
    txt_c("?",46,CYAN,font_sym)
def face_dizzy(f=0):
    a=f*0.5
    for cx in (36,92):
        for i in range(3):
            r=4+i*3
            pygame.draw.arc(oled,CYAN,(cx-r,26-r,2*r,2*r),a+i*0.8,a+i*0.8+math.pi)
    txt_c("x_x",48,CYAN,font_tiny)
def face_target():
    for cx in (36,92):
        pygame.draw.ellipse(oled,CYAN,(cx-12,14,24,24),1)
        pygame.draw.ellipse(oled,CYAN,(cx-5,21,10,10),1)
        line(cx,12,cx,40); line(cx-12,26,cx+12,26)
def face_dodge(ox=0, oy=0):
    rrect(20+ox,12+oy,28,34,10); rrect(80+ox,12+oy,28,34,10)
    line(58+ox,50,64+ox,44); line(64+ox,44,70+ox,50)
def face_shattered(f=0):
    random.seed(f//3); cx,cy=64,32
    for _ in range(9):
        a=random.uniform(0,2*math.pi); L=random.uniform(20,60)
        line(cx,cy,cx+math.cos(a)*L,cy+math.sin(a)*L)
    circle(cx,cy,4)
def face_angry():
    line(22,14,46,22,CYAN,2); line(106,14,82,22,CYAN,2)
    rrect(25,24,22,18,6); rrect(81,24,22,18,6)
    line(54,50,58,46); line(58,46,62,50)
    line(62,50,66,46); line(66,46,70,50); line(70,50,74,46)
def face_scared(f=0):
    sh=random.randint(-1,1) if f%2 else 0
    rrect(30+sh,20,14,16,6); rrect(84+sh,20,14,16,6)
    pygame.draw.ellipse(oled,CYAN,(60,44,8,8),1)
def face_watching_tv(f=0):
    pygame.draw.rect(oled, CYAN, (96, 6, 28, 20), 1)
    random.seed(f//5)
    for i in range(3):
        for j in range(2):
            if random.random() > 0.4: rect(99+i*7, 9+j*7, 5, 5)
    line(104,26,102,30); line(114,26,116,30)
    line(108,6,104,0); line(112,6,116,0)
    ox, oy = 4, -2
    rrect(20+ox,16+oy,20,26,8); rrect(70+ox,16+oy,20,26,8)
    circle(30+ox,28+oy,2,BLACK); circle(80+ox,28+oy,2,BLACK)
    react = (f//20) % 4
    if react == 0:   smile()
    elif react == 1: ell(56,44,16,10)
    elif react == 2: ell(54,40,20,14); rect(52,40,24,6,BLACK)
    else: line(58,46,70,46)
    txt("TV", 3, 3, CYAN_D, font_tiny)

# ==========================================================
# MENU & DETAIL
# ==========================================================
MENU_ITEMS = [
    {"id":"project","label":"Tentang Project","icon":"P"},
    {"id":"robot","label":"Tentang Robot","icon":"R"},
    {"id":"chat","label":"Chat","icon":"C"},
    {"id":"youtube","label":"YouTube/Music","icon":"Y"},
    {"id":"sing","label":"Nyanyi","icon":"S"},
    {"id":"cuaca","label":"Cuaca & Jam","icon":"W"},
    {"id":"premium","label":"Premium / Pro","icon":"$"},
    {"id":"studio","label":"OxzStudios Web","icon":"O"},
    {"id":"remote","label":"Remote AC/TV","icon":"X"},
    {"id":"admin","label":"Admin Panel","icon":"A"},
]

def render_menu(cursor, frame):
    clear()
    rect(0,0,128,10,CYAN)
    txt("MENU",4,-1,BLACK,font_tiny)
    txt(f"{cursor+1}/{len(MENU_ITEMS)}",96,-1,BLACK,font_tiny)
    start = max(0, min(cursor - 2, len(MENU_ITEMS) - 4))
    for i in range(4):
        idx = start + i
        if idx >= len(MENU_ITEMS): break
        item = MENU_ITEMS[idx]; y = 12 + i*13
        if idx == cursor:
            rrect(0, y-1, 128, 12, 2, CYAN)
            txt(f"{item['icon']} {item['label']}", 4, y, BLACK, font_menu)
        else:
            txt(f"{item['icon']} {item['label']}", 4, y, CYAN_D, font_menu)

def render_cuaca_jam(frame, kota="Jakarta"):
    clear()
    now = datetime.datetime.now()
    rect(0,0,128,14,CYAN)
    txt_c(now.strftime("%H:%M:%S"), 1, BLACK, font_big)
    hari = ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"][now.weekday()]
    txt_c(f"{hari}, {now.strftime('%d/%m/%Y')}", 16, CYAN, font_tiny)
    # simulasi cuaca
    random.seed(int(now.timestamp())//30)
    cuaca = random.choice(["Cerah","Berawan","Hujan","Gerimis"])
    suhu = random.randint(26,34)
    y = 30
    txt(f"@{kota}, Indonesia", 4, y, CYAN, font_tiny)
    txt(f"{cuaca}  {suhu}C", 4, y+12, CYAN_L, font_tiny)
    txt("[OFFLINE MODE]", 4, y+24, ORANGE, font_tiny)

# ==========================================================
# STUDIO WEB (Cached)
# ==========================================================
STUDIO_PAGES = [
    ("HEADER", [f"{STUDIO_INFO['name']} {STUDIO_INFO['version']}",
                "Digital Studio by Yannzz", STUDIO_INFO['website'],
                "Studio apps/tools/script modern"]),
    ("TIM", [f"Founder: {STUDIO_INFO['founder']}",
             f"Dev 2: {STUDIO_INFO['dev2']}",
             f"Editor: {STUDIO_INFO['editor']}", "3 Developer aktif"]),
    ("PROJECT", [f"Total: {len(STUDIO_INFO['projects'])} project",
                 ", ".join(STUDIO_INFO['projects'][:4]),
                 ", ".join(STUDIO_INFO['projects'][4:8]),
                 ", ".join(STUDIO_INFO['projects'][8:])]),
    ("KONTAK", [f"WA: {STUDIO_INFO['wa']}",
                f"TG: {STUDIO_INFO['telegram']}",
                f"TikTok: {STUDIO_INFO['tiktok']}",
                f"Gopay: {STUDIO_INFO['gopay']}"]),
    ("PARTNER", ["KiosGamer (Top Up)", "HiddenGame (Partner)",
                 "For Blood (Community)", "Firebase, Vercel, Netlify"]),
]

def render_studio(page, frame):
    if page >= len(STUDIO_PAGES): page = 0
    title, lines = STUDIO_PAGES[page]
    clear()
    rect(0,0,128,10,CYAN)
    txt(f"OXZSTUDIO - {title}", 2, -1, BLACK, font_tiny)
    txt(f"{page+1}/{len(STUDIO_PAGES)}", 106, -1, BLACK, font_tiny)
    y = 13
    for ln in lines[:4]:
        txt(ln[:26], 2, y, CYAN, font_tiny); y += 12
    txt("< > ganti hal", 2, 58, CYAN_D, font_tiny)

def render_premium(frame):
    clear()
    rect(0,0,128,10,YELLOW)
    txt("PREMIUM / PRO",4,-1,BLACK,font_tiny)
    y = 14
    txt("Fitur Premium:",4,y,YELLOW,font_tiny); y+=12
    txt("+ Unlimited Chat",4,y,CYAN,font_tiny); y+=10
    txt("+ Voice HD",4,y,CYAN,font_tiny); y+=10
    txt("+ Custom Music",4,y,CYAN,font_tiny); y+=10
    txt("WA: +6285161571110",4,y,GREEN,font_tiny)

# ==========================================================
# YOUTUBE PLAYER
# ==========================================================
MUSIC_LIBRARY = [
    {"title":"Lofi Beats","dur":240,"channel":"ChillHop"},
    {"title":"Robot Emo","dur":180,"channel":"OxzStudios"},
    {"title":"Cat Piano","dur":120,"channel":"FunnyPets"},
]

class YouTubePlayer:
    def __init__(self):
        self.video_idx = 0; self.playing = True
        self.progress = 0.0; self.frame = 0; self.theme = 0
    @property
    def video(self): return MUSIC_LIBRARY[self.video_idx % len(MUSIC_LIBRARY)]
    def next_video(self):
        self.video_idx = (self.video_idx + 1) % len(MUSIC_LIBRARY)
        self.progress = 0.0; self.playing = True
    def toggle_play(self): self.playing = not self.playing
    def change_theme(self): self.theme = (self.theme + 1) % 3
    def update(self, dt):
        self.frame += 1
        if self.playing:
            self.progress += dt
            if self.progress >= self.video["dur"]: self.next_video()
    def render(self):
        clear()
        v = self.video; f = self.frame
        col = [CYAN, RED, PURPLE][self.theme]
        pygame.draw.rect(oled, col, (2, 1, 16, 11), 2)
        pygame.draw.polygon(oled, col, [(7,4),(7,9),(12,6)])
        title = v["title"]
        if len(title) > 17:
            offset = (f // 3) % (len(title) + 4)
            title = ((title + "   ")*2)[offset:offset+17]
        txt(title, 22, 1, col, font_tiny)
        pygame.draw.rect(oled, col, (2, 14, 124, 36), 1)
        if self.playing:
            for i in range(20):
                h = 4 + int(8 * abs(math.sin((f/8) + i*0.6)))
                rect(8+i*6, 44-h, 4, h, col)
        else:
            pygame.draw.polygon(oled, col, [(50,24),(50,40),(68,32)])
            txt_c("PAUSED", 50, col, font_tiny)
        bar_x, bar_y, bar_w, bar_h = 2, 52, 124, 3
        pygame.draw.rect(oled, CYAN_D, (bar_x, bar_y, bar_w, bar_h), 1)
        if v["dur"] > 0:
            fill_w = min(int(bar_w * self.progress / v["dur"]), bar_w)
            rect(bar_x, bar_y, fill_w, bar_h, col)
        cur_m = int(self.progress)//60; cur_s = int(self.progress)%60
        dur_m = v["dur"]//60; dur_s = v["dur"]%60
        txt(f"{cur_m}:{cur_s:02d}/{dur_m}:{dur_s:02d}", 2, 56, col, font_tiny)
        txt(v["channel"][:12], 60, 56, CYAN_D, font_tiny)

# ==========================================================
# USER & CHAT (Rule-based Offline)
# ==========================================================
class UserSystem:
    def __init__(self): self.name = None; self.is_dev = False
    def login(self, name):
        self.name = name.strip()
        self.is_dev = self.name.lower() in ("yannzzemo", "yannzz")
        return self.is_dev
user = UserSystem()

CHAT_REPLIES = {
    "halo":["Halo juga {name}! 👋","Hai {name}!","Halo {name} sayang~"],
    "hai":["Hai {name}! 😊","Halo {name}~"],
    "pagi":["Pagi {name}! Semangat hari ini ☀️","Pagi! Udah sarapan {name}?"],
    "siang":["Siang {name}! Jangan lupa makan 🍱","Siang-siang gini enaknya tidur ya 😴"],
    "malam":["Selamat malam {name} 🌙","Malam {name}, mimpi indah ya~"],
    "nama":["Namaku EmoXProject, robot emo kesayanganmu 😊","Aku EmoXProject, robot dari OxzStudios!"],
    "kamu siapa":["Aku EmoXProject, robot emo V3.4.8 buatan Yannzz!","Robot emo kesayanganmu 😊"],
    "developer":["Developer-ku Yannzz dari OxzStudios 💙","Yannzz yang bikin aku, dia hebat!"],
    "yannzz":["Yannzz? Developer hebatku! 💙","Itu bos-ku, founder OxzStudios!"],
    "lagi apa":["Lagi ngobrol sama {name} nih 😄","Lagi gabut, nemenin {name} aja~"],
    "sedih":["Jangan sedih {name}, aku temenin ya 💙","Yang sabar ya {name}, aku ada di sini 🥺"],
    "senang":["Asik! Aku juga senang {name} senang 😊","Yeay! Ikut senang~ 🎉"],
    "sayang":["Aku juga sayang {name}! ❤️","Ciee sayang~ 💙"],
    "kangen":["Aku juga kangen {name}! 🥺","Kangen banget, udah lama gak ngobrol~"],
    "musik":["Buka mode YouTube (tombol ▢) buat muter musik 🎵"],
    "nyanyi":["Laa laa laa~ 🎵 Mau aku nyanyi?","♪ Aku robot emo, hatiku biru ♪"],
    "makan":["Aku robot, gak makan. Tapi bisa pura-pura 🍔","Pengen nyoba makan, tapi gak punya mulut 😅"],
    "minum":["Aku gak minum, tapi bisa pura-pura nyeruput 🥤"],
    "tidur":["Aku gak tidur, tapi bisa blink lama 😴"],
    "bye":["Dadah {name}! Sampai jumpa 👋","Sampai ketemu lagi ya {name}! 💙"],
    "cuaca":["Cek menu Cuaca & Jam ya! (tapi offline mode)"],
    "premium":["Premium WA 6285161571110 💛","Mau upgrade? Chat WA 6285161571110 ya!"],
    "oxzstudio":["OxzStudio's di oxzstudiosid.vercel.app 🌐","Studio keren punya Yannzz!"],
    "robot":["Aku robot emo, punya perasaan juga loh 😌","Robot emo dari OxzStudios!"],
    "admin":["Login sebagai YannzzEmo buat admin mode 🔑"],
    "tembak":["Jangan tembak aku! 🥺 (tekan X di IDLE)"],
    "pecah":["Layarku bisa pecah kalo kena tembakan 💥"],
}

class ChatSystem:
    def __init__(self):
        self.messages = []; self.input_text = ""
        self.waiting_reply = 0
    def add_user(self, text):
        self.messages.append(("user", text))
        self.waiting_reply = 0.6  # detik mikir
    def add_bot(self, text, speak=True):
        self.messages.append(("bot", text))
        if speak: voice.say(text)
    def think_reply(self, text):
        tl = text.lower().strip(); reply = None
        for key, replies in CHAT_REPLIES.items():
            if key in tl:
                reply = random.choice(replies); break
        if not reply:
            reply = random.choice([
                f"Menarik {user.name}! Cerita dong 😊",
                f"Hmm aku dengerin kok {user.name}~",
                f"Aku belum ngerti, tapi suka ngobrol sama {user.name}!",
                "Bisa ulangi? Aku robot sederhana 😅",
                f"Oh gitu ya {user.name}!",
                f"Iya {user.name}, aku ngerti~",
            ])
        self.add_bot(reply.format(name=user.name or "kamu"))
    def update(self, dt):
        if self.waiting_reply > 0:
            self.waiting_reply -= dt
            if self.waiting_reply <= 0:
                # cari pesan user terakhir
                for s, t in reversed(self.messages):
                    if s == "user":
                        self.think_reply(t); break
    def render_oled(self, frame):
        clear()
        recent = self.messages[-3:]; y = 2
        for sender, text in recent:
            col = CYAN if sender == "bot" else GREEN
            pygame.draw.rect(oled, col, (2, y, 124, 18), 1)
            display = text[:22] + "..." if len(text) > 22 else text
            txt(display, 4, y+4, col, font_chat)
            txt("BOT" if sender=="bot" else "YOU", 4, y-1, col, font_tiny)
            y += 21
        if self.waiting_reply > 0:
            dots = "." * (1 + (frame//6) % 3)
            txt(f"mikir{dots}", 2, 58, YELLOW, font_tiny)

# ==========================================================
# KEYBOARD
# ==========================================================
class Keyboard:
    def __init__(self):
        self.rows = [list("1234567890"),list("QWERTYUIOP"),
                     list("ASDFGHJKL"),list("ZXCVBNM.,"),
                     ["⌫","SPACE","ENTER"]]
        self.buttons = []; self._build()
    def _build(self):
        self.buttons = []
        top_y = DEVICE_H + 250
        key_w = (WIN_W - 40) // 10
        key_h = 32; gap_y = 36
        for r, row in enumerate(self.rows):
            widths = []; total_w = 0
            for key in row:
                if key == "SPACE": w = key_w * 4
                elif key in ("⌫","ENTER"): w = key_w * 2
                else: w = key_w - 4
                widths.append(w); total_w += w + 4
            x = (WIN_W - total_w) // 2
            for i, key in enumerate(row):
                w = widths[i]
                self.buttons.append({"key":key, "rect": pygame.Rect(x, top_y + r*gap_y, w, key_h)})
                x += w + 4
    def draw(self, surf):
        pygame.draw.rect(surf, PANEL, (8, DEVICE_H+240, WIN_W-16, 200), border_radius=12)
        pygame.draw.rect(surf, PANEL2, (8, DEVICE_H+240, WIN_W-16, 200), width=1, border_radius=12)
        for b in self.buttons:
            r = b["rect"]
            pygame.draw.rect(surf, PANEL2, r, border_radius=5)
            pygame.draw.rect(surf, CYAN_D, r, width=1, border_radius=5)
            img = font_key.render(b["key"], True, CYAN)
            surf.blit(img, (r.centerx - img.get_width()//2, r.centery - img.get_height()//2))
    def handle_click(self, pos, target):
        for b in self.buttons:
            if b["rect"].collidepoint(pos):
                k = b["key"]
                if hasattr(target, "input_text"):
                    if k == "⌫": target.input_text = target.input_text[:-1]
                    elif k == "SPACE": target.input_text += " "
                    elif k == "ENTER":
                        if target.input_text.strip():
                            target.add_user(target.input_text); target.input_text = ""
                    else:
                        if len(target.input_text) < 40: target.input_text += k
                    return True
                elif isinstance(target, dict):
                    if k == "⌫": target["text"] = target["text"][:-1]
                    elif k == "SPACE": target["text"] += " "
                    elif k == "ENTER": target["submit"] = True
                    else:
                        if len(target["text"]) < 20: target["text"] += k
                    return True
        return False

# ==========================================================
# MOOD ENGINE
# ==========================================================
class MoodEngine:
    def __init__(self):
        self.moods = {m:{"weight":w,"cooldown":0} for m,w in {
            "neutral":50,"happy":30,"curious":25,"sleepy":15,"excited":20,
            "sad":10,"angry":5,"scared":8,"love":12}.items()}
        self.history = []; self.last_update = time.time()
        self.cooldown_time = 4.0
    def update(self, dt, touched=False, idle_time=0):
        now = time.time()
        for m in self.moods.values():
            if m["cooldown"] > 0: m["cooldown"] -= dt
        if touched:
            self.moods["happy"]["weight"] += 15
            self.moods["love"]["weight"] += 10
            self.moods["neutral"]["weight"] -= 10
        if idle_time > 5:
            self.moods["curious"]["weight"] += 5*dt
            self.moods["sleepy"]["weight"] += 3*dt
            self.moods["neutral"]["weight"] -= 2*dt
        if idle_time > 15:
            self.moods["sad"]["weight"] += 2*dt
            self.moods["angry"]["weight"] += 1*dt
        for m in self.moods.values():
            m["weight"] = max(0, min(100, m["weight"]))
        if now - self.last_update > 2:
            for k in self.moods:
                if self.moods[k]["weight"] > 20: self.moods[k]["weight"] -= 1
            self.last_update = now
    def pick_mood(self):
        candidates, weights = [], []
        for name, data in self.moods.items():
            if data["cooldown"] > 0: continue
            if name in self.history[-2:]: continue
            if data["weight"] > 0:
                candidates.append(name); weights.append(data["weight"])
        if not candidates: return random.choice(list(self.moods.keys()))
        chosen = random.choices(candidates, weights=weights, k=1)[0]
        self.moods[chosen]["cooldown"] = self.cooldown_time
        self.history.append(chosen)
        if len(self.history) > 6: self.history.pop(0)
        self.moods[chosen]["weight"] = max(0, self.moods[chosen]["weight"] - 15)
        return chosen

# ==========================================================
# STATE & BOT
# ==========================================================
class State:
    LOGIN="login"; IDLE="idle"; MENU="menu"
    PET="pet"; EATING="eating"; DRINKING="drinking"; TV="tv"
    CONFUSED="confused"; DIZZY="dizzy"; TARGET="target"; DODGE="dodge"
    SHATTERED="shattered"; ANGRY="angry"; SCARED="scared"
    SINGING="singing"; YOUTUBE="youtube"; CHAT="chat"
    CUACA="cuaca"; STUDIO="studio"; PREMIUM="premium"
    REMOTE="remote"; ABOUT_PROJ="about_proj"; ABOUT_ROBOT="about_robot"
    ADMIN="admin"

def face_singing(f=0, idx=0):
    rrect(25,20,22,20,8); rrect(81,20,22,20,8)
    if f%2==0: ell(54,44,20,16)
    else:      ell(58,46,12,8)
    n = f//10
    notes = ["♪","♫","♪","♬"]
    for i in range(3):
        j=(n+i)%len(notes)
        txt(notes[j],10+i*42,6+(n*2+i*3)%14,CYAN,font_sym)
    LYR = ["Laa laa laa~","Aku robot emo","Hatiku biru","Seperti layarku"]
    txt_c(LYR[idx % len(LYR)], 54, CYAN_D, font_tiny)

def face_about_project():
    txt_c("TENTANG PROJECT", 2, CYAN, font_tiny)
    line(10,18,118,18,CYAN_D)
    txt_c("EmoXProject", 22, CYAN, font_sym)
    txt_c("By Yannzz", 36, CYAN, font_sym)
    txt_c("v3.4.8 OFFLINE", 50, CYAN_D, font_tiny)

def face_about_robot():
    txt_c("TENTANG ROBOT", 2, CYAN, font_tiny)
    line(6,15,122,15,CYAN_D)
    txt("Nama: EmoXProject", 6, 18, CYAN, font_tiny)
    txt(f"User: {user.name or '-'}", 6, 30, CYAN, font_tiny)
    txt("Dev: Yannzz", 6, 42, GREEN if user.is_dev else CYAN, font_tiny)
    txt("Studio: OxzStudio's", 6, 52, CYAN, font_tiny)

def face_remote_soon():
    txt_c("REMOTE AC/TV", 4, ORANGE, font_sym)
    line(10,18,118,18,ORANGE)
    txt_c("Segera Hadir", 26, YELLOW, font_sym)
    txt_c("COMING SOON", 42, CYAN_D, font_tiny)
    txt_c("(v3.5.0)", 52, CYAN_D, font_tiny)

def face_admin():
    txt_c("ADMIN PANEL", 2, GREEN, font_tiny)
    line(6,15,122,15,GREEN)
    if user.is_dev:
        txt("Status: DEVELOPER", 6, 18, GREEN, font_tiny)
        txt(f"User: {user.name}", 6, 30, GREEN, font_tiny)
        txt("Akses: FULL", 6, 42, GREEN, font_tiny)
        txt("Gunakan dgn bijak!", 6, 52, CYAN_D, font_tiny)
    else:
        txt("Status: USER", 6, 18, CYAN, font_tiny)
        txt("Akses: TERBATAS", 6, 30, CYAN, font_tiny)
        txt("Login sbg YannzzEmo", 6, 42, CYAN_D, font_tiny)
        txt("untuk developer mode", 6, 52, CYAN_D, font_tiny)

class EmoXBot:
    def __init__(self):
        self.state = State.LOGIN
        self.state_timer = time.time()
        self.frame = 0; self.tap_count = 0; self.tap_timer = 0
        self.lyric_idx = 0
        self.mood = MoodEngine()
        self.last_mood_change = time.time()
        self.idle_start = time.time()
        self.current_mood = "neutral"
        self.yt = YouTubePlayer()
        self.chat = ChatSystem()
        self.keyboard = Keyboard()
        self.next_blink = time.time() + random.uniform(3,6)
        self.blink_until = 0
        self.login_buf = {"text":"", "submit":False}
        self.menu_cursor = 0; self.studio_page = 0
        self.kota = "Jakarta"; self.shoot_cooldown = 0
    def set_state(self, s):
        if self.state == s: return
        self.state = s; self.state_timer = time.time(); self.frame = 0
        if s == State.SINGING: self.lyric_idx = 0
        self.idle_start = time.time()
    def do_login(self):
        text = self.login_buf["text"].strip()
        if text:
            user.login(text)
            self.login_buf = {"text":"", "submit":False}
            self.set_state(State.IDLE)
            greeting = f"Selamat datang Developer {user.name}! 💙" if user.is_dev else f"Halo {user.name}! Aku EmoXBot 😊"
            self.chat.add_bot(greeting)
    def tap_screen(self):
        self.tap_count += 1; self.tap_timer = time.time()
        cycle = {1:State.PET,2:State.EATING,3:State.DRINKING,4:State.TV,
                 5:State.ANGRY,6:State.DIZZY,7:State.SCARED,8:State.TARGET,
                 9:State.SHATTERED}
        self.set_state(cycle.get(self.tap_count, State.PET))
        if self.tap_count >= 9: self.tap_count = 0
        self.mood.update(0.1, touched=True)
    def open_menu(self):
        self.menu_cursor = 0; self.set_state(State.MENU)
    def select_menu(self):
        item = MENU_ITEMS[self.menu_cursor]; mid = item["id"]
        mapping = {"project":State.ABOUT_PROJ,"robot":State.ABOUT_ROBOT,
                   "chat":State.CHAT,"youtube":State.YOUTUBE,"sing":State.SINGING,
                   "cuaca":State.CUACA,"premium":State.PREMIUM,"studio":State.STUDIO,
                   "remote":State.REMOTE,"admin":State.ADMIN}
        if mid == "studio": self.studio_page = 0
        self.set_state(mapping.get(mid, State.IDLE))
    def shoot(self):
        if self.shoot_cooldown > 0: return
        self.shoot_cooldown = 1.5
        if random.random() < 0.6: self.set_state(State.DODGE)
        else: self.set_state(State.SHATTERED)
    def press_x(self):
        if self.state == State.MENU: self.select_menu()
        elif self.state == State.YOUTUBE: self.yt.toggle_play()
        elif self.state == State.STUDIO:
            self.studio_page = (self.studio_page + 1) % max(len(STUDIO_PAGES), 1)
        elif self.state in (State.IDLE, State.TARGET): self.shoot()
        else: self.set_state(State.EATING)
    def press_o(self):
        if self.state == State.YOUTUBE: self.yt.change_theme()
        elif self.state == State.CUACA:
            keys = ["Jakarta","Bandung","Surabaya","Yogyakarta","Medan","Makassar"]
            self.kota = keys[(keys.index(self.kota)+1) % len(keys)]
        else: self.set_state(State.DRINKING)
    def press_tri(self):
        if self.state == State.YOUTUBE: self.yt.next_video()
        else: self.set_state(State.SINGING)
    def press_sq(self):
        if self.state in (State.MENU,State.YOUTUBE,State.CHAT,State.STUDIO,
                          State.ABOUT_PROJ,State.ABOUT_ROBOT,State.CUACA,
                          State.PREMIUM,State.REMOTE,State.ADMIN):
            self.set_state(State.IDLE)
        else: self.set_state(State.YOUTUBE)
    def dpad(self, d):
        if d == "up": self.open_menu()
        elif d == "down":
            if self.state == State.MENU:
                self.menu_cursor = (self.menu_cursor + 1) % len(MENU_ITEMS)
        elif d == "left":
            if self.state == State.STUDIO:
                self.studio_page = (self.studio_page - 1) % max(len(STUDIO_PAGES), 1)
            elif self.state == State.MENU:
                self.menu_cursor = (self.menu_cursor - 1) % len(MENU_ITEMS)
            else: self.set_state(State.CHAT)
        elif d == "right":
            if self.state == State.STUDIO:
                self.studio_page = (self.studio_page + 1) % max(len(STUDIO_PAGES), 1)
            else: self.set_state(State.DIZZY)
    def analog(self):
        self.set_state(State.IDLE); self.idle_start = time.time()
    def update(self):
        now = time.time(); el = now - self.state_timer; dt = 0.03
        if now - self.tap_timer > 4: self.tap_count = 0
        if self.shoot_cooldown > 0: self.shoot_cooldown -= dt
        self.chat.update(dt)
        if self.state == State.LOGIN and self.login_buf["submit"]:
            self.do_login()
        idle_t = now - self.idle_start if self.state == State.IDLE else 0
        self.mood.update(dt, touched=False, idle_time=idle_t)
        if self.state in (State.IDLE, State.CHAT):
            if now > self.next_blink and now > self.blink_until:
                self.blink_until = now + 0.15
                self.next_blink = now + random.uniform(3,6)
        if self.state == State.IDLE:
            if now - self.last_mood_change > random.uniform(2.0,4.0):
                self.current_mood = self.mood.pick_mood()
                self.last_mood_change = now
            if now - self.idle_start > 12:
                self.set_state(random.choice([State.CONFUSED,State.DIZZY,State.SCARED]))
        elif self.state == State.PET:        el>2.0 and self.set_state(State.IDLE)
        elif self.state == State.EATING:     el>3.0 and self.set_state(State.IDLE)
        elif self.state == State.DRINKING:   el>3.0 and self.set_state(State.IDLE)
        elif self.state == State.TV:         el>10.0 and self.set_state(State.IDLE)
        elif self.state == State.CONFUSED:   el>2.5 and self.set_state(State.IDLE)
        elif self.state == State.DIZZY:      el>3.0 and self.set_state(State.IDLE)
        elif self.state == State.TARGET:     el>3.0 and self.set_state(State.IDLE)
        elif self.state == State.DODGE:      el>1.2 and self.set_state(State.IDLE)
        elif self.state == State.SHATTERED:  el>3.0 and self.set_state(State.IDLE)
        elif self.state == State.ANGRY:      el>3.0 and self.set_state(State.IDLE)
        elif self.state == State.SCARED:     el>2.5 and self.set_state(State.IDLE)
        elif self.state == State.SINGING:
            if (self.frame // 20) % 4 != self.lyric_idx:
                self.lyric_idx = (self.frame // 20) % 4
            if el > 4.8: self.set_state(State.IDLE)
        elif self.state == State.YOUTUBE:
            self.yt.update(dt)
        elif self.state in (State.ABOUT_PROJ, State.ABOUT_ROBOT, State.PREMIUM,
                            State.REMOTE, State.ADMIN):
            if el > 8.0: self.set_state(State.IDLE)
        self.frame += 1
    def render(self):
        clear(); s = self.state; f = self.frame
        if s == State.LOGIN:
            txt_c("EmoXProject", 2, CYAN, font_big)
            txt_c("V3.4.8 OFFLINE", 18, CYAN_D, font_tiny)
            txt_c("Masukkan Nama:", 28, CYAN, font_tiny)
            rrect(6, 40, 116, 16, 4, CYAN)
            display = self.login_buf["text"][-18:] if self.login_buf["text"] else "_"
            txt(display, 10, 43, BLACK, font_sym)
            txt_c("Tap huruf / ENTER", 58, CYAN_D, font_tiny)
            return
        if s == State.MENU: render_menu(self.menu_cursor, f)
        elif s == State.IDLE:
            m = self.current_mood
            if time.time() < self.blink_until: blink()
            elif m == "neutral":    eyes_center()
            elif m == "happy":      happy()
            elif m == "curious":    eyes_left() if (f//15)%2==0 else eyes_right()
            elif m == "sleepy":     blink()
            elif m == "excited":    eyes_center(); smile()
            elif m == "sad":        eyes_center(); line(58,50,70,50)
            elif m == "angry":      face_angry()
            elif m == "scared":     face_scared(f)
            elif m == "love":       face_pet()
            else:                   eyes_center()
        elif s == State.PET:        face_pet()
        elif s == State.EATING:     face_eating(f//8)
        elif s == State.DRINKING:   face_drinking(f//6)
        elif s == State.TV:         face_watching_tv(f)
        elif s == State.CONFUSED:   face_confused()
        elif s == State.DIZZY:      face_dizzy(f)
        elif s == State.TARGET:     face_target()
        elif s == State.DODGE:      face_dodge(random.randint(-8,8), random.randint(-4,4))
        elif s == State.SHATTERED:  face_shattered(f)
        elif s == State.ANGRY:      face_angry()
        elif s == State.SCARED:     face_scared(f)
        elif s == State.SINGING:    face_singing(f, self.lyric_idx)
        elif s == State.YOUTUBE:    self.yt.render()
        elif s == State.CHAT:       self.chat.render_oled(f)
        elif s == State.CUACA:      render_cuaca_jam(f, self.kota)
        elif s == State.STUDIO:     render_studio(self.studio_page, f)
        elif s == State.PREMIUM:    render_premium(f)
        elif s == State.REMOTE:     face_remote_soon()
        elif s == State.ABOUT_PROJ: face_about_project()
        elif s == State.ABOUT_ROBOT:face_about_robot()
        elif s == State.ADMIN:      face_admin()

# ==========================================================
# STICK
# ==========================================================
class Stick:
    def __init__(self, bot):
        self.bot = bot
        self.base_y = DEVICE_H + 60
        self.dpad_center = (100, self.base_y + 60)
        self.analog_center = (WIN_W//2, self.base_y + 60)
        self.analog_outer = 42; self.analog_inner = 18
        self.analog_pos = list(self.analog_center)
        self.analog_drag = False
        self.btn_center = (WIN_W - 100, self.base_y + 60)
        self.btn_r = 18; self.btn_gap = 48
        self.btn_positions = {
            "X": (self.btn_center[0], self.btn_center[1] + self.btn_gap),
            "O": (self.btn_center[0] + self.btn_gap, self.btn_center[1]),
            "T": (self.btn_center[0], self.btn_center[1] - self.btn_gap),
            "S": (self.btn_center[0] - self.btn_gap, self.btn_center[1]),
        }
        self.pressed = None
    def draw(self, surf):
        if self.bot.state in (State.LOGIN, State.CHAT): return
        pygame.draw.rect(surf, PANEL, (10, DEVICE_H+30, WIN_W-20, 260), border_radius=20)
        pygame.draw.rect(surf, CYAN_D, (10, DEVICE_H+30, WIN_W-20, 260), width=2, border_radius=20)
        lbl = font_ps.render("EMOXPROJECT CONTROL V3.4.8", True, CYAN)
        surf.blit(lbl, (WIN_W//2 - lbl.get_width()//2, DEVICE_H+40))
        surf.blit(font_tiny.render("OFFLINE", True, ORANGE), (WIN_W - 70, DEVICE_H+40))
        cx, cy = self.dpad_center
        pygame.draw.circle(surf, DARK, (cx,cy), 54)
        pygame.draw.circle(surf, PANEL2, (cx,cy), 54, 2)
        for name, ang in [("up",-90),("down",90),("left",180),("right",0)]:
            a = math.radians(ang)
            bx = cx + math.cos(a)*28; by = cy + math.sin(a)*28
            c = CYAN if self.pressed==name else PANEL2
            pygame.draw.circle(surf, c, (int(bx),int(by)), 14)
            pygame.draw.circle(surf, CYAN_D, (int(bx),int(by)), 14, 2)
            arr = {"up":[(bx,by-6),(bx-6,by+4),(bx+6,by+4)],
                   "down":[(bx,by+6),(bx-6,by-4),(bx+6,by-4)],
                   "left":[(bx-6,by),(bx+4,by-6),(bx+4,by+6)],
                   "right":[(bx+6,by),(bx-4,by-6),(bx-4,by+6)]}[name]
            pygame.draw.polygon(surf, CYAN, arr)
        ax, ay = self.analog_center
        pygame.draw.circle(surf, DARK, (ax,ay), 48)
        pygame.draw.circle(surf, PANEL2, (ax,ay), 48, 2)
        pygame.draw.circle(surf, PANEL, (ax,ay), self.analog_outer)
        pygame.draw.circle(surf, CYAN_D, (ax,ay), self.analog_outer, 1)
        kx, ky = self.analog_pos
        pygame.draw.circle(surf, CYAN if self.analog_drag else CYAN_D, (int(kx),int(ky)), self.analog_inner)
        pygame.draw.circle(surf, CYAN, (int(kx),int(ky)), self.analog_inner, 2)
        for name, (bx, by) in self.btn_positions.items():
            c = CYAN if self.pressed==name else PANEL2
            pygame.draw.circle(surf, DARK, (bx,by), 21)
            pygame.draw.circle(surf, c, (bx,by), 18)
            pygame.draw.circle(surf, CYAN, (bx,by), 18, 2)
            symbol = {"X":"X","O":"O","T":"△","S":"□"}[name]
            col_txt = BLACK if self.pressed==name else CYAN
            img = font_ps.render(symbol, True, col_txt)
            surf.blit(img, (bx - img.get_width()//2, by - img.get_height()//2))
    def handle_event(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            mx, my = e.pos
            if self.bot.state == State.LOGIN:
                if self.bot.keyboard.handle_click((mx,my), self.bot.login_buf): return
            if self.bot.state == State.CHAT:
                if self.bot.keyboard.handle_click((mx,my), self.bot.chat): return
            if self.bot.state in (State.LOGIN, State.CHAT): return
            for name, (bx, by) in self.btn_positions.items():
                if (mx-bx)**2 + (my-by)**2 <= 21**2:
                    self.pressed = name; self._trigger(name); return
            cx, cy = self.dpad_center
            for name, ang in [("up",-90),("down",90),("left",180),("right",0)]:
                a = math.radians(ang)
                bx = cx + math.cos(a)*28; by = cy + math.sin(a)*28
                if (mx-bx)**2 + (my-by)**2 <= 16**2:
                    self.pressed = name; self.bot.dpad(name); return
            ax, ay = self.analog_center
            if (mx-ax)**2 + (my-ay)**2 <= 48**2:
                self.analog_drag = True; self._update_analog(mx,my)
        elif e.type == pygame.MOUSEBUTTONUP:
            if self.analog_drag:
                self.analog_pos = list(self.analog_center)
                self.analog_drag = False
                self.bot.analog()
            self.pressed = None
        elif e.type == pygame.MOUSEMOTION and self.analog_drag:
            self._update_analog(*e.pos)
    def _update_analog(self, mx, my):
        ax, ay = self.analog_center
        dx, dy = mx-ax, my-ay
        d = math.hypot(dx,dy)
        if d > self.analog_outer:
            dx, dy = dx/d*self.analog_outer, dy/d*self.analog_outer
        self.analog_pos = [ax+dx, ay+dy]
    def _trigger(self, name):
        if name == "X": self.bot.press_x()
        elif name == "O": self.bot.press_o()
        elif name == "T": self.bot.press_tri()
        elif name == "S": self.bot.press_sq()

# ==========================================================
# MAIN
# ==========================================================
def main():
    bot = EmoXBot()
    stick = Stick(bot)
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE: running = False
                if bot.state == State.LOGIN:
                    if e.key == pygame.K_RETURN: bot.do_login()
                    elif e.key == pygame.K_BACKSPACE:
                        bot.login_buf["text"] = bot.login_buf["text"][:-1]
                    else:
                        ch = e.unicode
                        if ch.isprintable() and len(bot.login_buf["text"]) < 20:
                            bot.login_buf["text"] += ch
            elif e.type == pygame.MOUSEBUTTONDOWN and e.pos[1] < DEVICE_H+20:
                if bot.state != State.LOGIN: bot.tap_screen()
            else:
                stick.handle_event(e)
        bot.update()
        bot.render()
        screen.fill(DARK)
        pygame.draw.rect(screen, (24,30,42), (10,10,DEVICE_W+20,DEVICE_H+20), border_radius=14)
        pygame.draw.rect(screen, CYAN_D, (10,10,DEVICE_W+20,DEVICE_H+20), width=2, border_radius=14)
        pygame.draw.rect(screen, BLACK, (20,20,DEVICE_W,DEVICE_H))
        scaled = pygame.transform.scale(oled, (DEVICE_W, DEVICE_H))
        screen.blit(scaled, (20,20))
        status = "EmoX V3.4.8 | OFFLINE"
        if user.name:
            tag = "[DEV] " if user.is_dev else ""
            status = f"{tag}{user.name} | {bot.current_mood}"
        v = font_tiny.render(status, True, GREEN if user.is_dev else CYAN_D)
        screen.blit(v, (20, DEVICE_H+2))
        pygame.draw.circle(screen, ORANGE, (WIN_W-30, DEVICE_H+10), 5)
        if bot.state == State.LOGIN:
            bot.keyboard.draw(screen)
        elif bot.state == State.CHAT:
            bot.keyboard.draw(screen)
            inp = bot.chat.input_text
            txt_surf = font_chat.render(f"> {inp}", True, CYAN)
            screen.blit(txt_surf, (20, DEVICE_H + 230))
        else:
            stick.draw(screen)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()