import tkinter as tk
from tkinter import StringVar, Entry, Listbox, messagebox
from PIL import Image, ImageTk
import pygame
import requests

class PotterDBApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Chronicles of the Wizarding World")
        self.root.geometry("1200x800")  # Adjusted window size
        self.root.resizable(0, 0)

        # Initialize music
        pygame.mixer.init()
        self.music_playing = True
        self.play_background_music("C:/Users/ferna/OneDrive/Documents/GitHub/skills-portfolio-PetrasCyberExpert/A2 - DDA/PotterDB App/audios/hed.mp3")

        # Base URL for the API
        self.api_base_url = "https://api.potterdb.com/v1"

        # Create frames for each section
        self.frames = {}
        self.create_frames()

        # Show the intro page first
        self.show_intro_page()

        # Quiz variables
        self.score = 0
        self.current_question = 0
        self.attempts = 0
        self.current_difficulty = "easy"
        self.questions = {
            "easy": [
                {"question": "What is Harry Potter's middle name?", "options": ["James", "Albus", "Tom", "Lucius"], "answer": "James"},
                {"question": "What house is Harry Potter in?", "options": ["Gryffindor", "Slytherin", "Hufflepuff", "Ravenclaw"], "answer": "Gryffindor"},
            ],
            "medium": [
                {"question": "What is the name of Harry's owl?", "options": ["Hedwig", "Crookshanks", "Fawkes", "Scabbers"], "answer": "Hedwig"},
                {"question": "Who teaches Potions at Hogwarts?", "options": ["Snape", "McGonagall", "Flitwick", "Sprout"], "answer": "Snape"},
            ],
            "hard": [
                {"question": "What is the name of the Weasley's house?", "options": ["The Burrow", "Hogwarts", "Number 4 Privet Drive", "Godric's Hollow"], "answer": "The Burrow"},
                {"question": "What spell is used to disarm an opponent?", "options": ["Expelliarmus", "Stupefy", "Avada Kedavra", "Lumos"], "answer": "Expelliarmus"},
            ]
        }

    def load_image(self, path):
        """Load an image using Pillow and return a PhotoImage."""
        try:
            image = Image.open(path)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            return None

    def play_background_music(self, file):
        """Play background music in a loop."""
        try:
            pygame.mixer.music.load(file)
            pygame.mixer.music.play(loops=-1)
        except Exception as e:
            print(f"Error playing music: {e}")

    def show_intro_page(self):
        """Display the intro page with title, text, and a start button."""
        intro_frame = tk.Frame(self.root, bg='#06004B')
        intro_frame.pack(fill="both", expand=True)

        # Background image
        bg_image = self.load_image('C:/Users/ferna/OneDrive/Documents/GitHub/skills-portfolio-PetrasCyberExpert/A2 - DDA/PotterDB App/background/intro.jpeg')
        if bg_image:
            bg_label = tk.Label(intro_frame, image=bg_image)
            bg_label.place(relwidth=1, relheight=1)
            bg_label.image = bg_image  # Keep a reference to prevent garbage collection

        # Title and text
        title_label = tk.Label(intro_frame, text="Welcome to Harry Potter: Where the Magic Lives on!", font=("Arial", 30), fg="Yellow", bg='#06004B')
        title_label.pack(pady=100)

        intro_text_label = tk.Label (intro_frame, text="A Journey where the Magic Never ends and the wonders continue to unfold!\nClick Start to Begin your journey.", font=("Arial", 18), fg="Yellow", bg='#06004B')
        intro_text_label.pack()

        # Start button to enter the app
        start_button = tk.Button(intro_frame, text="Start", font=("Arial", 18), command=lambda: self.start_main_app(intro_frame), bg="yellow", fg="white", relief="flat", borderwidth=5, highlightthickness=0, activebackground="darkblue", activeforeground="white")
        start_button.pack(pady=30)

    def start_main_app(self, intro_frame):
        """Hide the intro page and start the main app."""
        intro_frame.destroy()  # Remove the intro page
        self.create_sidebar()  # Create the sidebar
        self.show_frame('home')  # Show the home frame

    def create_sidebar(self):
        """Create the sidebar for navigation."""
        self.sidebar = tk.Frame(self.root, width=276, bg='#06004B')  # Adjust width
        self.sidebar.pack(side="left", fill="y")

        # Create a logo image
        logo_image = self.load_image('C:/Users/ferna/OneDrive/Documents/GitHub/skills-portfolio-PetrasCyberExpert/A2 - DDA/PotterDB App/buttons/png.com.png')  # Update this path
        if logo_image:
            logo_label = tk.Label(self.sidebar, image=logo_image, borderwidth=0, highlightthickness=0)
            logo_label.image = logo_image  # Keep a reference
            logo_label.pack(pady=10)

        buttons = [
            ("Home", self.show_frame, 'home', 'C:/Users/ferna/OneDrive/Documents/GitHub/skills-portfolio-PetrasCyberExpert/A2 - DDA/PotterDB App/buttons/home.png'),
            ("About", self.show_frame, 'about', 'C:/Users/ferna/OneDrive/Documents/GitHub/skills-portfolio-PetrasCyberExpert/A2 - DDA/PotterDB App/buttons/info.png'),
            ("Characters", self.show_frame, 'characters', 'C:/Users/ferna/OneDrive/Documents/GitHub/skills-portfolio-PetrasCyberExpert/A2 - DDA/PotterDB App/buttons/character.png'),
            ("Books & Movies", self.show_frame, 'books_movies', 'C:/Users/ferna/OneDrive/Documents/GitHub/skills-portfolio-PetrasCyberExpert/A2 - DDA/PotterDB App/buttons/book.png'),
            ("Spells & Potions", self.show_frame, 'spells_potions', 'C:/Users/ferna/OneDrive/Documents/GitHub/skills-portfolio-PetrasCyberExpert/A2 - DDA/PotterDB App/buttons/magic-book.png'),
            ("Map", self.show_frame, 'map', 'C:/Users/ferna/OneDrive/Documents/GitHub/skills-portfolio-PetrasCyberExpert/A2 - DDA/PotterDB App/buttons/map.png'),
            ("Quiz Game", self.show_frame, 'quiz', 'C:/Users/ferna/OneDrive/Documents/GitHub/skills-portfolio-PetrasCyberExpert/A2 - DDA/PotterDB App/buttons/quiz.png'),
            ("Instructions", self.show_frame, 'instructions', 'C:/Users/ferna/OneDrive/Documents/GitHub/skills-portfolio-PetrasCyberExpert/A2 - DDA/PotterDB App/buttons/direction.png'),
            ("Mute/Unmute", self.toggle_music, None, 'C:/Users/ferna/OneDrive/Documents/GitHub/skills-portfolio-PetrasCyberExpert/A2 - DDA/PotterDB App/buttons/volume.png'),
        ]

        for text, command, *args, icon_path in buttons:
            icon = self.load_image(icon_path)
            if icon:
                btn = tk.Button(
                    self.sidebar,
                    text=text,
                    bg='#06004B',
                    fg="white",
                    font=("Arial", 12),
                    relief="solid",
                    borderwidth=5,
                    command=lambda cmd=command, arg=args: cmd(*arg) if arg else cmd(),
                    padx=10,
                    pady=10,
                    height=2,
                    width=15,
                    highlightbackground="#06004B",
                    activebackground="lightblue",
                    activeforeground="white",
                    compound="left",  # Place text to the right of the icon
                    image=icon
                )
                btn.image = icon 
                btn.pack(fill="x", pady=5, padx=5)

    def create_frames(self):
        """Create frames for each section."""
 
        self.frames['home'] = tk.Frame(self.root, bg='#DCCDAE')
        self.frames['about'] = tk.Frame(self.root, bg='#DCCDAE')
        self.frames['characters'] = tk.Frame(self.root, bg='#DCCDAE')
        self.frames['books_movies'] = tk.Frame(self.root, bg='#DCCDAE')
        self.frames['spells_potions'] = tk.Frame(self.root, bg='#DCCDAE')
        self.frames['map'] = tk.Frame(self.root, bg='#DCCDAE')
        self.frames['quiz'] = tk.Frame(self.root, bg='#DCCDAE')
        self.frames['instructions'] = tk.Frame(self.root, bg='#DCCDAE')
        self.frames['score'] = tk.Frame(self.root, bg='#DCCDAE')
        self.frames['thank_you'] = tk.Frame(self.root, bg='#DCCDAE')

        for frame in self.frames.values():
            frame.pack(fill="both", expand=True)

        self.populate_home_frame()
        self.populate_about_frame()
        self.populate_characters_frame()
        self.populate_books_movies_frame()
        self.populate_spells_and_potions_frame()
        self.populate_map_frame()
        self.populate_quiz_frame()
        self.populate_instructions_frame()

    def show_frame(self, frame_name):
        """Raise the specified frame to the top for viewing."""
        for frame in self.frames.values():
            frame.pack_forget()  # Hide all frames
        self.frames[frame_name].pack(fill="both", expand=True)  # Show the selected frame

    def populate_home_frame(self):
        """Populate the Home frame with welcome text and background image."""
        bg_image = self.load_image('C:/Users/ferna/OneDrive/Documents/GitHub/skills-portfolio-PetrasCyberExpert/A2 - DDA/PotterDB App/background/H.jpeg')  
        if bg_image:
            bg_label = tk.Label(self.frames['home'], image=bg_image)
            bg_label.place(relwidth=1, relheight=1)
            bg_label.image = bg_image  # Keep a reference

        home_label = tk.Label(self.frames['home'], text="Welcome to Chronicles of the Wizarding World!", font=("Arial", 24), fg="black", bg='#DCCDAE')
        home_label.pack(pady=20)

    def populate_about_frame(self):
        """Populate the About frame with information about the app."""
        bg_image = self.load_image('C:/Users/ferna/OneDrive/Documents/GitHub/skills-portfolio-PetrasCyberExpert/A2 - DDA/PotterDB App/background/H.jpeg')  
        if bg_image:
            bg_label = tk.Label(self.frames['about'], image=bg_image)
            bg_label.place(relwidth=1, relheight=1)
            bg_label.image = bg_image  # Keep a reference

        about_text = "This app provides information about the Harry Potter universe, including characters, books, spells, and more."
        about_label = tk.Label(self.frames['about'], text=about_text, font=("Arial", 16), fg="black", bg='#DCCDAE', justify="left")
        about_label.pack(pady=20)

    def populate_characters_frame(self):
        """Populate the Characters frame with a search bar and character details."""
        bg_image = self.load_image('C:/Users/ferna/OneDrive/Documents/GitHub/skills-portfolio-PetrasCyberExpert/A2 - DDA/PotterDB App/background/H.jpeg')  
        if bg_image:
            bg_label = tk.Label(self.frames['characters'], image=bg_image)
            bg_label.place(relwidth=1, relheight=1)
            bg_label.image = bg_image  # Keep a reference

        search_var = StringVar()
        search_entry = Entry(self.frames['characters'], textvariable=search_var, font=("Arial", 14), bg="beige")
        search_entry.place(relx=0.5, rely=0.1, anchor="center")

        search_button = tk.Button(self.frames['characters'], text="Search", command=lambda: self.search_characters(search_var.get()), font=("Arial", 14))
        search_button.place(relx=0.5, rely=0.15, anchor="center")

        self.characters_listbox = Listbox(self.frames['characters'], font=("Arial", 14))
        self.characters_listbox.place(relx=0.5, rely=0.3, anchor="center", width=400, height=200)

        self.character_info_label = tk.Label(self.frames['characters'], text="", font=("Arial", 14), fg="black", bg='#DCCDAE')
        self.character_info_label.place(relx=0.5, rely=0.6, anchor="center")

        self.load_characters_data()

        self.characters_listbox.bind('<<ListboxSelect>>', self.display_character_info)

    def load_characters_data(self):
        """Load characters data from the API and populate the listbox."""
        characters = self.get_characters_data()
        if characters:
            for character in characters:
                self.characters_listbox.insert(tk.END, character['name'])
        else:
            messagebox.showerror("Error", "Failed to load character data.")

    def search_characters(self, query):
        """Search for characters based on the query."""
        self.characters_listbox.delete(0, tk.END)
        characters = self.get_characters_data()
        suggestions = [character for character in characters if query.lower() in character['name'].lower()]
        for character in suggestions:
            self.characters_listbox.insert(tk.END, character['name'])

    def get_characters_data(self):
        """Get characters data from the API."""
        try:
            response = requests.get(f"{self.api_base_url}/characters?page[size]=25")
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()

            if isinstance(data, dict) and 'data' in data:
                return [
                    {
                        "name": character['attributes'].get('name', 'Unknown'),
                        "birth": character['attributes'].get('born', 'Unknown'),
                        "age": character['attributes'].get('age', 'Unknown'),
                        "role": character['attributes'].get('role', 'Unknown'),
                        "image": character['attributes'].get('image', 'path/to/default_image.png')
                    }
                    for character in data['data']
                ]
            else:
                print("Unexpected response format for characters data:", data)
                return []

        except requests.exceptions.RequestException as e:
            print(f"Error fetching characters data: {e}")
            return []

    def display_character_info(self, event):
        """Display character information when selected from the list."""
        selected_index = self.characters_listbox.curselection()
        if selected_index:
            character = self.get_characters_data()[selected_index[0]]
            info_text = f"Name: {character['name']}\nRole: {character['role']}\nAge: {character['age']}\nBirth: {character['birth']}"
            self.character_info_label.config(text=info_text)

            character_image = self.load_image(character['image'])
            if character_image:
                character_image_label = tk.Label(self.frames['characters'], image=character_image)
                character_image_label.image = character_image  # Keep a reference
                character_image_label.place(relx=0.5, rely=0.8, anchor="center")

    def populate_books_movies_frame(self):
        """Populate the Books & Movies frame with a search bar and details."""
        bg_image = self.load_image('C:/Users/ferna/OneDrive/Documents/GitHub/skills-portfolio-PetrasCyberExpert/A2 - DDA/PotterDB App/background/H.jpeg')  
        if bg_image:
            bg_label = tk.Label(self.frames['books_movies'], image=bg_image)
            bg_label.place(relwidth=1, relheight=1)
            bg_label.image = bg_image  # Keep a reference

        search_var = StringVar()
        search_entry = Entry(self.frames['books_movies'], textvariable=search_var, font=("Arial", 14), bg="beige")
        search_entry.place(relx=0.5, rely=0.1, anchor="center")

        search_button = tk.Button(self.frames['books_movies'], text="Search", command=lambda: self.search_books_movies(search_var.get()), font=("Arial", 14))
        search_button.place(relx=0.5, rely=0.15, anchor="center")

        self.books_and_movies_listbox = Listbox(self.frames['books_movies'], font=("Arial", 14))
        self.books_and_movies_listbox.place(relx=0.5, rely=0.3, anchor="center", width=400, height=200)

        self.book_info_label = tk.Label(self.frames['books_movies'], text="", font=("Arial", 14), fg="black", bg='#DCCDAE')
        self.book_info_label.place(relx=0.5, rely=0.6, anchor="center")

        self.load_books_and_movies_data()
        self.books_and_movies_listbox.bind('<<ListboxSelect>>', self.display_book_info)

    def load_books_and_movies_data(self):
        """Load books and movies data from the API and populate the listbox."""
        books_and_movies = self.get_books_and_movies_data()
        if books_and_movies:
            for item in books_and_movies:
                self.books_and_movies_listbox.insert(tk.END, item['title'])
        else:
            messagebox.showerror("Error", "Failed to load books and movies data.")

    def search_books_movies(self, query):
        """Search for books and movies based on the query."""
        self.books_and_movies_listbox.delete(0, tk.END)
        books_and_movies = self.get_books_and_movies_data()
        suggestions = [item for item in books_and_movies if query.lower() in item['title'].lower()]
        for item in suggestions:
            self.books_and_movies_listbox.insert(tk.END, item['title'])

    def get_books_and_movies_data(self):
        """Get books and movies data from the API."""
        try:
            response = requests.get(f"{self.api_base_url}/books")  # Updated endpoint
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list):
                return [
                    {
                        "title": item.get('attributes', {}).get('title', 'Unknown'),
                        "launch": item.get('attributes', {}).get('release_date', 'Unknown'),
                        "description": item.get('attributes', {}).get('summary', 'No description available'),
                        "image": item.get('attributes', {}).get('cover', 'path/to/default_image.png')
                    }
                    for item in data
                ]
            else:
                print("Unexpected response format for books and movies data:", data)
                return []

        except requests.exceptions.RequestException as e:
            print(f"Error fetching books and movies data: {e}")
            return []

    def display_book_info(self, event):
        """Display book information when selected from the list."""
        selected_index = self.books_and_movies_listbox.curselection()
        if selected_index:
            book = self.get_books_and_movies_data()[selected_index[0]]
            info_text = f"Title: {book['title']}\nLaunch: {book['launch']}\nDescription: {book['description']}"
            self.book_info_label.config(text=info_text)

            book_image = self.load_image(book['image'])
            if book_image:
                book_image_label = tk.Label(self.frames['books_movies'], image=book_image)
                book_image_label.image = book_image  # Keep a reference
                book_image_label.place(relx=0.5, rely=0.8, anchor="center")

    def populate_spells_and_potions_frame(self):
        """Populate the Spells & Potions frame with a search bar and details."""
        bg_image = self.load_image('C:/Users/ferna/OneDrive/Documents/GitHub/skills-portfolio-PetrasCyberExpert/A2 - DDA/PotterDB App/background/H.jpeg')  
        if bg_image:
            bg_label = tk.Label(self.frames['spells_potions'], image=bg_image)
            bg_label.place(relwidth=1, relheight=1)
            bg_label.image = bg_image  # Keep a reference

        search_var = StringVar()
        search_entry = Entry(self.frames['spells_potions'], textvariable=search_var, font=("Arial", 14), bg="beige")
        search_entry.place(relx=0.5, rely=0.1, anchor="center")

        search_button = tk.Button(self.frames['spells_potions'], text="Search", command=lambda: self.search_spells_potions(search_var.get()), font=("Arial", 14))
        search_button.place(relx=0.5, rely=0.15, anchor="center")

        self.spells_and_potions_listbox = Listbox(self.frames['spells_potions'], font=("Arial", 14))
        self.spells_and_potions_listbox.place(relx=0.5, rely=0.3, anchor="center", width=400, height=200)

        self.spell_info_label = tk.Label(self.frames['spells_potions'], text="", font=("Arial", 14), fg="black", bg='#DCCDAE')
        self.spell_info_label.place(relx=0.5, rely=0.6, anchor="center")

        self.load_spells_and_potions_data()
        self.spells_and_potions_listbox.bind('<<ListboxSelect>>', self.display_spell_info)

    def load_spells_and_potions_data(self):
        """Load spells and potions data from the API and populate the listbox."""
        spells_and_potions = self.get_spells_and_potions_data()
        if spells_and_potions:
            for item in spells_and_potions:
                self.spells_and_potions_listbox.insert(tk.END, item['name'])
        else:
            messagebox.showerror("Error", "Failed to load spells and potions data.")

    def search_spells_potions(self, query):
        """Search for spells and potions based on the query."""
        self.spells_and_potions_listbox.delete(0, tk.END)
        spells_and_potions = self.get_spells_and_potions_data()
        suggestions = [item for item in spells_and_potions if query.lower() in item['name'].lower()]
        for item in suggestions:
            self.spells_and_potions_listbox.insert(tk.END, item['name'])

    def get_spells_and_potions_data(self):
        """Get spells and potions data from the API."""
        try:
            response = requests.get(f"{self.api_base_url}/spells")  # Updated endpoint
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list):
                return [
                    {
                        "name": item.get('attributes', {}).get('name', 'Unknown'),
                        "description": item.get('attributes', {}).get('description', 'No description available'),
                        "function": item.get('attributes', {}).get('function', 'No function available'),
                        "image": item.get('attributes', {}).get('image', 'path/to/default_image.png')
                    }
                    for item in data
                ]
            else:
                print("Unexpected response format for spells and potions data:", data)
                return []

        except requests.exceptions.RequestException as e:
            print(f"Error fetching spells and potions data: {e}")
            return []

    def display_spell_info(self, event):
        """Display spell information when selected from the list."""
        selected_index = self.spells_and_potions_listbox.curselection()
        if selected_index:
            spell = self.get_spells_and_potions_data()[selected_index[0]]
            info_text = f"Name: {spell['name']}\nDescription: {spell['description']}\nFunction: {spell['function']}"
            self.spell_info_label.config(text=info_text)

            spell_image = self.load_image(spell['image'])
            if spell_image:
                spell_image_label = tk.Label(self.frames['spells_potions'], image=spell_image)
                spell_image_label.image = spell_image  # Keep a reference
                spell_image_label.place(relx=0.5, rely=0.8, anchor="center")

    def populate_map_frame(self):
        """Populate the Map frame with a suggestion for a map API."""
        bg_image = self.load_image('C:/Users/ferna/OneDrive/Documents/GitHub/skills-portfolio-PetrasCyberExpert/A2 - DDA/PotterDB App/background/H.jpeg')  
        if bg_image:
            bg_label = tk.Label(self.frames['map'], image=bg_image)
            bg_label.place(relwidth=1, relheight=1)
            bg_label.image = bg_image  # Keep a reference

        map_label = tk.Label(self.frames['map'], text="For the Harry Potter map, consider using the HP-API.", font=("Arial", 16), fg="black", bg='#DCCDAE')
        map_label.place(relx=0.5, rely=0.5, anchor="center")

    def populate_quiz_frame(self):
        """Populate the Quiz frame with introductory questions."""
        bg_image = self.load_image('C:/Users/ferna/OneDrive/Documents/GitHub/skills-portfolio-PetrasCyberExpert/A2 - DDA/PotterDB App/background/1.jpeg')  
        if bg_image:
            bg_label = tk.Label(self.frames['quiz'], image=bg_image)
            bg_label.place(relwidth=1, relheight=1)
            bg_label.image = bg_image  # Keep a reference

        self.score = 0
        self.current_question = 0
        self.attempts = 0

        self.question_label = tk.Label(self.frames['quiz'], text="", font=("Arial", 16), fg="black", bg='#DCCDAE')
        self.question_label.place(relx=0.5, rely=0.2, anchor="center")

        self.option_buttons = []
        for idx in range(4):
            option_button = tk.Button(self.frames['quiz'], text="", font=("Arial", 14), command=lambda idx=idx: self.check_answer(idx), bg="orange")
            option_button.place(relx=0.5, rely=0.3 + idx * 0.1, anchor="center")
            self.option_buttons.append(option_button)

        self.continue_button = tk.Button(self.frames['quiz'], text="Continue", command=self.next_question, font=("Arial", 14), bg="orange")
        self.continue_button.place(relx=0.5, rely=0.8, anchor="center")

        self.start_quiz()

    def start_quiz(self):
        """Start the quiz."""
        self.current_question = 0
        self.attempts = 0
        self.update_question()

    def update_question(self):
        """Update the question and options for the quiz."""
        if self.current_question < len(self.questions[self.current_difficulty]):
            question_data = self.questions[self.current_difficulty][self.current_question]
            self.question_label.config(text=question_data["question"])
            for idx, option in enumerate(question_data["options"]):
                self.option_buttons[idx].config(text=option)
        else:
            self.end_quiz()

    def check_answer(self, selected_index):
        """Check if the selected answer is correct."""
        question_data = self.questions[self.current_difficulty][self.current_question]
        if question_data["options"][selected_index] == question_data["answer"]:
            self.score += 5  # Add 5 points for a correct answer
            messagebox.showinfo("Correct!", "You got it right!")
        else:
            self.attempts += 1
            if self.attempts < 3:
                messagebox.showinfo("Incorrect", "Try again!")
            else:
                messagebox.showinfo("Incorrect", f"The correct answer was: {question_data['answer']}")
                self.current_question += 1
                self.attempts = 0
        self.next_question()

    def next_question(self):
        """Move to the next question or end the quiz."""
        self.current_question += 1
        self.update_question()

    def end_quiz(self):
        """End the quiz and show the score."""
        messagebox.showinfo("Quiz Finished", f"Your score: {self.score}")
        self.show_frame('score')

    def populate_score_frame(self):
        """Populate the Score frame with the user's score."""
        score_label = tk.Label(self.frames['score'], text=f"Your score: {self.score}", font=("Arial", 24), fg="black", bg='#DCCDAE')
        score_label.pack(pady=20)

        return_button = tk.Button(self.frames['score'], text="Return to Home", command=lambda: self.show_frame('home'), font=("Arial", 14))
        return_button.pack(pady=20)

    def populate_instructions_frame(self):
        """Populate the Instructions frame."""
        bg_image = self.load_image('C:/Users/ferna/OneDrive/Documents/GitHub/skills-portfolio-PetrasCyberExpert/A2 - DDA/PotterDB App/background/B.jpeg')  
        if bg_image:
            bg_label = tk.Label(self.frames['instructions'], image=bg_image)
            bg_label.place(relwidth=1, relheight=1)
            bg_label.image = bg_image  # Keep a reference

        instructions_text = """Instructions:
1. Use the sidebar to navigate through the app.
2. In the Characters tab, use the search bar to find characters.
3. In the Books & Movies tab, search for titles.
4. In the Quiz tab, answer the questions within the time limit.
5. Enjoy exploring the Harry Potter universe!"""
        instructions_label = tk.Label(
    self.frames['instructions'], text=instructions_text, font=("Arial", 16), fg="black", bg='#DCCDAE', justify="left")
        instructions_label.place(relx=0.5, rely=0.3, anchor="center")

    def toggle_music(self):
        """Toggle music play/pause."""
        if self.music_playing:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        self.music_playing = not self.music_playing

if __name__ == "__main__":
    root = tk.Tk()
    app = PotterDBApp(root)
    root.mainloop()