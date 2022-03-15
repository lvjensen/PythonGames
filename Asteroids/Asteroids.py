"""
File: asteroids.py
Author: Logan Jensen

This program implements the asteroids game.
"""
import arcade
import math
import random
from random import randint
from abc import abstractmethod
from abc import ABC

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60
bulletpic = 'images/laser.png'
BULLET_TEXTURE = arcade.load_texture(bulletpic)
bullet_width = BULLET_TEXTURE.width
bullet_height = BULLET_TEXTURE.height
bullet_alpha = 1

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30
shippic = "images/ship.png"
SHIP_TEXTURE = arcade.load_texture(shippic)
ship_width = SHIP_TEXTURE.width
ship_height = SHIP_TEXTURE.height
ship_alpha = 1


INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15
bigpic = "images/large.png"
BIG_ROCK_TEXTURE = arcade.load_texture(bigpic)
big_width = BIG_ROCK_TEXTURE.width
big_height = BIG_ROCK_TEXTURE.height
big_alpha = 1


MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5
mediumpic = "images/medium.png"
MEDIUM_ROCK_TEXTURE = arcade.load_texture(mediumpic)
medium_width = MEDIUM_ROCK_TEXTURE.width
medium_height = MEDIUM_ROCK_TEXTURE.height
medium_alpha = 1

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2
smallpic = "images/small.png"
SMALL_ROCK_TEXTURE = arcade.load_texture(smallpic)
small_width = SMALL_ROCK_TEXTURE.width
small_height = SMALL_ROCK_TEXTURE.height
small_alpha = 1



class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    """

    def __init__(self, width, height):

        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        self.held_keys = set()

        """
        Create ship class, asteroids list and bullets list to be appended with asteroids and then bullets later on.
        Also, distributes the asteroids so they don't start directly over ship.

        """
        self.ship = Ship()
        self.asteroids = []
        self.bullets = []
        for i in range(0,5):
            large = Large()
            self.asteroids.append(large)
        for i in self.asteroids:
            newvar = randint(0,1)
            if newvar == 1:
                i.center.x = random.uniform(0, 300)
            else:
                i.center.x = random.uniform(500, 800)

    def on_draw(self):

        # clear the screen to begin drawing
        arcade.start_render()

        """
        Draw ship, asteroids in asteroids list, bullets in bullets list
        Displays messages based on outcome of game

        """
        self.ship.draw()

        for i in self.bullets:
            i.draw()

        for asteroid in self.asteroids:
            asteroid.draw()

        # Message displayed if ship dies
        if not self.ship.alive:
            dead_text = 'Wo unto the blind that will not see;\nfor they shall perish also.'
            dead_x = 200
            dead_y = SCREEN_HEIGHT // 2
            arcade.draw_text(dead_text, start_x=dead_x, start_y=dead_y, font_size=20, color=arcade.color.YELLOW)

        # Message displayed if game is won
        if not self.asteroids:
            win_text = 'That whosoever believeth in him\nshould not perish,\nbut have eternal life.'
            win_x = 200
            win_y = SCREEN_HEIGHT // 2
            arcade.draw_text(win_text, start_x=win_x, start_y=win_y, font_size=20, color=arcade.color.YELLOW)


    def update(self, delta_time):

        self.check_keys()

        """
        advances ship, asteroids in asteroids list, bullets in bullets list
        cleans up dead asteroids and bullets

        """
        self.ship.advance()
        for i in self.asteroids:
            i.advance()
        for i in self.bullets:
            i.advance()
            i.lives -=1
            if i.lives == 0:
                i.alive = False

        self.cleanup_zombies()
        self.check_off_screen()
        # TODO: Check for collisions
        """
        checks if bullet hits asteroids by measuring distance from asteroids to bullets.
        If hit, calls asteroid's breaks function
        checks if asteroids are too close to ship
        if they are too close, ship is dead
        """

        for bullet in self.bullets:
            for asteroid in self.asteroids:

                if bullet.alive and asteroid.alive:
                    hit_range = bullet.radius + asteroid.radius

                    if (abs(bullet.center.x - asteroid.center.x) < hit_range and
                                abs(bullet.center.y - asteroid.center.y) < hit_range):

                        bullet.alive = False
                        if asteroid.breaks():
                            self.asteroids += asteroid.breaks()
                            asteroid.alive = False

        for asteroid in self.asteroids:
            bad_pilot = asteroid.radius + self.ship.radius

            if (abs(self.ship.center.x - asteroid.center.x) < bad_pilot and
                                abs(self.ship.center.y - asteroid.center.y) < bad_pilot):
                self.ship.alive = False

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.turn_left()

        if arcade.key.RIGHT in self.held_keys:
            self.ship.turn_right()

        if arcade.key.UP in self.held_keys:
            self.ship.speed_up()


        if arcade.key.DOWN in self.held_keys:
            self.ship.slow_down()


    def on_key_press(self, key: int, modifiers: int):
        """
        if space bar is pressed, a bullet is added to the class bullets list
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # TODO: Fire the bullet here!
                bullet = Bullet()
                bullet.center.x = self.ship.center.x
                bullet.center.y = self.ship.center.y
                bullet.fire(self.ship)
                self.bullets.append(bullet)


    def cleanup_zombies(self):

        """
        if bullets and asteroids are not alive, removes bullets and asteroids
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for asteroid in self.asteroids:
            if not asteroid.alive:
                self.asteroids.remove(asteroid)

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)

    def check_off_screen(self):
        """
        checks to see if bullets/asteroids aren't on screen, and if soo calls off screen
        """

        for asteroid in self.asteroids:
            asteroid.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.ship.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

        for i in self.bullets:
            i.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT)


class Point:

    def __init__(self): # define point variables for other classes
        self.x = 0.0
        self.y = 0.0

class Velocity:

    def __init__(self): # define velocities for other classes
        self.dx = 0.0
        self.dy = 0.0


class Fly(ABC): #flying objects class
    """
    The Fly Object class is an class where the other classes receive their framework.
    """

    def __init__(self):
        self.center = Point()
        self.velo = Velocity()
        self.angle = 0
        self.radius = 0
        self.alive = False
        self.turn = 0

    def advance(self): #advance flying objects
        self.center.x += self.velo.dx
        self.center.y += self.velo.dy
        self.angle += self.turn

    @abstractmethod
    def draw(self):
        pass

    def is_off_screen(self, width, height):

        if self.center.x < 0:
            self.center.x = SCREEN_WIDTH
        elif self.center.x > SCREEN_WIDTH:
            self.center.x = 0
        elif self.center.y < 0:
            self.center.y = SCREEN_HEIGHT
        elif self.center.y > SCREEN_HEIGHT:
            self.center.y = 0

    @property #property to reset velocity to zero when dead
    def alive(self):
        return self._alive

    @alive.setter
    def alive(self, value):
        self._alive = value
        if not self._alive:
            self.velo.dx = 0
            self.velo.dy = 0


class Bullet(Fly): #bullet inheriting flying objects
    """
    has the framework for bullets. The fire functions lets the bullet be fired from the ship in the same angle as the ship.
    """

    def __init__(self):
        super().__init__()
        self.radius = BULLET_RADIUS
        self.lives = 60


    def draw(self): #draw bullet
        arcade.draw_texture_rectangle(self.center.x, self.center.y, bullet_width, bullet_height, BULLET_TEXTURE, self.angle, bullet_alpha)

    def fire(self, ship): #Fire depending on angle of rifle
        self.alive = True
        self.angle = ship.angle + 90
        self.velo.dx = math.cos(math.radians(self.angle))*10 + ship.velo.dx
        self.velo.dy = math.sin(math.radians(self.angle))*10 + ship.velo.dy


class Asteroid(Fly): #Asteroid to be inherited
    """
    Creates the general framework for Large, Medium, and Small Asteroids
    """
    def __init__(self):
        super().__init__()
        self.center.y = random.uniform(0, 600)
        self.center.x = random.uniform(0, 800)
        self.alive = True

    @abstractmethod
    def draw(self): #design more in-depth in inherited classes
        pass

    @abstractmethod
    def breaks(self):
        pass


class Large(Asteroid): # Large Asteroid following target class
    """
    These next 3 classes instill the framework of the Large, Medium, and Small Asteroids; inheriting from the general Asteroid class.
    Each have an __init__, draw, and breaks
    """
    def __init__(self):
        super().__init__()
        self.radius = BIG_ROCK_RADIUS
        self.turn = BIG_ROCK_SPIN
        self.velo.dx = random.uniform(-2,2)
        self.velo.dy = random.uniform(-2,2)

    def draw(self): #draw target when alive
        if self.alive == True:
            arcade.draw_texture_rectangle(self.center.x, self.center.y, big_width, big_height, BIG_ROCK_TEXTURE, self.angle, big_alpha)

    def breaks(self): # the Large Asteroid breaks into 2 Medium Asteroids and a Small Asteroid.
        med1 = Medium()
        med1.center.x = self.center.x
        med1.center.y = self.center.y
        med1.velo.dy = self.velo.dy + 2
        med1.velo.dx = self.velo.dx
        med2 = Medium()
        med2.center.x = self.center.x
        med2.center.y = self.center.y
        med2.velo.dy = self.velo.dy - 2
        med2.velo.dx = self.velo.dx
        sm1 = Small()
        sm1.center.x = self.center.x
        sm1.center.y = self.center.y
        sm1.velo.dx = self.velo.dx + 5
        sm1.velo.dy = self.velo.dy
        list = []
        list.append(med1)
        list.append(med2)
        list.append(sm1)
        return list


class Medium(Asteroid):

    def __init__(self):
        super().__init__()
        self.radius = MEDIUM_ROCK_RADIUS
        self.turn = MEDIUM_ROCK_SPIN

    def draw(self): #draw target when alive
        if self.alive == True:
            arcade.draw_texture_rectangle(self.center.x, self.center.y, medium_width, medium_height, MEDIUM_ROCK_TEXTURE, self.angle, medium_alpha)

    def breaks(self):
        list = []
        sm1 = Small()
        sm1.center.x = self.center.x
        sm1.center.y = self.center.y
        sm1.velo.dx = self.velo.dx + 1.5
        sm1.velo.dy = self.velo.dy + 1.5
        list.append(sm1)
        sm2 = Small()
        sm2.center.x = self.center.x
        sm2.center.y = self.center.y
        sm2.velo.dx = self.velo.dx - 1.5
        sm2.velo.dy = self.velo.dy - 1.5
        list.append(sm2)
        return list


class Small(Asteroid):

    def __init__(self):
        super().__init__()
        self.radius = SMALL_ROCK_RADIUS
        self.turn = SMALL_ROCK_SPIN

    def draw(self): #draw target when alive
        if self.alive == True:
            arcade.draw_texture_rectangle(self.center.x, self.center.y, small_width, small_height, SMALL_ROCK_TEXTURE, self.angle, small_alpha)

    def breaks(self):
        bullet = Bullet()
        self.alive = False



class Ship(Fly):

    """
    The ship class creates the original settings of the ship. Also it has the variables that control how it moves.
    """

    def __init__(self):
        super().__init__()
        self.center.x = SCREEN_WIDTH // 2 # ship starts in middle of screen
        self.center.y = SCREEN_HEIGHT // 2
        self.velo._dx = 0 #ship starts not moving
        self.velo._dy = 0
        self.angle = 0
        self.radius = SHIP_RADIUS
        self.alive = True

    def draw(self):
        if self.alive == True:
            arcade.draw_texture_rectangle(self.center.x, self.center.y, ship_width, ship_height, SHIP_TEXTURE, self.angle, ship_alpha)


    def turn_left(self):
        self.angle += 3 #these change the angle of the ship to turn

    def turn_right(self):
        self.angle -= 3

    def speed_up(self): #positive acceleration
        speed = .25
        angle = self.angle + 90
        self.velo.dx += math.cos(math.radians(angle)) * speed
        self.velo.dy += math.sin(math.radians(angle)) * speed

    def slow_down(self): #negative acceleration
        speed =.25
        angle = self.angle + 90
        self.velo.dx -= math.cos(math.radians(angle)) * speed
        self.velo.dy -= math.sin(math.radians(angle)) * speed












# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()
