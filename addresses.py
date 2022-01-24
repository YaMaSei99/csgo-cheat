# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 20:36:10 2021

@author: YaMaSei 
@netvars: https://github.com/frk1/hazedumper
"""
import pymem
import time
import re

csgo_running = False

while not csgo_running:
    try:
        pm = pymem.Pymem( "csgo.exe" )
        client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
        engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
        csgo_running = True
    except Exception:
        print("Waiting for csgo.exe ...")
        time.sleep(5)
        continue

def getSig(modname, pattern, offset=0, extra=0, relative=True, default= 0x0):
    try:
        pm = pymem.Pymem("csgo.exe")
        module = pymem.process.module_from_name(pm.process_handle, modname)
        bytes = pm.read_bytes(module.lpBaseOfDll, module.SizeOfImage)
        match = re.search(pattern, bytes).start()
        non_relative = pm.read_int(module.lpBaseOfDll + match + offset) + extra
        yes_relative = pm.read_int(module.lpBaseOfDll + match + offset) + extra - module.lpBaseOfDll
        return "0x{:X}".format(yes_relative) if relative else "0x{:X}".format(non_relative)
    except Exception:
        return default

## netvars

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

## Signatures

dwSetClanTag = 0x8A290;
dwbSendPackets = 0xD93D2;
is_c4_owner = 0x3C5890;
set_abs_angles = 0x1E5010;
set_abs_origin = 0x1E4E50;

## Sig scanning

print("scanning signatures ...")

anim_overlays = int(getSig("client.dll", rb'\x8B\x89....\x8D\x0C\xD1',2,0,False,hex(0x2990)),0)
clientstate_choked_commands = int(getSig("engine.dll", rb'\x8B\x87....\x41',2,0,False,hex(0x4D30)),0)
clientstate_delta_ticks = int(getSig("engine.dll", rb'\xC7\x87........\xFF\x15....\x83\xC4\x08',2,0,False,hex(0x174)),0)
clientstate_last_outgoing_command = int(getSig("engine.dll", rb'\x8B\x8F....\x8B\x87....\x41',2,0,False,hex(0x4D2C)),0)
clientstate_net_channel = int(getSig("engine.dll", rb'\x8B\x8F....\x8B\x01\x8B\x40\x18',2,0,False,hex(0x9C)),0)
convar_name_hash_table = int(getSig("vstdlib.dll", rb'\x8B\x3C\x85',3,0,True,hex(0x2F0F8)),0)
dwClientState = int(getSig("engine.dll", rb'\xA1....\x33\xD2\x6A\x00\x6A\x00\x33\xC9\x89\xB0',1,0,True,hex(0x589FC4)),0)
dwClientState_GetLocalPlayer = int(getSig("engine.dll", rb'\x8B\x80....\x40\xC3',2,0,False,hex(0x180)),0)
dwClientState_IsHLTV = int(getSig("engine.dll", rb'\x80\xBF.....\x0F\x84....\x32\xDB',2,0,False,hex(0x4D48)),0)
dwClientState_Map = int(getSig("engine.dll", rb'\x05....\xC3\xCC\xCC\xCC\xCC\xCC\xCC\xCC\xA1',1,0,False,hex(0x28C)),0)
dwClientState_MapDirectory = int(getSig("engine.dll", rb'\xB8....\xC3\x05....\xC3',7,0,False,hex(0x188)),0)
dwClientState_MaxPlayer = int(getSig("engine.dll", rb'\xA1....\x8B\x80....\xC3\xCC\xCC\xCC\xCC\x55\x8B\xEC\x8A\x45\x08',7,0,False,hex(0x388)),0)
dwClientState_PlayerInfo = int(getSig("engine.dll", rb'\x8B\x89....\x85\xC9\x0F\x84....\x8B\x01',2,0,False,hex(0x52C0)),0)
dwClientState_State = int(getSig("engine.dll", rb'\x83\xB8.....\x0F\x94\xC0\xC3',2,0,False,hex(0x108)),0)
dwClientState_ViewAngles = int(getSig("engine.dll", rb'\xF3\x0F\x11\x86....\xF3\x0F\x10\x44\x24.\xF3\x0F\x11\x86',4,0,False,hex(0x4D90)),0)
dwEntityList = int(getSig("client.dll", rb'\xBB....\x83\xFF\x01\x0F\x8C....\x3B\xF8',1,0,True,hex(0x4DD1E1C)),0)
dwForceAttack = int(getSig("client.dll", rb'\x89\x0D....\x8B\x0D....\x8B\xF2\x8B\xC1\x83\xCE\x04',2,0,True,hex(0x32022D0)),0)
dwForceAttack2 = int(getSig("client.dll", rb'\x89\x0D....\x8B\x0D\x8B\xF2\x8B\xC1\x83\xCE\x04',2,36,True,hex(0x32022F4)),0)
dwForceBackward = int(getSig("client.dll", rb'\x55\x8B\xEC\x51\x53\x8A\x5D\x08',287,0,True,hex(0x320230C)),0)
dwForceForward = int(getSig("client.dll", rb'\x55\x8B\xEC\x51\x53\x8A\x5D\x08',245,0,True,hex(0x3202300)),0)
dwForceJump = int(getSig("client.dll", rb'\x8B\x0D....\x8B\xD6\x8B\xC1\x83\xCA\x02',2,0,True,hex(0x527BC98)),0)
dwForceLeft = int(getSig("client.dll", rb'\x55\x8B\xEC\x51\x53\x8A\x5D\x08',465,0,True,hex(0x3202318)),0)
dwForceRight = int(getSig("client.dll", rb'\x55\x8B\xEC\x51\x53\x8A\x5D\x08',512,0,True,hex(0x3202324)),0)
dwGameDir = int(getSig("engine.dll", rb'\x68....\x8D\x85....\x50\x68....\x68',1,0,True,hex(0x628700)),0)
dwGameRulesProxy = int(getSig("client.dll", rb'\xA1....\x85\xC0\x0F\x84....\x80\xB8.....\x74\x7A',1,0,True,hex(0x52EECFC)),0)
dwGetAllClasses = int(getSig("client.dll", rb'\xA1....\xC3\xCC\xCC\xCC\xCC\xCC\xCC\xCC\xCC\xCC\xCC\xA1....\xB9',1,0,True,hex(0xDDFBFC)),0)
dwGlobalVars = int(getSig("engine.dll", rb'\x68....\x68....\xFF\x50\x08\x85\xC0',1,0,True,hex(0x589CC8)),0)
dwGlowObjectManager = int(getSig("client.dll", rb'\xA1\xA8\x01\x75\x4B',1,4,True,hex(0x531A118)),0)
dwInput = int(getSig("client.dll", rb'\xB9....\xF3\x0F\x11\x04\x24\xFF\x50\x10',1,0,True,hex(0x52233F0)),0)
dwLocalPlayer = int(getSig("client.dll", rb'\x8D\x34\x85....\x89\x15....\x8B\x41\x08\x8B\x48\x04\x83\xF9\xFF',3,4,True,hex(0xDB65EC)),0)
dwMouseEnable = int(getSig("client.dll", rb'\xB9....\xFF\x50\x34\x85\xC0\x75\x10',1,48,True,hex(0xDBC288)),0)
dwMouseEnablePtr = int(getSig("client.dll", rb'\xB9....\xFF\x50\x34\x85\xC0\x75\x10',1,0,True,hex(0xDBC258)),0)
dwPlayerResource = int(getSig("client.dll", rb'\x8B\x3D....\x85\xFF\x0F\x84....\x81\xC7',2,0,True,hex(0x3200680)),0)
dwRadarBase = int(getSig("client.dll", rb'\xA1....\x8B\x0C\xB0\x8B\x01\xFF\x50.\x46\x3B\x35....\x7C\xEA\x8B\x0D',1,0,True,hex(0x5206B94)),0)
dwSensitivity = int(getSig("client.dll", rb'\x81\xF9....\x75\x1D\xF3\x0F\x10\x05....\xF3\x0F\x11\x44\x24.8B\x44\x24\x0C\x35....\x89\x44\x24\x0C',2,44,True,hex(0xDBC124)),0)
dwSensitivityPtr = int(getSig("client.dll", rb'\x81\xF9....\x75\x1D\xF3\x0F\x10\x05....\xF3\x0F\x11\x44\x24.8B\x44\x24\x0C\x35....\x89\x44\x24\x0C',2,0,True,hex(0xDBC0F8)),0)
dwViewMatrix = int(getSig("client.dll", rb'\x0F\x10\x05....\x8D\x85....\xB9',3,176,True,hex(0x4DC3734)),0)
dwWeaponTable = int(getSig("client.dll", rb'\xB9....\x6A\x00\xFF\x50\x08\xC3',1,0,True,hex(0x5223EB8)),0)
dwWeaponTableIndex = int(getSig("client.dll", rb'\x39\x86....\x74\x06\x89\x86....\x8B\x86',2,0,False,hex(0x326C)),0)
dwYawPtr = int(getSig("client.dll", rb'\x81\xF9....\x75\x16\xF3\x0F\x10\x05....\xF3\x0F\x11\x45.\x81\x75.....\xEB\x0A\x8B\x01\x8B\x40\x30\xFF\xD0\xD9\x5D\x0C\x8B\x55\x08',2,0,True,hex(0xDBBEE8)),0)
dwZoomSensitivityRatioPtr = int(getSig("client.dll", rb'\x81\xF9....\x75\x1A\xF3\x0F\x10\x05....\xF3\x0F\x11\x45.\x8B\x45\xF4\x35....\x89\x45\xFC\xEB\x0A\x8B\x01\x8B\x40\x30\xFF\xD0\xD9\x5D\xFC\xA1',2,0,True,hex(0xDC1D38)),0)
dwppDirect3DDevice9 = int(getSig("shaderapidx9.dll", rb'\xA1....\x50\x8B\x08\xFF\x51\x0C',1,0,True,hex(0xA5050)),0)
find_hud_element = int(getSig("client.dll", rb'\x55\x8B\xEC\x53\x8B\x5D\x08\x56\x57\x8B\xF9\x33\xF6\x39\x77\x28',0,0,False,hex(0x2A434760)),0)
interface_engine_cvar = int(getSig("vstdlib.dll", rb'\x8B\x0D....\xC7\x05',2,0,True,hex(0x3E9EC)),0)
m_bDormant = int(getSig("client.dll", rb'\x8A\x81....\xC3\x32\xC0',2,8,False,hex(0xED)),0)
m_flSpawnTime = int(getSig("client.dll", rb'\x89\x86....\xE8....\x80\xBE.....',2,0,False,hex(0x103C0)),0)
m_pStudioHdr = int(getSig("client.dll", rb'\x8B\xB6....\x85\xF6\x74\x05\x83\x3E\x00\x75\x02\x33\xF6\xF3\x0F\x10\x44\x24',2,0,False,hex(0x2950)),0)
m_pitchClassPtr = int(getSig("client.dll", rb'\xA1....\x89\x74\x24\x28',1,0,True,hex(0x5206E30)),0)
m_yawClassPtr = int(getSig("client.dll", rb'\x81\xF9....\x75\x16\xF3\x0F\x10\x05....\xF3\x0F\x11\x45.\x81\x75.....\xEB\x0A\x8B\x01\x8B\x40\x30\xFF\xD0\xD9\x5D\x0C\x8B\x55\x08',2,0,True,hex(0xDBBEE8)),0)
model_ambient_min = int(getSig("engine.dll", rb'\xF3\x0F\x10\x0D....\xF3\x0F\x11\x4C\x24.\x8B\x44\x24\x20\x35....\x89\x44\x24\x0C',4,0,True,hex(0x58D03C)),0)

print("offsets updated")
