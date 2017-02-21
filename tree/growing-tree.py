import pygame
import sys
import time
import math

class Twig:
    def __init__(self, start, speed, accel, scale, steps, depth):
        """
        self.branch_steps = 4
        self.speed_decay = 0.9
        """
        self.branch_angle = 0.7
        self.branch_side = 1.0

        self.depth = depth - 1
        self.points = [start, start]
        self.children = []

        #self.points.append(start)
        self.speed = speed
        self.accel = accel
        self.scale = scale
        self.steps = steps

        self.stepCount = 0

        self.ispeed = speed
        self.iaccel = accel


    def mod2(self, vec):
        return vec[0]*vec[0] + vec[1] * vec[1]


    def sub(self, vec1, vec2):
        return (vec1[0] - vec2[0], vec1[1] - vec2[1])


    def add(self, vec1, vec2):
        return (vec1[0] + vec2[0], vec1[1] + vec2[1])


    def mul(sel, vec, fact):
        return (vec[0] * fact, vec[1] * fact)

    def rotate(self, vec, a):
		x, y = vec
		x1 = x * math.cos(a) - y * math.sin(a)
		y1 = x * math.sin(a) + y * math.cos(a)
		return (x1 , y1)


    def grow(self): 

        if self.stepCount > self.steps:
            return
        self.stepCount += 1

        if math.sqrt(self.mod2(self.speed)) <= 1:
            return
            
        if self.depth < 0:
            return

        self.points[0] = self.points[1]
        self.points[1] = self.add(self.points[1], self.mul(self.speed, self.scale))
        self.branch()

        self.speed = self.add(self.speed, self.accel)
        
        for child in self.children:
            child.grow()
        """
        if self.depth < 0:
            return

        if self.steps >= self.branch_steps:
            return
            
        #if self.mod2(self.speed) <= 150:
        #    return
            
        #self.points.append(self.add(self.points[-1], self.speed))
        self.points[0] = self.points[1]
        self.points[1] = self.add(self.points[1], self.speed)

        self.speed = self.mul(self.speed, self.speed_decay)

        self.steps += 1

        if self.steps >= self.branch_steps:
            self.branch()
        """


    def branch(self):
        self.branch_angle *= -1
        angle = self.branch_angle * self.branch_side
        self.children.append(
            Twig(
                self.points[-1],
                self.rotate(self.speed, angle),
                self.rotate(self.accel, angle),
                self.scale * 0.3,
                self.steps,
                self.depth
            )
        )

        self.branch_angle *= -1
        angle = self.branch_angle * self.branch_side
        self.children.append(
            Twig(
                self.points[-1],
                self.rotate(self.speed, angle),
                self.rotate(self.accel, angle),
                self.scale * 0.3,
                self.steps,
                self.depth
            )
        )
        

    def draw(self, surface):
        pygame.draw.lines(surface, (255, 255, 255), True, self.points, 1)
        for child in self.children:
            child.draw(surface)
        

pygame.init()
screen = pygame.display.set_mode((800,600))

tree = Twig((400, 600), (0, -30), (0, 3), 1.0, 10, 4)

while True:
    #screen.fill((0,0,0))
    tree.grow()
    tree.draw(screen)
    pygame.display.update()

    time.sleep(0.1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
