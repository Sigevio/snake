class Snake:
    def __init__(self, start_x: int, start_y: int) -> None:
        self.length = 1
        self.direction = 'down'
        self.head = BodyPart(start_x, start_y)
        self.body = []

        self.dead = False
    
    def get_length(self) -> int:
        return len(self.body) + 1

    def move(self, apple_x: int, apple_y: int) -> bool:
        if self.body:
            last_x = self.body[-1].x
            last_y = self.body[-1].y
            for i in range(len(self.body) - 1, -1, -1):
                if i == 0:
                    self.body[i].move(self.head.x, self.head.y)
                else:
                    self.body[i].move(self.body[i-1].x, self.body[i-1].y)
        else:
            last_x = self.head.x
            last_y = self.head.y
        if self.direction == 'down':
            self.head.move(self.head.x, self.head.y+1)
        elif self.direction == 'up':
            self.head.move(self.head.x, self.head.y-1)
        elif self.direction == 'left':
            self.head.move(self.head.x-1, self.head.y)
        elif self.direction == 'right':
            self.head.move(self.head.x+1, self.head.y)
        if self.head.x == apple_x and self.head.y == apple_y:
            self.body.append(BodyPart(last_x, last_y))
        for body_part in self.body:
            if body_part.x == self.head.x and body_part.y == self.head.y:
                self.dead = True
        return self.head.x == apple_x and self.head.y == apple_y

class BodyPart:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
    
    def move(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
