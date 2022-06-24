# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 22:55:51 2022

@author: Yannic
"""

import pymem
import time
import addresses as ad
from enum import Enum

dwClientState = ad.dwClientState
dwLocalPlayer = ad.dwLocalPlayer
dwEntityList = ad.dwEntityList
m_hViewModel = ad.m_hViewModel
m_flFallbackWear = ad.m_flFallbackWear
m_nFallbackPaintKit = ad.m_nFallbackPaintKit
m_iItemIDHigh = ad.m_iItemIDHigh
m_iEntityQuality = ad.m_iEntityQuality
m_iItemDefinitionIndex = ad.m_iItemDefinitionIndex
m_hActiveWeapon = ad.m_hActiveWeapon
m_hMyWeapons = ad.m_hMyWeapons

## not included in addresses

m_iViewModelIndex = 0x3250
m_nModelIndex = 0x258
m_dwModelPrecache = 0x52a4

#####################################

class ItemDefinitionIndex(Enum):
	WEAPON_DEAGLE = 1
	WEAPON_ELITE = 2
	WEAPON_FIVESEVEN = 3
	WEAPON_GLOCK = 4
	WEAPON_AK47 = 7
	WEAPON_AUG = 8
	WEAPON_AWP = 9
	WEAPON_FAMAS = 10
	WEAPON_G3SG1 = 11
	WEAPON_GALILAR = 13
	WEAPON_M249 = 14
	WEAPON_M4A1 = 16
	WEAPON_MAC10 = 17
	WEAPON_P90 = 19
	WEAPON_MP5_SD = 23
	WEAPON_UMP45 = 24
	WEAPON_XM1014 = 25
	WEAPON_BIZON = 26
	WEAPON_MAG7 = 27
	WEAPON_NEGEV = 28
	WEAPON_SAWEDOFF = 29
	WEAPON_TEC9 = 30
	WEAPON_TASER = 31
	WEAPON_HKP2000 = 32
	WEAPON_MP7 = 33
	WEAPON_MP9 = 34
	WEAPON_NOVA = 35
	WEAPON_P250 = 36
	WEAPON_SCAR20 = 38
	WEAPON_SG556 = 39
	WEAPON_SSG08 = 40
	WEAPON_KNIFE = 42
	WEAPON_FLASHBANG = 43
	WEAPON_HEGRENADE = 44
	WEAPON_SMOKEGRENADE = 45
	WEAPON_MOLOTOV = 46
	WEAPON_DECOY = 47
	WEAPON_INCGRENADE = 48
	WEAPON_C4 = 49
	WEAPON_KNIFE_T = 59
	WEAPON_M4A1_SILENCER = 60
	WEAPON_USP_SILENCER = 61
	WEAPON_CZ75A = 63
	WEAPON_REVOLVER = 64
	WEAPON_KNIFE_BAYONET = 500
	WEAPON_KNIFE_CSS = 503
	WEAPON_KNIFE_FLIP = 505
	WEAPON_KNIFE_GUT = 506
	WEAPON_KNIFE_KARAMBIT = 507
	WEAPON_KNIFE_M9_BAYONET = 508
	WEAPON_KNIFE_TACTICAL = 509
	WEAPON_KNIFE_FALCHION = 512
	WEAPON_KNIFE_SURVIVAL_BOWIE = 514
	WEAPON_KNIFE_BUTTERFLY = 515
	WEAPON_KNIFE_PUSH = 516
	WEAPON_KNIFE_CORD = 517
	WEAPON_KNIFE_CANIS = 518
	WEAPON_KNIFE_URSUS = 519
	WEAPON_KNIFE_GYPSY_JACKKNIFE = 520
	WEAPON_KNIFE_OUTDOOR = 521
	WEAPON_KNIFE_STILETTO = 522
	WEAPON_KNIFE_WIDOWMAKER = 523
	WEAPON_KNIFE_SKELETON = 525
	GLOVE_STUDDED_BLOODHOUND = 5027
	GLOVE_T_SIDE = 5028
	GLOVE_CT_SIDE = 5029
	GLOVE_SPORTY = 5030
	GLOVE_SLICK = 5031
	GLOVE_LEATHER_WRAP = 5032
	GLOVE_MOTORCYCLE = 5033
	GLOVE_SPECIALIST = 5034
	GLOVE_HYDRA = 5035
    
knifeNames = ["Bayonet",
              "Flip Knife",
              "Gut Knife",
              "Karambit",
              "M9 Bayonet",
              "Huntsman Knife",
              "Falchion Knife",
              "Bowie Knife",
              "Butterfly Knife",
              "Shadow Daggers",
              "Ursus Knife",
              "Navaja Knife",
              "Stiletto Knife",
              "Talon Knife",
              "Classic Knife",
              "Paracord Knife",
              "Survival Knife",
              "Nomad Knife",
              "Skeleton Knife"]

knifeIDs = [ItemDefinitionIndex.WEAPON_KNIFE_BAYONET,
            ItemDefinitionIndex.WEAPON_KNIFE_FLIP,
            ItemDefinitionIndex.WEAPON_KNIFE_GUT,
            ItemDefinitionIndex.WEAPON_KNIFE_KARAMBIT,
            ItemDefinitionIndex.WEAPON_KNIFE_M9_BAYONET,
            ItemDefinitionIndex.WEAPON_KNIFE_TACTICAL,
            ItemDefinitionIndex.WEAPON_KNIFE_FALCHION,
            ItemDefinitionIndex.WEAPON_KNIFE_SURVIVAL_BOWIE,
            ItemDefinitionIndex.WEAPON_KNIFE_BUTTERFLY,
            ItemDefinitionIndex.WEAPON_KNIFE_PUSH,
            ItemDefinitionIndex.WEAPON_KNIFE_URSUS,
            ItemDefinitionIndex.WEAPON_KNIFE_GYPSY_JACKKNIFE,
            ItemDefinitionIndex.WEAPON_KNIFE_STILETTO,
            ItemDefinitionIndex.WEAPON_KNIFE_WIDOWMAKER,
            ItemDefinitionIndex.WEAPON_KNIFE_CSS,
            ItemDefinitionIndex.WEAPON_KNIFE_CORD,
            ItemDefinitionIndex.WEAPON_KNIFE_CANIS,
            ItemDefinitionIndex.WEAPON_KNIFE_OUTDOOR,
            ItemDefinitionIndex.WEAPON_KNIFE_SKELETON]

   
def GetModelIndexByName(modelName: str) -> int:
    cstate = pm.read_uint(engine + dwClientState)
    nst = pm.read_uint(cstate + m_dwModelPrecache)
    nsd = pm.read_uint(nst + 0x40)
    nsdi = pm.read_uint(nsd + 0xC)
    
    for i in range(0,1024):
        nsdi_i = pm.read_uint(nsdi + 0xC + i * 0x34)
        string = pm.read_string(nsdi_i, byte = 128)
        if string == modelName:
            return i
        
def GetModelIndex(itemIndex):
    
    if itemIndex == ItemDefinitionIndex.WEAPON_KNIFE.value:
        return GetModelIndexByName("models/weapons/v_knife_default_ct.mdl")
    elif itemIndex == ItemDefinitionIndex.WEAPON_KNIFE_T.value:
        return GetModelIndexByName("models/weapons/v_knife_default_t.mdl")
    elif itemIndex == ItemDefinitionIndex.WEAPON_KNIFE_BAYONET.value:
        return GetModelIndexByName("models/weapons/v_knife_bayonet.mdl")
    elif itemIndex == ItemDefinitionIndex.WEAPON_KNIFE_FLIP.value:
        return GetModelIndexByName("models/weapons/v_knife_flip.mdl")
    elif itemIndex == ItemDefinitionIndex.WEAPON_KNIFE_GUT.value:
        return GetModelIndexByName("models/weapons/v_knife_gut.mdl")
    elif itemIndex == ItemDefinitionIndex.WEAPON_KNIFE_KARAMBIT.value:
        return GetModelIndexByName("models/weapons/v_knife_karam.mdl")
    elif itemIndex == ItemDefinitionIndex.WEAPON_KNIFE_M9_BAYONET.value:
        return GetModelIndexByName("models/weapons/v_knife_m9_bay.mdl")
    elif itemIndex == ItemDefinitionIndex.WEAPON_KNIFE_TACTICAL.value:
        return GetModelIndexByName("models/weapons/v_knife_tactical.mdl")
    elif itemIndex == ItemDefinitionIndex.WEAPON_KNIFE_FALCHION.value:
        return GetModelIndexByName("models/weapons/v_knife_falchion_advanced.mdl")
    elif itemIndex == ItemDefinitionIndex.WEAPON_KNIFE_SURVIVAL_BOWIE.value:
        return GetModelIndexByName("models/weapons/v_knife_survival_bowie.mdl")
    elif itemIndex == ItemDefinitionIndex.WEAPON_KNIFE_BUTTERFLY.value:
        return GetModelIndexByName("models/weapons/v_knife_butterfly.mdl")
    elif itemIndex == ItemDefinitionIndex.WEAPON_KNIFE_PUSH.value:
        return GetModelIndexByName("models/weapons/v_knife_push.mdl")
    elif itemIndex == ItemDefinitionIndex.WEAPON_KNIFE_URSUS.value:
        return GetModelIndexByName("models/weapons/v_knife_ursus.mdl")
    elif itemIndex == ItemDefinitionIndex.WEAPON_KNIFE_GYPSY_JACKKNIFE.value:
        return GetModelIndexByName("models/weapons/v_knife_gypsy_jackknife.mdl")
    elif itemIndex == ItemDefinitionIndex.WEAPON_KNIFE_STILETTO.value:
        return GetModelIndexByName("models/weapons/v_knife_stiletto.mdl")
    elif itemIndex == ItemDefinitionIndex.WEAPON_KNIFE_WIDOWMAKER.value:
        return GetModelIndexByName("models/weapons/v_knife_widowmaker.mdl")
    elif itemIndex == ItemDefinitionIndex.WEAPON_KNIFE_CSS.value:
        return GetModelIndexByName("models/weapons/v_knife_css.mdl")
    elif itemIndex == ItemDefinitionIndex.WEAPON_KNIFE_CORD.value:
        return GetModelIndexByName("models/weapons/v_knife_cord.mdl")
    elif itemIndex == ItemDefinitionIndex.WEAPON_KNIFE_CANIS.value:
        return GetModelIndexByName("models/weapons/v_knife_canis.mdl")
    elif itemIndex == ItemDefinitionIndex.WEAPON_KNIFE_OUTDOOR.value:
        return GetModelIndexByName("models/weapons/v_knife_outdoor.mdl")
    elif itemIndex == ItemDefinitionIndex.WEAPON_KNIFE_SKELETON.value:
        return GetModelIndexByName("models/weapons/v_knife_skeleton.mdl")
    else:
        return 0

def GetWeaponSkin(itemIndex):
    if itemIndex == ItemDefinitionIndex.WEAPON_DEAGLE.value:
        return 12
    elif itemIndex == ItemDefinitionIndex.WEAPON_FIVESEVEN.value:
        return 44
    elif itemIndex == ItemDefinitionIndex.WEAPON_GLOCK.value:
        return 38
    elif itemIndex == ItemDefinitionIndex.WEAPON_AK47.value:
        return 675
    elif itemIndex == ItemDefinitionIndex.WEAPON_AUG.value:
        return 455
    elif itemIndex == ItemDefinitionIndex.WEAPON_AK47.value:
        return 675
    elif itemIndex == ItemDefinitionIndex.WEAPON_AWP.value:
        return 344
    elif itemIndex == ItemDefinitionIndex.WEAPON_FAMAS:
        return 260
    elif itemIndex == ItemDefinitionIndex.WEAPON_G3SG1.value:
        return 438
    elif itemIndex == ItemDefinitionIndex.WEAPON_GALILAR.value:
        return 379
    elif itemIndex == ItemDefinitionIndex.WEAPON_M249.value:
        return 469
    elif itemIndex == ItemDefinitionIndex.WEAPON_AK47.value:
        return 675
    elif itemIndex == ItemDefinitionIndex.WEAPON_M4A1.value:
        return 309
    elif itemIndex == ItemDefinitionIndex.WEAPON_MAC10.value:
        return 433
    elif itemIndex == ItemDefinitionIndex.WEAPON_P90.value:
        return 359
    elif itemIndex == ItemDefinitionIndex.WEAPON_MP5_SD.value:
        return 810
    elif itemIndex == ItemDefinitionIndex.WEAPON_UMP45.value:
        return 37
    elif itemIndex == ItemDefinitionIndex.WEAPON_XM1014.value:
        return 852
    elif itemIndex == ItemDefinitionIndex.WEAPON_BIZON.value:
        return 542
    elif itemIndex == ItemDefinitionIndex.WEAPON_MAG7.value:
        return 737
    elif itemIndex == ItemDefinitionIndex.WEAPON_NEGEV.value:
        return 763
    elif itemIndex == ItemDefinitionIndex.WEAPON_TEC9.value:
        return 179
    elif itemIndex == ItemDefinitionIndex.WEAPON_HKP2000.value:
        return 591
    elif itemIndex == ItemDefinitionIndex.WEAPON_MP7.value:
        return 102
    elif itemIndex == ItemDefinitionIndex.WEAPON_MP9.value:
        return 734
    elif itemIndex == ItemDefinitionIndex.WEAPON_NOVA.value:
        return 537
    elif itemIndex == ItemDefinitionIndex.WEAPON_P250.value:
        return 102
    elif itemIndex == ItemDefinitionIndex.WEAPON_SCAR20.value:
        return 954
    elif itemIndex == ItemDefinitionIndex.WEAPON_SG556.value:
        return 287
    elif itemIndex == ItemDefinitionIndex.WEAPON_SSG08.value:
        return 624
    elif itemIndex == ItemDefinitionIndex.WEAPON_AK47.value:
        return 675
    elif itemIndex == ItemDefinitionIndex.WEAPON_M4A1_SILENCER.value:
        return 430
    elif itemIndex == ItemDefinitionIndex.WEAPON_USP_SILENCER.value:
        return 1040
    elif itemIndex == ItemDefinitionIndex.WEAPON_CZ75A.value:
        return 350
    elif itemIndex == ItemDefinitionIndex.WEAPON_REVOLVER.value:
        return 38
    else:
        return 0
    

csgo_running = False

while not csgo_running:
    try:
        pm = pymem.Pymem("csgo.exe")
        client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
        engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
        csgo_running = True
    except Exception:
        time.sleep(5)
        continue
 
def changeKnife():
    
    # set knife model and skin here 

    knifeIndex = ItemDefinitionIndex.WEAPON_KNIFE_KARAMBIT.value
    knifeSkin = 561

    itemIDHigh = -1
    entityQuality = 3
    fallbackWear = 0.0001
    
    modelIndex = 0
    localPlayer = 0
    
    while(True):

        try:

            tempPlayer = pm.read_int(client + dwLocalPlayer)
            if not tempPlayer: # client not connected to any server (works most of the time)
                modelIndex = 0
                continue
            elif tempPlayer != localPlayer: # local base changed (new server join/demo record)
                localPlayer = tempPlayer
                modelIndex = 0
            
            while not modelIndex:
                modelIndex = GetModelIndex(knifeIndex)
            
            
            for i in range(0,8): # loop through m_hMyWeapons slots (8 will be enough)

                # get entity of weapon in current slot
                currentWeapon = pm.read_int(localPlayer + m_hMyWeapons + i * 0x4) & 0xfff
                currentWeapon = pm.read_int(client + dwEntityList + (currentWeapon - 1) * 0x10)
                if not currentWeapon: continue
        
                weaponIndex = pm.read_short(currentWeapon + m_iItemDefinitionIndex)
                weaponSkin = GetWeaponSkin(weaponIndex)
            
                # for knives, set item and model related properties
                if weaponIndex == ItemDefinitionIndex.WEAPON_KNIFE.value or weaponIndex == ItemDefinitionIndex.WEAPON_KNIFE_T.value or weaponIndex == knifeIndex:
                    pm.write_short(currentWeapon + m_iItemDefinitionIndex, knifeIndex)
                    pm.write_uint(currentWeapon + m_nModelIndex, modelIndex)
                    pm.write_uint(currentWeapon + m_iViewModelIndex, modelIndex)
                    pm.write_int(currentWeapon + m_iEntityQuality, entityQuality)
                    weaponSkin = knifeSkin
                
                if weaponSkin: # set skin properties
                    pm.write_int(currentWeapon + m_iItemIDHigh, itemIDHigh)
                    pm.write_uint(currentWeapon + m_nFallbackPaintKit, weaponSkin)
                    pm.write_float(currentWeapon + m_flFallbackWear, fallbackWear)
        
            # get entity of weapon in our hands 
            activeWeapon = pm.read_int(localPlayer + m_hActiveWeapon) & 0xfff
            activeWeapon = pm.read_int(client + dwEntityList + (activeWeapon - 1) * 0x10)
            if not activeWeapon: continue
    
            weaponIndex = pm.read_short(activeWeapon + m_iItemDefinitionIndex)
            if weaponIndex != knifeIndex: continue
        
            # get viewmodel entity
            activeViewModel = pm.read_uint(localPlayer + m_hViewModel) & 0xfff
            activeViewModel = pm.read_uint(client + dwEntityList + (activeViewModel - 1) * 0x10)
            if not activeViewModel: continue
    
            pm.write_uint(activeViewModel + m_nModelIndex, modelIndex)

        except Exception:
            continue
        

        
    
