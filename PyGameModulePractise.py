import pygame as pg
from pygame import display as disp
from pygame import draw as draw
from pygame import Surface as sf
from pygame import Color

Surface = pg.Surface((300, 500))
red = Color.r
draw.circle(Surface, color=red, pos=(200, 200), radius=3, width=0)

