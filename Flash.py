import tkinter as tk
from PIL import Image, ImageTk
import os
import random

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard Study App")
        
        # List of flashcards with paths that could either be valid file paths or strings
        self.flashcards = [
            ("image1_question.png", "image1_answer.png"), 
            ("What is 2 + 2?", "4"),                    
            ("image2_question.png", "image2_answer.png"), 
            ("Who wrote '1984'?", "George Orwell"),       
        ]
        
        self.card_index = 0
        self.show_images = True  # Flag to switch between image/text modes
        self.answer_is_shown = False  # Track if the card is flipped

        # Create widgets
        self.content_label = tk.Label(self.root, width=400, height=400)
        self.content_label.pack(pady=20)

        # Show Answer button
        self.answer_button = tk.Button(self.root, text="Flip Card", command=self.flip_card, font=("Arial", 16))
        self.answer_button.pack(pady=10)

        # Next and Previous Buttons
        self.previous_button = tk.Button(self.root, text="Previous", command=self.previous_card, font=("Arial", 16))
        self.previous_button.pack(side="left", padx=20, pady=10)

        self.next_button = tk.Button(self.root, text="Next", command=self.next_card, font=("Arial", 16))
        self.next_button.pack(side="right", padx=20, pady=10)

        # Shuffle Button
        self.shuffle_button = tk.Button(self.root, text="Shuffle", command=self.shuffle_cards, font=("Arial", 16))
        self.shuffle_button.pack(pady=10)

        # Quit Button
        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit, font=("Arial", 16))
        self.quit_button.pack(pady=20)

        # Show the first flashcard
        self.show_question()

        # Bind keyboard events for navigation
        self.root.bind("<Left>", self.previous_card)
        self.root.bind("<Right>", self.next_card)
        self.root.bind("a", self.previous_card)
        self.root.bind("d", self.next_card)

        # Bind keyboard events to flip the card
        self.root.bind("<space>", self.flip_card)
        self.root.bind("w", self.flip_card)

    def shuffle_cards(self):
        # Shuffle the flashcards and reset the flip state
        random.shuffle(self.flashcards)
        self.card_index = 0  # Reset to the first card after shuffle
        self.answer_is_shown = False 
        self.show_question()

    def flip_card(self, event=None):
        if self.answer_is_shown:
            self.show_question()
        else:
            self.show_answer()

        self.answer_is_shown = not self.answer_is_shown

    def next_card(self, event=None):
        # Move to the next flashcard, wrap around if at the end
        self.card_index = (self.card_index + 1) % len(self.flashcards)
        self.answer_is_shown = False 
        self.show_question()

    def previous_card(self, event=None):
        # Move to the previous flashcard, wrap around if at the beginning
        self.card_index = (self.card_index - 1) % len(self.flashcards)
        self.answer_is_shown = False
        self.show_question()

    def show_question(self):
        question = self.flashcards[self.card_index][0]

        if self.is_valid_image(question):
            self.display_image(question)
        else:
            self.display_text(question)

    def show_answer(self):
        answer = self.flashcards[self.card_index][1]
        
        if self.is_valid_image(answer):
            self.display_image(answer)
        else:
            self.display_text(answer)

    def display_image(self, image_path):
        # Open the image and resize it to fit the label size
        try:
            image = Image.open(image_path)
            image = image.resize((400, 400), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            # Update the label with the new image
            self.content_label.config(image=photo, text="")
            self.content_label.image = photo
        except Exception as e:
            # If image loading fails, display the error message as text
            self.display_text(f"Error loading image: {e}")

    def display_text(self, text):
        # Display the text question or answer
        self.content_label.config(image="", text=text)
        self.content_label.config(font=("Arial", 20), width=30, height=3, anchor="center")

    def is_valid_image(self, file_path):
        # Check if the path exists and is an image file
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')
        return os.path.isfile(file_path) and file_path.lower().endswith(image_extensions)

# Create the Tkinter root window
root = tk.Tk()

# Instantiate the FlashcardApp
app = FlashcardApp(root)

# Start the Tkinter event loop
root.mainloop()
