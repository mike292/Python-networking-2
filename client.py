import pygame
from network import Network

WIDTH = 500
HEIGHT = 500
BODY = (WIDTH, HEIGHT)
BACKGROUND = (255, 255, 255)  # white
GREEN = (0, 255, 0)
RED = (255, 0, 0)
window = pygame.display.set_mode(BODY)
pygame.display.set_caption("Client")

clientNumber = 0


class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.velocity = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.x += self.velocity
        if keys[pygame.K_UP]:
            self.y -= self.velocity
        if keys[pygame.K_DOWN]:
            self.y += self.velocity

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


def readPosition(position):
    position = position.split(",")
    return int(position[0]), int(position[1])


def makePosition(tuple):  # creates a tuple
    return str(tuple[0]) + "," + str(tuple[1])


def draw(window, player, player2):

    window.fill(BACKGROUND)
    player.draw(window)
    player2.draw(window)
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    network = Network()
    startPosition = readPosition(network.getPos())
    player = Player(startPosition[0], startPosition[1], 100, 100, GREEN)
    player2 = Player(0, 0, 100, 100, RED)

    run = True
    while run:
        clock.tick(60)

        # send this player's current position and receives the position of player 2
        playerPosition = (player.x, player.y)
        p2pos = readPosition(network.send(makePosition(playerPosition)))
        player2.x = p2pos[0]
        player2.y = p2pos[1]
        player2.update()  # sets the player 2's position

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        player.move()
        draw(window, player, player2)


main()
pygame.quit()
