import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Word bank with hints for each word
words = {
    "1": [("cat", "It's an animal"), ("dog", "It's man's best friend"), ("sun", "It shines bright in the sky"), ("tree", "It grows leaves"), ("ball", "It's round and fun to play with")],
    "2": [("python", "It's a programming language"), ("planet", "It orbits a star"), ("school", "A place of learning"), ("guitar", "A musical instrument"), ("basket", "You can carry fruits in it")],
    "3": [("hangman", "The name of this game"), ("elephant", "The largest land animal"), ("challenge", "A test of skill"), ("developer", "One who writes code"), ("university", "Higher education institute")]
}

# --- GUI SETUP ---
root = tk.Tk()
root.title("Hangman Game")
root.configure(bg="white")

current_level = None
word = ""
hint = ""
word_display = []
attempts = 0
guessed_letters = []
correct_guesses = 0
wrong_guesses = 0

# Load images
header_img = Image.open("header.png").resize((600, 100))
header_photo = ImageTk.PhotoImage(header_img)
header_label = tk.Label(root, image=header_photo, bg="white")
header_label.pack()

footer_img = Image.open("footer.png").resize((600, 100))
footer_photo = ImageTk.PhotoImage(footer_img)
footer_label = tk.Label(root, image=footer_photo, bg="white")
footer_label.pack(side="bottom")

final_img = Image.open("hangman.png").resize((200, 200))
final_photo = ImageTk.PhotoImage(final_img)

congrats_img = Image.open("congrats.gif").resize((200, 200))
congrats_photo = ImageTk.PhotoImage(congrats_img)

# Title Label
title_label = tk.Label(root, text="Hangman Game", font=("Arial", 32, "bold"), fg="white", bg="#2196f3", pady=10)
title_label.pack(fill="x")

# Frames
level_frame = tk.Frame(root, bg="white")
game_frame = tk.Frame(root, bg="white")
result_frame = tk.Frame(root, bg="white")

# Hint label
hint_label = tk.Label(game_frame, text="", font=("Arial", 14, "italic"), fg="#FF5733", bg="white")
hint_label.pack(pady=(10, 0))

# --- LEVEL SELECTION ---
def show_level_selection():
    game_frame.pack_forget()
    result_frame.pack_forget()
    level_frame.pack(pady=50)

def start_game(level):
    global word, word_display, attempts, guessed_letters, correct_guesses, wrong_guesses, current_level, hint
    current_level = level
    selected = random.choice(words[level])
    word, hint = selected
    word_display = ["_"] * len(word)
    attempts = {"1": 8, "2": 6, "3": 4}[level]
    guessed_letters = []
    correct_guesses = 0
    wrong_guesses = 0

    hint_label.config(text=f"💡 Hint: {hint}")
    show_game_ui()

def restart_game():
    show_level_selection()

def exit_game():
    root.destroy()

# --- GAME UI ---
def show_game_ui():
    level_frame.pack_forget()
    result_frame.pack_forget()
    entry.delete(0, tk.END)
    update_ui()
    game_frame.pack(pady=10)

def update_ui():
    word_label.config(text=" ".join(word_display))
    attempts_label.config(text=f"Attempts Left: {attempts}")
    guessed_label.config(text=f"Guessed Letters: {' '.join(guessed_letters) if guessed_letters else 'None'}")
    correct_label.config(text=f"Correct Guesses: {correct_guesses}")
    wrong_label.config(text=f"Wrong Guesses: {wrong_guesses}")

# --- GUESS HANDLER ---
def guess_letter():
    global attempts, correct_guesses, wrong_guesses
    guess = entry.get().lower()
    entry.delete(0, tk.END)

    if len(guess) != 1 or not guess.isalpha():
        messagebox.showerror("Invalid Input", "Please enter a single letter.")
        return

    if guess in guessed_letters:
        messagebox.showinfo("Already Guessed", "You already guessed this letter!")
        return

    guessed_letters.append(guess)

    if guess in word:
        for i, letter in enumerate(word):
            if letter == guess:
                word_display[i] = guess
        correct_guesses += 1
    else:
        attempts -= 1
        wrong_guesses += 1

    update_ui()

    if "_" not in word_display:
        show_result(True)
    elif attempts <= 0:
        show_result(False)

# --- RESULT SCREEN ---
def show_result(win):
    game_frame.pack_forget()
    result_frame.pack(pady=20)
    for widget in result_frame.winfo_children():
        widget.destroy()

    img = congrats_photo if win else final_photo
    img_label = tk.Label(result_frame, image=img, bg="white")
    img_label.pack(pady=10)

    msg = f"🎉 Congrats!\nYou Win! 🏆" if win else f"😢 You Failed!\nThe word was: {word} 💔"
    msg_label = tk.Label(result_frame, text=msg, font=("Arial", 18), bg="white")
    msg_label.pack(pady=5)

    tk.Button(result_frame, text="Restart Game", font=("Arial", 14), bg="#90EE90", command=restart_game).pack(pady=5)
    tk.Button(result_frame, text="Exit", font=("Arial", 14), bg="#ff7f7f", command=exit_game).pack(pady=5)

# --- BUILD LEVEL FRAME ---
tk.Label(level_frame, text="Select Difficulty Level", font=("Arial", 18), bg="white").pack(pady=10)
tk.Button(level_frame, text="Easy", font=("Arial", 14), width=15, bg="#64b5f6", command=lambda: start_game("1")).pack(pady=5)
tk.Button(level_frame, text="Medium", font=("Arial", 14), width=15, bg="#2196f3", command=lambda: start_game("2")).pack(pady=5)
tk.Button(level_frame, text="Hard", font=("Arial", 14), width=15, bg="#1565c0", command=lambda: start_game("3")).pack(pady=5)

# --- BUILD GAME FRAME ---
word_label = tk.Label(game_frame, font=("Arial", 24), bg="white")
word_label.pack(pady=10)

attempts_label = tk.Label(game_frame, font=("Arial", 14), bg="white")
attempts_label.pack(pady=5)

guessed_label = tk.Label(game_frame, font=("Arial", 14), bg="white")
guessed_label.pack(pady=5)

correct_label = tk.Label(game_frame, font=("Arial", 14), bg="white")
correct_label.pack(pady=5)

wrong_label = tk.Label(game_frame, font=("Arial", 14), bg="white")
wrong_label.pack(pady=5)

entry = tk.Entry(game_frame, font=("Arial", 14), width=5)
entry.pack(pady=10)

guess_button = tk.Button(game_frame, text="Guess", font=("Arial", 14), bg="#90EE90", command=guess_letter)
guess_button.pack(pady=5)

# Start with level selection
show_level_selection()

# Run the app
root.mainloop()
