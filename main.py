from tkinter import *
import pandas
import random
import time

BACKGROUND_COLOR = "#B1DDC6"
GRAY = "#4D4D4D"
BLACK = "#000000"
WHITE = "#FFFFFF"
current_card = {}

# Pandas
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def replace_canvas_word(word):
    canvas.itemconfig(word_text, text=word)


def next_card():
    global current_card
    current_card = random.choice(to_learn)
    replace_canvas_word(current_card["French"])


def click_right_button():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()
    reset_card()
    window.after(3000, func=flip_card)


def click_wrong_button():
    next_card()
    reset_card()
    window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(front_card, image=capstone_card_back)
    canvas.itemconfig(language_text, text="English", fill=WHITE)
    canvas.itemconfig(word_text, text=current_card["English"], fill=WHITE)


def reset_card():
    canvas.itemconfig(front_card, image=capstone_card_front)
    canvas.itemconfig(language_text, text="French", fill=BLACK)
    canvas.itemconfig(word_text, fill=BLACK)


# Window
window = Tk()
window.title("Capstone")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Flashcard Images
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
capstone_card_front = PhotoImage(file="images/card_front.png")
capstone_card_back = PhotoImage(file="images/card_back.png")
front_card = canvas.create_image(400, 263, image=capstone_card_front)
canvas.grid(column=0, row=0, columnspan=2)
language_text = canvas.create_text(400, 150, text="French", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 300, text="", font=("Ariel", 55, "bold"))

# Buttons
right_button_image = PhotoImage(file="images/right.png")
wrong_button_image = PhotoImage(file="images/wrong.png")
right_button = Button(image=right_button_image, highlightthickness=0, borderwidth=0, bd=0,
                      activebackground=BACKGROUND_COLOR, command=click_right_button)
wrong_button = Button(image=wrong_button_image, highlightthickness=0, borderwidth=0, bd=0,
                      activebackground=BACKGROUND_COLOR, command=click_wrong_button)
right_button.grid(row=1, column=0)
wrong_button.grid(row=1, column=1)

next_card()
window.after(5000, func=flip_card)

window.mainloop()
