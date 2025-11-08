# typing_page.py
from nicegui import ui
import random
from UI import SoftBtn, Label, INIT_THEME, TextArea, Col, Row, Div
from library.formHandler import Variable, Group

# ---------- Paragraph Texts ----------
PARAGRAPHS = [
    """Typing is one of the most essential skills in today’s digital world. 
    Whether you are writing an email, coding a program, or chatting with friends, 
    your typing speed and accuracy can make a big difference. 
    Practicing consistently helps you build rhythm and muscle memory over time.""",

    """Technology is advancing faster than ever before. 
    Artificial intelligence, automation, and robotics are reshaping industries across the world. 
    Learning programming languages like Python gives you an edge to innovate and build creative solutions.""",

    """A good typist doesn’t focus on speed alone, but on accuracy and consistency. 
    When you type carefully, your fingers learn the correct positions and patterns. 
    Over time, your speed will naturally increase without errors or strain.""",

    """Success in life often depends on small daily habits. 
    Spending just a few minutes every day improving your typing skills 
    can lead to huge productivity gains. 
    Remember, improvement is a journey, not a race.""",

    """Python is known for its simplicity and readability. 
    Developers around the globe love it because it allows them to express complex ideas in very few lines of code. 
    From data science to web development, Python can do almost everything.""",

    """Typing efficiently is not just about hitting keys faster. 
    It’s about understanding your keyboard layout, maintaining proper posture, 
    and keeping your focus steady. 
    Once you master this, typing feels natural and effortless.""",

    """Discipline is the secret ingredient behind mastery. 
    Every time you practice typing with focus, your brain builds stronger connections. 
    Those small, invisible improvements compound into powerful results over time.""",

    """The world communicates through keyboards more than any other tool. 
    Every message, document, and idea you share travels through your fingertips. 
    The better you type, the clearer and faster you connect with the world.""",
]

# ---------- UI Page ----------
async def create():
    INIT_THEME()
    target = Variable("target", random.choice(PARAGRAPHS))
    timer = Variable("timer", 0)
    typed = Variable("typed", "")
    started = Variable("started", False)
    status = Variable("status", "")
    group = Group([target, timer, typed, started, status])

    with Col("w-full h-full"):
        target_field = TextArea(model=group.target, props="readonly")
        typing_field = TextArea(model=group.typed)
        status_label = 

