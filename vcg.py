import random as rand
import itertools 

import logging as logger

valuationRange = (2, 20)
logger.basicConfig(level=logger.INFO)

def create_random_players(n: int):
    scenario = []
    for player in range(n):
        playerValuations = []
        for item in range(n):
            playerValuations.append(rand.randint(*valuationRange))
        scenario.append(playerValuations)

    logger.info("Created %d random players: ", n)
    if logger.getLogger().level == logger.INFO:
        for i in range(len(scenario)):
            logger.info("\tplayer %d: %s",i, str(scenario[i]))

    return scenario

def get_all_options_from_scenario(scenario): # O(n!)
    options = {}
    for currOption in (itertools.permutations(range(len(scenario)))):
        currValue = []
        for player, item in enumerate(currOption):
            currValue.append(scenario[player][item])
        options[currOption] = currValue
    
    logger.info("Calculated all the %d options: ", len(options))
    if logger.getLogger().level == logger.INFO and len(options) < 3:
        for optionIndex, key in enumerate(options.keys()):
            logger.info("\toption %d: %s", optionIndex, key)
            for playerIndex, value in enumerate(key):
                logger.info("\t\tfor player %d give item %d", playerIndex, value)
    elif logger.getLogger().level == logger.INFO:
        for key in options.keys():
            logger.info("\toption %s: %s", key, options[key])

    return options

def find_best_option(options:dict, withOutPlayer: int=-1):
    Max = -1
    for key in options:
        Sum = 0
        for i in range(len(options[key])):
            if i == withOutPlayer:
                continue
            Sum += options[key][i]
        if Sum > Max:
            Max = Sum
            bestOption = key
    if logger.getLogger().level == logger.INFO:
        if withOutPlayer == -1:
            logger.info("Best option is: %s", str(bestOption)+":"+str(options[bestOption]))
        else:
            logger.info("Best option without player %d is: %s", withOutPlayer, str(bestOption)+":"+str(options[bestOption]))
    return bestOption, options[bestOption]
   
def calculate_payments(options, bestOptionKey, n):
    payments = []
    for player in range(n):
        currBest, _ = find_best_option(options, withOutPlayer=player)
        SumWithoutPlayer = 0
        for i in range(len(options[currBest])):
            if i == player:
                continue
            SumWithoutPlayer += options[currBest][i]

        SumWithPlayer = 0
        for i in range(len(options[bestOptionKey])):
            if i == player:
                continue
            SumWithPlayer += options[bestOptionKey][i] 
        logger.info("calculated payment for player %d: %d-%d=%d", player, SumWithoutPlayer, SumWithPlayer, SumWithoutPlayer-SumWithPlayer)
        payments.append(SumWithoutPlayer-SumWithPlayer)
    
    return payments

n = 2
scenario = create_random_players(n)
options = get_all_options_from_scenario(scenario)
# options, n = {1: [8, 5, 3], 2: [4, 8, 5], 3: [3, 1, 3]}, 3 # example from class
bestOptionKey, bestOptionValues = find_best_option(options)
payments = calculate_payments(options, bestOptionKey, n)
print(payments)



