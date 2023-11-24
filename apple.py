import random





class Apple:
    m_frenzied_tracker = False
    m_frenzy_iterator = -1
    m_existing_apples =[]

    def __init__(self, canvas, size, snake_coordinates):
        self.coordinates = []
        self.canvas = canvas
        self.size = size
        self.color = "red"  # Food color

        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        x = random.randint(1, (canvas_width // self.size) - 1) * self.size
        y = random.randint(1, (canvas_height // self.size) - 1) * self.size
        if self.spawn_point_check(x, y, snake_coordinates):
            self.coordinates.append((x, y))
            self.m_existing_apples.append((x,y))
            # Create a red oval for the food item
            self.oval = self.canvas.create_oval(x, y, x + self.size, y + self.size, fill=self.color)

    def spawn_point_check(self, x, y, snake_coordinates):
        occupied_space = self.m_existing_apples + snake_coordinates
        if [x, y] in occupied_space:
            return False
        return True

    def delete(self):
        self.canvas.delete(self.oval)


    def engage_frenzy(self):
        _m_frenzied_tracker = True
        Apple.m_frenzy_iterator = 1

    def disengage_frenzy(self):
        Apple.m_frenzied_tracker = False
        Apple.m_frenzy_iterator=-1

    def reset(self):
        self.disengage_frenzy()
        self.m_existing_apples = []
        self.coordinates = []
