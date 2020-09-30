import arcade
import math
import random
from random import randint
from abc import abstractmethod
from abc import ABC

# These are Global constants to use throughout the game
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500

RIFLE_WIDTH = 100
RIFLE_HEIGHT = 20
RIFLE_COLOR = arcade.color.DARK_RED

BULLET_RADIUS = 3
BULLET_COLOR = arcade.color.BLACK_OLIVE
BULLET_SPEED = 10

TARGET_RADIUS = 20
TARGET_COLOR = arcade.color.CARROT_ORANGE
TARGET_SAFE_COLOR = arcade.color.AIR_FORCE_BLUE
TARGET_SAFE_RADIUS = 15




class Rifle:
    """
    The rifle is a rectangle that tracks the mouse.
    """
    def __init__(self):
        self.center = Point()
        self.center.x = 0
        self.center.y = 0

        self.angle = 45

    def draw(self):
        arcade.draw_rectangle_filled(self.center.x, self.center.y, RIFLE_WIDTH, RIFLE_HEIGHT, RIFLE_COLOR, self.angle)


class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)

        self.rifle = Rifle()
        self.score = 0

        self.bullets = []

        # TODO: Create a list for your targets (similar to the above bullets)
        self.targets = []

        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # draw each object
        self.rifle.draw()

        for bullet in self.bullets:
            bullet.draw()

        # TODO: iterate through your targets and draw them...

        for i in self.targets:
            i.draw()

        self.draw_score()

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.NAVY_BLUE)

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_collisions()
        self.check_off_screen()

        # decide if we should start a target
        if random.randint(1, 50) == 1:
            self.create_target()

        for bullet in self.bullets:
            bullet.advance()

        # TODO: Iterate through your targets and tell them to advance

        for i in self.targets:
            i.advance()

    def create_target(self):
        """
        Creates a new target of a random type and adds it to the list.
        :return:
        """

        # TODO: Decide what type of target to create and append it to the list
        ran = randint(1,3)
        if ran == 1:
            target = Standard()
        elif ran == 2:
            target = Safe()
        elif ran == 3:
            target = Strong()

        self.targets.append(target)

    def check_collisions(self):
        """
        Checks to see if bullets have hit targets.
        Updates scores and removes dead items.
        :return:
        """

        # NOTE: This assumes you named your targets list "targets"

        for bullet in self.bullets:
            for target in self.targets:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and target.alive:
                    too_close = bullet.radius + target.radius

                    if (abs(bullet.center.x - target.center.x) < too_close and
                                abs(bullet.center.y - target.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False
                        self.score += target.hit()

                        # We will wait to remove the dead objects until after we
                        # finish going through the list

        # Now, check for anything that is dead, and remove it
        self.cleanup_zombies()

    def cleanup_zombies(self):
        """
        Removes any dead bullets or targets from the list.
        :return:
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for target in self.targets:
            if not target.alive:
                self.targets.remove(target)

    def check_off_screen(self):
        """
        Checks to see if bullets or targets have left the screen
        and if so, removes them from their lists.
        :return:
        """
        for bullet in self.bullets:
            if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.bullets.remove(bullet)

        for target in self.targets:
            if target.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.targets.remove(target)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # set the rifle angle in degrees
        self.rifle.angle = self._get_angle_degrees(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # Fire!
        angle = self._get_angle_degrees(x, y)

        bullet = Bullet()
        bullet.fire(angle)

        self.bullets.append(bullet)

    def _get_angle_degrees(self, x, y):
        """
        Gets the value of an angle (in degrees) defined
        by the provided x and y.
        """
        # get the angle in radians
        angle_radians = math.atan2(y, x)

        # convert to degrees
        angle_degrees = math.degrees(angle_radians)

        return angle_degrees

# Creates the game and starts it going

class Point:

    def __init__(self): # define random point variables
        self.x = 0.0
        self.y = 0.0

class Velocity:

    def __init__(self): # define random velocities
        self.dx = random.uniform(1, 5)
        self.dy = random.uniform(-5, 5)

class Fly(ABC): #flying objects class

    def __init__(self):
        self.center = Point()
        self.velo = Velocity()
        self.radius = 0
        self.alive = False

    def advance(self): #advance flying objects
        self.center.x += self.velo.dx
        self.center.y += self.velo.dy

    @abstractmethod
    def draw(self): #design later
        pass

    def is_off_screen(self, screen_width, screen_height): #when objects leave screen
        if self.center.x > screen_width + 10:
            self.alive = False
            return True
        if self.center.y > screen_height or self.center.y <0:
            self.alive = False
            return True


class Bullet(Fly): #bullet inheriting flying objects

    def __init__(self):
        super().__init__()
        self.radius = BULLET_RADIUS

    def draw(self): #draw bullet
        arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, BULLET_COLOR)

    def fire(self, angle): #Fire depending on angle of rifle
        self.alive = True
        self.draw()
        self.velo.dx = math.cos(math.radians(angle))*20
        self.velo.dy = math.sin(math.radians(angle))*20
        self.advance()


class Target(Fly): #target to be inherited

    def __init__(self):
        super().__init__()
        self.radius = TARGET_RADIUS
        self.center.y = random.uniform(250, 500)
        self.alive = True

    @abstractmethod
    def draw(self): #design more in-depth in inherited classes
        pass

    @abstractmethod
    def hit(self):
        pass

class Standard(Target): # standard target following target class

    def __init__(self):
        super().__init__()

    def draw(self): #draw target when alive
        if self.alive == True:
            arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, TARGET_COLOR)

    def hit(self): #target dies and gives points
        bullet = Bullet()
        self.alive = False
        return 5

class Strong(Target): #Strong target following target class

    def __init__(self):
        super().__init__()
        self.lives = 3

    def draw(self): # draw target when it is alive with the amount of lives it has
        if self.alive == True:
            arcade.draw_circle_outline(self.center.x, self.center.y, self.radius, TARGET_COLOR)
            text_x = self.center.x - (self.radius / 2)
            text_y = self.center.y - (self.radius / 2)
            arcade.draw_text(repr(self.lives), text_x, text_y, TARGET_COLOR, font_size=20)


    def hit(self): #Extra strong target, requires 3 hits. Loses 1 life with each hit
        bullet = Bullet()
        too_close = bullet.radius + self.radius
        if self.lives > 1:
            self.lives -= 1
            return 0
        elif self.lives == 1:
            self.alive = False
            return 15


class Safe(Target): #Blue Safe Target

    def __init__(self): # Set Variables
        super().__init__()
        self.radius = TARGET_SAFE_RADIUS

    def draw(self): #Draw Safe target when it is alive
        if self.alive == True:
            arcade.draw_circle_filled(self.center.x, self.center.y, self.radius, TARGET_SAFE_COLOR)


    def hit(self): #Don't hit the safe target, you lose points!
        bullet = Bullet()
        self.alive = False
        return -10



window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()
