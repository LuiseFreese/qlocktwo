from datetime import datetime
import tkinter as tk
import math


phrases = [
    ("IT'S", 0), ("JUST AFTER", 30), ("NEARLY", 60),
    ("FIVE", 90), ("TEN", 120), ("A QUARTER", 150),
    ("HALF", 180), ("TO", 210), ("PAST", 240),
    ("MINUTES", 270), ("ALMOST", 300), ("A LITTLE", 330)
]

# Function to determine which phrases to highlight based on time
def get_highlighted_phrases():
    now = datetime.now()
    hour = now.hour % 12 or 12 
    minute = now.minute

    # Determine next hour for "TO" cases
    next_hour = (hour + 1) % 12 or 12

    # Highlight phrases dynamically
    if minute < 5:
        return ["IT'S", "ALMOST", f"{hour} O'CLOCK"]
    elif minute < 10:
        return ["IT'S", "JUST AFTER", "FIVE", "PAST", f"{hour}"]
    elif minute < 15:
        return ["IT'S", "TEN", "PAST", f"{hour}"]
    elif minute < 20:
        return ["IT'S", "A LITTLE", "AFTER", "A QUARTER", "PAST", f"{hour}"]
    elif minute < 25:
        return ["IT'S", "NEARLY", "TWENTY", "PAST", f"{hour}"]
    elif minute < 30:
        return ["IT'S", "HALF", "PAST", f"{hour}"]
    elif minute < 35:
        return ["IT'S", "JUST AFTER", "HALF", "PAST", f"{hour}"]
    elif minute < 40:
        return ["IT'S", "A LITTLE", "BEFORE", "TWENTY", "TO", f"{next_hour}"]
    elif minute < 45:
        return ["IT'S", "A QUARTER", "TO", f"{next_hour}"]
    elif minute < 50:
        return ["IT'S", "TEN", "TO", f"{next_hour}"]
    elif minute < 55:
        return ["IT'S", "FIVE", "TO", f"{next_hour}"]
    elif minute < 60:
        return ["IT'S", "ALMOST", f"{next_hour} O'CLOCK"]

# Create the GUI
def create_word_clock():
    root = tk.Tk()
    root.title("Radial Word Clock")
    root.configure(bg="black")

    canvas = tk.Canvas(root, width=400, height=450, bg="black", highlightthickness=0)
    canvas.pack()

    # Draw the phrases in a radial layout
    phrase_labels = []
    for phrase, angle in phrases:
        x = 200 + 150 * math.cos(math.radians(angle - 90))
        y = 200 + 150 * math.sin(math.radians(angle - 90))
        label = canvas.create_text(
            x, y,
            text=phrase,
            font=("Helvetica", 14),
            fill="gray"
        )
        phrase_labels.append((label, phrase))


    hour_label = canvas.create_text(
        200, 200,
        text="",
        font=("Helvetica", 24, "bold"),
        fill="#ff69b4"
    )

   
    signature = canvas.create_text(
        200, 430,
        text="Made with <3 by Luise",
        font=("Helvetica", 10),
        fill="#888888"
    )

    # Function to update the highlighted phrases
    def refresh():
        highlighted_phrases = get_highlighted_phrases()
        for label, phrase in phrase_labels:
            if phrase in highlighted_phrases:
                canvas.itemconfig(label, fill="#ff69b4", font=("Helvetica", 14, "bold"))
            else:
                canvas.itemconfig(label, fill="gray", font=("Helvetica", 14))

        # Highlight the current hour in the center
        current_hour = next(
            (phrase for phrase in highlighted_phrases if phrase.endswith("O'CLOCK") or phrase.isdigit()),
            ""
        )
        canvas.itemconfig(hour_label, text=current_hour)

        root.after(1000, refresh) 

    refresh()
    root.mainloop()


if __name__ == "__main__":
    create_word_clock()
