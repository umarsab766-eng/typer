from UI import INIT_THEME, Label
from nicegui import ui
from comps.CompHeader import CompHeader
from ENV import THEME_DEFAULT

async def create():
    INIT_THEME()
    # ---------- HEADER ----------
    CompHeader()
    # ---------- MAIN CONTENT ----------
    with ui.column().classes("w-[100vw] h-[100vh] items-center justify-center"):
        with ui.element("div").classes("card").style(f"""
        background: linear-gradient(
            135deg, 
            {THEME_DEFAULT['primary']} 0%, 
            {THEME_DEFAULT['primary']}88 40%,
            white 60%, 
            {THEME_DEFAULT['secondary']} 100%
        );
        """):
            ui.markdown("""
# 💫 About Typer

Welcome to **Typer**, your personal typing speed test app built with love 💚 using **NiceGUI**.  
Here, you can practice and improve your typing skills in a clean, dark-themed environment.

---

### 🧠 Features:
- Real-time typing speed tracking  
- Error detection and accuracy display  
- Save your best scores  
- Smooth & modern design

---

### 🚀 Goal:
Typer is made to help you type faster, smarter, and more accurately — while enjoying the process.

---

### 👨‍💻 Developer:
**Ahmadi Devil King**  
> "Speed is not just how fast you type, but how confident you are in every key."
""").classes("text-white text-left")

            Label("© 2025 Typer | All Rights Reserved").classes("footer text-gray-400")
