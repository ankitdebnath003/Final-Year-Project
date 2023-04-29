import wave

# Define allowed files.
allowedExtentions = {'wav'}

"""
This function is used to check for the file extension and if the extension is allowed to be
used then the function proceed further.
"""
def isAllowedAudioFile(fileName):
    return '.' in fileName and fileName.rsplit('.', 1)[1].lower() in allowedExtentions

"""
This function is used to check for the valid .wav file extension.
"""
def isValidWavFile(filePath):
    try:
        with wave.open(filePath, 'rb') as wavFile:
            if wavFile.getnchannels() != 2 or wavFile.getsampwidth() != 2 or wavFile.getcomptype() != 'NONE':
                return False
            return True
    except wave.Error:
        return False

"""
This function is used to encrypt the text message in the audio file and save it 
locally to make it available for download.
"""
def encodeAudioData(audioFile, data, stegoFile):
    audio = wave.open(audioFile, mode='rb')

    nFrames = audio.getnframes()
    frames = audio.readframes(nFrames)
    frameList = list(frames)
    frameBytes = bytearray(frameList)
    
    res = ''.join(format(i, '08b') for i in bytearray(data, encoding ='utf-8'))     
    print("\nThe string after binary conversion :- " + (res))   
    length = len(res)
    print("\nLength of binary after conversion :- ",length)

    data = data + '*^*^*'

    result = []
    for c in data:
        bits = bin(ord(c))[2:].zfill(8)
        result.extend([int(b) for b in bits])

    j = 0 
    for i in range(0, len(result), 1): 
        res = bin(frameBytes[j])[2:].zfill(8)
        if res[len(res)-4] == result[i]:
            frameBytes[j] = (frameBytes[j] & 253)      #253: 11111101
        else:
            frameBytes[j] = (frameBytes[j] & 253) | 2
            frameBytes[j] = (frameBytes[j] & 254) | result[i]
        j = j + 1
    
    frameModified = bytes(frameBytes)

    with wave.open(stegoFile, 'wb') as fd:
        fd.setparams(audio.getparams())
        fd.writeframes(frameModified)
    print("\nEncoded the data successfully in the audio file.")    
    audio.close()

"""
This function is used to get the encoded audio file and extract the encrypted 
message and show it to the user.
"""
def decodeAudioData(audioFile):
    try:
        audio = wave.open(audioFile, mode='rb')

        nFrames = audio.getnframes()
        frames = audio.readframes(nFrames)
        frameList = list(frames)
        frameBytes = bytearray(frameList)

        extracted = ""
        p = 0

        allBytes = [extracted[i: i + 8] for i in range(0, len(extracted), 8)]
        decodedMsg = ""
        for byte in allBytes:
            decodedMsg += chr(int(byte, 2))
            if decodedMsg[-5:] == "*^*^*":
                print("The Encoded data was: ", decodedMsg[:-5])
                return True, decodedMsg[:-5]

        for i in range(len(frameBytes)):
            if p == 1:
                break
            res = bin(frameBytes[i])[2:].zfill(8)
            if res[len(res) - 2] == '0':
                extracted += res[len(res) - 4]
            else:
                extracted += res[len(res) - 1]

            allBytes = [extracted[i: i + 8] for i in range(0, len(extracted), 8)]
            decodedMsg = ""
            for byte in allBytes:
                decodedMsg += chr(int(byte, 2))
                if decodedMsg[-5:] == "*^*^*":
                    print("The Encoded data was: ", decodedMsg[:-5])
                    p = 1
                    return True, decodedMsg[:-5]

        return False, None

    except wave.Error:
        return False, None