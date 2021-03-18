import numpy as np
import random as rd


# Sensor data to chances convertation
def sense(k, chances):
    for i in range(len(chances)):
        for j in range(len(chances[i])):
            if world[i][j] == measurements[k]:
                chances[i][j] = chances[i][j] * pHit
            else:
                chances[i][j] = chances[i][j] * pLoss
    equalizer = np.sum(chances)
    for i in range(len(chances)):
        for j in range(len(chances[i])):
            chances[i][j] = np.round(chances[i][j] / equalizer, 2)
    return chances


# Movement data to chances convertation
def move(k, chances):
    res = np.zeros((5, 5))

    if trace[k] == 'L':
        copy = chances[:, [0]]
        chances = np.delete(chances, 0, 1)
        chances = np.append(chances, copy, axis=1)

        for i in range(len(res)):
            for j in range(len(res[i])):
                res[i][j] = chances[i][j] * pExact
                res[i][j] = res[i][j] + chances[i][j - 1] * pOvershoot
                if j == len(res) - 1:
                    res[i][j] = res[i][j] + chances[i][0] * pUndershoot
                else:
                    res[i][j] = res[i][j] + chances[i][j + 1] * pUndershoot

        res = beatifulizer(res)

    elif trace[k] == 'R':
        copy = chances[:, [len(chances) - 1]]
        chances = np.delete(chances, len(chances) - 1, 1)
        chances = np.append(copy, chances, axis=1)

        for i in range(len(res)):
            for j in range(len(res[i])):
                res[i][j] = chances[i][j] * pExact
                res[i][j] = res[i][j] + chances[i][j - 1] * pUndershoot
                if j == len(res) - 1:
                    res[i][j] = res[i][j] + chances[i][0] * pOvershoot
                else:
                    res[i][j] = res[i][j] + chances[i][j + 1] * pOvershoot

        res = beatifulizer(res)

    elif trace[k] == 'D':
        copy = chances[[len(chances) - 1], :]
        chances = np.delete(chances, len(chances) - 1, 0)
        chances = np.append(copy, chances, axis=0)

        for i in range(len(res)):
            for j in range(len(res[i])):
                res[i][j] = chances[i][j] * pExact
                res[i][j] = res[i][j] + chances[i - 1][j] * pUndershoot
                if i == len(res) - 1:
                    res[i][j] = res[i][j] + chances[0][j] * pOvershoot
                else:
                    res[i][j] = res[i][j] + chances[i + 1][j] * pOvershoot

        res = beatifulizer(res)

    elif trace[k] == 'U':
        copy = chances[[0], :]
        chances = np.delete(chances, 0, 0)
        chances = np.append(chances, copy, axis=0)

        for i in range(len(res)):
            for j in range(len(res[i])):
                res[i][j] = chances[i][j] * pExact
                res[i][j] = res[i][j] + chances[i - 1][j] * pOvershoot
                if i == len(res) - 1:
                    res[i][j] = res[i][j] + chances[0][j] * pUndershoot
                else:
                    res[i][j] = res[i][j] + chances[i + 1][j] * pUndershoot

        res = beatifulizer(res)
    return res


def beatifulizer(array):
    for i in range(len(array)):
        for j in range(len(array[i])):
            array[i][j] = np.round(array[i][j], 2)
    return array


# Random 5x5 world generation - path is fixed
def worldgen():
    fieldtype = ['green', 'red']
    world = np.chararray((5, 5), 5, unicode=True)
    for i in range(len(world)):
        for j in range(len(world[i])):
            world[i][j] = fieldtype[rd.randrange(0, 2, 1)]
    measurements = [world[0][0], world[1][0], world[1][1], world[1][2], world[1][3], world[2][3], world[3][3],
                    world[4][3], world[4][2], world[4][1]]
    return world, measurements


p = np.ones(25) * 1 / 25
pHit = 0.6
pLoss = 0.2
pExact = 0.8
pOvershoot = 0.1
pUndershoot = 0.1

world, measurements = worldgen()
trace = ['D', 'R', 'R', 'R', 'D', 'D', 'D', 'L', 'L', 'L']  # Directions array for matrix shifting
chances = np.ones((5, 5)) * 1 / 25

for k in range(0, len(measurements)):
    print("Sensoring №" + str(k))
    chances = sense(k, chances)
    print(chances)
    print("\n")

    print("Moving №" + str(k))
    chances = move(k, chances)
    print(chances)
    print("\n")
