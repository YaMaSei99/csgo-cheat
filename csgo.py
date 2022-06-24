# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 21:48:44 2021

@author: YaMaSei
"""
import pymem
import sys
import os
import argparse
import distutils.util
import numpy as np
import time
import keyboard as kb
import addresses as ad
import KnifeChanger as kc

from threading import Thread, Lock
from pynput.keyboard import Key, Controller, Listener
from win32api import GetSystemMetrics

parser = argparse.ArgumentParser(description='Cheat arguments')
parser.add_argument('--esp','-esp', type=distutils.util.strtobool, default='true')
parser.add_argument('--aim','-aim', type=distutils.util.strtobool, default='true')
args = parser.parse_args()

    
keyboard = Controller()

## global vars

SCREEN_WIDTH = GetSystemMetrics(0)
SCREEN_HEIGHT = GetSystemMetrics(1)
deltaT = 0.010
counter_start = 0
fullTrigger = True
was_pressed = False
was_pressed_2 = False
was_forced = False
wall_on = True
head = None
enemies = None
angles = None
csgo_running = False
aim = bool(args.aim)
esp = bool(args.esp)

while not csgo_running:
    try:
        ## pymem
        pm = pymem.Pymem("csgo.exe")
        client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
        engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
        player = pm.read_uint(int(client + ad.dwLocalPlayer))
        engine_pointer = pm.read_uint(int(engine + ad.dwClientState))
        csgo_running = True
    except Exception:
        print("waiting for csgo.exe ...")
        time.sleep(5)
        continue

## locks
enemies_lock = Lock()
angles_lock = Lock()
wall_on_lock = Lock()
fullTrigger_lock = Lock()

## methods

def on_press(key):
    if key == Key.end:
        os._exit(0)

def pixelToAngles(x,y,player):
    
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    
    ## 720 Pixel = 45 grad
    dx = x-(SCREEN_WIDTH/2)
    dy = y-(SCREEN_HEIGHT/2)
    
    fov = pm.read_int(player + ad.m_iFOV)
    if not fov == 0:
        distanceToScreen = (SCREEN_WIDTH/2) / np.tan((fov/2) * (np.pi/180))
    else:
        distanceToScreen = (SCREEN_WIDTH/2)
    yaw = np.arctan(dx/distanceToScreen) * (180/np.pi)
    pitch = np.arctan(dy/(np.sqrt(distanceToScreen**2+dx**2))) * (180/np.pi)
    return  pitch,yaw 
                     

def GetPosition(player):
    pos = np.array([])
    for i in range(3):
        cord = pm.read_float(int(player + ad.m_vecOrigin + i * 0x4))
        pos = np.append(pos, cord)
    return pos

# returns pitch, yaw of camera
def GetViewAngles(engine_pointer):
    angles = np.array([])
    for i in range(2):
        angle = pm.read_float(engine_pointer + ad.dwClientState_ViewAngles + i * 0x4)
        angles = np.append(angles, angle)
    return angles

def GetCameraPosition(player):
    pos = np.array([])
    for i in range(3):
        cord = pm.read_float(int(player + ad.m_vecViewOffset + i * 0x4))
        offset = np.append(pos, cord)
        playerPos = GetPosition(player)
    return playerPos + offset

def GetVecVelocity (player):
    vel = np.array([])
    for i in range(3):
        cord = pm.read_float(int(player + ad.m_vecVelocity + i * 0x4))
        vel = np.append(vel, cord)
    return vel

def SetVelocity (vel, player):
    for i in range(3):
        pm.write_float(int(player + ad.m_vecVelocity + i * 0x4), vel[i])
        

def GetHealth (player):
    
    try:
        health = pm.read_int(player + ad.m_iHealth)
        return health
    except Exception:
        raise

def GetTeam(player):
    try:
        return pm.read_int(int(player + ad.m_iTeamNum))
    except pymem.exception.MemoryReadError:
        raise
        
def GetEnemies(client, my_team):
    enemies = np.array([])
    for i in range(65):
        try:
            enemy = pm.read_uint(int(client + ad.dwEntityList + i * 0x10))
            enemy_team = GetTeam(enemy)
            dormant = IsDormant(enemy)  
            if enemy_team != my_team and not dormant: ##
                enemies = np.append(enemies, enemy)
        except pymem.exception.MemoryReadError:
            continue
    return enemies

## Does the player exist

def IsDormant(player):
    try:
        return pm.read_bool(int(player + ad.m_bDormant))
    except pymem.exception.MemoryReadError:
        return True

# Get WorldPos of bone. BoneID 8 = Head

def GetBonePos(player, boneID=8):
    try:
        base = pm.read_uint(int(player + ad.m_dwBoneMatrix))
        bone = np.zeros(3)
        bone[0] = pm.read_float(base + 0x30 * boneID + 0x0C)
        bone[1] = pm.read_float(base + 0x30 * boneID + 0x1C)
        bone[2] = pm.read_float(base + 0x30 * boneID + 0x2C)
    except pymem.exception.MemoryReadError:
        raise
    return bone

# Snap to head - simulated mouse input/ write viewAngles

def UpdateViewAngles (head, client, engine_pointer, player, adjust_x = 0, adjust_y = 0, maxDeltaAngle = 3):
    
    if  head is None:
        return None
    
    pos = WorldToScreen(head, client)
    
    if pos is None:
        return None
    
    pos[0] += adjust_x
    pos[1] -= adjust_y
    d_pitch, d_yaw = pixelToAngles(pos[0], pos[1], player)
    
    if np.absolute(d_pitch) > maxDeltaAngle or np.absolute(d_yaw) > maxDeltaAngle:
        return None
    
    pitch, yaw = GetViewAngles(engine_pointer)
    pitch = pitch + d_pitch
    yaw = yaw - d_yaw
    
    if np.absolute(pitch) > 180:
        if pitch < 0:
            pitch = pitch + 360
        else:
            pitch = pitch - 360
    
    pitch = np.clip(pitch, -179, 179)
    
    if np.absolute(yaw) > 180:
        if yaw < 0:
            yaw = yaw + 360
        else:
            yaw = yaw - 360
    
    yaw = np.clip(yaw, -179, 179)
    
    angles = np.array([pitch,yaw])
    return angles
       

def ClosestEnemyAlive (client, enemies):
    
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    
    screenCenter = np.array([SCREEN_WIDTH/2,SCREEN_HEIGHT/2])
    distance = np.Infinity
    closest = None
    for enemy in enemies:
        try:
            e_health = pm.read_int(int(enemy + ad.m_iHealth))
            if not IsDormant(enemy) and e_health > 0:
                e_pos = GetPosition(enemy)
                e_screen = WorldToScreen(e_pos, client)
                if e_screen is None:
                    continue
                d = np.linalg.norm(e_screen - screenCenter)
                if d < distance:
                    distance = d
                    closest = enemy
        except pymem.exception.MemoryReadError:
            continue
    return closest


def RotateVector (pitch, yaw, vec): # pitch, -yaw
    
    pitch = pitch * (np.pi/180)
    yaw = yaw * (np.pi/180)
    
    Rx = np.array([[1,      0,           0        ],
                   [0,np.cos(pitch),-np.sin(pitch)],
                   [0,np.sin(pitch),np.cos(pitch) ]])
    
    Rz = np.array([[np.cos(yaw),-np.sin(yaw), 0],
                   [np.sin(yaw),np.cos(yaw),  0],
                   [    0,            0,      1]])
    
    M = np.matmul(Rx,Rz)
    return np.matmul(M, vec)

    
def GetViewMatrix(client):
    m = np.array([])
    base = client + ad.dwViewMatrix
    for i in range(4):
        for j in range(4):
            m = np.append(m, pm.read_float(base + i * 0x10 + j * 0x4))
    m = m.reshape(4,4) 
    return m

def WorldToScreen (point, client):
    
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    
    vm = GetViewMatrix(client)
    point = np.append(point,1).reshape(4,1)
    clip = np.matmul(vm, point).reshape(4) # clip coordinates
    if clip[3] < 1:
        return
    ndc = clip / clip[3] # normalized device space
    ndc[1] = -1* ndc[1]
    
    x = (SCREEN_WIDTH/2)* ndc[0] + ndc[0] + (SCREEN_WIDTH/2) # window cod
    y = (SCREEN_HEIGHT/2)* ndc[1] + ndc[1] + (SCREEN_HEIGHT/2) 
    
    #if x >= 0 and x < 1440 and y >= 0 and y < 1080:
    return np.array([x,y])

def Esp(e_lock, w_lock):
    
    global enemies
    global counter_start
    global wall_on
    
    counter_start = 0
    
    while True:
        time.sleep(0.017)
        glowObjectManager = pm.read_uint(client + ad.dwGlowObjectManager)
        w_lock.acquire()
        if wall_on:
            w_lock.release()
            t = time.time()
            if t - counter_start > deltaT:
                e_lock.acquire()
                if  not enemies is None :
                    for enemy in enemies:
                        
                        try:
                        
                            glowIndex = pm.read_uint(int(enemy + ad.m_iGlowIndex))
                            
                            pm.write_float(glowObjectManager + (glowIndex * 0x38) + 0x8, 1.0)
                            pm.write_float(glowObjectManager + (glowIndex * 0x38) + 0xC, 0.0)
                            pm.write_float(glowObjectManager + (glowIndex * 0x38) + 0x10, 0.0)
                            pm.write_float(glowObjectManager + (glowIndex * 0x38) + 0x14, 0.7)
                            
                            pm.write_bool(glowObjectManager + (glowIndex * 0x38) + 0x27, True)
                            pm.write_bool(glowObjectManager + (glowIndex * 0x38) + 0x28, True)
                        
                        except Exception:
                            continue
                e_lock.release()
                counter_start = time.time()
        else:
            w_lock.release()
   
def WriteViewAngles (pitch, yaw, engine_pointer):
    try:
        pm.write_float(engine_pointer + ad.dwClientState_ViewAngles, pitch)
        pm.write_float(engine_pointer + ad.dwClientState_ViewAngles + 0x4, yaw)
    except Exception as e:
        print(e)

def AimLock (angles_lock, fullTrigger_lock):
    
    global engine_pointer
    global angles
    global fullTrigger
    
    player = pm.read_uint(int(client + ad.dwLocalPlayer))
    
    while True:
        time.sleep(0.0001)
        
        if kb.is_pressed('alt'): #GetAsyncKeyState(0x01)
            fullTrigger_lock.acquire()
            if fullTrigger:
                angles_lock.acquire()
                if not angles is None:
                    SetVelocity(np.zeros(3), player)
                    WriteViewAngles(angles[0], angles[1], engine_pointer)
                angles_lock.release()
            fullTrigger_lock.release()
        

def ForceUpdate():
    pm.write_int(int(engine + ad.dwClientState + ad.clientstate_delta_ticks), -1)
    
def GetVisible(enemy):
    return pm.read_bool(enemy + ad.m_bSpottedByMask)

def AutoStop(player, client, engine_pointer):
    
    pitch, yaw = GetViewAngles(engine_pointer)
    vec = GetVecVelocity(player)
    vec = RotateVector(pitch, -yaw, vec)
    velocity = np.linalg.norm(vec)
    
    if not kb.is_pressed('w') and  not kb.is_pressed('s') and not kb.is_pressed('a') and not kb.is_pressed('d') and velocity >= 28.29:
        if vec[0] >= 20: # forward
            pm.write_int(client + ad.dwForceBackward, 6)
        if vec[0] <= 20: # backward
            pm.write_int(client + ad.dwForceForward, 6)
        if vec[1] >= 20: # left
            pm.write_int(client + ad.dwForceRight, 6)
        if vec[1] <= 20: # right
            pm.write_int(client + ad.dwForceLeft, 6)

def BHop (player, client):
 
    if not kb.is_pressed('space'):
        return
    
    flags = pm.read_int(player + ad.m_fFlags)
    if flags == 257:
        pm.write_int(client + ad.dwForceJump, 6)
        time.sleep(0.010)                            

def startThreads ():
    
    os.system("cls")
    print("\n"+ "###########################" + "\n" + "## CSGO CHEAT by YaMaSei ##" + "\n" + "###########################" + "\n")
    
    ## Threads
    
    wallHack = Thread(name="ESP", target=Esp, args=(enemies_lock,wall_on_lock))
    aimBot = Thread(name="Aimbot", target=AimLock, args=(angles_lock, fullTrigger_lock))
    skinChanger = Thread(name= "knifeChanger", target=kc.changeKnife, args=())
    
    if esp:
        wallHack.start()
        print("esp active")
    if aim:
        aimBot.start()
        print("aimbot active")
    skinChanger.start()
    print("knife/skin changer active")

## main

InGame = False

while not InGame:
    try:
        player = pm.read_uint(int(client + ad.dwLocalPlayer))
        pos = GetPosition(player)
        if not pos is None:
            time.sleep(1)
            startThreads()
            InGame = True
    except Exception:
        print("waiting for connection")
        time.sleep(5)
        continue
                      
with Listener(on_press=on_press) as listener:
    
    skin_counter_start = 0
    
    while True:
        
        time.sleep(0.0001)
        try:
            
            ## find closest enemy
            
            player = pm.read_uint(int(client + ad.dwLocalPlayer))
            my_team = GetTeam(player)
            enemies_lock.acquire()
            enemies = GetEnemies(client, my_team)
            enemies_lock.release()
            closest = ClosestEnemyAlive(client, enemies)

            # auto bhop
            BHop(player, client)
    
            ## No flash
            pm.write_float(player + ad.m_flFlashMaxAlpha, float(0))
    
            if GetHealth(player) <= 0 or closest is None:
                head = None
            else:
                head = GetBonePos(closest)
            
            ## update viewAngles for locking on closest enemy
            
            angles_lock.acquire()    
            angles = UpdateViewAngles(head, client, engine_pointer, player)
            angles_lock.release()
            
            ## toggle walls on/off
            
            if kb.is_pressed('+'):
                if not was_pressed:
                    wall_on_lock.acquire()
                    wall_on = not wall_on
                    wall_on_lock.release()
                    if wall_on:
                        print("walls on")
                    else:
                        print("walls off")
                    was_pressed = True
            else:
                was_pressed = False
                
            if kb.is_pressed('f1'):
                if not was_pressed_2:
                    fullTrigger_lock.acquire()
                    fullTrigger = not fullTrigger
                    if fullTrigger:
                        print("aim lock on")
                    else:
                        print("aim lock off")
                    fullTrigger_lock.release()
                    was_pressed_2 = True
            else:
                was_pressed_2 = False
             
        except Exception:
            continue
    
    








        



