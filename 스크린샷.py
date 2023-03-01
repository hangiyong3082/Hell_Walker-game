#-*- coding:utf-8 -*-
import pygame as pg, os, time, random, math, sys, json
from pygame.locals import *
from 함수 import *

change_dir('.')

def Screenshot(screen):
    timeTaken = time.asctime()
    timeTaken = timeTaken.replace(" ","_")
    timeTaken = timeTaken.replace(":","_")
    saveFile = resource_path("screenshot")+f"\\{timeTaken}"+".png"
    pg.image.save(screen,saveFile)