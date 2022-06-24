# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 17:28:32 2022

@author: YaMaSei
"""

import time
import pymem
from Utils import get_sig

# netvars

cs_gamerules_data = 0x0;
m_ArmorValue = 0x117CC;
m_Collision = 0x320;
m_CollisionGroup = 0x474;
m_Local = 0x2FCC;
m_MoveType = 0x25C;
m_OriginalOwnerXuidHigh = 0x31D4;
m_OriginalOwnerXuidLow = 0x31D0;
m_SurvivalGameRuleDecisionTypes = 0x1328;
m_SurvivalRules = 0xD00;
m_aimPunchAngle = 0x303C;
m_aimPunchAngleVel = 0x3048;
m_angEyeAnglesX = 0x117D0;
m_angEyeAnglesY = 0x117D4;
m_bBombDefused = 0x29C0;
m_bBombPlanted = 0x9A5;
m_bBombTicking = 0x2990;
m_bFreezePeriod = 0x20;
m_bGunGameImmunity = 0x9990;
m_bHasDefuser = 0x117DC;
m_bHasHelmet = 0x117C0;
m_bInReload = 0x32B5;
m_bIsDefusing = 0x997C;
m_bIsQueuedMatchmaking = 0x74;
m_bIsScoped = 0x9974;
m_bIsValveDS = 0x7C;
m_bSpotted = 0x93D;
m_bSpottedByMask = 0x980;
m_bStartedArming = 0x3400;
m_bUseCustomAutoExposureMax = 0x9D9;
m_bUseCustomAutoExposureMin = 0x9D8;
m_bUseCustomBloomScale = 0x9DA;
m_clrRender = 0x70;
m_dwBoneMatrix = 0x26A8;
m_fAccuracyPenalty = 0x3340;
m_fFlags = 0x104;
m_flC4Blow = 0x29A0;
m_flCustomAutoExposureMax = 0x9E0;
m_flCustomAutoExposureMin = 0x9DC;
m_flCustomBloomScale = 0x9E4;
m_flDefuseCountDown = 0x29BC;
m_flDefuseLength = 0x29B8;
m_flFallbackWear = 0x31E0;
m_flFlashDuration = 0x10470;
m_flFlashMaxAlpha = 0x1046C;
m_flLastBoneSetupTime = 0x2928;
m_flLowerBodyYawTarget = 0x9ADC;
m_flNextAttack = 0x2D80;
m_flNextPrimaryAttack = 0x3248;
m_flSimulationTime = 0x268;
m_flTimerLength = 0x29A4;
m_hActiveWeapon = 0x2F08;
m_hBombDefuser = 0x29C4;
m_hMyWeapons = 0x2E08;
m_hObserverTarget = 0x339C;
m_hOwner = 0x29DC;
m_hOwnerEntity = 0x14C;
m_hViewModel = 0x3308;
m_iAccountID = 0x2FD8;
m_iClip1 = 0x3274;
m_iCompetitiveRanking = 0x1A84;
m_iCompetitiveWins = 0x1B88;
m_iCrosshairId = 0x11838;
m_iDefaultFOV = 0x333C;
m_iEntityQuality = 0x2FBC;
m_iFOV = 0x31F4;
m_iFOVStart = 0x31F8;
m_iGlowIndex = 0x10488;
m_iHealth = 0x100;
m_iItemDefinitionIndex = 0x2FBA;
m_iItemIDHigh = 0x2FD0;
m_iMostRecentModelBoneCounter = 0x2690;
m_iObserverMode = 0x3388;
m_iShotsFired = 0x103E0;
m_iState = 0x3268;
m_iTeamNum = 0xF4;
m_lifeState = 0x25F;
m_nBombSite = 0x2994;
m_nFallbackPaintKit = 0x31D8;
m_nFallbackSeed = 0x31DC;
m_nFallbackStatTrak = 0x31E4;
m_nForceBone = 0x268C;
m_nTickBase = 0x3440;
m_nViewModelIndex = 0x29D0;
m_rgflCoordinateFrame = 0x444;
m_szCustomName = 0x304C;
m_szLastPlaceName = 0x35C4;
m_thirdPersonViewAngles = 0x31E8;
m_vecOrigin = 0x138;
m_vecVelocity = 0x114;
m_vecViewOffset = 0x108;
m_viewPunchAngle = 0x3030;
m_zoomLevel = 0x33E0;

# signatures 

csgo_running = False

while not csgo_running:
    try:
        ## pymem
        pm = pymem.Pymem("csgo.exe")
        csgo_running = True
    except Exception:
        time.sleep(5)
        continue

dwLocalPlayer = get_sig(pm, "client.dll", pattern= rb'\x8D\x34\x85....\x89\x15....\x8B\x41\x08\x8B\x48\x04\x83\xF9\xFF', extra=4, offset=3, b_relative=True)
print("dwLocalPlayer -> "+dwLocalPlayer)
dwLocalPlayer = int(dwLocalPlayer,0)
dwClientState = get_sig(pm, "engine.dll", pattern= rb'\xA1....\x33\xD2\x6A\x00\x6A\x00\x33\xC9\x89\xB0', extra=0, offset=1, b_relative=True)
print("dwClientState -> "+dwClientState)
dwClientState = int(dwClientState,0)
dwClientState_ViewAngles = get_sig(pm, "engine.dll", pattern=rb'\xF3\x0F\x11\x86....\xF3\x0F\x10\x44\x24.\xF3\x0F\x11\x86', extra=0, offset=4, b_relative=False)
print("dwClientState_ViewAngles -> "+dwClientState_ViewAngles)
dwClientState_ViewAngles = int(dwClientState_ViewAngles,0)
dwEntityList = get_sig(pm, "client.dll", pattern=rb'\xBB....\x83\xFF\x01\x0F\x8C....\x3B\xF8', extra=0, offset=1, b_relative=True)
print("dwEntityList -> "+dwEntityList)
dwEntityList = int(dwEntityList,0)
dwForceBackward = get_sig(pm, "client.dll", pattern=rb'\x55\x8B\xEC\x51\x53\x8A\x5D\x08', extra=0, offset=287, b_relative=True)
print("dwForceBackward -> "+dwForceBackward)
dwForceBackward = int(dwForceBackward,0)
dwForceForward = get_sig(pm, "client.dll", pattern=rb'\x55\x8B\xEC\x51\x53\x8A\x5D\x08', extra=0, offset=245, b_relative=True)
print("dwForceForward -> "+dwForceForward)
dwForceForward = int(dwForceForward,0)
dwForceJump = get_sig(pm, "client.dll", pattern=rb'\x8B\x0D....\x8B\xD6\x8B\xC1\x83\xCA\x02', extra=0, offset=2, b_relative=True)
print("dwForceJump -> "+dwForceJump)
dwForceJump = int(dwForceJump,0)
dwForceLeft = get_sig(pm, "client.dll", pattern=rb'\x55\x8B\xEC\x51\x53\x8A\x5D\x08', extra=0, offset=465, b_relative=True)
print("dwForceLeft -> "+dwForceLeft)
dwForceLeft = int(dwForceLeft,0)
dwForceRight = get_sig(pm, "client.dll", pattern=rb'\x55\x8B\xEC\x51\x53\x8A\x5D\x08', extra=0, offset=512, b_relative=True)
print("dwForceRight -> "+dwForceRight)
dwForceRight = int(dwForceRight,0)
dwGlowObjectManager = get_sig(pm, "client.dll", pattern=rb'\xA1....\xA8\x01\x75\x4B', extra=4, offset=1, b_relative=True)
print("dwGlowObjectManager -> "+dwGlowObjectManager)
dwGlowObjectManager = int(dwGlowObjectManager,0)
dwViewMatrix = get_sig(pm, "client.dll", pattern=rb'\x0F\x10\x05....\x8D\x85....\xB9', extra=176, offset=3, b_relative=True)
print("dwViewMatrix -> "+dwViewMatrix)
dwViewMatrix = int(dwViewMatrix,0)
m_bDormant = get_sig(pm, "client.dll", pattern=rb'\x8A\x81....\xC3\x32\xC0', extra=8, offset=2, b_relative=False)
print("m_bDormant -> "+m_bDormant)
m_bDormant = int(m_bDormant,0)