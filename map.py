import random

def map(d): # This function generates the environment from a dimension (d) and number of mines (n).
    map = []
    for i in range(d): # loops make a dXd map full of 0's
        map.append([])
        for j in range(d):
            r = random.random()
            if r <= 0.2:
                map[i].append(1) # flat
            elif r <= 0.5:
                map[i].append(2) # hilly
            elif r <= 0.8:
                map[i].append(3) # forest
            else:
                map[i].append(4) # caves
    return map
######################################################################################################################
######################################################################################################################

# Driver script
d = 50 # environment dimension
map = map(d) # creates environment
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in map]))

