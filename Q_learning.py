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


class Blob:
    def __init__(self):
        self.x=np.random.randint(0,SIZE)
        self.y=np.random.randint(0,SIZE)
    def __str__(self):
        return f"{self.x},{self.y}"
    def __sub__(self,other):
        return (self.x-other.x,self.y-other.y)
    def action(self,choice):
        if choice==0 :
            self.move(x=1,y=1)
        elif choice==1 :
           self.move(x=-1,y=-1)
        elif choice==2 :
            self.move(x=-1,y=1)
        elif choice==3 :
            self.move(x=1,y=-1)
    def move(self,x=False,y=False):
        if not x:
            self.x+= np.random.randint(-1,2)
        else:
            self.x+=x
        if not y:
            self.y+= np.random.randint(-1,2)
        else:
            self.y+=y
         
        if self.x<0:
            self.x=0
        elif self.x>SIZE-1:
            self.x=SIZE-1
        if self.y<0:
            self.y=0
        elif self.y>SIZE-1:
            self.y=SIZE-1

if start_q_table is None:
    q_table= {}
    for x1 in range (-SIZE+1,SIZE):
        for y1 in range (-SIZE+1,SIZE):
            for x2 in range (-SIZE+1,SIZE):
                for y2 in range (-SIZE+1,SIZE):
                    q_table[(x1,y1),(x2,y2)]= [np.random.uniform(-5,0) for i in range (4)]
else :
    with open(start_q_table,"rb") as f:
        q_table=pickle.load(f)
episode_rewards=[]    

        
for episode in range (HM_EPISODES):
    player=Blob()
    food=Blob()
    enemy=Blob()
    
    if episode % SHOW_EVERY ==0:
        print(f"on # {episode} , epsilon : {epsilon}")
        print(f"{SHOW_EVERY} ep mean {np.mean (episode_rewards[-SHOW_EVERY:])}")                 
        show=True
   else:
        show=False
    
    episode_reward=0
    for i in range (200):
        obs=(player-food,player-enemy)
        if np.random.random() > epsilon:
            action=np.argmax(q_table[obs])
        else:
            action=np.random.randint(0,4)
            
            #may be later 
            enemy.move()
            food.move()
            ############
        
        if player.x==enemy.x and player.y ==enemy.y:
            reward= -ENEMY_PENALTY
        elif player.x==food.x and player.y ==food.y:
            reward=FOOD_REWARD
        else:
            reward=-MOVE_PENALITY
        
        new_obs=(player-food, player-enemy)
        max_feature_q=np.max(q_table[new_obs])
        current_q=q_table[obs][action]
        
