'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
#####
Ammaar Siddiqui
Pong
Version 2.0
This program adds collision detection between the paddles and the balls and base level physics. It keeps track of the highscores and displays them after each game.
'''

# Ammaar Siddiqui
# Advanced Computer Programming
# 2/22/19

import pygame
import sys
import time

background = (0, 0, 0)
entity_color = (255, 255, 255)
POINTS1 = 0
POINTS2 = 0
WHITE = (255, 255, 255)

score_display = False


class Entity(pygame.sprite.Sprite):
    """Inherited by any object in the game."""

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # This makes a rectangle around the entity, used for anything
        # from collision to moving around.
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Paddle(Entity):
    """
    Player controlled or AI controlled, main interaction with
    the game
    """

    def __init__(self, x, y, width, height):
        super(Paddle, self).__init__(x, y, width, height)

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(entity_color)


class Player(Paddle):
    """The player controlled Paddle"""

    def __init__(self, x, y, width, height):
        super(Player, self).__init__(x, y, width, height)

        # How many pixels the Player Paddle should move on a given frame.
        self.y_change = 0
        # How many pixels the paddle should move each frame a key is pressed.
        self.y_dist = 5

    def MoveKeyDown(self, key):
        """Responds to a key-down event and moves accordingly"""
        if (key == pygame.K_UP):
            self.y_change += -self.y_dist
        elif (key == pygame.K_DOWN):
            self.y_change += self.y_dist

    def MoveKeyUp(self, key):
        global POINTS1
        global POINTS2
        global score_display
        """Responds to a key-up event and stops movement accordingly"""
        if (key == pygame.K_UP):
            self.y_change += self.y_dist
        elif (key == pygame.K_DOWN):
            self.y_change += -self.y_dist
        if (key == pygame.K_SPACE):
            if score_display:
                POINTS1 = 0
                POINTS2 = 0
                ball.rect.x = window_width / 2
                ball.rect.y = window_height / 2
                score_display = False
                file = open("highscores.txt", "w")
                for score in scores:
                    file.write(score + "\n")
                file.close()

    def update(self):
        """
        Moves the paddle while ensuring it stays in bounds
        """
        # Moves it relative to its current location.
        self.rect.move_ip(0, self.y_change)

        # If the paddle moves off the screen, put it back on.
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > window_height - self.height:
            self.rect.y = window_height - self.height


class Enemy(Paddle):
    """
    AI controlled paddle, simply moves towards the ball
    and nothing else.
    """

    def __init__(self, x, y, width, height):
        super(Enemy, self).__init__(x, y, width, height)

        self.y_change = 5

    def update(self):
        """
        Moves the Paddle while ensuring it stays in bounds
        """
        # Moves the Paddle up if the ball is above,
        # and down if below.
        if ball.rect.y < self.rect.y:
            self.rect.y -= self.y_change
        elif ball.rect.y > self.rect.y:
            self.rect.y += self.y_change

        # The paddle can never go above the window since it follows
        # the ball, but this keeps it from going under.
        if self.rect.y + self.height > window_height:
            self.rect.y = window_height - self.height


class Ball(Entity):
    """
    The ball!  Moves around the screen.
    """

    def __init__(self, x, y, width, height):
        super(Ball, self).__init__(x, y, width, height)

        self.image = pygame.Surface([width, height])
        self.image.fill(entity_color)

        self.x_direction = 1
        # Positive = down, negative = up
        self.y_direction = 1
        # Current speed.
        self.speed = 5

    def update(self):
        global POINTS1
        global POINTS2
        # Move the ball!
        self.rect.move_ip(self.speed * self.x_direction,
                          self.speed * self.y_direction)

        # Keep the ball in bounds, and make it bounce off the sides.

        if self.rect.colliderect(player.rect):
            if self.rect.y < player.rect.y + 25:
                if self.y_direction > 0:
                    self.y_direction *= -1
                elif self.y_direction < 0:
                    self.y_direction *= 1
            if self.rect.y > player.rect.y + 25:
                if self.y_direction > 0:
                    self.y_direction *= 1
                elif self.y_direction < 0:
                    self.y_direction *= -1
            self.x_direction *= -1
            self.speed += 1
            enemy.y_change+= 1.6
        if self.rect.colliderect(enemy.rect):
            if self.rect.y < enemy.rect.y + 25:
                if self.y_direction > 0:
                    self.y_direction *= -1
                elif self.y_direction < 0:
                    self.y_direction *= 1
            if self.rect.y > enemy.rect.y + 25:
                if self.y_direction > 0:
                    self.y_direction *= 1
                elif self.y_direction < 0:
                    self.y_direction *= -1
            self.x_direction *= -1
            self.speed += 1.5

        if self.rect.y < 0:
            self.y_direction *= -1
        elif self.rect.y > window_height - 20:
            self.y_direction *= -1
        if self.rect.x < 0:
            POINTS2 += 1
            self.rect.x = window_width / 2
            self.rect.y = window_height / 2
            self.speed = 5
            enemy.y_change = 5
        elif self.rect.x > window_width - 20:
            POINTS1 += 1
            self.rect.x = window_width / 2
            self.rect.y = window_height / 2
            self.speed = 5
            enemy.y_change = 5


pygame.init()

window_width = 700
window_height = 400
screen = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Pong")

clock = pygame.time.Clock()

ball = Ball(window_width / 2, window_height / 2, 20, 20)
player = Player(20, window_height / 2, 20, 50)
enemy = Enemy(window_width - 40, window_height / 2, 20, 50)

all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(ball)
all_sprites_list.add(player)
all_sprites_list.add(enemy)


def update_score1():  # function changes score
    font = pygame.font.SysFont("comicsansms", 25)
    text = font.render(str(POINTS1), True, (WHITE))
    return text


def update_score2():  # function changes score
    font = pygame.font.SysFont("comicsansms", 25)
    text = font.render(str(POINTS2), True, (WHITE))
    return text


while True:
    # Event processing here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            player.MoveKeyDown(event.key)
        elif event.type == pygame.KEYUP:
            player.MoveKeyUp(event.key)

    for ent in all_sprites_list:
        ent.update()

    screen.fill(background)

    text1 = update_score1()  # updates score
    screen.blit(text1, (300, 25))

    text2 = update_score2()  # updates score
    screen.blit(text2, (400, 25))

    all_sprites_list.draw(screen)

    if POINTS2 >= 3:
        screen.fill(background)
        score_display = True
        file = open("highscores.txt", "r")
        scores = file.readlines()
        file.close()
        scores = [score.replace('\n', '') for score in scores]
        if POINTS1 > int(scores[9]):
            for score in scores:
                if POINTS1 >= int(score):
                    scores.insert(scores.index(score), str(POINTS1))
                    break
            del scores[-1]
        font = pygame.font.SysFont("arialblack", 25)
        highscore_text = font.render("Highscores:", True, (WHITE))
        continue_text = font.render("Press Spacebar to continue", True, (WHITE))
        text1 = font.render("1. " + scores[0], True, (WHITE))
        text2 = font.render("2. " + scores[1], True, (WHITE))
        text3 = font.render("3. " + scores[2], True, (WHITE))
        text4 = font.render("4. " + scores[3], True, (WHITE))
        text5 = font.render("5. " + scores[4], True, (WHITE))
        text6 = font.render("6. " + scores[5], True, (WHITE))
        text7 = font.render("7. " + scores[6], True, (WHITE))
        text8 = font.render("8. " + scores[7], True, (WHITE))
        text9 = font.render("9. " + scores[8], True, (WHITE))
        text10 = font.render("10. " + scores[9], True, (WHITE))
        screen.blit(highscore_text, (250, 0))
        screen.blit(text1, (300, 25))
        screen.blit(text2, (300, 50))
        screen.blit(text3, (300, 75))
        screen.blit(text4, (300, 100))
        screen.blit(text5, (300, 125))
        screen.blit(text6, (300, 150))
        screen.blit(text7, (300, 175))
        screen.blit(text8, (300, 200))
        screen.blit(text9, (300, 225))
        screen.blit(text10, (300, 250))
        screen.blit(continue_text, (175, 300))

    pygame.display.flip()

    clock.tick(60)
