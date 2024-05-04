# Import the pygame module
import pygame
import random
import sys
import os.path
import math


from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_o,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

SEA_HEIGHT = 300

IMAGES_FOLDER = "images"
SOUNDS_FOLDER = "sounds"


def play_sound(sound_file):

    # play sound once
    if sound_file is not None:
        try:
            soundObj = pygame.mixer.Sound(sound_file)
            soundObj.play(0)
        except Exception as error:
            print(f"Failed to play sound. Error message was: {error}")


class Boat(pygame.sprite.Sprite):

    NORMAL_SPEED = 10
    POWER_UP_SPEEED = 50

    def __init__(self):

        super(Boat, self).__init__()

        self.normal_image = pygame.image.load(
            os.path.join(folder, IMAGES_FOLDER, "boat.png")
        ).convert()
        self.power_up_image = pygame.image.load(
            os.path.join(folder, IMAGES_FOLDER, "power_up_boat.png")
        ).convert()

        self._set_normal_image()

        self.rect = self.surf.get_rect(
            center=(
                100,
                SCREEN_HEIGHT / 2,
            )
        )

        self.speed = Boat.NORMAL_SPEED
        self.power_up_duration = 0
        self.power_up_active = False

    def _make_transparent(self):
        transparent_color = self.surf.get_at((0, 0))
        self.surf.set_colorkey(transparent_color, RLEACCEL)

    def move_up(self):
        if (self.rect[1] + self.rect[2]) > SEA_HEIGHT:
            self.rect.move_ip(0, -self.speed)
            self.update_power_up()

    def move_down(self):
        if (self.rect[1] + self.rect[2]) < SCREEN_HEIGHT:
            self.rect.move_ip(0, self.speed)
            self.update_power_up()

    def move_left(self):
        if self.rect[0] > 0:
            self.rect.move_ip(-self.speed, 0)
            self.update_power_up()

    def move_right(self):
        if (self.rect[0] + self.rect[3]) < SCREEN_WIDTH:
            self.rect.move_ip(self.speed, 0)
            self.update_power_up()

    def power_up(self):
        self.speed = Boat.POWER_UP_SPEEED
        self.power_up_active = True
        self.power_up_duration = 5000
        self._set_power_up_image()

    def update_power_up(self):

        if self.power_up_active:
            if self.power_up_duration > 0:
                self.power_up_duration -= self.speed
            else:
                self.power_up_active = False
                self._set_normal_image()
                self.speed = Boat.NORMAL_SPEED

    def _set_normal_image(self):
        self.surf = self.normal_image
        self._make_transparent()

    def _set_power_up_image(self):
        self.surf = self.power_up_image
        self._make_transparent()

    def update(self, pressed_keys):

        up = pressed_keys[K_UP]
        down = pressed_keys[K_DOWN]
        left = pressed_keys[K_LEFT]
        right = pressed_keys[K_RIGHT]
        o = pressed_keys[K_o]

        if o:
            boat.center()

        if right:
            boat.move_right()

        if left:
            boat.move_left()

        if up:
            boat.move_up()

        if down:
            boat.move_down()

        # draw boat
        screen.blit(boat.surf, boat.rect)


class Booster(pygame.sprite.Sprite):

    def __init__(self):
        super(Booster, self).__init__()
        self.surf = pygame.image.load(
            os.path.join(folder, IMAGES_FOLDER, "power_up.png")
        ).convert()
        transparent_color = self.surf.get_at((0, 0))
        self.surf.set_colorkey(transparent_color, RLEACCEL)

        self.rect = self.surf.get_rect(
            center=(
                random.randint(200, SCREEN_WIDTH),
                300,
            )
        )

    @classmethod
    def should_add(cls):

        r = random.randint(0, 1000)

        return r > 997


class Artefact(pygame.sprite.Sprite):

    def __init__(self):
        super(Artefact, self).__init__()
        self.surf = pygame.image.load(
            os.path.join(folder, IMAGES_FOLDER, "treasure.png")
        ).convert()
        transparent_color = self.surf.get_at((0, 0))
        self.surf.set_colorkey(transparent_color, RLEACCEL)

        self.rect = self.surf.get_rect(
            center=(
                random.randint(200, SCREEN_WIDTH),
                300,
            )
        )

    @classmethod
    def should_add(cls):

        r = random.randint(0, 1000)

        return r > 997


class Shark(pygame.sprite.Sprite):

    def __init__(self):

        super(Shark, self).__init__()

        self.shark_image = pygame.image.load(
            os.path.join(folder, IMAGES_FOLDER, "shark.png")
        )

        self.transparent_color_shark = self.shark_image.get_at((0, 0))
        self.shark_image.set_colorkey(self.transparent_color_shark, RLEACCEL)

        self.shark_flip_image = pygame.transform.flip(self.shark_image, True, False)

        self.surf = self.shark_image

        self.rect = self.surf.get_rect(
            center=(
                300,
                600,
            )
        )

        self.shark_step_x = -5
        self.shark_step_y = 1

    def update(self):

        self.rect.move_ip(self.shark_step_x, self.shark_step_y)

        if self.rect[0] < 0:
            self.shark_step_x = 5
            self.surf = self.shark_flip_image

        if self.rect[0] > 800:
            self.shark_step_x = -5
            self.surf = self.shark_image

        if (self.rect[1] + self.rect[3]) > SCREEN_HEIGHT and self.shark_step_y > 0:
            self.shark_step_y *= -1

        if (self.rect[1]) < (SCREEN_HEIGHT - SEA_HEIGHT) and self.shark_step_y < 0:
            self.shark_step_y *= -1

        # draw shark
        screen.blit(self.surf, self.rect)


class JellyFish(pygame.sprite.Sprite):

    def __init__(self):

        super(JellyFish, self).__init__()

        self.image = pygame.image.load(
            os.path.join(
                folder,
                IMAGES_FOLDER,
                "jellyfish.png",
            )
        )

        self.transparent_color_shark = self.image.get_at((0, 0))
        self.image.set_colorkey(self.transparent_color_shark, RLEACCEL)

        self.flip_image = pygame.transform.flip(self.image, True, False)

        self.surf = self.image

        self.rect = self.surf.get_rect(
            center=(
                300,
                600,
            )
        )

    def update(self, player):

        step_x = player.rect[0] - self.rect[0]
        step_y = player.rect[1] - self.rect[1]

        dist = math.sqrt(step_x * step_x + step_y * step_y)

        if dist > 0:
            step_x = int(step_x / dist * 3)
            step_y = int(step_y / dist * 3)

        self.rect.move_ip(step_x, step_y)

        # draw shark
        screen.blit(self.surf, self.rect)


# Setup the clock for a decent framerate

clock = pygame.time.Clock()

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)

running = True

folder = os.path.abspath(os.path.dirname(__file__))

power_up_sound = os.path.join(
    folder,
    SOUNDS_FOLDER,
    "power_up.wav",
)
lose_sound = os.path.join(
    folder,
    SOUNDS_FOLDER,
    "lose.mp3",
)

boat = Boat()
shark = Shark()
jelly = JellyFish()

boosters = pygame.sprite.Group()
sharks = pygame.sprite.Group()
artefacts = pygame.sprite.Group()
jellies = pygame.sprite.Group()

sharks.add(shark)
jellies.add(jelly)

# Set up the font
font = pygame.font.SysFont("Comic Sans MS", 36)

score = 0

while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()

    # Drawing Background
    screen.fill(white)
    pygame.draw.rect(
        screen, blue, pygame.Rect(0, SEA_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    boat.update(pressed_keys)
    shark.update()
    jelly.update(boat)

    if not boat.power_up_active and len(boosters) == 0 and Booster.should_add():
        booster = Booster()
        boosters.add(booster)

    for booster in boosters:
        screen.blit(booster.surf, booster.rect)

    if len(artefacts) == 0 and Artefact.should_add():
        artefact = Artefact()
        artefacts.add(artefact)

    for artefact in artefacts:
        screen.blit(artefact.surf, artefact.rect)

    # Render the score text
    score_text = font.render("Score: " + str(score), True, black)

    # Get the text size
    text_width, text_height = score_text.get_size()

    # Position the score text in the top right corner
    x = SCREEN_WIDTH - text_width - 10  # Adjust the position as needed
    y = 10  # Adjust the position as needed

    # Draw the score text on the window
    screen.blit(score_text, (x, y))

    # update screen
    pygame.display.update()

    if len(pygame.sprite.spritecollide(boat, artefacts, dokill=True)) > 0:
        score += 1

    if len(pygame.sprite.spritecollide(boat, boosters, dokill=True)) > 0:
        boat.power_up()
        if os.path.isfile(power_up_sound):
            play_sound(power_up_sound)

    if len(pygame.sprite.spritecollide(boat, sharks, dokill=True)) > 0:
        if os.path.isfile(lose_sound):
            play_sound(lose_sound)
        pygame.time.delay(5000)
        running = False

    if len(pygame.sprite.spritecollide(boat, jellies, dokill=True)) > 0:
        if os.path.isfile(lose_sound):
            play_sound(lose_sound)
        pygame.time.delay(5000)
        running = False

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)
