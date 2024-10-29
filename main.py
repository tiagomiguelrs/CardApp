from tkinter import *
import pandas as pd
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
BACK_CARD_RGB = "#90C0AD"
LANGUAGE_FONT = ("Arial", 40, "italic")
WORD_FONT = ("Arial", 60, "bold")
WAITING_TIME = 2000

# Empty containers -----------------------------------------------------------------------------------------------------
""
known_word_indexes = []
known_word_dict = {}
unknown_word_indexes = []
unknown_word_dict = {}

# Pandas read and dump into dictionary ---------------------------------------------------------------------------------
words_df = pd.read_csv("data/french_words.csv")
# print(words_df)

words_dict = {index:{"french":row.French, "english":row.English} for (index, row) in words_df.iterrows()}
# print(words_dict)

index_list = [i for i in range(len(words_dict))]
# print(words_list)

# Save back into data --------------------------------------------------------------------------------------------------
def save_to_csv(knew: str):
    if knew == "known":
        l = known_word_indexes
        name = "known_words"
    elif knew == "unknown":
        l = unknown_word_indexes
        name = "unknown_words"
    # save_dict = {words_dict[index]["french"]:words_dict[index]["english"] for index in l}
    save_dict = {
        "French":[words_dict[index]["french"] for index in l],
        "English":[words_dict[index]["english"] for index in l]
    }
    df = pd.DataFrame.from_dict(data=save_dict)
    df.to_csv(f"data/{name}.csv", index=False)


# UX -------------------------------------------------------------------------------------------------------------------
# Reveal english translation -------------------------------------------------------------------------------------------
def reveal_translation():
    global dict_index, card
    card_c.itemconfig(card, image=green_card_img)
    en_text = words_dict[dict_index]["english"]
    card_c.itemconfig(card_title, text="English", fill="white")
    card_c.itemconfig(card_word, text=en_text, fill="white")
    enable_buttons()


# Pick french word -----------------------------------------------------------------------------------------------------
def pick_french_word():
    global dict_index, card
    card_c.itemconfig(card, image=white_card_img)
    fr_text = words_dict[dict_index]["french"]
    card_c.itemconfig(card_title, text="French", fill="black")
    card_c.itemconfig(card_word, text=fr_text, fill="black")


# Set word -------------------------------------------------------------------------------------------------------------
def set_word():
    global dict_index
    try:
        dict_index = choice(index_list)    # The number chosen here relates to the words_dict index.
    except IndexError:
        card_c.itemconfig(card_title, text="")
        card_c.itemconfig(card_word, text="")
        card_c.coords(card_title, 400, 250)
        card_c.itemconfig(card_title, text="You have completed\nthe flash cards!")
        disable_buttons()
    else:
        pick_french_word()
        window.after(ms=WAITING_TIME, func=reveal_translation)


# right button action --------------------------------------------------------------------------------------------------
def right_button_action():
    global dict_index
    disable_buttons()
    add_to_list(known_word_indexes)


# wrong button action --------------------------------------------------------------------------------------------------
def wrong_button_action():
    global dict_index
    disable_buttons()
    add_to_list(unknown_word_indexes)


# Choose which list function -------------------------------------------------------------------------------------------
def add_to_list(l):
    try:
        l.append(dict_index)
    except NameError:
        set_word()
        card_c.itemconfig(card_intro, text="")
    else:
        index_list.remove(dict_index)
        set_word()


# Buttons' state -------------------------------------------------------------------------------------------------------
def disable_buttons():
    right_b.config(state="disabled")
    wrong_b.config(state="disabled")


def enable_buttons():
    right_b.config(state="normal")
    wrong_b.config(state="normal")


# UI -------------------------------------------------------------------------------------------------------------------
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Card canvas
white_card_img = PhotoImage(file="images/card_front.png")
green_card_img = PhotoImage(file="images/card_back.png")

card_c = Canvas(master=window, highlightthickness=0, width=800, height=526, bg=BACKGROUND_COLOR)
card = card_c.create_image(400, 263, image=white_card_img)
card_title = card_c.create_text(250, 140, text="", fill="black", font=LANGUAGE_FONT)
card_word = card_c.create_text(300, 300, text="", fill="black", font=WORD_FONT)
card_intro = card_c.create_text(400, 200, text="Press any button to start", fill="black", font=LANGUAGE_FONT)
card_c.grid(column=0, row=0, columnspan=2)

# Wrong button
wrong_b = Button(master=window, highlightthickness=0, command=wrong_button_action)
wrong_img = PhotoImage(file="images/wrong.png")
wrong_b.config(image=wrong_img, bd=0)
wrong_b.grid(column=0, row=1)

# Right button
right_b = Button(master=window, highlightthickness=0, command=right_button_action)
right_img = PhotoImage(file="images/right.png")
right_b.config(image=right_img, bd=0)
right_b.grid(column=1, row=1)

window.mainloop()

save_to_csv("known")
save_to_csv("unknown")