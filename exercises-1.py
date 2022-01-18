from numpy import array # pip install numpy
from pprint import pprint # pip install pprint

#################
#   Functions   #
#################
def mod3(arg):
    return arg % 3

def weight(word):
    count = 0
    for i in word:
        if i != 0: count += 1
    return count

def d(word1, word2):
    if len(word1) != len(word2): return 0
    return weight([word1[i] - word2[i] for i in range(len(word1))])

def code(g):
    return array(
        [
            mod3(vec) for vec in [
                g[0] + g[0] + g[0],
                g[0],
                g[1],
                g[0] + g[0],
                g[1] + g[1],
                g[0] + g[1],
                g[0] + g[0] + g[1],
                g[0] + g[1] + g[1],
                g[0] + g[0] + g[1] + g[1],
            ]
        ]
    )

def dot(v1, v2):
    prod = 0
    if len(v1) == len(v2):
        for i in range(len(v1)):
            prod += v1[i] * v2[i]
    return prod

def matMul(m1, m2):
    return array([[dot(m, n) for m in m2] for n in m1])

def test(testCodeWord, ParityCheckMatrix, silent = False):
    syndrome = [dot(v, testCodeWord) for v in ParityCheckMatrix]
    if not silent: 
        pprint('Test code:')
        pprint(testCodeWord)

        pprint('Syndrome:')
        pprint(mod3(array(syndrome)))

    return mod3(array(syndrome))

def minD(code):
    weightList = []
    ncode = [mod3(word1 - word2) for word1 in code for word2 in code]
    for word in ncode:
        w = 0
        for i in word:
            if i != 0: w += 1

        if w != 0: weightList.append(w)

    return min(weightList)

#################
#   Exercise 1. #
#################
pprint('------- Exercise 1. -------')

n = 4
k = 2

# Basis vectors
x = array([1, 0, 1, 2])
y = array([0, 1, 1, 1])

# Generator matrix
G = array([ x, y ])

# The generated code
C = code(G)

pprint('The code C:')
pprint(C.tolist())

# 'The code C:'
# [[0, 0, 0, 0],
#  [1, 0, 1, 2],
#  [0, 1, 1, 1],
#  [2, 0, 2, 1],
#  [0, 2, 2, 2],
#  [1, 1, 2, 0],
#  [2, 1, 0, 2],
#  [1, 2, 0, 1]]

# Min Hamming distance
d = minD(C)

pprint('Min Hamming distance:')
pprint(d)

# 'Min Hamming distance:'
# 3

# Parity check matrix
h1 = mod3(array([-x[2], -y[2], 1, 0]))
h2 = mod3(array([-x[3], -y[3], 0, 1]))
H = array([ h1, h2 ])

pprint('Parity check matrix H:')
pprint(H)

# Test H
test([0, 1, 0, 1], H) # syndrome == [2, 0]

for v in C:
    test(v, H) # syndrome == [0, 0]

# Find if MDS
if d == n - k + 1: pprint('MDS') # This will be printed
else: pprint('Not MDS')   

#################
#   Exercise 2. #
#################
pprint('------- Exercise 2. -------')

zeroVec = [0, 0, 0, 0]

BallWithDistanceOfOnefromZeroVector = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
    [2, 0, 0, 0],
    [0, 2, 0, 0],
    [0, 0, 2, 0],
    [0, 0, 0, 2],
]

for word in BallWithDistanceOfOnefromZeroVector:
    test(word, H)

incomingMessage = [2, 0, 0, 1]

def findCoset(syndrome):
    for word in BallWithDistanceOfOnefromZeroVector:
        cosetHeaderSyndrome = test(word, H, True)
        
        isCoset = True;
        for index, value in enumerate(cosetHeaderSyndrome):
            if value != syndrome[index]: isCoset = False

        if isCoset:
            pprint('Coset:')
            pprint(word)
            return word

incomingSyndrome = test(incomingMessage, H, True) # [1, 0]

coset = findCoset(incomingSyndrome)

correctWord = mod3(array(incomingMessage) - array(coset)).tolist()
pprint('Correct word:')
pprint(correctWord)

#################
#   Exercise 3. #
#################
pprint('------- Exercise 3. -------')

h1 = array([1, 1, 1, 0])
h2 = array([2, 0, 1, 1])

H = array([ h1, h2 ])

C = code(H)

N = array(
    [
        [0],
        [1],
        [2],
        [1],
    ]
).transpose()

pprint(mod3(matMul(H,N)))
