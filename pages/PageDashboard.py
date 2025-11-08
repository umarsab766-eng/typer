# typing_page.py
from nicegui import ui
import random
from UI import SoftBtn, Label, INIT_THEME, TextArea, Col, Row
from library.formHandler import Variable, Group

# ---------- Paragraph Texts ----------
PARAGRAPHS = [
    """Typing is one of the most essential skills in today’s digital world. Whether you are writing an email, coding a program, or chatting with friends, your typing speed and accuracy can make a big difference. Practicing consistently helps you build rhythm and muscle memory over time.""",
    """Technology is advancing faster than ever before. Artificial intelligence, automation, and robotics are reshaping industries across the world. Learning programming languages like Python gives you an edge to innovate and build creative solutions.""",
    """A good typist doesn’t focus on speed alone, but on accuracy and consistency. When you type carefully, your fingers learn the correct positions and patterns. Over time, your speed will naturally increase without errors or strain.""",
]


# ---------- Helper Class ----------
class NumVar(Variable):
    def __init__(self, name, value=None):
        super().__init__(name, value or 0)

    def inc(self, i=1):
        self.value += i


# ---------- Functions ----------
def start_typing(timer, group):
    if not group.started.value:
        group.started.value = True
        timer.activate()
        group.status.value = "🕒 Typing started..."
    else:
        group.status.value = "Already running..."


# ---------- UI Page ----------
async def create():
    INIT_THEME()

    target = Variable("target", random.choice(PARAGRAPHS))
    timer = NumVar("timer", 0)
    typed = Variable("typed", "")
    started = Variable("started", False)
    status = Variable("status", "")
    group = Group([target, timer, typed, started, status])

    timer_widget = ui.timer(1, group.timer.inc)
    timer_widget.deactivate()

    with Col("w-full h-full items-center justify-center gap-4 p-6"):
        Label("💻 Typing Practice Test").classes("text-2xl font-bold text-center")

        # Target text area (read-only)
        TextArea(
            model=group.target,
            props="readonly",
            autogrow=True,
            clas="w-full text-lg border border-gray-400 rounded-lg p-2 bg-gray-100",
        )

        # Typing area
        typing_field = TextArea(
            model=group.typed,
            autogrow=True,
            clas="w-full text-lg border border-blue-400 rounded-lg p-2",
        )

        # Buttons and Status
        with Row().classes("gap-3 justify-center items-center"):
            SoftBtn(
                text="Start Typing",
                on_click=lambda: start_typing(timer_widget, group),
            )
            status_label = Label().bind_text_from(group.status, "value")

    return group
