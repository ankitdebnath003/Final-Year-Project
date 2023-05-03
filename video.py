import math
import os
import shutil
from subprocess import call, STDOUT
import cv2
from stegano import lsb

# Define allowed video files.
allowedExtentions = {'mp4', 'avi'}

"""
This function is used to check for the file extension and if the extension is allowed to be
used then the function proceed further.
"""
def isAllowedVideoFile(fileName):
    return '.' in fileName and fileName.rsplit('.', 1)[1].lower() in allowedExtentions

"""
This function is used to split the message to be encrypted into words of approximately
same length. It takes input the message and return the message after divided 
into words and returns the splitted list.
"""
def splitMessage(msg, count = 10):
    # Divide the string into equal number of words and store the length of each word.
    msgLength = math.ceil(len(msg) / count)
    c = 0
    currentMsg = ''
    splitMsg = []

    # Iterate over each word of the message.
    for ch in msg:
        currentMsg += ch
        c += 1

        # Checking if the word count matches the current character count then add
        # the current word to the list.
        if c == msgLength:
            splitMsg.append(currentMsg)
            currentMsg = ''
            c = 0
    if c != 0:
        splitMsg.append(currentMsg)
    return splitMsg

"""
This function is used to extract frames from a video file and saving them as 
individual image files in a temporary folder.
"""
def extractFrames(video):
    # Checking if the temp folder not exist then create a folder named temp.
    if not os.path.exists("./temp"):
        os.makedirs("temp")
    tempFolder = "./temp"
    vidCap = cv2.VideoCapture(video)
    count = 0
    while True:
        success, image = vidCap.read()
        if not success:
            break
        # Extract the frames and create .png files in the temp folder.
        cv2.imwrite(os.path.join(tempFolder, "{:d}.png".format(count)), image)
        count += 1

"""
This function is used to hide existed encrypted message in the frames.
"""
def hideExistingMsg(frameList):
    for f_name in frameList:
        # Hide an empty string to overwrite the existing text.
        secret_enc = lsb.hide(f_name, " ")  
        secret_enc.save(f_name)

"""
This function is used to get the encrypted message if it exists in any frame of
the video and return the frame list.
"""
def getExistingEncryptedFrame(root = "./temp/"):
    frameList = []
    try:
        # Iterate over each frames to get the encrypted message if exists.
        for i in range(0, len(os.listdir(root)) - 1):
            frameName = "{}{}.png".format(root, i)
            # Get the encrypted message if exist otherwise it will go to the except block.
            secretMsg = lsb.reveal(frameName)
            # If it gets any encrypted message then add the frame name to the list.
            frameList.append(frameName)
            if secretMsg is None:
                break
    except:
        return frameList
    
"""
This function is used to embed the encrypted messages into the frames of the video.
"""
def embedMessageInFrames(msg, root = "./temp/"):
    splitMsgList = splitMessage(msg)
    for i in range(0, len(splitMsgList)):
        frameName = "{}{}.png".format(root, i)
        # Embed the split message into the frame.
        embeddedFrame = lsb.hide(frameName, splitMsgList[i])
        embeddedFrame.save(frameName)

"""
This function is used to clear the temp folder that stores each frame of the video file.
"""
def cleanTempFolder(path = "./temp"):
    if os.path.exists(path):
        shutil.rmtree(path)

"""
This function is used to decode the video file and get the encrypted message and
return it.
"""
def decodeVideo(file):
    # Calling the function the extract the frames from the video file.
    extractFrames(file)
    encryptedMsg = []
    root = "./temp/"
    decodedMsg = ''
    try:
        # Getting the encrypted messages from each frame of the video file.
        for i in range(0, len(os.listdir(root)) - 1):
            frameName = "{}{}.png".format(str(root), str(i))
            hiddenMsg = lsb.reveal(frameName)
            if hiddenMsg is None:
                break
            encryptedMsg.append(hiddenMsg)
    except IndexError as e:
        print('')

    # Join the list of the encrypted message as a string.
    decodedMsg = decodedMsg.join([i for i in encryptedMsg])
    cleanTempFolder()
    os.remove(file)
    if decodedMsg == '':
        return "No encrypted message is in the video file."
    return decodedMsg

"""
This function is used to encrypt the video file with the message.
"""
def encodeVideo(videoFile, msg):
    # This function is called to extract the frames from the video file.
    extractFrames(videoFile)
    # This function is called to get the list of frames if any frame is encrypted beforehand.
    frameList = getExistingEncryptedFrame()
    # Checking if any encrypted frames are found or not.
    if (len(frameList)):
        # This function is called to hide the message in the existed frames.
        hideExistingMsg(frameList)

    # It extracts the audio file from the video and then embed the encrypted message
    # into the frames and then all the frames are combined into the video and then
    # the audio file is added to the video file.
    call(["ffmpeg", "-i", videoFile, "-q:a", "0", "-map", "a", "temp/audio.mp3", "-y"], stdout=open(os.devnull, "w"),
            stderr=STDOUT)
    embedMessageInFrames(msg)
    call(["ffmpeg", "-i", "temp/%d.png", "-vcodec", "png", "temp/Embedded_Video.mp4", "-y"],
            stdout=open(os.devnull, "w"), stderr=STDOUT)
    call(["ffmpeg", "-i", "temp/Embedded_Video.mp4", "-i", "temp/audio.mp3", "-codec", "copy", "Embedded_Video.mp4",
            "-y"], stdout=open(os.devnull, "w"), stderr=STDOUT)
    os.remove(videoFile)
    os.rename("Embedded_Video.mp4", videoFile)
    cleanTempFolder()