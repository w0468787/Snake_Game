import random
from tkinter import ALL

from apple import Apple


class Snake:
    def __init__(self, canvas, size):
        self.neon_mode=False
        self.direction = "Down"
        self.canvas = canvas
        self.size = size
        self.coordinates = []
        self.squares = []
        # Snake color
        if self.neon_mode == False:
            self.color = "#0000FF"  # Snake color


        canvas.update()
        # canvas_width = canvas.winfo_width()
        # canvas_height = canvas.winfo_height()
        #
        # x = random.randint(1, (canvas_width // self.size) - 1) * self.size
        # y = random.randint(1, (canvas_height // self.size) - 1) * self.size
        #
        # # Create two adjacent squares for the initial snake body segment
        # square_1 = self.canvas.create_rectangle(x, y, x + self.size, y + self.size, fill=self.color)
        # square_2 = self.canvas.create_rectangle(x - self.size, y, x, y + self.size, fill=self.color)
        #
        #
        # self.coordinates.append((x, y))
        # self.squares.extend([square_1, square_2])

    def generate_random_color(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = "#{:02X}{:02X}{:02X}".format(r, g, b)
        return color

    def reset_snake(self):
        self.coordinates.clear()
        self.squares.clear()
        self.neon_mode = False
        self.direction = "Down"
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        x = random.randint(1, (canvas_width // self.size) - 1) * self.size
        y = random.randint(1, (canvas_height // self.size) - 1) * self.size

        # Create two adjacent squares for the initial snake body segment
        square_1 = self.canvas.create_rectangle(x, y, x + self.size, y + self.size, fill=self.color)
        square_2 = self.canvas.create_rectangle(x - self.size, y, x, y + self.size, fill=self.color)

        self.coordinates.append((x, y))
        self.squares.extend([square_1, square_2])

    def move(self, direction):
        head_x, head_y = self.coordinates[0]

        if direction == "Up":
            new_head = (head_x, head_y - self.size)
        elif direction == "Down":
            new_head = (head_x, head_y + self.size)
        elif direction == "Left":
            new_head = (head_x - self.size, head_y)
        elif direction == "Right":
            new_head = (head_x + self.size, head_y)

        # Create a new head square at the new position
        head_square = self.canvas.create_rectangle(new_head[0], new_head[1],
                                                   new_head[0] + self.size, new_head[1] + self.size,
                                                   fill=self.color)

        # Add the new head to the coordinates list and squares list
        self.coordinates.insert(0, new_head)
        self.squares.insert(0, head_square)

        # Remove the last tail square to simulate the snake movement
        tail_square = self.squares.pop()
        self.canvas.delete(tail_square)

        if len(self.coordinates) > len(self.squares):
            self.coordinates.pop()

# function to check snake's collision and position
    def check_collisions(self):
      x, y = self.coordinates[0]
      if x < 0 or x >= self.canvas.winfo_width():
        return True
      elif y < 0 or y >= self.canvas.winfo_height():
        return True
      for body_part in self.coordinates[1:]:
        body_x,body_y=body_part
        if x == body_x and y == body_y:
            return True

      return False

    def check_apple_collision(self, apples):
        # Get the head coordinates of the snake
        snake_head_x, snake_head_y = self.coordinates[0]

        # Iterate through each apple in the list
        for index, apple in enumerate(apples):
            # Get the coordinates of the current apple
            apple_coordinates = apple.coordinates

            # Check if the head of the snake is at the same position as the current apple
            if (snake_head_x, snake_head_y) in apple_coordinates:
                # Delete the apple with matching coordinates
                apples[index].delete()

                return True  # Collision with apple

        # No collision with any apple in the list
        return False

    def eat(self):
        # Get the coordinates of the last part of the snake
        last_x, last_y = self.coordinates[-1]

        # Determine the position of the new body part based on the snake's direction
        if self.direction == "Up":
            new_x, new_y = last_x, last_y + self.size
        elif self.direction == "Down":
            new_x, new_y = last_x, last_y - self.size
        elif self.direction == "Left":
            new_x, new_y = last_x + self.size, last_y
        elif self.direction == "Right":
            new_x, new_y = last_x - self.size, last_y

        # Add the new body part to the snake
        body_part = self.canvas.create_rectangle(new_x, new_y, new_x + self.size, new_y + self.size, fill=self.color)
        self.squares.append(body_part)
        self.coordinates.append((new_x, new_y))
        Apple.m_frenzy_iterator+=1

    def neon_snake(self):
        # Set a random color for the snake
        #self.color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        self.color=self.generate_random_color()
        for square in self.squares:
            square_color = self.generate_random_color()
            self.canvas.itemconfig(square, fill=square_color)


    def delete_snake(self):
        for square in self.squares:
            self.canvas.delete(square)
        self.squares = []
        self.coordinates = []