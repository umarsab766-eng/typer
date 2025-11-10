# typing_dashboard_true.py
from nicegui import ui
import random
from UI import Label, INIT_THEME, TextArea, SoftBtn, Col, Row, Div, Card, Select
from library.formHandler import Variable, Group
import json

# Paragraphs organized by difficulty level
EASY_PARAGRAPHS = [
    "The quick brown fox jumps over the lazy dog. This pangram contains all letters of the alphabet.",
    "Technology has revolutionized the way we communicate, work, and live in the modern world.",
    "Practice makes perfect. The more you type, the faster and more accurate you'll become.",
    "In the digital age, typing skills are essential for productivity and effective communication.",
    "Learning to type without looking at the keyboard is a valuable skill that saves time and effort.",
]

MEDIUM_PARAGRAPHS = [
    "The quick brown fox jumps over the lazy dog. This pangram contains all letters of the alphabet and is commonly used for testing typewriters and computer keyboards. It demonstrates the full range of characters in a single sentence.",
    "Technology has revolutionized the way we communicate, work, and live in the modern world. From smartphones to artificial intelligence, innovation continues to shape our daily lives in ways we couldn't have imagined just a decade ago.",
    "Practice makes perfect. The more you type, the faster and more accurate you'll become. Regular practice helps build muscle memory and improves your overall typing speed. Consistency is key to developing this valuable skill.",
    "In the digital age, typing skills are essential for productivity and effective communication. Whether you're writing emails, coding, or creating documents, fast typing saves valuable time and allows you to focus on the content rather than the mechanics.",
    "Learning to type without looking at the keyboard is a valuable skill that saves time and effort. Touch typing allows you to focus on the content rather than the mechanics of typing. With proper technique, you can significantly increase your typing speed.",
]

HARD_PARAGRAPHS = [
    "The quick brown fox jumps over the lazy dog. This pangram contains all letters of the alphabet and is commonly used for testing typewriters and computer keyboards. It demonstrates the full range of characters in a single sentence, making it an ideal tool for evaluating typing proficiency and keyboard layout efficiency.",
    "Technology has revolutionized the way we communicate, work, and live in the modern world. From smartphones to artificial intelligence, innovation continues to shape our daily lives in ways we couldn't have imagined just a decade ago. The rapid pace of technological advancement presents both opportunities and challenges for society as we adapt to new tools and platforms.",
    "Practice makes perfect. The more you type, the faster and more accurate you'll become. Regular practice helps build muscle memory and improves your overall typing speed. Consistency is key to developing this valuable skill that will serve you well throughout your academic and professional career. Set aside dedicated time each day to hone your typing abilities.",
    "In the digital age, typing skills are essential for productivity and effective communication. Whether you're writing emails, coding, or creating documents, fast typing saves valuable time and allows you to focus on the content rather than the mechanics. Developing proficient typing skills can significantly enhance your efficiency in virtually any computer-based task.",
    "Learning to type without looking at the keyboard is a valuable skill that saves time and effort. Touch typing allows you to focus on the content rather than the mechanics of typing. With proper technique, you can significantly increase your typing speed and accuracy. Mastering this skill requires patience and consistent practice, but the long-term benefits are substantial.",
]

class NumVar(Variable):
    def __init__(self, name, value=None):
        super().__init__(name, value or 0)
    def inc(self, i=1): self.value += i
    def dec(self, i=1): self.value -= i
    def reset(self): self.value = 0

# ---------------- metrics ----------------
def compute_wpm(typed_text, elapsed_seconds):
    if elapsed_seconds <= 0: return 0
    words = len(typed_text.strip().split())
    minutes = elapsed_seconds / 60.0
    return round(words / minutes) if minutes > 0 else 0

def compute_accuracy(target_text, typed_text):
    if not typed_text: return 0
    correct = sum(1 for i, ch in enumerate(typed_text) if i < len(target_text) and ch == target_text[i])
    return round((correct / max(1, len(typed_text))) * 100, 1)

# ---------------- UI page ----------------
async def create():
    INIT_THEME()
    
    # Set beautiful gradient background
    ui.query('body').style('background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; margin: 0; font-family: "Inter", "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;')
    ui.query('.nicegui-content').classes('p-0')

    # Variables
    target = Variable('target', random.choice(EASY_PARAGRAPHS))
    duration_min = Variable('duration_min', 1)
    remaining = NumVar('remaining', 60)
    initial = NumVar('initial', 60)
    typed = Variable('typed', '')
    started = Variable('started', False)
    status = Variable('status', 'Click "Start Typing" to begin')
    highlighted_text = Variable('highlighted_text', target.value)
    last_typed_length = Variable('last_typed_length', 0)  # Track last typed length for optimization
    completed = Variable('completed', False)  # Track if paragraph is completed

    group = Group([target, duration_min, remaining, initial, typed, started, status, highlighted_text, last_typed_length, completed])

    # UI elements
    wpm_label = None
    acc_label = None
    time_label = None
    target_display = None
    typing_field = None
    start_button = None
    stop_button = None
    reset_button = None
    progress_bar = None
    duration_select = None
    completion_message = None

    # ----------------- Functions -----------------
    def format_mm_ss(sec):
        sec = max(0, int(sec))
        return f"{sec//60:02d}:{sec%60:02d}"

    def update_highlighted_text():
        """Ultra-fast highlighting using JavaScript for instant response"""
        target_text = target.value
        typed_text = typed.value
        
        # Get current and previous typed length
        current_length = len(typed_text)
        previous_length = last_typed_length.value
        
        # Update the last typed length
        last_typed_length.value = current_length
        
        # Use JSON to properly escape the text for JavaScript
        target_json = json.dumps(target_text)
        typed_json = json.dumps(typed_text)
        
        ui.run_javascript(f'''
            const targetText = {target_json};
            const typedText = {typed_json};
            const targetElement = document.querySelector('.typing-target');
            
            if (!targetElement) return;
            
            // Add CSS properties to ensure proper wrapping
            targetElement.style.wordWrap = 'break-word';
            targetElement.style.overflowWrap = 'break-word';
            targetElement.style.whiteSpace = 'normal';
            targetElement.style.display = 'block';
            targetElement.style.width = '100%';
            
            let html = '';
            const lenTarget = targetText.length;
            const lenTyped = typedText.length;
            
            for (let i = 0; i < lenTarget; i++) {{
                const char = targetText.charAt(i);
                if (i < lenTyped) {{
                    if (char === typedText.charAt(i)) {{
                        // Correct character - green highlight with animation
                        html += '<span style="background-color: #10b981; color: white; padding: 2px 4px; border-radius: 4px; margin: 0 1px; margin-bottom: 1px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); transition: all 0.2s ease; display: inline-block;">' + char + '</span>';
                    }} else {{
                        // Incorrect character - red highlight with animation
                        html += '<span style="background-color: #ef4444; color: white; padding: 2px 4px; border-radius: 4px; margin: 0 1px; margin-bottom: 1px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); transition: all 0.2s ease; display: inline-block;">' + char + '</span>';
                    }}
                }} else {{
                    // Not yet typed - subtle background
                    if(char.trim()){{
                        html += '<span style="background-color: rgba(255,255,255,0.2); color: #1f2937; padding: 2px 4px; border-radius: 4px; margin: 0 1px; margin-bottom: 1px; display: inline-block;">' + char + '</span>';
                    }} else {{
                        html += '<span style="padding: 2px 4px; border-radius: 4px; margin: 0 1px; margin-bottom: 1px; display: inline-block;">' + '</span>';
                    }}
                }}
            }}
            
            targetElement.innerHTML = html;
        ''')
        # Update progress bar
        if len(target_text) > 0:
            progress = min(1.0, current_length / len(target_text))
            progress_bar.value = progress
            
            # Check if paragraph is completed
            if current_length >= len(target_text) and started.value and not completed.value:
                completed.value = True
                finish_test(completed_early=True)

    def select_paragraph_by_duration():
        """Select paragraph based on duration - longer and more difficult for longer tests"""
        duration = int(duration_select.value)
        
        if duration <= 3:
            # Easy paragraphs for short tests
            target.value = random.choice(EASY_PARAGRAPHS)
        elif duration <= 6:
            # Medium paragraphs for medium tests
            target.value = random.choice(MEDIUM_PARAGRAPHS)
        else:
            # Hard paragraphs for long tests
            target.value = random.choice(HARD_PARAGRAPHS)
        
        highlighted_text.value = target.value
        last_typed_length.value = 0
        completed.value = False
        update_highlighted_text()

    def on_duration_change():
        try:
            val = int(duration_select.value)
        except:
            val = 1
        duration_min.value = val
        if not started.value:
            remaining.value = val*60
            initial.value = val*60
            time_label.text = format_mm_ss(remaining.value)
            # Select appropriate paragraph for the duration
            select_paragraph_by_duration()

    def start_test():
        started.value = True
        completed.value = False
        status.value = 'Typing in progress...'
        start_button.set_visibility(False)
        stop_button.set_visibility(True)
        reset_button.set_visibility(True)
        duration_select.set_visibility(False)
        typing_field.set_visibility(True)
        tick.activate()

    def stop_test():
        started.value = False
        tick.deactivate()
        start_button.set_visibility(True)
        stop_button.set_visibility(False)
        reset_button.set_visibility(True)
        duration_select.set_visibility(True)
        typing_field.set_visibility(False)
        status.value = 'Test stopped! Click "Start Typing" to try again or "Reset" to start over.'

    def finish_test(completed_early=False):
        started.value = False
        tick.deactivate()
        start_button.set_visibility(True)
        stop_button.set_visibility(False)
        reset_button.set_visibility(True)
        duration_select.set_visibility(True)
        typing_field.set_visibility(False)
        
        # Calculate elapsed time
        if completed_early:
            elapsed = initial.value - remaining.value
            status.value = '🎉 Paragraph completed! Great job!'
            completion_message.text = 'You completed the paragraph before time ran out!'
            completion_message.style('color: #10b981; font-weight: bold;')
        else:
            elapsed = initial.value
            status.value = 'Test completed!'
            completion_message.text = 'Time ran out!'
            completion_message.style('color: #ef4444; font-weight: bold;')
        
        # Show results
        typed_text = typed.value
        wpm = compute_wpm(typed_text, elapsed)
        acc = compute_accuracy(target.value, typed_text)
        
        dialog = ui.dialog()
        with dialog, Card().classes('p-1 rounded-2xl shadow-2xl bg-white max-w-md w-full'):
            ui.markdown('### 🎉 Test Complete').classes('text-center mb-6 text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-pink-600 text-2xl font-bold')
            
            with Col().classes('gap-4 w-full'):
                with Row().classes('w-full justify-between items-center p-3 bg-gray-50 rounded-lg'):
                    with Row().classes('items-center gap-2'):
                        ui.icon('schedule', size='1.5rem').classes('text-purple-600')
                        Label('Time:').classes('font-semibold text-gray-700')
                    Label(format_mm_ss(elapsed)).classes('font-mono text-gray-900 font-bold')
                
                with Row().classes('w-full justify-between items-center p-3 bg-gray-50 rounded-lg'):
                    with Row().classes('items-center gap-2'):
                        ui.icon('speed', size='1.5rem').classes('text-blue-600')
                        Label('WPM:').classes('font-semibold text-gray-700')
                    Label(str(wpm)).classes('font-mono text-gray-900 font-bold text-xl')
                
                with Row().classes('w-full justify-between items-center p-3 bg-gray-50 rounded-lg'):
                    with Row().classes('items-center gap-2'):
                        ui.icon('target', size='1.5rem').classes('text-green-600')
                        Label('Accuracy:').classes('font-semibold text-gray-700')
                    Label(f"{acc}%").classes('font-mono text-gray-900 font-bold text-xl')
                
                with Row().classes('w-full justify-between items-center p-3 bg-gray-50 rounded-lg'):
                    with Row().classes('items-center gap-2'):
                        ui.icon('text_fields', size='1.5rem').classes('text-indigo-600')
                        Label('Characters:').classes('font-semibold text-gray-700')
                    Label(str(len(typed_text))).classes('font-mono text-gray-900 font-bold')
                
                with Row().classes('w-full justify-between items-center p-3 bg-gray-50 rounded-lg'):
                    with Row().classes('items-center gap-2'):
                        ui.icon('trending_up', size='1.5rem').classes('text-pink-600')
                        Label('Progress:').classes('font-semibold text-gray-700')
                    Label(f"{min(100, round(len(typed_text) / len(target.value) * 100))}%").classes('font-mono text-gray-900 font-bold text-xl')
            
            with Row().classes('w-full justify-center gap-3 mt-6'):
                SoftBtn('Close', on_click=dialog.close, clr='error')
                SoftBtn('Try Again', on_click=lambda: (dialog.close(), reset_test()))
        
        dialog.open()

    def reset_test():
        started.value = False
        tick.deactivate()
        start_button.set_visibility(True)
        stop_button.set_visibility(False)
        reset_button.set_visibility(False)
        duration_select.set_visibility(True)
        typing_field.set_visibility(False)
        typed.value = ''
        remaining.value = int(duration_select.value)*60
        initial.value = remaining.value
        time_label.text = format_mm_ss(remaining.value)
        status.value = 'Click "Start Typing" to begin'
        last_typed_length.value = 0
        completed.value = False
        completion_message.text = ''
        select_paragraph_by_duration()
        update_live_stats()

    def update_live_stats():
        elapsed = initial.value - remaining.value
        typed_text = typed.value
        wpm = compute_wpm(typed_text, elapsed)
        acc = compute_accuracy(target.value, typed_text)
        
        wpm_label.text = str(wpm)
        acc_label.text = f"{acc}%"
        
        # Update highlighted text
        update_highlighted_text()

    def on_tick():
        if not started.value: return
        remaining.dec(1)
        time_label.text = format_mm_ss(remaining.value)
        update_live_stats()
        if remaining.value <= 0:
            finish_test()

    def on_typing_input(e):
        if started.value:
            update_live_stats()

    # --- Layout ---
    # Top Header with Stats - Glassmorphism effect
    with ui.header():
        with Row().classes('w-full items-center justify-between max-w-7xl mx-auto'):
            with Row().classes('items-center gap-8'):
                with Col().classes('items-center'):
                    wpm_label = Label('0').classes('text-3xl font-bold')
                    Label('WPM').classes('text-sm')
                
                with Col().classes('items-center'):
                    acc_label = Label('0%').classes('text-3xl font-bold')
                    Label('Accuracy').classes('text-sm')
                
                with Col().classes('items-center'):
                    time_label = Label('01:00').classes('text-3xl font-bold')
                    Label('Time').classes('text-sm')

    # Main Content Area
    with Div().classes('grid grid-cols-1 sm:grid-cols-2 gap-1'):
        # Paragraph Display - Beautiful card with shadow
        with Card().classes('w-full p-1 bg-transparent shadow-none'):
            ui.markdown('Type the text below').classes('text-gray-800 font-bold text-lg')            
            target_display = ui.html(highlighted_text.value, sanitize=False).classes(
                'w-full p-1 text-lg font-mono min-h-[150px] typing-target'
            )
        
        # Input Field - Beautiful card with shadow
        with Card().classes('w-full p-1 bg-transparent shadow-none'):
            ui.markdown('Your typing').classes('text-black font-bold text-lg')
            typing_field = TextArea(model=group.typed, autogrow=True)
            typing_field.set_visibility(False)

    # Footer with Controls - Glassmorphism effect
    with ui.footer():
        with Row().classes('w-full items-center justify-between max-w-7xl mx-auto'):
            with Col().classes('gap-2'):
                Label().bind_text_from(group.status, 'value').classes('text-white font-medium text-lg')
                completion_message = Label('').classes('text-sm text-white')
            
            with Row().classes('items-center gap-6'):
                # Duration selector - Beautiful styling
                with Row().classes('items-center gap-3 bg-white/20 backdrop-blur-sm px-4 py-2 rounded-xl'):
                    ui.icon('timer', size='1.5rem').classes('text-white')
                    duration_select = Select(
                        options=[str(i) for i in range(1,11)], 
                        value='1',
                        on_change=lambda: on_duration_change()
                    ).classes('bg-white/90 text-gray-800 rounded-lg px-3 py-1 font-medium')
                    Label('min').classes('text-white font-medium')
                
                # Progress bar - Beautiful styling
                with Col().classes('gap-1'):
                    Label('Progress').classes('text-white text-sm font-medium')
                    progress_bar = ui.linear_progress(value=0, show_value=True, color='secondary').classes('w-64 h-3 rounded-full')
                
                # Button group - Beautiful styling with hover effects
                with Row().classes('gap-3'):
                    start_button = SoftBtn('Start Typing', on_click=start_test)
                    stop_button = SoftBtn('Stop', on_click=stop_test, clr='error')
                    stop_button.set_visibility(False)
                    reset_button = SoftBtn('Reset', on_click=reset_test, clr='accent')
                    reset_button.set_visibility(False)

    # ----------------- Bindings -----------------
    tick = ui.timer(1, on_tick)
    tick.deactivate()

    typing_field.on('change', on_typing_input)

    # initialize
    remaining.value = int(duration_select.value)*60
    initial.value = remaining.value
    time_label.text = format_mm_ss(remaining.value)
    select_paragraph_by_duration()
    update_highlighted_text()

    return group