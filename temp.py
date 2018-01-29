from numpy import *;#导入numpy的库函数
import numpy as np; #这个方式使用numpy的函数时，需要以np.开头。
import csv

def direction(last_position,position,car_id):
    direction=0
    deta_y=position[0]-last_position[car_id][0]
    deta_x=position[1]-last_position[car_id][1]
    ### direction in martrix
    if abs(deta_y)>abs(deta_x):
        if deta_y>0:
            direction=3
        else:
            direction=1
    else:
        if deta_x>0:
            direction=2
        else:
            direction=4
    return direction

def follow(lastposition,position,direction,Map):

    if direction==1:
        followers=Map[lastposition[0]:,lastposition[1]]
        
        move=len(followers)
        Map[position[0]:position[0]+move,position[1]]+=followers
        Map[lastposition[0]:,lastposition[1]] -=followers
        
    if direction==2:
        followers=Map[lastposition[0],:lastposition[1]]
        move=lastposition[1]
        Map[position[0],position[1]-move:position[1]]+=followers
        Map[lastposition[0],:lastposition[1]] -=followers
    if direction==3:
        followers=Map[:lastposition[0],lastposition[1]]
        move=len(followers)
        Map[position[0]-move:position[0],position[1]]+=followers
        Map[:lastposition[0],lastposition[1]] -=followers
    if direction==4:
        followers=Map[lastposition[0],lastposition[1]:] 
        move=400-lastposition[1]
        Map[position[0],position[1]:position[1]+move]+=followers
        Map[lastposition[0],lastposition[1]:]-=followers
        
def conflict(Map):
    for i in range(1200):
        for j in range(400):
            if Map[i,j]>1:
                Map[i,j]=1


data=csv.reader(open('data.csv','r'))
i=0
Map=np.zeros([1200,400])
Map=np.matrix(Map)
origin_Map=Map
route=[]
last_position={}
start_time= -inf
for item in data:

    for j in range(len(item)):
        if j==0:
            item[j]=int(item[j],16)
        else:
            item[j]=float(item[j])
            if j==2:
                x=round((item[j]-520000)/5)

            if j==3:
                y=round((item[j]-53000)/5)
    if Map[y,x] != 1:          
        Map[y,x] =1
print('Create Map')  
data=csv.reader(open('data.csv','r'))    
for item in data:
    i+=1  
    for j in range(len(item)):
        if j==0:
            item[j]=int(item[j],16)
        else:
            item[j]=float(item[j])
            if j==2:
                x=round((item[j]-520000)/5)

            if j==3:
                y=round((item[j]-53000)/5)
    if Map[y,x] != 1:          
        Map[y,x] =1
    car_id=item[0]
    car_time=item[1]
    position=[y,x]
    print(i)
    
    if car_time<(start_time+10):
        route[-1].append([car_id,y,x])
        
    else:

        start_time=car_time
        route.append([[car_id,y,x]])
        conflict(Map)
        
       
    if car_id in last_position.keys():
        new_direction=direction(last_position,position, car_id)
        follow(last_position[car_id],position,new_direction,Map)
        
        
    last_position[car_id]=position
    if (car_time- 1493852410)>7200:
        break
       
#create Map csv    
np.savetxt('new.csv', origin_Map, delimiter = ',') 
np.savetxt('taffic.csv', Map, delimiter = ',') 
## determine the direction





    
#每个路口一个dic写转弯车辆统计
#第一个就是出现的频率