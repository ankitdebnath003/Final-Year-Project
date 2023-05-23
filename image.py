import math
import cv2

# Define allowed files.
allowedExtentions = {'bmp'}

"""
This function is used to check for the file extension and if the extension is allowed to be
used then the function proceed further.
"""
def isAllowedImageFile(fileName: str):
    return '.' in fileName and fileName.rsplit('.', 1)[1].lower() in allowedExtentions

"""
This function is used to do image encoding by modifying the pixels of the image 
and the message. It takes the image ,text and the image output name as input
and after encrypt the message into the image it saves the image locally to make
it available for download.
"""
def encodeImageData(imgFile: str, message: str, outputName: str):
    # Load the image.
    img = cv2.imread(imgFile)
    # Store each character's ASCII value of the message.
    message = [format(ord(i), '08b') for i in message]
    _, width, _ = img.shape
    # Algorithm to encode the image.
    pixelRequired = len(message) * 3
    rowRequired = pixelRequired / width
    rowRequired = math.ceil(rowRequired)

    count, charCount = 0, 0
    for i in range(rowRequired + 1):
        while count < width and charCount < len(message):
            char = message[charCount]
            charCount += 1
            # charIndex holds each characters index and char holds each character.
            for charIndex, char in enumerate(char):
                if (char == '1' and img[i][count][charIndex % 3] % 2 == 0) or (
                        char == '0' and img[i][count][charIndex % 3] % 2 == 1):
                    img[i][count][charIndex % 3] -= 1
                if charIndex % 3 == 2:
                    count += 1
                if charIndex == 7:
                    if charCount * 3 < pixelRequired and img[i][count][2] % 2 == 1:
                        img[i][count][2] -= 1
                    if charCount * 3 >= pixelRequired and img[i][count][2] % 2 == 0:
                        img[i][count][2] -= 1
                    count += 1
        count = 0
    # Write the encrypted image into a new file.
    cv2.imwrite(outputName, img)

"""
This function is used to decrypt the encrypted image file and get the encrypted 
message. It takes the image file as input and return the decoded message.
"""
def decodeImageData(imgFile: str):
    # Algorithm to decrypt the data from the image.
    img = cv2.imread(imgFile)
    data = []
    stop = False
    for rowIndex, row in enumerate(img):
        row.tolist()
        for pixelIndex, pixel in enumerate(row):
            if pixelIndex % 3 == 2:
                # By extracting the LSBs of the first two color channels and 
                # checking the LSB of the third color channel, the code is able 
                # to decode the information embedded in the image until the stop 
                # condition is met.
                data.append(bin(pixel[0])[-1])
                data.append(bin(pixel[1])[-1])
                if bin(pixel[2])[-1] == '1':
                    stop = True
                    break
            else:
                # Retrieves the first (red) color channel value of the pixel and
                # converts it to a binary string representation and takes the 
                # last character of that binary string. This last character 
                # represents the LSB of the red color channel.
                data.append(bin(pixel[0])[-1])
                # Retrieves the same data as the previous data, but for the 
                # second (green) color channel of the pixel.
                data.append(bin(pixel[1])[-1])
                # Retrieves the same data as the previous data, but for the 
                # third (blue) color channel of the pixel.
                data.append(bin(pixel[2])[-1])
        if stop:
            break
    decodedMessage = []
    # Join all the bits to form letters.
    for i in range(int((len(data) + 1) / 8)):
        decodedMessage.append(data[i * 8:(i * 8 + 8)])
    # Join all the letters to form the message.
    decodedMessage = [chr(int(''.join(i), 2)) for i in decodedMessage]
    # os.remove(imgFile)
    return ''.join(decodedMessage)