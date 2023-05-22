import wave
import os

# Define allowed audio files.
allowedExtentions = {'wav'}

"""
This function is used to check for the file extension and if the extension is 
allowed to be used then the function proceed further.
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

    # Getting the frames of the audio file and converted into a list of integers 
    # and then into a bytearray.
    nFrames = audio.getnframes()
    frames = audio.readframes(nFrames)
    frameList = list(frames)
    frameBytes = bytearray(frameList)
    
    # Converting data into binary representation using the UTF-8 encoding.
    res = ''.join(format(i, '08b') for i in bytearray(data, encoding ='utf-8'))

    data = data + '*^*^*'

    result = []
    # Each character of the data is converted into its binary representation and 
    # the individual bits are added to the result list.
    for ch in data:
        bits = bin(ord(ch))[2:].zfill(8)
        result.extend([int(b) for b in bits])

    j = 0 
    # This loop iterates over each bit in result and modifies the corresponding 
    # bits in the audio file frames. If the bit in res matches the least significant 
    # bit (LSB) of the frame byte, the LSB remains unchanged. Otherwise, the LSB 
    # is flipped to match the bit in result.
    for i in range(0, len(result), 1): 
        res = bin(frameBytes[j])[2:].zfill(8)
        if res[len(res)-4] == result[i]:
            frameBytes[j] = (frameBytes[j] & 253)      #253: 11111101
        else:
            frameBytes[j] = (frameBytes[j] & 253) | 2
            frameBytes[j] = (frameBytes[j] & 254) | result[i]
        j = j + 1
    
    # The modified frame bytes are converted back to bytes.
    frameModified = bytes(frameBytes)

    # A new wave file is created with the same parameters as the original audio file. 
    # The modified frame bytes are written to the stego file.
    with wave.open(stegoFile, 'wb') as fd:
        fd.setparams(audio.getparams())
        fd.writeframes(frameModified)  
    audio.close()
    # os.remove(audioFile)

"""
This function is used to get the encoded audio file and extract the encrypted 
message and show it to the user.
"""
def decodeAudioData(audioFile):
    try:
        audio = wave.open(audioFile, mode='rb')

        # Getting the frames of the audio file and converted into a list of integers 
        # and then into a bytearray.
        nFrames = audio.getnframes()
        frames = audio.readframes(nFrames)
        frameList = list(frames)
        frameBytes = bytearray(frameList)

        extracted = ""
        p = 0

        # Divides the extracted string into group of 8 characters.
        allBytes = [extracted[i: i + 8] for i in range(0, len(extracted), 8)]
        decodedMsg = ""
        # Decodes each byte from binary to its corresponding character.
        for byte in allBytes:
            decodedMsg += chr(int(byte, 2))
            if decodedMsg[-5:] == "*^*^*":
                return True, decodedMsg[:-5]    

        # It extracts the least significant bit (LSB) from each byte and appends 
        # it to the extracted string. After each bit extraction, it reconstructs 
        # the bytes by grouping every 8 bits, forming a list called allBytes.
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

            # Iterates over each byte then converts it from binary to an integer 
            # and then converts the integer to its corresponding character.
            for byte in allBytes:
                decodedMsg += chr(int(byte, 2))
                if decodedMsg[-5:] == "*^*^*":
                    p = 1
                    os.remove(audioFile)
                    return True, decodedMsg[:-5]

        return False, None

    except wave.Error:
        return False, None