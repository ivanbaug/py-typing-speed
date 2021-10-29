import tkinter as tk
import tkinter.font as tkFont
from tkinter import Label, ttk, messagebox
from tkinter.constants import CENTER, END, GROOVE, NONE, RIDGE, WORD

import json, random, time


FONT_NAME = "Helvetica"


sample_text = "Cras varius ex ut cursus gravida. Curabitur vitae leo egestas, imperdiet nibh eget, finibus justo. Nulla et libero tortor. Integer gravida, nisl ac maximus ullamcorper, libero nisi maximus felis, eget feugiat leo orci vitae urna. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Nullam enim ante, pellentesque in pharetra nec, maximus nec orci. Aliquam erat volutpat."
my_index = 0


class Window(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.init_parent()

        # Add Style-Theme
        self.style = ttk.Style(self.parent)
        ## Import the tcl file
        self.parent.tk.call("source", "project\\themes\\forest-light.tcl")
        ## Set the theme with the theme_use method
        self.style.theme_use("forest-light")

        # Define fonts
        self.font_practice_box = tkFont.Font(family=FONT_NAME, size=16)
        self.font_title = tkFont.Font(family=FONT_NAME, size=20, weight="bold")
        self.font_info_box = tkFont.Font(family=FONT_NAME, size=12)

        # Initial Phrase
        self.word_list = self.load_words()
        self.rand_phrase, self.word_num = self.get_random_phrase(self.word_list)
        self.char_num = len(self.rand_phrase)
        self.tindex = 0
        self.welcome_str = "Welcome to the typing speed test, it will start automatically when you begin typing, glhf!"

        # Timing vars
        self.test_started = False
        self.test_ended = False
        self.t_start = time.perf_counter()
        self.t_end = 1000

        # Title
        self.title_label = ttk.Label(
            self, text="Typing Speed Test", foreground="#008a25"
        )
        self.title_label.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.title_label.configure(font=self.font_title, anchor=CENTER)

        # Create a frame for information to the user
        self.info_frame = ttk.LabelFrame(self, text="Info", padding=(10, 10))
        self.info_frame.grid(row=1, column=0, padx=10, pady=(20, 10), sticky="nsew")

        # Info Text
        self.info_text = tk.Text(
            self.info_frame,
            width=70,
            height=2,
            padx=5,
            pady=5,
            wrap=WORD,
            highlightthickness=0,
            borderwidth=0,
        )
        self.info_text.configure(font=self.font_info_box)
        self.info_text.config(spacing3=10)
        self.info_to_display = self.gen_info_text(self.welcome_str)
        self.info_text.insert("1.0", self.info_to_display)
        self.info_text.grid(row=0, column=0)

        # Create a frame for practice text
        self.practice_frame = ttk.LabelFrame(
            self, text="Practice text", padding=(10, 10)
        )
        self.practice_frame.grid(row=2, column=0, padx=10, pady=(10, 10), sticky="nsew")
        # Practice Text
        self.practice_text = tk.Text(
            self.practice_frame,
            width=50,
            height=4,
            padx=20,
            pady=15,
            wrap=WORD,
            highlightthickness=0,
            borderwidth=0,
        )
        self.practice_text.configure(font=self.font_practice_box)
        self.practice_text.config(spacing1=10, spacing2=10)
        self.practice_text.tag_configure("center", justify="center")

        self.practice_text.insert("1.0", self.rand_phrase)
        self.practice_text.tag_add("center", "1.0", "end")
        self.practice_text.grid(row=0, column=0)

        self.entry_label = ttk.Label(self, text="Type your text below:")
        self.entry_label.grid(row=3, column=0, padx=10, pady=2, sticky="nsew")
        self.entry_label.configure(font=self.font_info_box)

        # Entry
        self.entry = ttk.Entry(self, justify="center")
        self.entry.insert(0, "")
        self.entry.bind("<Key>", self.keystroke)
        self.entry.grid(row=4, column=0, padx=10, pady=(8, 10), sticky="ew")

        # Accentbutton
        self.restart_btn = ttk.Button(
            self,
            text="Reset Typing Test",
            style="Accent.TButton",
            command=self.restart_test,
        )
        self.restart_btn.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")

    def init_parent(self):
        self.parent.title("Typing speed test")
        self.parent.config(padx=20, pady=20)
        self.parent.option_add("*tearOff", False)  # This is always a good idea
        # Make the app responsive
        self.parent.columnconfigure(index=0, weight=1)
        self.parent.columnconfigure(index=1, weight=1)
        self.parent.columnconfigure(index=2, weight=1)
        self.parent.rowconfigure(index=0, weight=1)
        self.parent.rowconfigure(index=1, weight=1)
        self.parent.rowconfigure(index=2, weight=1)

    def load_words(self):
        # Thank this guy for the wordlist : https://github.com/dwyl/english-words
        with open("project\\assets\\simple_dictionary.json") as word_file:
            valid_words = json.load(word_file)
        mlist = list(valid_words.keys())
        return mlist

    def get_random_phrase(self, word_list, min_words=10, max_words=25):
        word_num = random.randint(min_words, max_words)
        words = random.choices(word_list, k=word_num)
        phrase = " ".join(words)
        # print(word_num)
        # print(phrase)
        return (phrase, word_num)

    def gen_info_text(self, line1="hello", cpm=0, wpm=0):
        return f"{line1}\nCharacters per minute: {cpm}         ||        Words per minute: {wpm}"

    def keystroke(self, key):
        # If its the first character of the test start timing
        if not self.test_started:
            self.test_started = True
            self.t_start = time.perf_counter()

        # Compare if the character is the correct one
        current_char = self.practice_text.get(self.idx_to_position(self.tindex))
        key_pressed = key.char
        self.limit_entry_chars()
        msg = f"Try the following:{current_char}"
        if current_char == key_pressed:
            self.tindex += 1
            self.highlight_char(text=self.practice_text, index=self.tindex)
            msg = "You're doing great!"

        if not self.test_ended:
            cpm = 0
            if self.tindex > 1:
                dt = time.perf_counter() - self.t_start
                cps = float(self.tindex) / dt
                cpm = int(cps * 60)

            wpm = 0
            # When the last character is typed correctly end the test
            if self.tindex == self.char_num:
                self.test_ended = True
                self.practice_text.tag_delete("hl")
                self.t_end = time.perf_counter()
                dt = self.t_end - self.t_start
                wps = float(self.word_num) / dt
                wpm = int(wps * 60)
                msg = "Well done! Your results:"

            self.info_text.delete("1.0", END)
            self.info_to_display = self.gen_info_text(msg, cpm, wpm)
            if self.test_ended:
                messagebox.showinfo("You made it!", self.info_to_display)
            self.info_text.insert("1.0", self.info_to_display)

    def idx_to_position(self, index):
        return f"1.0+{index}c"

    def highlight_char(self, text, index):
        # turn previous character to normal color
        text.tag_delete("hl")
        # highlight next char
        idx = self.idx_to_position(index)
        text.tag_add("hl", idx)
        text.tag_config("hl", background="black", foreground="white")

    def restart_test(self):
        # reset info text
        self.info_text.delete("1.0", END)
        self.info_to_display = self.gen_info_text(self.welcome_str)
        self.info_text.insert("1.0", self.info_to_display)

        # reset practice text
        self.rand_phrase, self.word_num = self.get_random_phrase(self.word_list)
        self.char_num = len(self.rand_phrase)
        self.tindex = 0
        self.practice_text.delete("1.0", END)
        self.practice_text.insert("1.0", self.rand_phrase)
        self.practice_text.tag_add("center", "1.0", "end")

        self.test_started = False
        self.test_ended = False

    def limit_entry_chars(self):
        entry_txt = self.entry.get()
        if len(entry_txt) > 14:
            self.entry.delete(0, END)
            self.entry.insert(0, entry_txt[len(entry_txt) - 14 :])


# Define a function to highlight the text
def add_highlighter(text, qty):
    text.tag_add("start", "1.11")
    text.tag_config("start", background="black", foreground="white")
    print(text.index("end"))


# window = tk.Tk()
# window.title("Typing speed test")
# window.config(padx=20, pady=20)

# window.option_add("*tearOff", False)  # This is always a good idea

# # Make the app responsive
# window.columnconfigure(index=0, weight=1)
# window.columnconfigure(index=1, weight=1)
# window.columnconfigure(index=2, weight=1)
# window.rowconfigure(index=0, weight=1)
# window.rowconfigure(index=1, weight=1)
# window.rowconfigure(index=2, weight=1)

# Create a style
# style = ttk.Style(window)
# font_practice_box = tkFont.Font(family=FONT_NAME, size=16)
# font_title = tkFont.Font(family=FONT_NAME, size=20, weight="bold")
# font_info_box = tkFont.Font(family=FONT_NAME, size=12)

# # Import the tcl file
# window.tk.call("source", "project\\themes\\forest-light.tcl")

# # Set the theme with the theme_use method
# style.theme_use("forest-light")

# # Title
# title_label = ttk.Label(window, text="Typing Speed Test", foreground="#008a25")
# title_label.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
# title_label.configure(font=font_title, anchor=CENTER)


# # Create a frame for information to the user
# info_frame = ttk.LabelFrame(window, text="Info", padding=(10, 10))
# info_frame.grid(row=1, column=0, padx=10, pady=(20, 10), sticky="nsew")

# # Info Text
# info_text = tk.Text(
#     info_frame,
#     width=70,
#     height=2,
#     padx=5,
#     pady=5,
#     wrap=WORD,
#     highlightthickness=0,
#     borderwidth=0,
# )
# info_text.configure(font=font_info_box)
# info_text.config(spacing3=10)
# info_to_display = gen_info_text(
#     "Welcome to the typing speed test, it will start automatically when you begin typing, glhf!"
# )
# info_text.insert("1.0", info_to_display)
# info_text.grid(row=0, column=0)


# # Create a frame for practice text
# practice_frame = ttk.LabelFrame(window, text="Practice text", padding=(10, 10))
# practice_frame.grid(row=2, column=0, padx=10, pady=(10, 10), sticky="nsew")
# # Practice Text
# practice_text = tk.Text(
#     practice_frame,
#     width=50,
#     height=4,
#     padx=20,
#     pady=15,
#     wrap=WORD,
#     highlightthickness=0,
#     borderwidth=0,
# )
# practice_text.configure(font=font_practice_box)
# practice_text.config(spacing1=10, spacing2=10)
# practice_text.tag_configure("center", justify="center")
# rand_phrase = get_random_phrase(load_words())
# practice_text.insert("1.0", rand_phrase)
# practice_text.tag_add("center", "1.0", "end")
# practice_text.grid(row=0, column=0)

# entry_label = ttk.Label(window, text="Type your text below:")
# entry_label.grid(row=3, column=0, padx=10, pady=2, sticky="nsew")
# entry_label.configure(font=font_info_box)
# # Entry
# entry = ttk.Entry(window)
# entry.insert(0, "")
# entry.bind("<Key>", lambda event, arg=(0): keystroke(practice_text))
# entry.grid(row=4, column=0, padx=10, pady=(8, 10), sticky="ew")

# # Accentbutton
# accentbutton = ttk.Button(
#     window,
#     text="Reset Typing Test",
#     style="Accent.TButton",
#     command=lambda: add_highlighter(practice_text, 3),
# )
# accentbutton.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")


# window.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    Window(root).pack(fill="both", expand=True)
    root.mainloop()
# Notes:
# How to highlight text in a tkinter Text widget?  https://www.tutorialspoint.com/how-to-highlight-text-in-a-tkinter-text-widget

# @ViníciusGabriel: so, just the border? I don't have a system I can try it out on (linux ttk widgets don't look much different
#  from tkinter widgets), but you can probably get the look you want just by packing a borderless text widget inside a ttk.Entry
# widget so that you see the entry widget border.

# https://www.youtube.com/watch?v=qM3sXJhFGiA
