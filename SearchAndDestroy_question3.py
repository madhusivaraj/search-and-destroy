import random

def terrain_p_map(d): # Makes dxd map of terrains. Terrains represented by their p of giving false negatives.
    map = []
    for i in range(d):
        map.append([])
        for j in range(d):
            r = random.random()
            if r <= 0.2: # p of terrain being flat
                map[i].append(0.1) # p of false negative when searching flat terrain
            elif r <= 0.5: # p of terrain being hilly
                map[i].append(0.3) # p of false negative when searching hills
            elif r <= 0.8: # p of terrain being forrest
                map[i].append(0.7) # p of false negative when searching forest
            else: # p of terrain being caves
                map[i].append(0.9) # p of false negative when searching caves
    return map

def initial_pmap(d): # Initializes map of belief, each cell starting with equal p
    pmap = []
    p = 1/(d**2) # initial p of target in any cell is 1/(total cell number)
    for i in range(d):
        pmap.append([])
        for j in range(d):
            pmap[i].append(p)
    return pmap

def pmap_update(pmap, newdata, map): # Performs Bayesian update on all beliefs
    d = len(map)
    denom = 0 # denominator in Bayes' theorem used to update each p in belief map
    for i in range(d): # denom is sum over all i,j of P(is in cell i,j | all prev data) * P(most recent data | is in cell i,j)
        for j in range(d):
            if i == newdata[0] and j == newdata[1]: # if cell in question is latest cell queried
                denom = denom + pmap[i][j]*map[i][j] # P(most recent data | is in cell i,j) = that cell's terrain's prob of (false) neg
            else:
                denom = denom + pmap[i][j]*1 # P(most recent data | is in cell i,j) = that cell's prob of neg = 1
    for i in range(d):
        for j in range(d):
            if i == newdata[0] and j == newdata[1]:
                pmap[i][j] = pmap[i][j]*map[i][j]/denom # Posterior = Prior * Likelihood / Evidence
            else:
                pmap[i][j] = pmap[i][j]*1/denom # Posterior = Prior * Likelihood / Evidence
    return pmap

def highest_p_having(pmap): # Finds and returns cell with highest p of having target
    d = len(pmap)
    maxp = 0
    max_coord = [0, 0]
    for i in range(d):
        for j in range(d):
            if pmap[i][j] > maxp: # if current p is greater than previous max
                maxp = pmap[i][j] # it's the new max
                max_coord = [i, j] # note coordinates
    return max_coord

def highest_p_finding(pmap,tmap): # Finds and returns cell with highest p of finding target
    d = len(pmap)
    pfmap = [] # makes new map of p's of finding target at each cell
    for i in range(d):
        pfmap.append([])
        for j in range(d):
            pfmap[i].append(pmap[i][j]*(1-tmap[i][j])) # "p of finding" = (p of having) * (p of seeing it if there)
    maxp = 0
    max_coord = [0, 0]
    for i in range(d):
        for j in range(d):
            if pfmap[i][j] > maxp: # if current p is greater than previous max
                maxp = pfmap[i][j] # it's the new max
                max_coord = [i, j] # note coordinates
    return max_coord

def sum_probs(pmap): # sums up all p's in belief map to ensure they sum to 1
    d = len(pmap)
    totsum = 0
    for i in range(d):
        totsum = totsum + sum(pmap[i])
    print('Total sum of probabilities is',totsum,'.')

def SearchAndDestroy(d, decisionRule, movingAgent, movingTarget):
    # Initialize
    d = 50
    tmap = terrain_p_map(d) # map of terrains, represented by their p of giving false negatives
    pmap = initial_pmap(d) # map of agent's belief that target is in each cell
    newGuess = [random.randint(0, d-1),random.randint(0, d-1)] # initial cell to query
    initGuess = newGuess
    targetLocation = [random.randint(0, d-1),random.randint(0, d-1)] # (initial) target location
    count = 0

    ruleResults = []
    # Loop for rule 1
    while True:
        count += 1
        if newGuess == targetLocation: # if the target is in the queried cell
            if random.random() > tmap[newGuess[0]][newGuess[1]]: # if you don't get a false negative
                ruleResults.append(count)
                #print('Target found at',newGuess,'after',count,'queries.')
                #sum_probs(pmap)
                break
        else:
            pmap = pmap_update(pmap, newGuess, tmap) # update belief map
        newGuess = highest_p_having(pmap)

    # Loop for rule 2
    count = 0
    newGuess = initGuess
    pmap = initial_pmap(d)
    while True:
        count += 1
        if newGuess == targetLocation: # if the target is in the queried cell
            if random.random() > pmap[newGuess[0]][newGuess[1]]: # if you don't get a false negative
                ruleResults.append(count)
                #print('Target found at',newGuess,'after',count,'queries.')
                #sum_probs(pmap)
                break
        else:
            pmap = pmap_update(pmap, newGuess, tmap) # update belief map
        newGuess = highest_p_finding(pmap,tmap)
    print('Rule 1',ruleResults[0],'Rule 2',ruleResults[1])
    return ruleResults
            
#########################################################################################################
#########################################################################################################

# Driver Script
d = 50 # dimension of map
decisionRule = 0 # 0 = choose highest p of having target; 1 = choose highest p of finding target
movingAgent = 0 # 0 = default; 1 = agent moves according to question 4
movingTarget = 0 # 0 = target stationary; 1 = target moves according to bonus criteria
#SearchAndDestroy(d, decisionRule, movingAgent, movingTarget)

runs = 30
rule1Results = []
rule2Results = []
for i in range(runs):
    [a,b] = SearchAndDestroy(d, decisionRule, movingAgent, movingTarget)
    rule1Results.append(a)
    rule2Results.append(b)
import statistics
rule1Avg = statistics.mean(rule1Results)
rule1Stdev = statistics.stdev(rule1Results)
rule2Avg = statistics.mean(rule2Results)
rule2Stdev = statistics.stdev(rule2Results)
print('Rule 1 performance = ',rule1Avg,'+-',rule1Stdev)
print('Rule 2 performance = ',rule2Avg,'+-',rule2Stdev)
