from datetime import datetime, timedelta
import tkinter as tk
import math
import pytz

# Define time zones
PT = pytz.timezone("US/Pacific")
GMT = pytz.timezone("GMT")

# Manually calculate IST as GMT + 5:30
def get_ist_from_gmt(gmt_time):
    return gmt_time + timedelta(hours=5, minutes=30)

# Helper function to determine AM or PM
def get_am_pm(hour_24, invert=False):
    if invert:  # Flip AM/PM specifically for IST
        return "AM" if hour_24 >= 12 else "PM"
    else:
        if hour_24 == 0:  # Midnight
            return "AM"
        elif hour_24 < 12:
            return "AM"
        elif hour_24 == 12:  # Noon
            return "PM"
        else:
            return "PM"

# Helper function to format time
def format_time(current_time, invert_am_pm=False):
    hour_24 = current_time.hour
    hour_12 = hour_24 % 12 or 12  # Convert to 12-hour format
    minute = current_time.minute
    am_pm = get_am_pm(hour_24, invert=invert_am_pm)
    return f"{hour_12}:{minute:02d} {am_pm}"

# Determine highlighted phrases based on time
def get_highlighted_phrases(current_time):
    minute = current_time.minute
    hour_12 = current_time.hour % 12 or 12
    phrases = ["IT'S"]

    if 0 <= minute < 5:
        phrases.append(f"{hour_12} O'CLOCK")
    elif 5 <= minute < 10:
        phrases.extend(["FIVE", "PAST"])
    elif 10 <= minute < 15:
        phrases.extend(["TEN", "PAST"])
    elif 15 <= minute < 20:
        phrases.extend(["A QUARTER", "PAST"])
    elif 20 <= minute < 25:
        phrases.extend(["TWENTY", "PAST"])
    elif 25 <= minute < 30:
        phrases.extend(["TWENTY", "FIVE", "PAST"])
    elif 30 <= minute < 35:
        phrases.extend(["HALF", "PAST"])
    elif 35 <= minute < 40:
        next_hour = (hour_12 + 1) % 12 or 12
        phrases.extend(["TWENTY", "FIVE", "TO", f"{next_hour}"])
    elif 40 <= minute < 45:
        next_hour = (hour_12 + 1) % 12 or 12
        phrases.extend(["TWENTY", "TO", f"{next_hour}"])
    elif 45 <= minute < 50:
        next_hour = (hour_12 + 1) % 12 or 12
        phrases.extend(["A QUARTER", "TO", f"{next_hour}"])
    elif 50 <= minute < 55:
        next_hour = (hour_12 + 1) % 12 or 12
        phrases.extend(["TEN", "TO", f"{next_hour}"])
    elif 55 <= minute < 60:
        next_hour = (hour_12 + 1) % 12 or 12
        phrases.extend(["FIVE", "TO", f"{next_hour}"])

    return phrases

# Debugging function
def debug_current_times(pt_time, gmt_time, ist_time):
    print("Debugging Current Times:")
    print(f"PT (24-hour): {pt_time.hour}:{pt_time.minute:02d}, Converted: {format_time(pt_time)}")
    print(f"GMT (24-hour): {gmt_time.hour}:{gmt_time.minute:02d}, Converted: {format_time(gmt_time)}")
    print(f"IST (24-hour): {ist_time.hour}:{ist_time.minute:02d}, Converted: {format_time(ist_time, invert_am_pm=True)}")
    print("-" * 30)

# Create the GUI
def create_word_clock():
    root = tk.Tk()
    root.title("Word Clock with AM/PM Flip for IST")
    root.configure(bg="black")

    canvas = tk.Canvas(root, width=1200, height=600, bg="black", highlightthickness=0)
    canvas.pack()

    # Define radial layouts for PT, GMT, IST
    def create_clock(x_center, y_center, time_title, city):
        labels = []
        for phrase, angle in [
            ("IT'S", 0), ("JUST AFTER", 30), ("NEARLY", 60),
            ("FIVE", 90), ("TEN", 120), ("A QUARTER", 150),
            ("HALF", 180), ("TO", 210), ("PAST", 240),
            ("MINUTES", 270), ("ALMOST", 300), ("A LITTLE", 330)
        ]:
            x = x_center + 150 * math.cos(math.radians(angle - 90))
            y = y_center + 150 * math.sin(math.radians(angle - 90))
            label = canvas.create_text(
                x, y,
                text=phrase,
                font=("Helvetica", 14),
                fill="gray"
            )
            labels.append((label, phrase))

        hour_label = canvas.create_text(x_center, y_center, text="", font=("Helvetica", 24, "bold"), fill="#ff69b4")
        am_pm_label = canvas.create_text(x_center, y_center + 50, text="", font=("Helvetica", 16), fill="#ff69b4")
        time_zone_label = canvas.create_text(x_center, y_center + 200, text=time_title, font=("Helvetica", 12, "italic"), fill="#888888")
        city_label = canvas.create_text(x_center, y_center + 230, text=city, font=("Helvetica", 10), fill="#888888")

        return labels, hour_label, am_pm_label

    # Create PT, GMT, IST clocks
    pt_labels, pt_hour_label, pt_am_pm_label = create_clock(200, 200, "Pacific Time (PT)", "Los Angeles")
    gmt_labels, gmt_hour_label, gmt_am_pm_label = create_clock(600, 200, "Greenwich Mean Time (GMT)", "London")
    ist_labels, ist_hour_label, ist_am_pm_label = create_clock(1000, 200, "Indian Standard Time (IST)", "Mumbai")

    def refresh():
        # Get current times
        pt_time = datetime.now(PT)
        gmt_time = datetime.now(GMT)
        ist_time = get_ist_from_gmt(gmt_time)  # Manually calculate IST from GMT

        # Debug output
        debug_current_times(pt_time, gmt_time, ist_time)

        # Update clocks dynamically
        update_time_zone(pt_time, pt_labels, pt_hour_label, pt_am_pm_label)
        update_time_zone(gmt_time, gmt_labels, gmt_hour_label, gmt_am_pm_label)
        update_time_zone(ist_time, ist_labels, ist_hour_label, ist_am_pm_label, invert_am_pm=True)

        root.after(1000, refresh)

    def update_time_zone(current_time, labels, hour_label, am_pm_label, invert_am_pm=False):
        # Highlight phrases dynamically
        highlighted_phrases = get_highlighted_phrases(current_time)
        hour_12 = current_time.hour % 12 or 12
        am_pm = get_am_pm(current_time.hour, invert=invert_am_pm)

        canvas.itemconfig(hour_label, text=f"{hour_12} O'CLOCK")
        canvas.itemconfig(am_pm_label, text=am_pm)

        for label, phrase in labels:
            if phrase in highlighted_phrases:
                canvas.itemconfig(label, fill="#ff69b4", font=("Helvetica", 14, "bold"))
            else:
                canvas.itemconfig(label, fill="gray", font=("Helvetica", 14))

    refresh()
    root.mainloop()

# Main program
if __name__ == "__main__":
    create_word_clock()
