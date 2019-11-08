import random

def terrain_p_map(d):
    map = []
    for i in range(d):
        map.append([])
        for j in range(d):
            r = random.random()
            if r <= 0.2:
                map[i].append(0.1) # flat
            elif r <= 0.5:
                map[i].append(0.3) # hilly
            elif r <= 0.8:
                map[i].append(0.7) # forest
            else:
                map[i].append(0.9) # caves
    return map

def initial_pmap(d):
    pmap = []
    p = 1/(d**2)
    for i in range(d):
        pmap.append([])
        for j in range(d):
            pmap[i].append(p)
    return pmap

def pmap_update(pmap, newdata, map):
    d = len(map)
    denom = 0
    for i in range(d):
        for j in range(d):
            if i == newdata[0] and j == newdata[1]:
                denom = denom + pmap[i][j]*map[i][j]
            else:
                denom = denom + pmap[i][j]*1
    for i in range(d):
        for j in range(d):
            if i == newdata[0] and j == newdata[1]:
                pmap[i][j] = pmap[i][j]*map[i][j]/denom
            else:
                pmap[i][j] = pmap[i][j]*1/denom
    return pmap

def pick_newGuess(pmap):
    d = len(pmap)
    maxp = 0
    max_coord = [0, 0]
    for i in range(d):
        for j in range(d):
            if pmap[i][j] > maxp:
                maxp = pmap[i][j]
                max_coord = [i, j]
    return max_coord


def sum_probs(pmap):
    d = len(pmap)
    totsum = 0
    for i in range(d):
        totsum = totsum + sum(pmap[i])
    print('Total sum of probabilities is',totsum,'.')

##################################################################

# Initialize
d = 10
tmap = terrain_p_map(d)
pmap = initial_pmap(d)
newGuess = [random.randint(0, d-1),random.randint(0, d-1)]
hasTarget = 0
targetLocation = [random.randint(0, d-1),random.randint(0, d-1)]
count = 0
print("Initial Map", pmap)

# Loop
while hasTarget == 0:
    count += 1
    if newGuess == targetLocation:
        print('Target found at',newGuess,'after',count,'queries.')
        sum_probs(pmap)
        break
    else:
        pmap = pmap_update(pmap, newGuess, tmap)
    newGuess = pick_newGuess(pmap)
