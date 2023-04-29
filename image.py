from PIL import Image

# Define allowed files.
allowedExtentions = {'bmp'}

"""
This function is used to check for the file extension and if the extension is allowed to be
used then the function proceed further.
"""
def isAllowedImageFile(fileName):
    return '.' in fileName and fileName.rsplit('.', 1)[1].lower() in allowedExtentions

"""
This function is used to take a string data and converts each character of the 
string into its corresponding 8-bit binary representation using the ASCII value
and it takes the string as data and return the binary data. 
"""
def genData(data):
    binData = []

    # Convert each character into a binary representation.
    for ch in data:
        binData.append(format(ord(ch), '08b'))
    return binData

"""
This function is used for modifying the pixels of an image based on the binary 
data to be encoded. The function takes the pixels of the image and binary data
and embed the binary data into the pixels of the image.
"""
def modifyPixel(pixel, data):
    # Calling the function to get the binary data of the text message.
    dataList = genData(data)
    lenData = len(dataList)
    pixelIterator = iter(pixel)

    for i in range(lenData):
        # Extracting 3 pixels at a time.
        pixel = [value for value in pixelIterator.__next__()[:3] + pixelIterator.__next__()[:3] + pixelIterator.__next__()[:3]]

        # Modifies the pixel values based on the binary data, ensuring that '0' 
        # bits result in even pixel values and '1' bits result in odd pixel values.
        for j in range(0, 8):
            if dataList[i][j] == '0' and pixel[j] % 2 != 0:
                pixel[j] -= 1

            elif dataList[i][j] == '1' and pixel[j] % 2 == 0:
                if pixel[j] != 0:
                    pixel[j] -= 1
                else:
                    pixel[j] += 1

        # Eighth pixel of every set tells whether to stop or read further.
        # 0 means keep reading; 1 means the message is over.
        if i == lenData - 1:
            if pixel[-1] % 2 == 0 and pixel[-1] != 0:
                pixel[-1] -= 1
            else:
                pixel[-1] += 1
        elif pixel[-1] % 2 != 0:
                pixel[-1] -= 1

        pixel = tuple(pixel)
        yield pixel[0:3]
        yield pixel[3:6]
        yield pixel[6:9]

"""
This function is used to do image encoding by modifying the pixels of the image 
based on the provided data. It takes the image and text as input and embed the 
message into the pixel of the image.
"""
def encodeImagePixels(img, data):
    w = img.size[0]
    (x, y) = (0, 0)

    for pixel in modifyPixel(img.getdata(), data):
        # Putting modified pixels in the new image.
        img.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

"""
This function is used to do image encoding by modifying the pixels of the image 
and the message. It takes the image ,text and the image output name as input
and after encrypt the message into the image it it saves the image locally to make
it available for download.
"""
def encodeImageData(imageFilePath, msg, outputName):
    image = Image.open(imageFilePath, 'r')

    if (len(msg) == 0):
        raise ValueError('Data is empty')

    if len(msg) % 2 == 1:
        msg += ' '

    newImg = image.copy()
    # Calling the function to add message in each pixel of the image.
    encodeImagePixels(newImg, msg)
    # Saving the image locally to make it available for download.
    newImg.save(outputName, str(outputName.split(".")[1].upper()))

"""
This function is used to decrypt the encrypted image file and get the encrypted 
message. It takes the image file as input and return the decoded message.
"""
def decodeImageData(imageFile):
    image = Image.open(imageFile, 'r')
    decodedMsg = ''
    imgData = iter(image.getdata())

    while (True):
        pixels = [value for value in imgData.__next__()[:3] + imgData.__next__()[:3] + imgData.__next__()[:3]]
        binStr = ''
        for i in pixels[:8]:
            if (i % 2 == 0):
                binStr += '0'
            else:
                binStr += '1'

        decodedMsg += chr(int(binStr, 2))
        if (pixels[-1] % 2 != 0):
            return decodedMsg