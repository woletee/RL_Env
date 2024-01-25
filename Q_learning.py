import numpy as np
from PIL import Image 
import cv2
import matplotlib.pyplot as plt
import pickle 
from matplotlib import style
import time 

style.use("ggplot")

SIZE=10
HM_EPISODES=25000
MOVE_PENALITY=1
ENEMY_PENALTY=300
FOOD_REWARD=25
epsilon=0.9
EPS_DECAY=0.9998
SHOW_EVERY=3000



start_q_table=None #or file name if you have an exisiting q_table 

LEARNING_RATE=0.1
DISCOUNT=0.95

PLAYER_N=1
FOOD_N=2
ENEMY_N=3

d={1:(255,175,0),
   2:(0,255,0),
   3:(0,0,255)}
