import os, sys, pygame
from pygame.locals import *
from math import *

pygame.init()

path, file_name = os.path.split(__file__)
path = os.path.join(path, 'data')

WIDTH = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 60

MAGENTA = Color(255, 0, 255)

pygame.mouse.set_visible(False)
pygame.display.set_caption('Mario Kart')


class Driver(object):
    def __init__(self, image, start_pos):
        self.surface = pygame.image.load(os.path.join(path, image)).convert()
        self.surface.set_colorkey(MAGENTA)
        self.surface = pygame.transform.scale(self.surface, (64, 64))

        self.pos = list(start_pos)
        self.angle = 0
        self.velocity = 0

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[K_a] or keys[K_LEFT]:
            self.angle -= 14 / (1 + e**(-0.3 * self.velocity)) - 7
            #Sigmoid function to contain the angular velocity between 7 and -7

        if keys[K_d] or keys[K_RIGHT]:
            self.angle += 14 / (1 + e**(-0.3 * self.velocity)) - 7

        if keys[K_w] or keys[K_UP]:
            self.velocity += 3

        elif keys[K_s] or keys[K_DOWN]:
            self.velocity -= 1

        self.velocity *= 0.85

        self.pos[0] += self.velocity * sin(radians(self.angle))
        self.pos[1] -= self.velocity * cos(radians(self.angle))

    def render(self):
        SCREEN.blit(self.surface, (WIDTH / 2 - 32, HEIGHT / 2 - 32))


class Track(object):
    def __init__(self, image, tilt=1, zoom=1):
        self.surface = pygame.image.load(os.path.join(path,
                                                      image)).convert_alpha()
        self.angle = 0
        self.tilt = tilt
        self.zoom = zoom
        self.rect = self.surface.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

        self.image = self.surface
        self.image_rect = self.image.get_rect()

    def render(self, angle, center=(0, 0)):
        self.angle = angle

        self.image = self.surface
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.image_rect = self.image.get_rect()

        self.image = pygame.transform.scale(
            self.image,
            (int(self.image_rect.width * self.zoom),
             int((self.image_rect.height * self.zoom) / self.tilt)))

        self.image_rect = self.image.get_rect(center=(
            self.rect.centerx -
            ((center[0] * self.zoom) * cos(radians(-self.angle)) -
             (center[1] * self.zoom) * sin(radians(-self.angle))),
            self.rect.centery -
            ((center[0] * self.zoom) * sin(radians(-self.angle)) +
             (center[1] * self.zoom) * cos(radians(-self.angle))) / self.tilt))

        SCREEN.blit(self.image, self.image_rect)


def main():
    track = Track('MushroomCup1.png', tilt=4, zoom=7)
    toad = Driver('Toad Sprite.png', (408, 90))

    while True:
        SCREEN.fill((255, 255, 255))

        toad.move()

        track.render(toad.angle, toad.pos)
        toad.render()

        events = pygame.event.get()
        for event in events:
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        CLOCK.tick(FPS)


if __name__ == '__main__':
    main()
