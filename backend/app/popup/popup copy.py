# Feedback popup UI
import tkinter as tk
from tkinter import messagebox
import requests
import threading
import time
import random
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")
FEEDBACK_INTERVAL = 10
QUESTION_TYPE_CYCLE = ["comment", "emoji", "radio"]
popup_active = False
current_question_type_index = 0

# --- API Interaction Functions ---
def fetch_random_question(question_type):
    try:
        response = requests.get(f"{API_URL}/questions/{question_type}")
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        questions = response.json()
        return random.choice(questions) if questions else None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching question: {e}")
        return None

def submit_feedback(question_id, user_id, response_text=None, response_emoji=None, response_radio=None):
    try:
        payload = {
            "question_id": question_id,
            "user_id": user_id,
            "response_text": response_text,
            "response_emoji": response_emoji,
            "response_radio": response_radio
        }
        response = requests.post(f"{API_URL}/responses/", json=payload)
        response.raise_for_status()
        print("✅ Feedback submitted successfully!")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending feedback: {e}")


# --- Popup Window Functions ---
def show_popup():
    global popup_active, current_question_type_index, selected_emoji_value, selected_radio_value

    if popup_active:
        return

    question_type = QUESTION_TYPE_CYCLE[current_question_type_index]
    current_question_type_index = (current_question_type_index + 1) % len(QUESTION_TYPE_CYCLE)

    question = fetch_random_question(question_type)
    if not question:
        return

    popup_active = True
    popup = tk.Tk()
    popup.title("PulseBot Feedback")
    tk.Label(popup, text=question["question_text"], wraplength=400, font=("Arial", 14)).pack(padx=10, pady=10)

    # --- Question Type Handling ---
    if question["question_type"] == "comment":
        input_box = tk.Text(popup, height=5, width=50)
        input_box.pack(padx=10, pady=10)

        def submit_comment():
            response_text = input_box.get("1.0", tk.END).strip()
            if response_text:
                submit_feedback(question["question_id"], None, response_text=response_text)
                close_popup()

        tk.Button(popup, text="Submit", command=submit_comment).pack(pady=10)

    elif question["question_type"] == "emoji":
        emoji_frame = tk.Frame(popup)
        emoji_frame.pack(padx=10, pady=10)

        emoji_mapping = {"1": "😠", "2": "🙁", "3": "😐", "4": "🙂", "5": "😀"}
        selected_emoji_value = ""  # Reset for each popup

        for value, emoji_label in emoji_mapping.items():
            tk.Radiobutton(
                emoji_frame, text=emoji_label, value=value,
                indicatoron=0, width=5, height=2, font=("Arial", 20),
                command=lambda v=value: setattr(sys.modules[__name__], 'selected_emoji_value', v)
            ).pack(side="left", padx=10)

        def submit_emoji():
            if selected_emoji_value:
                submit_feedback(question["question_id"], None, response_emoji=int(selected_emoji_value))
                close_popup()
            else:
                messagebox.showwarning("Input Required", "Please select an emoji.")

        tk.Button(popup, text="Submit", command=submit_emoji).pack(pady=10)

    elif question["question_type"] == "radio":
        radio_frame = tk.Frame(popup)
        radio_frame.pack(padx=10, pady=10)

        options = ["Yes", "No", "Maybe"]
        selected_radio_value = ""  # Reset for each popup

        for option in options:
            tk.Radiobutton(
                radio_frame, text=option, value=option,
                indicatoron=0, width=10, height=2, font=("Arial", 14),
                command=lambda v=option: setattr(sys.modules[__name__], 'selected_radio_value', v)
            ).pack(side="left", padx=10)

        def submit_radio():
            if selected_radio_value:
                submit_feedback(question["question_id"], None, response_radio=selected_radio_value)
                close_popup()
            else:
                messagebox.showwarning("Input Required", "Please select an option.")

        tk.Button(popup, text="Submit", command=submit_radio).pack(pady=10)

    # --- Popup Closing ---
    def close_popup():
        global popup_active
        popup_active = False
        popup.destroy()
        threading.Thread(target=start_feedback_timer, daemon=True).start()

    popup.mainloop()


# --- Timer and Main Loop ---
def start_feedback_timer():
    time.sleep(FEEDBACK_INTERVAL)
    if not popup_active:
        root.event_generate("<<ShowPopup>>", when="tail")


root = tk.Tk()
root.withdraw()
root.bind("<<ShowPopup>>", lambda e: show_popup())

threading.Thread(target=start_feedback_timer, daemon=True).start()

print(f"PulseBot popup running (interval starts after submission: {FEEDBACK_INTERVAL} seconds)...")
root.mainloop()