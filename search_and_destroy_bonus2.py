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
    targetLocation = [random.randint(0, d-1),random.randint(0, d-1)] # (initial) target location
    count = 0
    
    if movingTarget==1:
        tracker=brokenTracker(targetLocation,tmap) #Gets initial tracker result
        possibleCells=[] #List of tuples, where tuples represent coordinates where target might be according to the tracker. 
        for i in range (d):
            for j in range (d):
                if tmap[i][j]!=tracker:
                    possibleCells.append((i,j)) #If the cell is not the terrain specified by the tracker, it might have the target, so add this coordinate to the list
        cell_index=possibleCells[random.randint(0,len(possibleCells)-1)] #Choose random coordinate that might have target
        newGuess=[cell_index[0],cell_index[1]] #Sets guess to random coordinate that might have target


        while True:
            count+=1
            if newGuess == targetLocation:
               if random.random() > tmap[newGuess[0]][newGuess[1]]:  #false negative
                   print('Target found at',newGuess,'after',count,'queries.')
                   break
            else:
                targetLocation= moveTarget(targetLocation)
                tracker=brokenTracker(targetLocation,tmap)
                possibleCells.clear()
                for i in range (d):
                    for j in range (d):
                        if tmap[i][j]!=tracker:
                            possibleCells.append((i,j))

                cell_index=possibleCells[random.randint(0,len(possibleCells)-1)] #Choose random coordinate that might have target
                newGuess=[cell_index[0],cell_index[1]]
    # Loop
    else:
        while True:
            count += 1
            if newGuess == targetLocation: # if the target is in the queried cell
                if random.random() > tmap[newGuess[0]][newGuess[1]]: # if you don't get a false negative
                    print('Target found at',newGuess,'after',count,'queries.')
                    sum_probs(pmap)
                    break
            else:
                pmap = pmap_update(pmap, newGuess, tmap) # update belief map
            if decisionRule == 0: # choose newGuess based on the chosen decision rule
                newGuess = highest_p_having(pmap)
            else:
                newGuess = highest_p_finding(pmap,tmap)

def moveTarget(currLocation): #Bonus function: moves target randomly to a neighbor and returns array of size 2 that corresponds to a coordinate
    if currLocation[0]==0:
        if currLocation[1]==0: #top left corner 
            #look bottom, right
            num=random.randint(0,1)
            if num==0: #go bottom
                return [currLocation[0]+1,currLocation[1]]
            else: #go right
                return [currLocation[0],currLocation[1]+1]

        elif currLocation[1]==49: #top right corner
            #look bottom, left
            num=random.randint(0,1)
            if num==0: #go bottom
                return [currLocation[0]+1,currLocation[1]]
            else: #go left
                return [currLocation[0],currLocation[1]-1]
        else: #top row
            #look bottom, left, right
            num=random.randint(0,2)
            if num==0: #go bottom
                return [currLocation[0]+1,currLocation[1]]
            if num==1: #go left
                return [currLocation[0],currLocation[1]-1]
            else: #go right
                return [currLocation[0],currLocation[1]+1]
    elif currLocation[0]==49:
        if currLocation[1]==0: #bot left corner
            #look top, right
            num=random.randint(0,1)
            if num==0: #go top
                return [currLocation[0]-1,currLocation[1]]
            else: #go right
                return [currLocation[0],currLocation[1]+1]
        elif currLocation[1]==49: #bot right corner
            #look top, left
            num=random.randint(0,1)
            if num==0: #go top
                return [currLocation[0]-1,currLocation[1]]
            else: #go left
                return [currLocation[0],currLocation[1]-1]
        else: #bottom row
            #look top, left, right
            num=random.randint(0,2)
            if num==0: #go top
                return [currLocation[0]-1,currLocation[1]]
            if num==1: #go left
                return [currLocation[0],currLocation[1]-1]
            else: #go right
                return [currLocation[0],currLocation[1]+1]
    elif currLocation[1]==0: #For lefthand side, don't have to account for corners because they're accounted for in previous statements
        #look top, right, bot
        num=random.randint(0,2)
        if num==0: #go top
            return [currLocation[0]-1,currLocation[1]]
        if num==1: #go bot
            return [currLocation[0]+1,currLocation[1]]
        else: #go right
            return [currLocation[0],currLocation[1]+1]
    elif currLocation[1]==49: #for righthand side, don't have to account for corners again
        #look top, left, bot
        num=random.randint(0,2)
        if num==0: #go top
            return [currLocation[0]-1,currLocation[1]]
        if num==1: #go bot
            return [currLocation[0]+1,currLocation[1]]
        else: #go left
            return [currLocation[0],currLocation[1]-1]
    else: #non-edge cell
        #look top, left, right, bot
        num=random.randint(0,3)
        if num==0: #go top
            return [currLocation[0]-1,currLocation[1]]
        if num==1: #go bot
            return [currLocation[0]+1,currLocation[1]]
        elif num==2: #go right
            return [currLocation[0],currLocation[1]+1]
        else: #go left
            return [currLocation[0],currLocation[1]-1]

def brokenTracker(target, tmap): #Bonus function: Determines terrain that target is in, and returns a terrain where the target is not randomly. Terrains are defined by false negative rates.
    if tmap[target[0]][target[1]]==0.1:
        xd= [0.3,0.7,0.9]
        return xd[random.randint(0,2)]
    elif tmap[target[0]][target[1]]==0.3:
        xd= [0.1,0.7,0.9]
        return xd[random.randint(0,2)]
    elif tmap[target[0]][target[1]]==0.7:
        xd= [0.1,0.3,0.9]
        return xd[random.randint(0,2)]
    else:
        xd= [0.1,0.3,0.7]
        return xd[random.randint(0,2)]


#########################################################################################################
#########################################################################################################

# Driver Script
d = 50 # dimension of map
decisionRule = 0 # 0 = choose highest p of having target; 1 = choose highest p of finding target
movingAgent = 0 # 0 = default; 1 = agent moves according to question 4
movingTarget = 1 # 0 = target stationary; 1 = target moves according to bonus criteria
SearchAndDestroy(d, decisionRule, movingAgent, movingTarget)