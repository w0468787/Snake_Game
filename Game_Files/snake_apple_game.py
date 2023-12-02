from tkinter import *
from tkinter import ttk
from apple import Apple
from snake import Snake

WIDTH = 600
HEIGHT = 400
BODY_SIZE = 20
FOOD_SIZE = 20


class SnakeGame:

    def __init__(self, root):
        self.time_between_turns = 100
        # Initialize screen size and window title
        self.first_turn_filter = True
        self.apples = []
        self.score = 0
        self.play_again_frame = None
        self.root = root
        self.root.title("snake apple game")
        self.game_over_flag = False
        self.game_mode_flag = 0
        self.menu_frame = None
        self.game_modes_frame = None
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.geometry("%dx%d" % (width, height))

        score = 0
        self.label = Label(self.root, text="Points:{}".format(score),
                           font=('consolas', 20))
        self.label.pack()
        # Create a frame
        self.frm = ttk.Frame(root, padding=10)
        self.frm.pack(fill=BOTH, expand=True)  # Use pack() to place the frame

        # Create a canvas inside the frame
        self.canvas = Canvas(self.frm, width=WIDTH, height=HEIGHT, bg="green")
        self.canvas.pack(fill=BOTH, expand=True)  # Use pack() to place the canvas inside the frame

        self.snake = Snake(self.canvas, BODY_SIZE)
        self.apple = Apple(self.canvas, FOOD_SIZE, self.snake.coordinates)

        # Bind arrow key events to corresponding methods
        self.root.bind('<Up>', lambda event: self.change_direction('Up'))
        self.root.bind('<Down>', lambda event: self.change_direction('Down'))
        self.root.bind('<Left>', lambda event: self.change_direction('Left'))
        self.root.bind('<Right>', lambda event: self.change_direction('Right'))

        # Lower the canvas to the background
        self.frm.lower(self.canvas)
        self.create_menu()
        self.root.mainloop()
        # Call the next_turn function initially to start the game loop

    def start_game(self):
        self.destroy_menus()
        self.reset_game()
        self.next_turn()

    def create_menu(self):
        self.menu_frame = ttk.Frame(self.root, padding=10)
        self.menu_frame.place(in_=self.canvas, anchor="center", relx=0.5, rely=0.5)

        play_button = Button(self.menu_frame, text="Play", command=self.start_game)
        play_button.pack(pady=10)

        game_modes_button = Button(self.menu_frame, text="Game Modes", command=self.show_game_modes)
        game_modes_button.pack(pady=10)

        exit_button = Button(self.menu_frame, text="Exit", command=self.root.destroy)
        exit_button.pack(pady=10)

    def destroy_menus(self):
        if hasattr(self, 'menu_frame') and self.menu_frame:
            self.menu_frame.destroy()
        if hasattr(self, 'game_modes_frame') and self.game_modes_frame:
            self.game_modes_frame.destroy()

    def show_game_modes(self):
        # Destroy the current menu frame
        # Destroy the current menu frame

        # Create a new frame for the game modes screen
        self.game_modes_frame = ttk.Frame(self.root, padding=10)
        self.game_modes_frame.place(in_=self.canvas, anchor="c", relx=0.5, rely=0.5)

        if hasattr(self, 'menu_frame') and self.menu_frame:
            self.menu_frame.destroy()
        # Create buttons for each game mode
        neon_snake_button = Button(self.game_modes_frame, text="Neon Snake", command=lambda: self.set_game_mode(1))
        neon_snake_button.pack(pady=10)

        # Add more buttons for other game modes
        # Example:
        frenzy_mode_button = Button(self.game_modes_frame, text="Apple Frenzy", command=lambda: self.set_game_mode(2))
        frenzy_mode_button.pack(pady=10)

        fast_snake_mode_button = Button(self.game_modes_frame, text="Speedy Snake", command=lambda: self.set_game_mode(3))
        fast_snake_mode_button.pack(pady=10)

    def set_game_mode(self, mode):
        self.game_mode_flag = mode

        if self.game_mode_flag == 1:
            self.snake.neon_mode = True

        if self.game_mode_flag == 2:
            Apple.engage_frenzy(self.apple)

        self.start_game()

    def change_direction(self, direction):
        current_direction = self.snake.direction

        # Check the conditions before changing the direction
        if (direction == "Up" and current_direction != "Down") or \
                (direction == "Down" and current_direction != "Up") or \
                (direction == "Left" and current_direction != "Right") or \
                (direction == "Right" and current_direction != "Left"):
            self.snake.direction = direction

    def next_turn(self):
        if not self.game_over_flag:
            if self.game_mode_flag == 1:
                self.snake.neon_snake()
                x, y = self.snake.coordinates[0]
                if (x, y) in self.apple.coordinates:
                    self.score += 1
                    self.label.config(text="Points:{}".format(self.score))
                    self.snake.eat()
                    self.apple.delete()
                    self.apple = Apple(self.canvas, FOOD_SIZE, self.snake.coordinates)
                self.snake.move(self.snake.direction)
            elif self.game_mode_flag == 2:
                if self.snake.check_apple_collision(self.apples):
                    self.score += 1
                    self.label.config(text="Points:{}".format(self.score))
                    self.snake.eat()
                    for i in range(Apple.m_frenzy_iterator):
                        self.apples.append(Apple(self.canvas, FOOD_SIZE, self.snake.coordinates))
                # Move the snake
                self.snake.move(self.snake.direction)
            elif self.game_mode_flag == 3:
                x, y = self.snake.coordinates[0]
                if (x, y) in self.apple.coordinates:
                    self.time_between_turns -= 5
                    self.score += 1
                    self.label.config(text="Points:{}".format(self.score))
                    self.snake.eat()
                    self.apple.delete()
                    self.apple = Apple(self.canvas, FOOD_SIZE, self.snake.coordinates)
                self.snake.move(self.snake.direction)
            else:
                x, y = self.snake.coordinates[0]
                if (x, y) in self.apple.coordinates:
                    self.score += 1
                    self.label.config(text="Points:{}".format(self.score))
                    self.snake.eat()
                    self.apple.delete()
                    self.apple = Apple(self.canvas, FOOD_SIZE, self.snake.coordinates)
                self.snake.move(self.snake.direction)

            # Check for collisions with the apple

            # Call the next_turn function again after a delay to create a game loop
            self.root.after(self.time_between_turns, self.next_turn)
            if self.snake.check_collisions():
                self.game_over()

    def game_over(self):
        self.game_over_flag = True
        self.canvas.delete(ALL)
        self.canvas.create_text(self.canvas.winfo_width() / 2,
                                self.canvas.winfo_height() / 2,
                                font=('consolas', 70),
                                text="GAME OVER", fill="red",
                                tag="gameover")
        self.play_again_frame = ttk.Frame(self.root, padding=10)
        self.play_again_frame.place(in_=self.canvas, anchor="s", relx=0.5, rely=1.0 - (50 / self.canvas.winfo_height()))

        # Create buttons for each game mode
        play_again_button = Button(self.play_again_frame, text="Play again", command=lambda: self.play_again())
        play_again_button.pack(pady=10)

    def reset_game(self):
        # Reset game state
        self.canvas.delete("gameover")
        self.snake.delete_snake()
        self.score = 0
        self.label.config(text="Points:{}".format(self.score))
        self.game_over_flag = False
        self.apple.reset()

        # Reset snake and apple
        self.snake.reset_snake()
        self.apple.delete()
        self.apple = Apple(self.canvas, FOOD_SIZE, self.snake.coordinates)
        self.apples.append(self.apple)

        # Destroy the play again frame if it exists
        if self.play_again_frame:
            self.play_again_frame.destroy()

    def play_again(self):
        self.reset_game()

        self.create_menu()
