import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter.constants import GROOVE, RIDGE, WORD

import json, random


FONT_NAME = "Helvetica"


sample_text = "Cras varius ex ut cursus gravida. Curabitur vitae leo egestas, imperdiet nibh eget, finibus justo. Nulla et libero tortor. Integer gravida, nisl ac maximus ullamcorper, libero nisi maximus felis, eget feugiat leo orci vitae urna. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nullam enim ante, pellentesque in pharetra nec, maximus nec orci. Aliquam erat volutpat."


def load_words():
    with open("project\\assets\\simple_dictionary.json") as word_file:
        valid_words = json.load(word_file)
    mlist = list(valid_words.keys())
    return mlist


def get_random_phrase(word_list, min_words=20, max_words=30):
    words = random.choices(word_list, k=random.randint(min_words, max_words))
    phrase = " ".join(words)
    print(phrase)
    return phrase


window = tk.Tk()
window.title("Typing speed test")
window.config(padx=20, pady=20)

window.option_add("*tearOff", False)  # This is always a good idea

# Make the app responsive
# window.columnconfigure(index=0, weight=1)
# window.columnconfigure(index=1, weight=1)
# window.columnconfigure(index=2, weight=1)
window.rowconfigure(index=0, weight=1)
window.rowconfigure(index=1, weight=1)
window.rowconfigure(index=2, weight=1)

# Create a style
style = ttk.Style(window)

font_big_box = tkFont.Font(family=FONT_NAME, size=16)

# Import the tcl file
window.tk.call("source", "project\\themes\\forest-light.tcl")

# Set the theme with the theme_use method
style.theme_use("forest-light")

practice_text = tk.Text(
    window,
    width=50,
    height=5,
    padx=20,
    pady=15,
    wrap=WORD,
    relief=GROOVE,
)
practice_text.configure(font=font_big_box)
practice_text.config(spacing1=10, spacing2=10)
practice_text.tag_configure("center", justify="center")
rand_phrase = get_random_phrase(load_words())
practice_text.insert("1.0", rand_phrase)
practice_text.tag_add("center", "1.0", "end")
practice_text.grid(row=0, column=0)


# Entry
entry = ttk.Entry(window)
entry.insert(0, "")
entry.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="ew")
# ###
# # Panedwindow
# paned = ttk.PanedWindow(window)
# paned.grid(row=0, column=0, pady=(25, 5), sticky="nsew", rowspan=3)

# # Pane #1
# pane_1 = ttk.Frame(paned, borderwidth=1)
# paned.add(pane_1, weight=1)
# # # Create a Frame for the Text view
# # treeFrame = ttk.Frame(pane_1)
# # treeFrame.pack(expand=True, fill="both", padx=5, pady=5)
# # Separator
# # separator = ttk.Separator(window)
# # separator.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="ew")

# greeting = tk.Label(pane_1, text="Hello, Tkinter", bg="blue")
# greeting.pack()
# # Pane #2
# pane_2 = ttk.Frame(paned, borderwidth=1)
# paned.add(pane_2, weight=1)

# greeting2 = tk.Label(pane_2, text="Hello, Tkinter", bg="green")
# greeting2.pack()

window.mainloop()


# Notes:
# How to highlight text in a tkinter Text widget?  https://www.tutorialspoint.com/how-to-highlight-text-in-a-tkinter-text-widget

# @ViníciusGabriel: so, just the border? I don't have a system I can try it out on (linux ttk widgets don't look much different
#  from tkinter widgets), but you can probably get the look you want just by packing a borderless text widget inside a ttk.Entry
# widget so that you see the entry widget border.

# https://www.youtube.com/watch?v=qM3sXJhFGiA
