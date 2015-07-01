#! /env/bin/python
import os, sys
import random
from PIL import Image

def convertToMatrix(array, height, width):
    i = 0
    matrix = []

    for r in range(height):
        row = []
        for c in range(width):
             row.append(array[i])
             i += 1
        matrix.append(row)
    return matrix

def convertToImageData(matrix, isTuple = False):
    data = reduce(lambda x,y: x+y, matrix)
    if isTuple:
        data = map(lambda x: (x,x,x), data)
    return data

def circularShift(array, numPositions, right = True):
    numPositions = numPositions % len(array)
    if right:
        return array[numPositions:] + array[:numPositions]
    else:
        return array[-numPositions:] + array[:-numPositions]

def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

def scramble(matrix, height, key, left = False):
    i = 0
    while i < height:
        alphaI = sum(matrix[i])
        MalphaI = alphaI % 2
        if left:
            matrix[i] = circularShift(matrix[i], key[i], MalphaI != 0)
        else:
            matrix[i] = circularShift(matrix[i], key[i], MalphaI == 0)
        i += 1

    return matrix

def XOR(matrix, vector, rotatedVector):
    for i in range(len(matrix))[0:2:]:
        for j in range(len(vector)):
            matrix[i][j] = matrix[i][j] ^ vector[j]

    for i in range(len(matrix))[1:2:]:
        for j in range(len(rotatedVector)):
            matrix[i][j] = matrix[i][j] ^ rotatedVector[j]

def validate(matrix, bits, height, width):
    maxColor = 1 << bits
    for i in range(height):
        for j in range(width):
            if matrix[i][j] >= maxColor:
                return False
    return True

def createRandomVector(minValue, maxValue, length):
    return [random.randint(minValue, maxValue) for i in range(length)]

def encryptdecrypt(image, maxIter = 1):
    bits = image.bits
    height = image.size[0]
    width = image.size[1]
    data = image.getdata()
    isTuple = False

    if type(data[0]) is tuple:
        isTuple = True
        data = [p[0] for p in data]

    print "converting to matrix..."
    matrix = convertToMatrix(data, height, width)

    # step 1
    print "creating random vectors..."
    Kr = createRandomVector(0, 1 << bits, height)
    Kc = createRandomVector(0, 1 << bits, width)

    print Kr
    print Kc

    # step 2
    iterations = 0

    while iterations < maxIter:
        print "3"
        iterations += 1

        image.putdata(convertToImageData(matrix, isTuple))
        image.show()

        print "4"
        matrix = scramble(matrix, height, Kr)

        image.putdata(convertToImageData(matrix, isTuple))
        image.show()

        print validate(matrix, height, width, bits)

        print "5"
        matrix = transpose(matrix)
        matrix = scramble(matrix, width, Kc)
        matrix = transpose(matrix)

        image.putdata(convertToImageData(matrix, isTuple))
        image.show()

        print "6"
        KcRot = Kc[:-1:]
        XOR(matrix, Kc, KcRot)

        image.putdata(convertToImageData(matrix, isTuple))
        image.show()
        print validate(matrix, height, width, bits)

        print "7"
        KrRot = Kr[:-1:]
        matrix = transpose(matrix)
        XOR(matrix, Kr, KrRot)
        matrix = transpose(matrix)

        image.putdata(convertToImageData(matrix, isTuple))
        image.show()
        print validate(matrix, height, width, bits)

    #reverse the process
    iterations = 0
    while iterations < maxIter:
        KrRot = Kr[:-1:]
        matrix = transpose(matrix)
        XOR(matrix, Kr, KrRot)
        matrix = transpose(matrix)

        image.putdata(convertToImageData(matrix, isTuple))
        image.show()

        KcRot = Kc[:-1:]
        XOR(matrix, Kc, KcRot)

        image.putdata(convertToImageData(matrix, isTuple))
        image.show()


        matrix = transpose(matrix)
        matrix = scramble(matrix, width, Kc, True)
        matrix = transpose(matrix)

        image.putdata(convertToImageData(matrix, isTuple))
        image.show()

        matrix = scramble(matrix, height, Kr, True)

        image.putdata(convertToImageData(matrix, isTuple))
        image.show()

        print validate(matrix, height, width, bits)
        iterations += 1


    #newImage = Image.new(image.mode, image.size)
    #newImage.putdata(convertToImageData(matrix))
    #image.putdata(convertToImageData(matrix, isTuple))
    #return image, Kr, Kc, maxIter

def decrypt(cypher, Kr, Kc, maxIter):
    height = cypher.size[0]
    width = cypher.size[1]
    isTuple = False

    data = cypher.getdata()
    if type(data[0]) is tuple:
        isTuple = True
        data = [p[0] for p in data]

    print "converting to matrix..."
    matrix = convertToMatrix(data, height, width)

    iterations = 0
    while iterations < maxIter:
        iterations += 1

        #KrRot = Kr[:-1:]
        #matrix = transpose(matrix)
        #XOR(matrix, Kr, KrRot)
        #matrix = transpose(matrix)

        #KcRot = Kc[:-1:]
        #XOR(matrix, Kc, KcRot)



        matrix = transpose(matrix)
        matrix = scramble(matrix, width, Kc, True)
        matrix = transpose(matrix)

        cypher.putdata(convertToImageData(matrix, isTuple))
        cypher.show()

        matrix = scramble(matrix, height, Kr, True)

        cypher.putdata(convertToImageData(matrix, isTuple))
        cypher.show()

    #decryptedImage = Image.new(cypher.mode, cypher.size)
    #decryptedImage.putdata(convertToImageData(matrix))
    cypher.putdata(convertToImageData(matrix))
    return cypher


def main(args):
    filename = ""
    maxIters = 1
    if len(args) >= 1:
        filename = args[0]
    if len(args) >= 2:
        maxIters = int(args[1])

    print "filename: ", filename
    jpgfile = Image.open(filename)
    #print jpgfile.depth
    print "bits = ", jpgfile.bits
    print "bands =", jpgfile.getbands()
    print "mode =", jpgfile.mode


    print jpgfile.bits, jpgfile.size, jpgfile.format
    print jpgfile
    print jpgfile.info

    #jpgfile.show()

    print "encrypting"
    encryptdecrypt(jpgfile, 1)
    #cypher, Kr, Kc, maxIter = encryptdecrypt(jpgfile, 20)

    #cypher.save("cypher.jpg")

    #cypherfile = Image.open("cypher.jpg")
    #cypherfile.show()

    #decrypted = decrypt(cypherfile, Kr, Kc, maxIter)
    #decrypted.show()
    #decrypted.save("decrypted.jpg")

if __name__ == "__main__":
    args = sys.argv[1:]
    print args
    main(args)
