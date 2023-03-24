import pygame as pg, os, time, random, math, sys, webbrowser, json
from pygame.locals import *

#점수 저장
def SaveScore(score):
    with open("score data.json") as f:
        data = json.load(f)

    if score > data['score']: data['score'] = score

    with open("score data.json",'w') as f:
        json.dump(data,f,indent=1)

#설정 저장
def SaveSetting(volume,lg,graphic):
    with open("setting data.json",'w') as f:
        data = {"volume":volume,"lg":lg,"graphic":graphic}
        json.dump(data,f,indent=1)

#클리어 횟수 저장
def SaveWin():
    with open("win data.json") as f:
        data = LoadWin()
        data['win'] += 1
    with open("win data.json",'w') as f:
        json.dump(data,f,indent=1)

#점수 불러오기
def LoadScore():
    #점수값이 있으면 로드, 없으면 0으로 저장
    try:
        with open("score data.json") as f:
            data = json.load(f)
    except:
        with open("score data.json",'w') as f:
            data = {'score':0}
            json.dump(data, f,indent=1)
    return data

#설정 불러오기
def LoadSetting():
    try:
        with open("setting data.json") as f:
            data = json.load(f)
    except:
        with open("setting data.json",'w') as f:
            data = {"volume":5,"lg":0,"graphic":1}
            json.dump(data, f,indent=1)
    return data

#클리어 횟수 불러오기
def LoadWin():
    try:
        with open("win data.json") as f:
            data = json.load(f)
    except:
        with open("win data.json",'w') as f:
            data = {"win":0}
            json.dump(data, f,indent=1)
    return data