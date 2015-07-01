from rccomponents import *

def extractDataMatrix(image):
    data = list(image.getdata())
    isTuple = False

    if type(data[0]) is tuple:
        isTuple = True
        data = [p[0] for p in data]

    return data, isTuple

def rcencrypt(image, maxIter = 1):
    #bits = image.bits
    bits = 8
    height = image.size[0]
    width = image.size[1]

    data, isTuple = extractDataMatrix(image)
    print data

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

    newImage = image.copy()
    newImage.putdata(convertToImageData(matrix))
    newImage.putdata(convertToImageData(matrix, isTuple))
    return newImage, Kr, Kc, maxIter

def decrypt(cypher, Kr, Kc, maxIter):
    height = cypher.size[0]
    width = cypher.size[1]

    data, isTuple = extractDataMatrix(cypher)
    print data

    print "converting to matrix..."
    matrix = convertToMatrix(data, height, width)

    iterations = 0
    while iterations < maxIter:
        iterations += 1

        KrRot = Kr[:-1:]
        matrix = transpose(matrix)
        XOR(matrix, Kr, KrRot)
        matrix = transpose(matrix)

        cypher.putdata(convertToImageData(matrix, isTuple))
        cypher.show()

        KcRot = Kc[:-1:]
        XOR(matrix, Kc, KcRot)

        cypher.putdata(convertToImageData(matrix, isTuple))
        cypher.show()

        matrix = transpose(matrix)
        matrix = scramble(matrix, width, Kc, True)
        matrix = transpose(matrix)

        cypher.putdata(convertToImageData(matrix, isTuple))
        cypher.show()

        matrix = scramble(matrix, height, Kr, True)

        cypher.putdata(convertToImageData(matrix, isTuple))
        cypher.show()

    decryptedImage = cypher.copy()
    decryptedImage.putdata(convertToImageData(matrix))
    decryptedImage.putdata(convertToImageData(matrix))
    return decryptedImage

plainfile = Image.open("images.jpg").convert(mode="L", palette="ADAPTIVE", colors=256)
print plainfile

cypher, Kr, Kc, maxIter = rcencrypt(plainfile)
cypher.save("images_encrypted.png")

cypherfile = Image.open("images_encrypted.png").convert(mode="L", palette="ADAPTIVE", colors=256)
cypherfile.show()

decrypted = decrypt(cypherfile, Kr, Kc, maxIter)
decrypted.show()
decrypted.save("images_decrypted.png")
