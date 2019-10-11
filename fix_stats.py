#!/usr/bin/env python

import os
from bs4 import BeautifulSoup
import math
import csv
import re

class Formulas(object):
    """ generated source for class Formulas """
    HP_REGENERATE_PERIOD = 3000

    #  3 secs
    SHIELD_DEFENSE_FAILED = 0

    #  no shield defense
    SHIELD_DEFENSE_SUCCEED = 1

    #  normal shield defense
    SHIELD_DEFENSE_PERFECT_BLOCK = 2

    #  perfect block
    SKILL_REFLECT_FAILED = 0

    #  no reflect
    SKILL_REFLECT_SUCCEED = 1

    #  normal reflect, some damage reflected some other not
    SKILL_REFLECT_VENGEANCE = 2

    #  100% of the damage affect both
    MELEE_ATTACK_RANGE = 40
    MAX_STAT_VALUE = 100
    STR_COMPUTE = [
		1.036,
		34.845
    ]
    INT_COMPUTE = [
		1.020,
		31.375
    ]
    DEX_COMPUTE = [
		1.009,
		19.360
    ]
    WIT_COMPUTE = [
		1.050,
		20.000
    ]
    CON_COMPUTE = [
		1.030,
		27.632
    ]
    MEN_COMPUTE = [
		1.010,
		-0.060
    ]
    WIT_BONUS = []
    MEN_BONUS = []
    INT_BONUS = []
    STR_BONUS = []
    DEX_BONUS = []
    CON_BONUS = []
    BASE_EVASION_ACCURACY = []
    SQRT_MEN_BONUS = []
    SQRT_CON_BONUS = []
    i = 0
    i = 0
    i = 0
    i = 0
    i = 0
    i = 0
    i = 0

    #  Precompute square root values
    i = 0
    i = 0

    def __init__(cls):

        for i in range(0, cls.MAX_STAT_VALUE):
            cls.STR_BONUS.append(math.floor(math.pow(cls.STR_COMPUTE[0], i - cls.STR_COMPUTE[1]) * 100 + .5) / 100)
            cls.MEN_BONUS.append(math.floor(math.pow(cls.MEN_COMPUTE[0], i - cls.MEN_COMPUTE[1]) * 100 + .5) / 100)
            cls.CON_BONUS.append(math.floor(math.pow(cls.CON_COMPUTE[0], i - cls.CON_COMPUTE[1]) * 100 + .5) / 100)
            cls.INT_BONUS.append(math.floor(math.pow(cls.INT_COMPUTE[0], i - cls.INT_COMPUTE[1]) * 100 + .5) / 100)
            cls.DEX_BONUS.append(math.floor(math.pow(cls.DEX_COMPUTE[0], i - cls.DEX_COMPUTE[1]) * 100 + .5) / 100)
            cls.BASE_EVASION_ACCURACY.append(math.sqrt(i) * 6)

    # 
    # 	 * @param cha The character to make checks on.
    # 	 * @return the period between 2 regenerations task (3s for Creature, 5 min for L2DoorInstance).
    #
    def getRegeneratePeriod(cls, cha):
        """ generated source for method getRegeneratePeriod """
        if isinstance(cha, (Door, )):
            return cls.HP_REGENERATE_PERIOD * 100
        #  5 mins
        return cls.HP_REGENERATE_PERIOD
        #  3s

    # 
    # 	 * @param cha The character to make checks on.
    # 	 * @return the HP regen rate (base + modifiers).
    #
    def calcHpRegen(cls, init, conval, level_mod):
        """ generated source for method calcHpRegen """
        #init = cha.getTemplate().getBaseHpReg()
        hpRegenMultiplier = 1
        hpRegenBonus = 0

        #  Add CON bonus
        init *= level_mod * cls.CON_BONUS[conval]
        if init < 1:
            init = 1
        return init * hpRegenMultiplier + hpRegenBonus

    def calc_HpRegen(cls, conval, level_mod):
        """ generated source for method calcHpRegen """
        init = 1
        hpRegenMultiplier = 1
        hpRegenBonus = 0

        #  Add CON bonus
        init *= level_mod * cls.CON_BONUS[conval]
        if init < 1:
            init = 1
        return init * hpRegenMultiplier + hpRegenBonus
    # 
    # 	 * @param cha The character to make checks on.
    # 	 * @return the MP regen rate (base + modifiers).
    #
    def calcMpRegen(cls, init, menval, level_mod):
        """ generated source for method calcMpRegen """
        #init = cha.getTemplate().getBaseMpReg()
        mpRegenMultiplier = 1
        mpRegenBonus = 0
        #  Add MEN bonus
        init *= level_mod * cls.MEN_BONUS[menval]
        if init < 1:
            init = 1
        return init * mpRegenMultiplier + mpRegenBonus

    def calc_MpRegen(cls, menval, level_mod):
        """ generated source for method calcMpRegen """
        init = 1
        mpRegenMultiplier = 1
        mpRegenBonus = 0
        #  Add MEN bonus
        init *= level_mod * cls.MEN_BONUS[menval]
        if init < 1:
            init = 1
        return init * mpRegenMultiplier + mpRegenBonus
    # 
    # 	 * @param player The player to make checks on.
    # 	 * @return the CP regen rate (base + modifiers).
    #
    def calcCpRegen(cls, player):
        """ generated source for method calcCpRegen """
        #  Calculate correct baseHpReg value for certain level of PC
        init = player.getTemplate().getBaseHpReg() + (((player.getLevel() - 1) / 10.0) if (player.getLevel() > 10) else 0.5)
        cpRegenMultiplier = Config.CP_REGEN_MULTIPLIER
        #  Calculate Movement bonus
        if player.isSitting():
            cpRegenMultiplier *= 1.5
        elif not player.isMoving():
            cpRegenMultiplier *= 1.1
        elif player.isRunning():
            cpRegenMultiplier *= 0.7
        #  Running
        #  Apply CON bonus
        init *= player.getLevelMod() * cls.CON_BONUS[player.getCON()]
        if init < 1:
            init = 1
        return player.calcStat(Stats.REGENERATE_CP_RATE, init, None, None) * cpRegenMultiplier

    # 
    # 	 * @param player the player to test on.
    # 	 * @return true if the player is near one of his clan HQ (+50% regen boost).
    #
    def calcSiegeRegenModifer(cls, player):
        """ generated source for method calcSiegeRegenModifer """
        if player == None:
            return False
        clan = player.getClan()
        if clan == None:
            return False
        siege = CastleManager.getInstance().getActiveSiege(player)
        if siege == None or not siege.checkSide(clan, SiegeSide.ATTACKER):
            return False
        return MathUtil.checkIfInRange(200, player, clan.getFlag(), True)

    # 
    # 	 * @param attacker The attacker, from where the blow comes from.
    # 	 * @param target The victim of the blow.
    # 	 * @param skill The skill used.
    # 	 * @param shld True if victim was wearign a shield.
    # 	 * @param ss True if ss were activated.
    # 	 * @return blow damage based on cAtk
    #
    def calcBlowDamage(cls, attacker, target, skill, shld, ss):
        """ generated source for method calcBlowDamage """
        defence = target.getPDef(attacker)
        if shld==cls.SHIELD_DEFENSE_SUCCEED:
            defence += target.getShldDef()
        elif shld==cls.SHIELD_DEFENSE_PERFECT_BLOCK:
            #  perfect block
            return 1
        isPvP = isinstance(attacker, (Playable, )) and isinstance(target, (Playable, ))
        power = skill.getPower()
        damage = 0
        damage += calcValakasAttribute(attacker, target, skill)
        if ss:
            damage *= 2.
            if skill.getSSBoost() > 0:
                power *= skill.getSSBoost()
        damage += power
        damage *= attacker.calcStat(Stats.CRITICAL_DAMAGE, 1, target, skill)
        damage *= ((attacker.calcStat(Stats.CRITICAL_DAMAGE_POS, 1, target, skill) - 1) / 2 + 1)
        damage += attacker.calcStat(Stats.CRITICAL_DAMAGE_ADD, 0, target, skill) * 6.5
        damage *= target.calcStat(Stats.CRIT_VULN, 1, target, skill)
        #  get the vulnerability for the instance due to skills (buffs, passives, toggles, etc)
        damage = target.calcStat(Stats.DAGGER_WPN_VULN, damage, target, None)
        damage *= 70. / defence
        #  Random weapon damage
        damage *= attacker.getRandomDamageMultiplier()
        #  Dmg bonusses in PvP fight
        if isPvP:
            damage *= attacker.calcStat(Stats.PVP_PHYS_SKILL_DMG, 1, None, None)
        return 1. if damage < 1 else damage

    # 
    # 	 * Calculated damage caused by ATTACK of attacker on target, called separatly for each weapon, if dual-weapon is used.
    # 	 * @param attacker player or NPC that makes ATTACK
    # 	 * @param target player or NPC, target of ATTACK
    # 	 * @param skill skill used.
    # 	 * @param shld target was using a shield or not.
    # 	 * @param crit if the ATTACK have critical success
    # 	 * @param ss if weapon item was charged by soulshot
    # 	 * @return damage points
    #
    def calcPhysDam(cls, attacker, target, skill, shld, crit, ss):
        """ generated source for method calcPhysDam """
        if isinstance(attacker, (Player, )):
            if pcInst.isGM() and not pcInst.getAccessLevel().canGiveDamage():
                return 0
        defence = target.getPDef(attacker)
        if shld==cls.SHIELD_DEFENSE_SUCCEED:
            defence += target.getShldDef()
        elif shld==cls.SHIELD_DEFENSE_PERFECT_BLOCK:
            #  perfect block
            return 1.
        isPvP = isinstance(attacker, (Playable, )) and isinstance(target, (Playable, ))
        damage = attacker.getPAtk(target)
        damage += calcValakasAttribute(attacker, target, skill)
        if ss:
            damage *= 2
        if skill != None:
            if ssBoost > 0 and ss:
                skillpower *= ssBoost
            damage += skillpower
        #  defence modifier depending of the attacker weapon
        weapon = attacker.getActiveWeaponItem()
        stat = None
        if weapon != None:
            if weapon.getItemType()==BOW:
                stat = Stats.BOW_WPN_VULN
            elif weapon.getItemType()==BLUNT:
                stat = Stats.BLUNT_WPN_VULN
            elif weapon.getItemType()==BIGSWORD:
                stat = Stats.BIGSWORD_WPN_VULN
            elif weapon.getItemType()==BIGBLUNT:
                stat = Stats.BIGBLUNT_WPN_VULN
            elif weapon.getItemType()==DAGGER:
                stat = Stats.DAGGER_WPN_VULN
            elif weapon.getItemType()==DUAL:
                stat = Stats.DUAL_WPN_VULN
            elif weapon.getItemType()==DUALFIST:
                stat = Stats.DUALFIST_WPN_VULN
            elif weapon.getItemType()==POLE:
                stat = Stats.POLE_WPN_VULN
            elif weapon.getItemType()==SWORD:
                stat = Stats.SWORD_WPN_VULN
        if crit:
            #  Finally retail like formula
            damage = 2 * attacker.calcStat(Stats.CRITICAL_DAMAGE, 1, target, skill) * attacker.calcStat(Stats.CRITICAL_DAMAGE_POS, 1, target, skill) * target.calcStat(Stats.CRIT_VULN, 1, target, None) * (70 * damage / defence)
            #  Crit dmg add is almost useless in normal hits...
            damage += (attacker.calcStat(Stats.CRITICAL_DAMAGE_ADD, 0, target, skill) * 70 / defence)
        else:
            damage = 70 * damage / defence
        if stat != None:
            damage = target.calcStat(stat, damage, target, None)
        #  Weapon random damage ; invalid for CHARGEDAM skills.
        if skill == None or skill.getEffectType() != L2SkillType.CHARGEDAM:
            damage *= attacker.getRandomDamageMultiplier()
        if isinstance(target, (Npc, )):
            if (target).getTemplate().getRace()==BEAST:
                multiplier = 1 + ((attacker.getPAtkMonsters(target) - target.getPDefMonsters(target)) / 100)
                damage *= multiplier
            elif (target).getTemplate().getRace()==ANIMAL:
                multiplier = 1 + ((attacker.getPAtkAnimals(target) - target.getPDefAnimals(target)) / 100)
                damage *= multiplier
            elif (target).getTemplate().getRace()==PLANT:
                multiplier = 1 + ((attacker.getPAtkPlants(target) - target.getPDefPlants(target)) / 100)
                damage *= multiplier
            elif (target).getTemplate().getRace()==DRAGON:
                multiplier = 1 + ((attacker.getPAtkDragons(target) - target.getPDefDragons(target)) / 100)
                damage *= multiplier
            elif (target).getTemplate().getRace()==BUG:
                multiplier = 1 + ((attacker.getPAtkInsects(target) - target.getPDefInsects(target)) / 100)
                damage *= multiplier
            elif (target).getTemplate().getRace()==GIANT:
                multiplier = 1 + ((attacker.getPAtkGiants(target) - target.getPDefGiants(target)) / 100)
                damage *= multiplier
            elif (target).getTemplate().getRace()==MAGICCREATURE:
                multiplier = 1 + ((attacker.getPAtkMagicCreatures(target) - target.getPDefMagicCreatures(target)) / 100)
                damage *= multiplier
        if damage > 0 and damage < 1:
            damage = 1
        elif damage < 0:
            damage = 0
        if isPvP:
            if skill == None:
                damage *= attacker.calcStat(Stats.PVP_PHYSICAL_DMG, 1, None, None)
            else:
                damage *= attacker.calcStat(Stats.PVP_PHYS_SKILL_DMG, 1, None, None)
        damage += calcElemental(attacker, target, None)
        return damage

    def calcMagicDam(cls, attacker, target, skill, shld, ss, bss, mcrit):
        """ generated source for method calcMagicDam """
        if isinstance(attacker, (Player, )):
            if pcInst.isGM() and not pcInst.getAccessLevel().canGiveDamage():
                return 0
        mDef = target.getMDef(attacker, skill)
        if shld==cls.SHIELD_DEFENSE_SUCCEED:
            mDef += target.getShldDef()
        elif shld==cls.SHIELD_DEFENSE_PERFECT_BLOCK:
            return 1.
        mAtk = attacker.getMAtk(target, skill)
        if bss:
            mAtk *= 4
        elif ss:
            mAtk *= 2
        damage = 91 * Math.sqrt(mAtk) / mDef * skill.getPower(attacker)
        if Config.MAGIC_FAILURES and not calcMagicSuccess(attacker, target, skill):
            if isinstance(attacker, (Player, )):
                if calcMagicSuccess(attacker, target, skill) and (target.getLevel() - attacker.getLevel()) <= 9:
                    if skill.getSkillType() == L2SkillType.DRAIN:
                        attacker.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.DRAIN_HALF_SUCCESFUL))
                    else:
                        attacker.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.ATTACK_FAILED))
                    damage /= 2
                else:
                    attacker.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.S1_RESISTED_YOUR_S2).addCharName(target).addSkillName(skill))
                    damage = 1
            if isinstance(target, (Player, )):
                if skill.getSkillType() == L2SkillType.DRAIN:
                    target.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.RESISTED_S1_DRAIN).addCharName(attacker))
                else:
                    target.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.RESISTED_S1_MAGIC).addCharName(attacker))
        elif mcrit:
            damage *= 4
        if isinstance(attacker, (Playable, )) and isinstance(target, (Playable, )):
            if skill.isMagic():
                damage *= attacker.calcStat(Stats.PVP_MAGICAL_DMG, 1, None, None)
            else:
                damage *= attacker.calcStat(Stats.PVP_PHYS_SKILL_DMG, 1, None, None)
        damage *= calcElemental(attacker, target, skill)
        return damage

    def calcMagicDam_0(cls, attacker, target, skill, mcrit, shld):
        """ generated source for method calcMagicDam_0 """
        mDef = target.getMDef(attacker.getOwner(), skill)
        if shld==cls.SHIELD_DEFENSE_SUCCEED:
            mDef += target.getShldDef()
        elif shld==cls.SHIELD_DEFENSE_PERFECT_BLOCK:
            return 1
        damage = 91 / mDef * skill.getPower()
        owner = attacker.getOwner()
        if Config.MAGIC_FAILURES and not calcMagicSuccess(owner, target, skill):
            if calcMagicSuccess(owner, target, skill) and (target.getLevel() - skill.getMagicLevel()) <= 9:
                if skill.getSkillType() == L2SkillType.DRAIN:
                    owner.sendPacket(SystemMessageId.DRAIN_HALF_SUCCESFUL)
                else:
                    owner.sendPacket(SystemMessageId.ATTACK_FAILED)
                damage /= 2
            else:
                owner.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.S1_RESISTED_YOUR_S2).addCharName(target).addSkillName(skill))
                damage = 1
            if isinstance(target, (Player, )):
                if skill.getSkillType() == L2SkillType.DRAIN:
                    target.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.RESISTED_S1_DRAIN).addCharName(owner))
                else:
                    target.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.RESISTED_S1_MAGIC).addCharName(owner))
        elif mcrit:
            damage *= 4
        damage *= calcElemental(owner, target, skill)
        return damage

    def calcCrit(cls, rate):
        """ generated source for method calcCrit """
        return rate > Rnd.get(1000)

    def calcBlow(cls, attacker, target, chance):
        """ generated source for method calcBlow """
        return attacker.calcStat(Stats.BLOW_RATE, chance * (1.0 + (attacker.getDEX() - 20) / 100), target, None) > Rnd.get(100)

    def calcLethal(cls, attacker, target, baseLethal, magiclvl):
        """ generated source for method calcLethal """
        chance = 0
        if magiclvl > 0:
            if delta >= -3:
                chance = (baseLethal * (float(attacker.getLevel()) / target.getLevel()))
            elif delta < -3 and delta >= -9:
                chance = (-3) * (baseLethal / (delta))
            else:
                chance = baseLethal / 15
        else:
            chance = (baseLethal * (float(attacker.getLevel()) / target.getLevel()))
        chance = 10 * attacker.calcStat(Stats.LETHAL_RATE, chance, target, None)
        if Config.DEVELOPER:
            cls.LOGGER.info("Current calcLethal: {} / 1000.", chance)
        return chance

    def calcLethalHit(cls, attacker, target, skill):
        """ generated source for method calcLethalHit """
        if target.isRaidRelated() or isinstance(target, (Door, )):
            return
        if isinstance(target, (Npc, )):
            if (target).getNpcId()==22215:
                pass
            elif (target).getNpcId()==22216:
                pass
            elif (target).getNpcId()==22217:
                pass
            elif (target).getNpcId()==35062:
                return
        if skill.getLethalChance2() > 0 and Rnd.get(1000) < cls.calcLethal(attacker, target, skill.getLethalChance2(), skill.getMagicLevel()):
            if isinstance(target, (Npc, )):
                target.reduceCurrentHp(target.getCurrentHp() - 1, attacker, skill)
            elif isinstance(target, (Player, )):
                if not player.isInvul():
                    if not (isinstance(attacker, (Player, )) and ((attacker).isGM() and not (attacker).getAccessLevel().canGiveDamage())):
                        player.setCurrentHp(1)
                        player.setCurrentCp(1)
                        player.sendPacket(SystemMessageId.LETHAL_STRIKE)
            attacker.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.LETHAL_STRIKE_SUCCESSFUL))
        elif skill.getLethalChance1() > 0 and Rnd.get(1000) < cls.calcLethal(attacker, target, skill.getLethalChance1(), skill.getMagicLevel()):
            if isinstance(target, (Npc, )):
                target.reduceCurrentHp(target.getCurrentHp() / 2, attacker, skill)
            elif isinstance(target, (Player, )):
                if not player.isInvul():
                    if not (isinstance(attacker, (Player, )) and ((attacker).isGM() and not (attacker).getAccessLevel().canGiveDamage())):
                        player.setCurrentCp(1)
                        player.sendPacket(SystemMessageId.LETHAL_STRIKE)
            attacker.sendPacket(SystemMessage.getSystemMessage(SystemMessageId.LETHAL_STRIKE_SUCCESSFUL))

    def calcMCrit(cls, mRate):
        """ generated source for method calcMCrit """
        if Config.DEVELOPER:
            cls.LOGGER.info("Current mCritRate: {} / 1000.", mRate)
        return mRate > Rnd.get(1000)

    def calcCastBreak(cls, target, dmg):
        """ generated source for method calcCastBreak """
        if target.isRaidRelated() or target.isInvul():
            return
        if isinstance(target, (Player, )) and (target).getFusionSkill() != None:
            target.breakCast()
            return
        if not target.isCastingNow() and (target.getLastSkillCast() != None and not target.getLastSkillCast().isMagic()):
            return
        rate = target.calcStat(Stats.ATTACK_CANCEL, 15 + Math.sqrt(13 * dmg) - (cls.MEN_BONUS[target.getMEN()] * 100 - 100), None, None)
        if rate > 99:
            rate = 99
        elif rate < 1:
            rate = 1
        if Config.DEVELOPER:
            cls.LOGGER.info("calcCastBreak rate: {}%.", int(rate))
        if Rnd.get(100) < rate:
            target.breakCast()

    def calcPAtkSpd(cls, attacker, target, rate):
        """ generated source for method calcPAtkSpd """
        if rate < 2:
            return 2700
        return int((470000 / rate))

    def calcAtkSpd(cls, attacker, skill, skillTime):
        """ generated source for method calcAtkSpd """
        if skill.isMagic():
            return int((skillTime * 333 / attacker.getMAtkSpd()))
        return int((skillTime * 333 / attacker.getPAtkSpd()))

    def calcHitMiss(cls, attacker, target):
        """ generated source for method calcHitMiss """
        chance = (80 + (2 * (attacker.getAccuracy() - target.getEvasionRate(attacker)))) * 10
        modifier = 100
        if attacker.getZ() - target.getZ() > 50:
            modifier += 3
        elif attacker.getZ() - target.getZ() < -50:
            modifier -= 3
        if GameTimeTaskManager.getInstance().isNight():
            modifier -= 10
        if attacker.isBehindTarget():
            modifier += 10
        elif not attacker.isInFrontOfTarget():
            modifier += 5
        chance *= modifier / 100
        if Config.DEVELOPER:
            cls.LOGGER.info("calcHitMiss rate: {}%, modifier : x{}.", chance / 10, +modifier / 100)
        return Math.max(Math.min(chance, 980), 200) < Rnd.get(1000)

    def calcShldUse(cls, attacker, target, skill):
        """ generated source for method calcShldUse """
        if skill != None and skill.ignoreShield():
            return 0
        item = target.getSecondaryWeaponItem()
        if item == None or not (isinstance(item, (Armor, ))):
            return 0
        shldRate = target.calcStat(Stats.SHIELD_RATE, 0, attacker, None) * cls.DEX_BONUS[target.getDEX()]
        if shldRate == 0.0:
            return 0
        degreeside = int(target.calcStat(Stats.SHIELD_DEFENCE_ANGLE, 120, None, None))
        if degreeside < 360 and (not target.isFacing(attacker, degreeside)):
            return 0
        shldSuccess = cls.SHIELD_DEFENSE_FAILED
        if attacker.getAttackType() == WeaponType.BOW:
            shldRate *= 1.3
        if shldRate > 0 and 100 - Config.PERFECT_SHIELD_BLOCK_RATE < Rnd.get(100):
            shldSuccess = cls.SHIELD_DEFENSE_PERFECT_BLOCK
        elif shldRate > Rnd.get(100):
            shldSuccess = cls.SHIELD_DEFENSE_SUCCEED
        if isinstance(target, (Player, )):
            if shldSuccess==cls.SHIELD_DEFENSE_SUCCEED:
                (target).sendPacket(SystemMessageId.SHIELD_DEFENCE_SUCCESSFULL)
            elif shldSuccess==cls.SHIELD_DEFENSE_PERFECT_BLOCK:
                (target).sendPacket(SystemMessageId.YOUR_EXCELLENT_SHIELD_DEFENSE_WAS_A_SUCCESS)
        return shldSuccess

    def calcMagicAffected(cls, actor, target, skill):
        """ generated source for method calcMagicAffected """
        type_ = skill.getSkillType()
        if target.isRaidRelated() and not calcRaidAffected(type_):
            return False
        defence = 0
        if skill.isActive() and skill.isOffensive():
            defence = target.getMDef(actor, skill)
        attack = 2 * actor.getMAtk(target, skill) * calcSkillVulnerability(actor, target, skill, type_)
        d = (attack - defence) / (attack + defence)
        d += 0.5 * Rnd.nextGaussian()
        return d > 0

    def calcSkillVulnerability(cls, attacker, target, skill, type_):
        """ generated source for method calcSkillVulnerability """
        multiplier = 1
        if skill.getElement() > 0:
            multiplier *= Math.sqrt(calcElemental(attacker, target, skill))
        if type_==BLEED:
            multiplier = target.calcStat(Stats.BLEED_VULN, multiplier, target, None)
        elif type_==POISON:
            multiplier = target.calcStat(Stats.POISON_VULN, multiplier, target, None)
        elif type_==STUN:
            multiplier = target.calcStat(Stats.STUN_VULN, multiplier, target, None)
        elif type_==PARALYZE:
            multiplier = target.calcStat(Stats.PARALYZE_VULN, multiplier, target, None)
        elif type_==ROOT:
            multiplier = target.calcStat(Stats.ROOT_VULN, multiplier, target, None)
        elif type_==SLEEP:
            multiplier = target.calcStat(Stats.SLEEP_VULN, multiplier, target, None)
        elif type_==MUTE:
            pass
        elif type_==FEAR:
            pass
        elif type_==BETRAY:
            pass
        elif type_==AGGDEBUFF:
            pass
        elif type_==AGGREDUCE_CHAR:
            pass
        elif type_==ERASE:
            pass
        elif type_==CONFUSION:
            multiplier = target.calcStat(Stats.DERANGEMENT_VULN, multiplier, target, None)
        elif type_==DEBUFF:
            pass
        elif type_==WEAKNESS:
            multiplier = target.calcStat(Stats.DEBUFF_VULN, multiplier, target, None)
        elif type_==CANCEL:
            multiplier = target.calcStat(Stats.CANCEL_VULN, multiplier, target, None)
        return multiplier

    def calcSkillStatModifier(cls, type_, target):
        """ generated source for method calcSkillStatModifier """
        multiplier = 1
        if type_==STUN:
            pass
        elif type_==BLEED:
            pass
        elif type_==POISON:
            multiplier = 2 - cls.SQRT_CON_BONUS[target.getStat().getCON()]
        elif type_==SLEEP:
            pass
        elif type_==DEBUFF:
            pass
        elif type_==WEAKNESS:
            pass
        elif type_==ERASE:
            pass
        elif type_==ROOT:
            pass
        elif type_==MUTE:
            pass
        elif type_==FEAR:
            pass
        elif type_==BETRAY:
            pass
        elif type_==CONFUSION:
            pass
        elif type_==AGGREDUCE_CHAR:
            pass
        elif type_==PARALYZE:
            multiplier = 2 - cls.SQRT_MEN_BONUS[target.getStat().getMEN()]
        return Math.max(0, multiplier)

    def getSTRBonus(cls, activeChar):
        """ generated source for method getSTRBonus """
        return cls.STR_BONUS[activeChar.getSTR()]

    def getLevelModifier(cls, attacker, target, skill):
        """ generated source for method getLevelModifier """
        if skill.getLevelDepend() == 0:
            return 1
        delta = (skill.getMagicLevel() if skill.getMagicLevel() > 0 else attacker.getLevel()) + skill.getLevelDepend() - target.getLevel()
        return 1 + ((0.01 if delta < 0 else 0.005) * delta)

    def getMatkModifier(cls, attacker, target, skill, bss):
        """ generated source for method getMatkModifier """
        mAtkModifier = 1
        if skill.isMagic():
            if bss:
                val = mAtk * 4.0
            mAtkModifier = (Math.sqrt(val) / target.getMDef(attacker, skill)) * 11.0
        return mAtkModifier

    def calcEffectSuccess(cls, attacker, target, effect, skill, shld, bss):
        """ generated source for method calcEffectSuccess """
        if shld == cls.SHIELD_DEFENSE_PERFECT_BLOCK:
            return False
        type_ = effect.effectType
        baseChance = effect.effectPower
        if type_ == None:
            return Rnd.get(100) < baseChance
        if type_ == L2SkillType.CANCEL:
            return True
        statModifier = cls.calcSkillStatModifier(type_, target)
        skillModifier = cls.calcSkillVulnerability(attacker, target, skill, type_)
        mAtkModifier = cls.getMatkModifier(attacker, target, skill, bss)
        lvlModifier = cls.getLevelModifier(attacker, target, skill)
        rate = Math.max(1, Math.min((baseChance * statModifier * skillModifier * mAtkModifier * lvlModifier), 99))
        if Config.DEVELOPER:
            cls.LOGGER.info("calcEffectSuccess(): name:{} eff.type:{} power:{} statMod:{} skillMod:{} mAtkMod:{} lvlMod:{} total:{}%.", skill.__name__, type_.__str__(), baseChance, String.format("%1.2f", statModifier), String.format("%1.2f", skillModifier), String.format("%1.2f", mAtkModifier), String.format("%1.2f", lvlModifier), String.format("%1.2f", rate))
        return (Rnd.get(100) < rate)

    def calcSkillSuccess(cls, attacker, target, skill, shld, bss):
        """ generated source for method calcSkillSuccess """
        if shld == cls.SHIELD_DEFENSE_PERFECT_BLOCK:
            return False
        type_ = skill.getEffectType()
        if target.isRaidRelated() and not calcRaidAffected(type_):
            return False
        baseChance = skill.getEffectPower()
        if skill.ignoreResists():
            return (Rnd.get(100) < baseChance)
        statModifier = cls.calcSkillStatModifier(type_, target)
        skillModifier = cls.calcSkillVulnerability(attacker, target, skill, type_)
        mAtkModifier = cls.getMatkModifier(attacker, target, skill, bss)
        lvlModifier = cls.getLevelModifier(attacker, target, skill)
        rate = Math.max(1, Math.min((baseChance * statModifier * skillModifier * mAtkModifier * lvlModifier), 99))
        if Config.DEVELOPER:
            cls.LOGGER.info("calcSkillSuccess(): name:{} type:{} power:{} statMod:{} skillMod:{} mAtkMod:{} lvlMod:{} total:{}%.", skill.__name__, skill.getSkillType().__str__(), baseChance, String.format("%1.2f", statModifier), String.format("%1.2f", skillModifier), String.format("%1.2f", mAtkModifier), String.format("%1.2f", lvlModifier), String.format("%1.2f", rate))
        return (Rnd.get(100) < rate)

    def calcCubicSkillSuccess(cls, attacker, target, skill, shld, bss):
        """ generated source for method calcCubicSkillSuccess """
        if calcSkillReflect(target, skill) != cls.SKILL_REFLECT_FAILED:
            return False
        if shld == cls.SHIELD_DEFENSE_PERFECT_BLOCK:
            return False
        type_ = skill.getEffectType()
        if target.isRaidRelated() and not calcRaidAffected(type_):
            return False
        baseChance = skill.getEffectPower()
        if skill.ignoreResists():
            return Rnd.get(100) < baseChance
        mAtkModifier = 1
        if skill.isMagic():
            if bss:
                val = mAtk * 4.0
            mAtkModifier = (Math.sqrt(val) / target.getMDef(None, None)) * 11.0
        statModifier = cls.calcSkillStatModifier(type_, target)
        skillModifier = cls.calcSkillVulnerability(attacker.getOwner(), target, skill, type_)
        lvlModifier = cls.getLevelModifier(attacker.getOwner(), target, skill)
        rate = Math.max(1, Math.min((baseChance * statModifier * skillModifier * mAtkModifier * lvlModifier), 99))
        if Config.DEVELOPER:
            cls.LOGGER.info("calcCubicSkillSuccess(): name:{} type:{} power:{} statMod:{} skillMod:{} mAtkMod:{} lvlMod:{} total:{}%.", skill.__name__, skill.getSkillType().__str__(), baseChance, String.format("%1.2f", statModifier), String.format("%1.2f", skillModifier), String.format("%1.2f", mAtkModifier), String.format("%1.2f", lvlModifier), String.format("%1.2f", rate))
        return (Rnd.get(100) < rate)

    def calcMagicSuccess(cls, attacker, target, skill):
        """ generated source for method calcMagicSuccess """
        lvlDifference = target.getLevel() - ((skill.getMagicLevel() if skill.getMagicLevel() > 0 else attacker.getLevel()) + skill.getLevelDepend())
        rate = 100
        if lvlDifference > 0:
            rate = (Math.pow(1.166, lvlDifference)) * 100
        if isinstance(attacker, (Player, )) and (attacker).getExpertiseWeaponPenalty():
            rate += 6000
        if Config.DEVELOPER:
            cls.LOGGER.info("calcMagicSuccess(): name:{} lvlDiff:{} fail:{}%.", skill.__name__, lvlDifference, String.format("%1.2f", rate / 100))
        rate = Math.min(rate, 9900)
        return (Rnd.get(10000) > rate)

    def calcManaDam(cls, attacker, target, skill, ss, bss):
        """ generated source for method calcManaDam """
        mAtk = attacker.getMAtk(target, skill)
        mDef = target.getMDef(attacker, skill)
        mp = target.getMaxMp()
        if bss:
            mAtk *= 4
        elif ss:
            mAtk *= 2
        damage = (Math.sqrt(mAtk) * skill.getPower(attacker) * (mp / 97)) / mDef
        damage *= cls.calcSkillVulnerability(attacker, target, skill, skill.getSkillType())
        return damage

    def calculateSkillResurrectRestorePercent(cls, baseRestorePercent, caster):
        """ generated source for method calculateSkillResurrectRestorePercent """
        if baseRestorePercent == 0 or baseRestorePercent == 100:
            return baseRestorePercent
        restorePercent = baseRestorePercent * cls.WIT_BONUS[caster.getWIT()]
        if restorePercent - baseRestorePercent > 20.0:
            restorePercent += 20.0
        restorePercent = Math.max(restorePercent, baseRestorePercent)
        restorePercent = Math.min(restorePercent, 90.0)
        return restorePercent

    def calcPhysicalSkillEvasion(cls, target, skill):
        """ generated source for method calcPhysicalSkillEvasion """
        if skill.isMagic():
            return False
        return Rnd.get(100) < target.calcStat(Stats.P_SKILL_EVASION, 0, None, skill)

    def calcSkillMastery(cls, actor, sk):
        """ generated source for method calcSkillMastery """
        if not (isinstance(actor, (Player, ))):
            return False
        if sk.getSkillType() == L2SkillType.FISHING:
            return False
        val = actor.getStat().calcStat(Stats.SKILL_MASTERY, 0, None, None)
        if (actor).isMageClass():
            val *= cls.INT_BONUS[actor.getINT()]
        else:
            val *= cls.STR_BONUS[actor.getSTR()]
        return Rnd.get(100) < val

    def calcValakasAttribute(cls, attacker, target, skill):
        """ generated source for method calcValakasAttribute """
        calcPower = 0
        calcDefen = 0
        if skill != None and skill.getAttributeName().contains("valakas"):
            calcPower = attacker.calcStat(Stats.VALAKAS, calcPower, target, skill)
            calcDefen = target.calcStat(Stats.VALAKAS_RES, calcDefen, target, skill)
        else:
            calcPower = attacker.calcStat(Stats.VALAKAS, calcPower, target, skill)
            if calcPower > 0:
                calcPower = attacker.calcStat(Stats.VALAKAS, calcPower, target, skill)
                calcDefen = target.calcStat(Stats.VALAKAS_RES, calcDefen, target, skill)
        return calcPower - calcDefen

    def calcElemental(cls, attacker, target, skill):
        """ generated source for method calcElemental """
        if skill != None:
            if element > 0:
                return 1 + (((attacker.getAttackElementValue(element) / 10.0) / 100.0) - (1 - target.getDefenseElementValue(element)))
            return 1
        elemDamage = 0
        i = 1
        while i < 7:
            elemDamage += Math.max(0, (attackerBonus - (attackerBonus * (target.getDefenseElementValue(i) / 100.0))))
            if target.getDefenseElementValue(i) < 1:
                elemDamage = elemDamage * target.getDefenseElementValue(i)
            i += 1
        return elemDamage

    def calcSkillReflect(cls, target, skill):
        """ generated source for method calcSkillReflect """
        if skill.ignoreResists() or not skill.canBeReflected():
            return cls.SKILL_REFLECT_FAILED
        if not skill.isMagic() and (skill.getCastRange() == -1 or skill.getCastRange() > cls.MELEE_ATTACK_RANGE):
            return cls.SKILL_REFLECT_FAILED
        reflect = cls.SKILL_REFLECT_FAILED
        if skill.getSkillType()==BUFF:
            pass
        elif skill.getSkillType()==REFLECT:
            pass
        elif skill.getSkillType()==HEAL_PERCENT:
            pass
        elif skill.getSkillType()==MANAHEAL_PERCENT:
            pass
        elif skill.getSkillType()==HOT:
            pass
        elif skill.getSkillType()==CPHOT:
            pass
        elif skill.getSkillType()==MPHOT:
            pass
        elif skill.getSkillType()==UNDEAD_DEFENSE:
            pass
        elif skill.getSkillType()==AGGDEBUFF:
            pass
        elif skill.getSkillType()==CONT:
            return cls.SKILL_REFLECT_FAILED
        elif skill.getSkillType()==PDAM:
            pass
        elif skill.getSkillType()==BLOW:
            pass
        elif skill.getSkillType()==MDAM:
            pass
        elif skill.getSkillType()==DEATHLINK:
            pass
        elif skill.getSkillType()==CHARGEDAM:
            if venganceChance > Rnd.get(100):
                reflect |= cls.SKILL_REFLECT_VENGEANCE
        reflectChance = target.calcStat(Stats.REFLECT_SKILL_MAGIC if (skill.isMagic()) else Stats.REFLECT_SKILL_PHYSIC, 0, None, skill)
        if Rnd.get(100) < reflectChance:
            reflect |= cls.SKILL_REFLECT_SUCCEED
        return reflect

    def calcFallDam(cls, actor, fallHeight):
        """ generated source for method calcFallDam """
        if not Config.ENABLE_FALLING_DAMAGE or fallHeight < 0:
            return 0
        return actor.calcStat(Stats.FALL, fallHeight * actor.getMaxHp() / 1000, None, None)

    def calcRaidAffected(cls, type_):
        """ generated source for method calcRaidAffected """
        if type_==MANADAM:
            pass
        elif type_==MDOT:
            return True
        elif type_==CONFUSION:
            pass
        elif type_==ROOT:
            pass
        elif type_==STUN:
            pass
        elif type_==MUTE:
            pass
        elif type_==FEAR:
            pass
        elif type_==DEBUFF:
            pass
        elif type_==PARALYZE:
            pass
        elif type_==SLEEP:
            pass
        elif type_==AGGDEBUFF:
            pass
        elif type_==AGGREDUCE_CHAR:
            if Rnd.get(1000) == 1:
                return True
        return False

    def calculateKarmaLost(cls, level, exp):
        """ generated source for method calculateKarmaLost """
        return int((exp / PlayerLevelData.getInstance().getPlayerLevel(level).getKarmaModifier() / 15))

    def calculateKarmaGain(cls, pkCount, isSummon):
        """ generated source for method calculateKarmaGain """
        result = 14400
        if pkCount < 100:
            result = int((((((pkCount - 1) * 0.5) + 1) * 60) * 4))
        elif pkCount < 180:
            result = int((((((pkCount + 1) * 0.125) + 37.5) * 60) * 4))
        if isSummon:
            result = ((pkCount & 3) + result) >> 2
        return result

    def getLevelMod(cls, level):
        return (100.0 - 11 + level) / 100.0;


    def calc_patk(cls, strval, levelmod):
        return cls.STR_BONUS[strval] * levelmod;

    def calc_pdef(cls, levelmod):
        return levelmod;

    def calc_mpmax(cls, menval):
        return cls.MEN_BONUS[menval]

    def calc_hpmax(cls, conval):
        return cls.CON_BONUS[conval]

    def calc_mdef(cls, menval, levelmod):
        return cls.MEN_BONUS[menval] * levelmod

    def calc_matk(cls, intval, levelmod):
        intb = cls.INT_BONUS[intval]
        lvlb = levelmod
        return ((lvlb * lvlb) * (intb * intb))

    def calc_patk_speed(cls, dexval):
        return cls.DEX_BONUS[dexval]

    def calc_patk_critical(cls, dexval):
	return cls.DEX_BONUS[dexval] * 10

    def calc_evasion(cls, dexval, level):
        return cls.BASE_EVASION_ACCURACY[dexval] + level

    def calc_move_speed(cls, dexval):
        return cls.DEX_BONUS[dexval]


a = Formulas()
#print 'P ATTACK: ' + str(a.calc_patk(60, a.getLevelMod(25)) * 22.45)
#print 'P DEF: ' + str(814.7 * a.calc_pdef(a.getLevelMod(25)))
#print 'M ATTACK: ' + str(a.calc_matk(76, a.getLevelMod(25)) * 1)
#print 'M DEF: ' + str(a.calc_mdef(80, a.getLevelMod(25)) * 149.04)
#print 'MP: ' + str(a.calc_mpmax(80) * 1676)
#print "HP: " + str(a.calc_hpmax(57) * 43316.308)
#
#print 'P ATTACK Speed: ' + str(a.calc_patk_speed(73) * 253)
#print 'P ATTACK Critical: ' + str(a.calc_patk_critical(73) * 4)
#print 'Move Speed: ' + str(a.calc_move_speed(73) * 190)
#print 'Evasion: ' + str(a.calc_evasion(73, 25))
#print 'HP Regen: ' + str(a.calcHpRegen(18.4385313667577, 57, a.getLevelMod(25)))
#print 'MP Regen: ' + str(a.calcMpRegen(1.5, 80, a.getLevelMod(25)))
#calcHpRegen(cls, init, conval, level_mod):

data ="""
 <npc id="25369" name="Soul Scavenger" title="Raid Boss">
  <set name="level" val="251"/>
  <set name="radius" val="20"/>
  <set name="height" val="42"/>
  <set name="rHand" val="0"/>
  <set name="lHand" val="0"/>
  <set name="type" val="RaidBoss"/>
  <set name="exp" val="612531"/>
  <set name="sp" val="52691"/>
  <set name="hp" val="4336.3085364372"/>
  <set name="mp" val="167"/>
  <set name="hpRegen" val="18.4385313667577"/>
  <set name="mpRegen" val="1.5"/>
  <set name="pAtk" val="74.2223188804512"/>
  <set name="pDef" val="314.7"/>
  <set name="mAtk" val="1"/>
  <set name="mDef" val="141.04"/>
  <set name="crit" val="4"/>
  <set name="atkSpd" val="251"/>
  <set name="str" val="61"/>
  <set name="int" val="71"/>
  <set name="dex" val="71"/>
  <set name="wit" val="71"/>
  <set name="con" val="51"/>
  <set name="men" val="81"/>
  <set name="corpseTime" val="7"/>
  <set name="walkSpd" val="100"/>
  <set name="runSpd" val="192"/>
  <set name="dropHerbGroup" val="0"/>
  <ai aggro="0" canMove="true" seedable="false" spsCount="0" spsRate="0" ssCount="0" ssRate="0" type="DEFAULT"/>
  <skills>
  </skills>
 </npc>
"""

def check_and_fix(npc, all_npcdata):
        npc_id = int(npc['id'])
        print("Checking npc id: %s" % npc_id)
        #if not npc_id == 20507:
        #    return
        if not npc_id in all_npcdata:
            print("NPC not found!")
            return
        level = int(npc.find("set", {"name": "level"})['val'])
        exp = int(npc.find("set", {"name": "exp"})['val'])
        sp = int(npc.find("set", {"name": "sp"})['val'])
        hp = float(npc.find("set", {"name": "hp"})['val'])
        mp = float(npc.find("set", {"name": "mp"})['val'])
        mpregen = float(npc.find("set", {"name": "mpRegen"})['val'])
        hpregen = float(npc.find("set", {"name": "hpRegen"})['val'])
        patk = float(npc.find("set", {"name": "pAtk"})['val'])
        pdef = float(npc.find("set", {"name": "pDef"})['val'])
        matk = float(npc.find("set", {"name": "mAtk"})['val'])
        mdef = float(npc.find("set", {"name": "mDef"})['val'])
        patk_critical = float(npc.find("set", {"name": "crit"})['val'])
        patk_speed = float(npc.find("set", {"name": "atkSpd"})['val'])
        run_speed = int(npc.find("set", {"name": "runSpd"})['val'])

        strval = int(npc.find("set", {"name": "str"})['val'])
        intval = int(npc.find("set", {"name": "int"})['val'])
        dexval = int(npc.find("set", {"name": "dex"})['val'])
        witval = int(npc.find("set", {"name": "wit"})['val'])
        conval = int(npc.find("set", {"name": "con"})['val'])
        menval = int(npc.find("set", {"name": "men"})['val'])

        npcdata = all_npcdata[npc_id]

        # check and fix basic attrs
        if strval != npcdata['str']:
            npc.find("set", {"name": "str"})['val'] = npcdata['str']
            print("Corrected STR")
        if intval != npcdata['int']:
            npc.find("set", {"name": "int"})['val'] = npcdata['int']
            print("Corrected INT")
        if dexval != npcdata['dex']:
            npc.find("set", {"name": "dex"})['val'] = npcdata['dex']
            print("Corrected dex")
        if witval != npcdata['wit']:
            npc.find("set", {"name": "wit"})['val'] = npcdata['wit']
            print("Corrected wit")
        if conval != npcdata['con']:
            npc.find("set", {"name": "con"})['val'] = npcdata['con']
            print("Corrected con")
        if menval != npcdata['men']:
            npc.find("set", {"name": "men"})['val'] = npcdata['men']
            print("Corrected men current %s new %s" % (menval, npcdata['men']))

        # level and exp and sp
        if level != npcdata['level']:
            npc.find("set", {"name": "level"})['val'] = npcdata['level']
            print("Corrected level current %s new %s" % (level, npcdata['level']))
        if exp != npcdata['exp']:
            npc.find("set", {"name": "exp"})['val'] = npcdata['exp']
            print("Corrected exp current %s new %s" % (exp, npcdata['exp']))
        if sp != npcdata['sp']:
            npc.find("set", {"name": "sp"})['val'] = npcdata['sp']
            print("Corrected sp")

        calc_hp = a.calc_hpmax(npcdata['con']) * hp
        if abs(calc_hp - npcdata['hp']) > 1:
            corrected = npcdata['hp'] / a.calc_hpmax(npcdata['con'])
            npc.find("set", {"name": "hp"})['val'] = corrected
            print("Wrong hp current %s, corrected: %s" % (str(hp), str(corrected)))

        calc_mp = a.calc_mpmax(npcdata['men']) * mp
        if abs(calc_mp - npcdata['mp']) > 1:
            corrected = npcdata['mp'] / a.calc_mpmax(npcdata['men'])
            npc.find("set", {"name": "mp"})['val'] = corrected
            print("Wrong mp, current %s, corrected: %s (%s)" % (str(mp), str(corrected), str(a.calc_mpmax(npcdata['men']) * corrected)))

        calc_patk = a.calc_patk(npcdata['str'], a.getLevelMod(npcdata['level'])) * patk
        if abs(calc_patk - npcdata['patk']) > 1:
            corrected = npcdata['patk'] / a.calc_patk(npcdata['str'], a.getLevelMod(npcdata['level']))
            npc.find("set", {"name": "pAtk"})['val'] = corrected
            print("Wrong patk, current %s, corrected: %s (%s)" % (str(patk), str(corrected), str(a.calc_patk(npcdata['str'], a.getLevelMod(npcdata['level']) * corrected))))

        calc_pdef = a.calc_pdef(a.getLevelMod(npcdata['level'])) * pdef
        if abs(calc_pdef - npcdata['pdef']) > 1:
            corrected = npcdata['pdef'] / a.calc_pdef(a.getLevelMod(npcdata['level']))
            npc.find("set", {"name": "pDef"})['val'] = corrected
            print("Wrong pdef, current %s, corrected: %s (%s)" % (str(pdef), str(corrected), str(a.calc_pdef(a.getLevelMod(npcdata['level'])) * corrected)))

        calc_matk = a.calc_matk(npcdata['int'], a.getLevelMod(npcdata['level'])) * matk
        print ("MATK %s " % calc_matk)
        if abs(calc_matk - npcdata['matk']) > 1:
            corrected = npcdata['matk'] / a.calc_matk(npcdata['int'], a.getLevelMod(npcdata['level']))
            npc.find("set", {"name": "mAtk"})['val'] = corrected
            print("Wrong matk, current %s, corrected: %s (%s)" % (str(matk), str(corrected), str(a.calc_matk(npcdata['int'], a.getLevelMod(npcdata['level'])) * corrected)))

        calc_mdef = a.calc_mdef(npcdata['men'], a.getLevelMod(npcdata['level'])) * mdef
        if abs(calc_mdef - npcdata['mdef']) > 1:
            corrected = npcdata['mdef'] / a.calc_mdef(npcdata['men'], a.getLevelMod(npcdata['level']))
            npc.find("set", {"name": "mDef"})['val'] = corrected
            print("Wrong mdef, current %s, corrected: %s (%s)" % (str(mdef), str(corrected), str(a.calc_mdef(npcdata['men'], a.getLevelMod(npcdata['level'])) * corrected)))

        calc_hpregen = a.calcHpRegen(hpregen, npcdata['con'], a.getLevelMod(npcdata['level']))
        if abs(calc_hpregen - npcdata['hp_regen']) > 1:
            corrected = npcdata['hp_regen'] / a.calc_HpRegen(npcdata['con'], a.getLevelMod(npcdata['level']))
            npc.find("set", {"name": "hpRegen"})['val'] = corrected
            print("Wrong hpregen, current %s, corrected: %s (%s)" % (str(hpregen), str(corrected), str(a.calcHpRegen(corrected, npcdata['con'], a.getLevelMod(npcdata['level'])))))

        calc_mpregen = a.calcMpRegen(mpregen, npcdata['men'], a.getLevelMod(npcdata['level']))
        if abs(calc_mpregen - npcdata['mp_regen']) > 1:
            corrected = npcdata['mp_regen'] / a.calc_MpRegen(npcdata['men'], a.getLevelMod(npcdata['level']))
            npc.find("set", {"name": "mpRegen"})['val'] = corrected
            print("Wrong mpregen, current %s, corrected: %s (%s)" % (str(mpregen), str(corrected), str(a.calcMpRegen(corrected, npcdata['men'], a.getLevelMod(npcdata['level'])))))

        calc_patk_speed = a.calc_patk_speed(npcdata['dex']) * patk_speed
        if abs(calc_patk_speed - npcdata['patk_speed']) > 1:
            corrected = int(math.ceil(npcdata['patk_speed'] / a.calc_patk_speed(npcdata['dex'])))
            npc.find("set", {"name": "atkSpd"})['val'] = corrected
            print("Wrong patk_speed, current %s, corrected: %s" % (str(patk_speed), str(corrected)))

        calc_run_speed = a.calc_move_speed(npcdata['dex']) * run_speed
        if abs(calc_run_speed - npcdata['run_speed']) > 1 and run_speed > 1:
            corrected = int(math.ceil(npcdata['run_speed'] / a.calc_move_speed(npcdata['dex'])))
            npc.find("set", {"name": "runSpd"})['val'] = corrected
            print("Wrong run_speed, current %s, corrected: %s" % (str(run_speed), str(corrected)))
        #calc_patk_critical = a.calc_patk_critical(npcdata['dex']) * patk_critical
        #if abs(calc_patk_critical - npcdata['patk_critical']) > 1:
            #corrected = npcdata['patk_critical'] / a.calc_patk_critical(npcdata['dex'])
            #npc.find("set", {"name": "crit"})['val'] = corrected
            #print("Wrong patk_critical, corrected: %s" % str(corrected))

        print("Done npc id: %s" % npc_id)
        #print 'P ATTACK: ' + str(a.calc_patk(60, a.getLevelMod(25)) * 22.45)
        #print 'P DEF: ' + str(814.7 * a.calc_pdef(a.getLevelMod(25)))
        #print 'M ATTACK: ' + str(a.calc_matk(76, a.getLevelMod(25)) * 1)
        #print 'M DEF: ' + str(a.calc_mdef(80, a.getLevelMod(25)) * 149.04)
        #print 'MP: ' + str(a.calc_mpmax(80) * 1676)
        #print "HP: " + str(a.calc_hpmax(57) * 43316.308)
        #
        #print 'P ATTACK Speed: ' + str(a.calc_patk_speed(73) * 253)
        #print 'P ATTACK Critical: ' + str(a.calc_patk_critical(73) * 4)
        #print 'Move Speed: ' + str(a.calc_move_speed(73) * 190)
        #print 'Evasion: ' + str(a.calc_evasion(73, 25))
        #print 'HP Regen: ' + str(a.calcHpRegen(18.4385313667577, 57, a.getLevelMod(25)))
        #print 'MP Regen: ' + str(a.calcMpRegen(1.5, 80, a.getLevelMod(25)))
        #print npc.prettify()



pattern = 'ID\s+.\s+(\d+?)\s+Level\s+.\s+(\d+?)\|Exp\s+.\s+(\d+?)\s+SP\s+.\s+(\d+?)\|\|HP\s+.\s+(\d+?)\s+HP Regeneration\s+.\s+(\d*,?\d*)\|MP\s+.\s+(\d+?)\s+MP Regeneration\s+.\s+(\d*,?\d*)\|\|P.Atk\s+.\s+(\d*,?\d*)\s+P.Def\s+.\s+(\d*,?\d*)\|M.Atk\s+.\s+(\d+?)\s+M.Def\s+.\s+(\d+?)\|P.Atk Speed\s+.\s+(\d+?)\s+M.Atk Speed\s+.\s+(\d+?)\|Atk Range\s+.\s+(\d+?)\|\|STR\s+.\s+(\d+?)\s+INT\s+.\s+(\d+?)\|CON\s+.\s+(\d+?)\s+WIT\s+.\s+(\d+?)\|DEX\s+.\s+(\d+?)\s+MEN\s+.\s+(\d+?)\|\|Aggro\s+.\s+(true|false)\s+Social\s+.\s+(true|false).*\|Walk Speed\s+.\s+(\d+?)\s+Run Speed\s+.\s+(\d+?)\|Sex'

def load():
    npcs = {}
    with open('skillname-stats.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #print(row['level'])
            stats = {}
            desc = row['description'].replace("\\\\n", "|")
            data = re.search(pattern, desc)
            if data:
                stats['id'] = int(data.group(1))
                stats['level'] = int(data.group(2))
                stats['exp'] = int(data.group(3))
                stats['sp'] = int(data.group(4))
                stats['hp'] = int(data.group(5))
                stats['hp_regen'] = float(data.group(6).replace(',', '.'))
                stats['mp'] = int(data.group(7))
                stats['mp_regen'] = float(data.group(8).replace(',', '.'))
                stats['patk'] = int(data.group(9))
                stats['pdef'] = int(data.group(10))
                stats['matk'] = int(data.group(11))
                stats['mdef'] = int(data.group(12))
                stats['patk_speed'] = int(data.group(13))
                stats['matk_speed'] = int(data.group(14))
                stats['atk_range'] = int(data.group(15))
                stats['str'] = int(data.group(16))
                stats['int'] = int(data.group(17))
                stats['con'] = int(data.group(18))
                stats['wit'] = int(data.group(19))
                stats['dex'] = int(data.group(20))
                stats['men'] = int(data.group(21))
                stats['agro'] = data.group(22)
                stats['social'] = data.group(23)
                stats['walk_speed'] = int(data.group(24))
                stats['run_speed'] = int(data.group(25))
            else:
                print desc
                break
            #if stats['id'] == 25369:
            #    for k, v in stats.iteritems():
            #        print k, v
            #    print desc
            #    print stats
            #    break
            #break
            npcs[stats['id']] = stats
    return npcs


def parse(old_xml_dir, new_xml_dir):
    npc_files = []
    npcdata = load()
    for file in os.listdir(old_xml_dir):
        if file.endswith(".xml"):
            # skip some files
            #if not "20000" in file :
            #if "12000-12999.xml" in file or "13000-13999.xml" in file:
            #        continue
            with open(os.path.join(old_xml_dir, file), "r") as f:
                contents = f.read()
                soup = BeautifulSoup(contents, "xml")
                npcs = soup.find_all("npc")

                for npc in npcs:
                    check_and_fix(npc, npcdata)

            with open(os.path.join(new_xml_dir, file), "w") as f:
                f.write(soup.prettify())
            #break

parse("aCis_datapack/data/xml/npcs/", "npcs_fixed/")
#npcdata = load()
#soup = BeautifulSoup(soup, "xml")
#npc = soup.find("npc")
#check_and_fix(npc, npcdata)
