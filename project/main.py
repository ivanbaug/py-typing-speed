import tkinter as tk
from tkinter import Label, ttk
import tkinter.font as tkFont
from tkinter.constants import CENTER, GROOVE, NONE, RIDGE, WORD

import json, random


FONT_NAME = "Helvetica"


sample_text = "Cras varius ex ut cursus gravida. Curabitur vitae leo egestas, imperdiet nibh eget, finibus justo. Nulla et libero tortor. Integer gravida, nisl ac maximus ullamcorper, libero nisi maximus felis, eget feugiat leo orci vitae urna. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nullam enim ante, pellentesque in pharetra nec, maximus nec orci. Aliquam erat volutpat."
my_index = 0


class Window(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent


def load_words():
    with open("project\\assets\\simple_dictionary.json") as word_file:
        valid_words = json.load(word_file)
    mlist = list(valid_words.keys())
    return mlist


def get_random_phrase(word_list, min_words=15, max_words=25):
    words = random.choices(word_list, k=random.randint(min_words, max_words))
    phrase = " ".join(words)
    print(phrase)
    return phrase


# Define a function to highlight the text
def add_highlighter(text, qty):
    text.tag_add("start", "1.11")
    text.tag_config("start", background="black", foreground="white")
    print(text.index("end"))


def highlight_char(text, index):
    # Convert to a position
    idx = f"1.0+{index}c"

    text.tag_add("hl", index)
    text.tag_config("hl", background="black", foreground="white")


def gen_info_text(line1="hello", cpm=0, wpm=0):
    return f"{line1}\nCharacters per minute: {cpm}         ||        Words per minute: {wpm}"


def keystroke(text):
    # print(self.char)
    global my_index
    my_index += 1
    highlight_char(text=text, index=my_index)


window = tk.Tk()
window.title("Typing speed test")
window.config(padx=20, pady=20)

window.option_add("*tearOff", False)  # This is always a good idea

# Make the app responsive
window.columnconfigure(index=0, weight=1)
window.columnconfigure(index=1, weight=1)
window.columnconfigure(index=2, weight=1)
window.rowconfigure(index=0, weight=1)
window.rowconfigure(index=1, weight=1)
window.rowconfigure(index=2, weight=1)

# Create a style
style = ttk.Style(window)
font_practice_box = tkFont.Font(family=FONT_NAME, size=16)
font_title = tkFont.Font(family=FONT_NAME, size=20, weight="bold")
font_info_box = tkFont.Font(family=FONT_NAME, size=12)

# Import the tcl file
window.tk.call("source", "project\\themes\\forest-light.tcl")

# Set the theme with the theme_use method
style.theme_use("forest-light")

# Title
title_label = ttk.Label(window, text="Typing Speed Test", foreground="#008a25")
title_label.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
title_label.configure(font=font_title, anchor=CENTER)


# Create a frame for information to the user
info_frame = ttk.LabelFrame(window, text="Info", padding=(10, 10))
info_frame.grid(row=1, column=0, padx=10, pady=(20, 10), sticky="nsew")

# Info Text
info_text = tk.Text(
    info_frame,
    width=70,
    height=2,
    padx=5,
    pady=5,
    wrap=WORD,
    highlightthickness=0,
    borderwidth=0,
)
info_text.configure(font=font_info_box)
info_text.config(spacing3=10)
info_to_display = gen_info_text(
    "Welcome to the typing speed test, it will start automatically when you begin typing, glhf!"
)
info_text.insert("1.0", info_to_display)
info_text.grid(row=0, column=0)


# Create a frame for practice text
practice_frame = ttk.LabelFrame(window, text="Practice text", padding=(10, 10))
practice_frame.grid(row=2, column=0, padx=10, pady=(10, 10), sticky="nsew")
# Practice Text
practice_text = tk.Text(
    practice_frame,
    width=50,
    height=4,
    padx=20,
    pady=15,
    wrap=WORD,
    highlightthickness=0,
    borderwidth=0,
)
practice_text.configure(font=font_practice_box)
practice_text.config(spacing1=10, spacing2=10)
practice_text.tag_configure("center", justify="center")
rand_phrase = get_random_phrase(load_words())
practice_text.insert("1.0", rand_phrase)
practice_text.tag_add("center", "1.0", "end")
practice_text.grid(row=0, column=0)

entry_label = ttk.Label(window, text="Type your text below:")
entry_label.grid(row=3, column=0, padx=10, pady=2, sticky="nsew")
entry_label.configure(font=font_info_box)
# Entry
entry = ttk.Entry(window)
entry.insert(0, "")
entry.bind("<Key>", lambda event, arg=(0): keystroke(practice_text))
entry.grid(row=4, column=0, padx=10, pady=(8, 10), sticky="ew")

# Accentbutton
accentbutton = ttk.Button(
    window,
    text="Reset Typing Test",
    style="Accent.TButton",
    command=lambda: add_highlighter(practice_text, 3),
)
accentbutton.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")


window.mainloop()

# if __name__ == "__main__":
#     root = tk.Tk()
#     Window(root).pack(side="top", fill="both", expand=True)
#     root.mainloop()
# Notes:
# How to highlight text in a tkinter Text widget?  https://www.tutorialspoint.com/how-to-highlight-text-in-a-tkinter-text-widget

# @ViníciusGabriel: so, just the border? I don't have a system I can try it out on (linux ttk widgets don't look much different
#  from tkinter widgets), but you can probably get the look you want just by packing a borderless text widget inside a ttk.Entry
# widget so that you see the entry widget border.

# https://www.youtube.com/watch?v=qM3sXJhFGiA
