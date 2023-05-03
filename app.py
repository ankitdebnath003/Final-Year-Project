from flask import Flask, render_template, request, session
from audio import *
from image import *
from video import *
import os
from werkzeug.utils import secure_filename

# Provide template folder name.
# The default folder name should be "templates" else need to mention custom 
# folder name for template path.
# The default folder name for static files should be "static" else need to 
# mention custom folder for static path.
app = Flask(__name__, template_folder = 'template', static_folder = '/')

# Defining upload folder path.
uploadFolder = ""

# Configure upload folder for Flask application
app.config['UploadFolder'] = uploadFolder

# Define secret key to enable session
app.secret_key = 'This is your secret key to utilize session in Flask'

"""
This route is used to show the index page of the project.
"""
@app.route('/')
def home():
    return render_template('home/index.html')

@app.route('/updateFile', methods=['GET'])
def updateFile():
    fileName = request.args.get('file')
    # Remove the file
    try:
        os.remove(fileName)
        return 'File removed successfully'
    except OSError as e:
        return f'Error removing the file: {str(e)}'

"""
This Route is used to redirect the user to the image page according to the user's
choice to either encrypt or decrypt the image file and according to that the respective
options are available. 
"""
@app.route('/image/<select>', methods = ["POST", "GET"])
@app.route('/image', defaults = {'select': 'default'}, methods = ["POST", "GET"])
def uploadImageFile(select):
    decodedMsg = None

    # When the user selects to encrypt the image file then the respective options
    # will be shown on the html page.
    if select == "encrypt":
        return render_template('image/index.html', value = "encode")
        
    # When the user selects to decrypt the image file then the respective options
    # will be shown on the html page.
    elif select == "decrypt":
        return render_template('image/index.html', value = "decode")

    # When the user submit the encode or decode button then this will be worked.
    if (request.method == 'POST'):

        # If the user wants to encode the image file with text message then this
        # condition will be satisfied. In this if block the data are taken from 
        # the form and embedded the text message in the image file and show the 
        # user to download the encrypted image file.
        if request.form['action'] == 'Encode':
            # Taking input of the message and image file.
            msg = request.form['inputText']
            image = request.files['uploadedImage']

            if image and isAllowedImageFile(image.filename):
                imageFileName = secure_filename(image.filename)
                imageFilePath = os.path.join(app.config['UploadFolder'], imageFileName)
                image.save(imageFilePath)

                outputName = "encodedimage.bmp"
                # Calling the function to encrypt the text message in the image file.
                encodeImageData(imageFilePath, msg, outputName)

                return render_template('image/index.html', filename = outputName, encoded = "")
            return "Invalid file format. Please upload a BMP Image file."

        # If the user wants to decode the image file then this condition will be 
        # satisfied. In this if block the text will be fetched from the encoded 
        # image file and show the encoded message to the user.
        elif request.form['action'] == 'Decode':
            image = request.files['uploadedImage']

            if image and isAllowedImageFile(image.filename):
                imageFileName = secure_filename(image.filename)
                imageFilePath = os.path.join(app.config['UploadFolder'], imageFileName)
                image.save(imageFilePath)

                # Calling the function to decrypt the audio file and get the 
                # decrypted message.
                decodedMsg = decodeImageData(imageFilePath)
                if decodedMsg != 'Ø':
                    return render_template('image/index.html', decodedMsg = decodedMsg, decoded = "")
                return render_template('image/index.html', decodedMsg = "No message is there. Please select a encrypted file.", decoded = "")
            return "Please Provide Only .bmp File"
    return render_template('image/index.html')

"""
This Route is used to redirect the user to the audio page according to the user's
choice to either encrypt or decrypt the audio file and according to that the respective
options are available. 
"""
@app.route('/audio/<select>', methods = ["POST", "GET"])
@app.route('/audio', defaults = {'select': 'default'}, methods = ["POST", "GET"])
def uploadAudioFile(select):
    decodedMsg = None

    # When the user selects to encrypt the audio file then the respective options
    # will be shown on the html page.
    if select == "encrypt":
        return render_template('audio/index.html', value = "encode")
        
    # When the user selects to decrypt the audio file then the respective options
    # will be shown on the html page.
    elif select == "decrypt":
        return render_template('audio/index.html', value = "decode")

    # When the user submit the encode or decode button then this will be worked.
    if (request.method == 'POST'):

        # If the user wants to encode the audio file with text message then this
        # condition will be satisfied. In this if block the data are taken from 
        # the form and embedded the text message in the audio file and show the 
        # user to download the encrypted audio file.
        if request.form['action'] == 'Encode':
            # Taking input of the message and audio file.
            msg = request.form['inputText']
            audio = request.files['uploadedAudio']

            if audio and isAllowedAudioFile(audio.filename):
                audioFileName = secure_filename(audio.filename)
                audioFilePath = os.path.join(app.config['UploadFolder'], audioFileName)
                audio.save(audioFilePath)

                if isValidWavFile(audioFilePath):
                    outputName = "encodedaudio.wav"

                    # Calling the function to encrypt the text message in the audio file.
                    encodeAudioData(audioFilePath, msg, outputName)

                    return render_template('audio/index.html', filename = outputName, encoded = "")
                return "Invalid WAV file. Please upload a valid WAV file."
            return "Invalid file format. Please upload a WAV file."

        # If the user wants to decode the audio file then this condition will be 
        # satisfied. In this if block the text will be fetched from the encoded 
        # audio file and show the encoded message to the user.
        elif request.form['action'] == 'Decode':
            audio = request.files['uploadedAudio']

            if audio and isAllowedAudioFile(audio.filename):
                audioFileName = secure_filename(audio.filename)
                audioFilePath = os.path.join(app.config['UploadFolder'], audioFileName)
                audio.save(audioFilePath)

                if isValidWavFile(audioFilePath):

                    # Calling the function to decrypt the audio file and get the 
                    # decrypted message.
                    flag, decodedMsg = decodeAudioData(audioFilePath)
                    if flag:
                        return render_template('audio/index.html', decodedMsg = decodedMsg, decoded = "")
                    return render_template('audio/index.html', decodedMsg = "No decoded value found in the WAV file.")
                return "Invalid WAV"
    return render_template('audio/index.html')


"""
This Route is used to redirect the user to the video page according to the user's
choice to either encrypt or decrypt the video file and according to that the respective
options are available. 
"""
@app.route('/video/<select>', methods = ["POST", "GET"])
@app.route('/video', defaults = {'select': 'default'}, methods = ["POST", "GET"])
def uploadVideoFile(select):
    decodedMsg = None

    # When the user selects to encrypt the video file then the respective options
    # will be shown on the html page.
    if select == "encrypt":
        return render_template('video/index.html', value = "encode")
        
    # When the user selects to decrypt the video file then the respective options
    # will be shown on the html page.
    elif select == "decrypt":
        return render_template('video/index.html', value = "decode")

    # When the user submit the encode or decode button then this will be worked.
    if (request.method == 'POST'):

        # If the user wants to encode the video file with text message then this
        # condition will be satisfied. In this if block the data are taken from 
        # the form and embedded the text message in the video file and show the 
        # user to download the encrypted video file.
        if request.form['action'] == 'Encode':
            # Taking input of the message and video file.
            msg = request.form['inputText']
            video = request.files['uploadedVideo']
            if video and isAllowedVideoFile(video.filename):
                videoFileName = secure_filename(video.filename)
                videoFilePath = os.path.join(app.config['UploadFolder'], videoFileName)
                video.save(videoFilePath)

                # Calling the function to encode the video file with the message.
                encodeVideo(videoFilePath, msg)
                return render_template('video/index.html', filename = videoFilePath, encoded = "")
            return "Invalid file format. Please upload a valid video file."

        # If the user wants to decode the video file then this condition will be 
        # satisfied. In this if block the text will be fetched from the encoded 
        # video file and show the encoded message to the user.
        elif request.form['action'] == 'Decode':
            video = request.files['uploadedVideo']

            if video and isAllowedVideoFile(video.filename):
                videoFileName = secure_filename(video.filename)
                videoFilePath = os.path.join(app.config['UploadFolder'], videoFileName)
                video.save(videoFilePath)

                # Calling the function to decrypt the video file and get the 
                # decrypted message.
                decodedMsg = decodeVideo(videoFilePath)
                return render_template('video/index.html', decodedMsg = decodedMsg, decoded = "")
            return render_template('video/index.html', decodedMsg = "Video File is not supported. Please provide another video.", decoded = "")
    return render_template('video/index.html')

"""
This Route is used to redirect the user to the image and audio page according 
to the user's choice to either encrypt or decrypt the image and video file 
and according to that the respective options are available. 
"""
@app.route('/imageAndAudio/<select>', methods = ["POST", "GET"])
@app.route('/imageAndAudio', defaults = {'select': 'default'}, methods = ["POST", "GET"])
def uploadImageAndAudioFile(select):
    decodedMsg = None

    # When the user selects to encrypt the image and audio file then the 
    # respective options will be shown on the html page.
    if select == "encrypt":
        return render_template('imageAndAudio/index.html', value = "encode")
        
    # When the user selects to decrypt the image and audio file then the 
    # respective options will be shown on the html page.
    elif select == "decrypt":
        return render_template('imageAndAudio/index.html', value = "decode")

    # When the user submit the encode or decode button then this will be worked.
    if (request.method == 'POST'):

        # If the user wants to encode the image and audio file with text message 
        # then this condition will be satisfied. In this if block the data are 
        # taken from the form and embedded the text message in the image and audio 
        # file and show the user to download the encrypted image and audio file.
        if request.form['action'] == 'Encode':
            # Taking input of the message and image file.
            imageMsg = request.form['inputTextImage']
            image = request.files['uploadedImage']
            # Taking input of the message and audio file.
            audioMsg = request.form['inputTextAudio']
            audio = request.files['uploadedAudio']
            if audio and image and isAllowedAudioFile(audio.filename) and isAllowedImageFile(image.filename):
                # Getting the image file name and save it to the local to access it.
                imageFileName = secure_filename(image.filename)
                imageFilePath = os.path.join(app.config['UploadFolder'], imageFileName)
                image.save(imageFilePath)

                # Getting the audio file name and save it to the local to access it.
                audioFileName = secure_filename(audio.filename)
                audioFilePath = os.path.join(app.config['UploadFolder'], audioFileName)
                audio.save(audioFilePath)

                # Calling the function to encrypt the text message in the image file.
                imageOutputName = "encodedimage.bmp"
                encodeImageData(imageFilePath, imageMsg, imageOutputName)

                # Calling the function to encrypt the text message in the audio file.
                audioOutputName = "encodedaudio.wav"
                encodeAudioData(audioFilePath, audioMsg, audioOutputName)
                return render_template('imageAndAudio/index.html', imagefilename = imageOutputName, audiofilename = audioOutputName, encoded = "")
            return "Invalid file format. Please upload a valid file."

        # If the user wants to decode the image and audio file then this condition 
        # will be satisfied. In this if block the text will be fetched from the 
        # encoded image and audio file and show the encoded message to the user.
        elif request.form['action'] == 'Decode':
            # Taking input of the image and audio file.
            image = request.files['uploadedImage']
            audio = request.files['uploadedAudio']

            if audio and image and isAllowedAudioFile(audio.filename) and isAllowedImageFile(image.filename):
                # Getting the image file name and save it to the local to access it.
                imageFileName = secure_filename(image.filename)
                imageFilePath = os.path.join(app.config['UploadFolder'], imageFileName)
                image.save(imageFilePath)

                # Getting the audio file name and save it to the local to access it.
                audioFileName = secure_filename(audio.filename)
                audioFilePath = os.path.join(app.config['UploadFolder'], audioFileName)
                audio.save(audioFilePath)

                # Calling the function to decrypt the image file and get the decrypted message.
                imageDecodedMsg = decodeImageData(imageFilePath)

                # Calling the function to decrypt the audio file and get the decrypted message.
                flag, audioDecodedMsg = decodeAudioData(audioFilePath)
                return render_template('imageAndAudio/index.html', decodedMsg = imageDecodedMsg + ' ' + audioDecodedMsg, decoded = "")
            return render_template('imageAndAudio/index.html', decodedMsg = "Video File is not supported. Please provide another video.", decoded = "")
    return render_template('imageAndAudio/index.html')

"""
This Route is used to redirect the user to the image and video page according 
to the user's choice to either encrypt or decrypt the image and video file 
and according to that the respective options are available. 
"""
@app.route('/imageAndVideo/<select>', methods = ["POST", "GET"])
@app.route('/imageAndVideo', defaults = {'select': 'default'}, methods = ["POST", "GET"])
def uploadImageAndVideoFile(select):
    decodedMsg = None

    # When the user selects to encrypt the image and video file then the 
    # respective options will be shown on the html page.
    if select == "encrypt":
        return render_template('imageAndVideo/index.html', value = "encode")
        
    # When the user selects to decrypt the image and video file then the 
    # respective options will be shown on the html page.
    elif select == "decrypt":
        return render_template('imageAndVideo/index.html', value = "decode")

    # When the user submit the encode or decode button then this will be worked.
    if (request.method == 'POST'):

        # If the user wants to encode the image and video file with text message 
        # then this condition will be satisfied. In this if block the data are 
        # taken from the form and embedded the text message in the image and video 
        # file and show the user to download the encrypted image and video file.
        if request.form['action'] == 'Encode':
            # Taking input of the message and image file.
            imageMsg = request.form['inputTextImage']
            image = request.files['uploadedImage']
            # Taking input of the message and video file.
            videoMsg = request.form['inputTextVideo']
            video = request.files['uploadedVideo']
            if video and image and isAllowedVideoFile(video.filename) and isAllowedImageFile(image.filename):
                # Getting the image file name and save it to the local to access it.
                imageFileName = secure_filename(image.filename)
                imageFilePath = os.path.join(app.config['UploadFolder'], imageFileName)
                image.save(imageFilePath)

                # Getting the video file name and save it to the local to access it.
                videoFileName = secure_filename(video.filename)
                videoFilePath = os.path.join(app.config['UploadFolder'], videoFileName)
                video.save(videoFilePath)

                # Calling the function to encrypt the text message in the image file.
                imageOutputName = "encodedimage.bmp"
                encodeImageData(imageFilePath, imageMsg, imageOutputName)

                # Calling the function to encrypt the text message in the video file.
                encodeVideo(videoFilePath, videoMsg)
                return render_template('imageAndVideo/index.html', imagefilename = imageOutputName, videofilename = videoFilePath, encoded = "")
            return "Invalid file format. Please upload a valid file."

        # If the user wants to decode the image and video file then this condition 
        # will be satisfied. In this if block the text will be fetched from the 
        # encoded image and video file and show the encoded message to the user.
        elif request.form['action'] == 'Decode':
            # Taking input of image and video file.
            image = request.files['uploadedImage']
            video = request.files['uploadedVideo']

            if video and image and isAllowedVideoFile(video.filename) and isAllowedImageFile(image.filename):
                # Getting the image file name and save it to the local to access it.
                imageFileName = secure_filename(image.filename)
                imageFilePath = os.path.join(app.config['UploadFolder'], imageFileName)
                image.save(imageFilePath)

                # Getting the video file name and save it to the local to access it.
                videoFileName = secure_filename(video.filename)
                videoFilePath = os.path.join(app.config['UploadFolder'], videoFileName)
                video.save(videoFilePath)

                # Calling the function to decrypt the image file and get the message.
                imageDecodedMsg = decodeImageData(imageFilePath)
                # Calling the function to decrypt the video file and get the message.
                videoDecodedMsg = decodeVideo(videoFilePath)
                return render_template('imageAndVideo/index.html', decodedMsg = imageDecodedMsg + ' ' + videoDecodedMsg, decoded = "")
            return render_template('imageAndVideo/index.html', decodedMsg = "Video File is not supported. Please provide another video.", decoded = "")
    return render_template('imageAndVideo/index.html')

"""
This Route is used to redirect the user to the audio and video page according 
to the user's choice to either encrypt or decrypt the audio and video file and 
according to that the respective options are available. 
"""
@app.route('/audioAndVideo/<select>', methods = ["POST", "GET"])
@app.route('/audioAndVideo', defaults = {'select': 'default'}, methods = ["POST", "GET"])
def uploadAudioAndVideoFile(select):
    decodedMsg = None

    # When the user selects to encrypt the audio and video file then the 
    # respective options will be shown on the html page.
    if select == "encrypt":
        return render_template('audioAndVideo/index.html', value = "encode")
        
    # When the user selects to decrypt the audio and video file then the 
    # respective options will be shown on the html page.
    elif select == "decrypt":
        return render_template('audioAndVideo/index.html', value = "decode")

    # When the user submit the encode or decode button then this will be worked.
    if (request.method == 'POST'):

        # If the user wants to encode the audio and video file with text message 
        # then this condition will be satisfied. In this if block the data are 
        # taken from the form and embedded the text message in the audio and video 
        # file and show the user to download the encrypted audio and video file.
        if request.form['action'] == 'Encode':
            # Taking input of the message and audio file.
            audioMsg = request.form['inputTextAudio']
            audio = request.files['uploadedAudio']
            # Taking input of the message and video file.
            videoMsg = request.form['inputTextVideo']
            video = request.files['uploadedVideo']
            if video and audio and isAllowedVideoFile(video.filename) and isAllowedAudioFile(audio.filename):
                # Getting the audio file name and save it to the local to access it.
                audioFileName = secure_filename(audio.filename)
                audioFilePath = os.path.join(app.config['UploadFolder'], audioFileName)
                audio.save(audioFilePath)

                # Getting the video file name and save it to the local to access it.
                videoFileName = secure_filename(video.filename)
                videoFilePath = os.path.join(app.config['UploadFolder'], videoFileName)
                video.save(videoFilePath)

                # Calling the function to encrypt the text message in the audio file.
                audioOutputName = "encodedaudio.wav"
                encodeAudioData(audioFilePath, audioMsg, audioOutputName)

                # Calling the function to encrypt the text message in the video file.
                encodeVideo(videoFilePath, videoMsg)
                return render_template('audioAndVideo/index.html', audiofilename = audioOutputName, videofilename = videoFilePath, encoded = "")
            return "Invalid file format. Please upload a valid file."

        # If the user wants to decode the audio and video file then this condition 
        # will be satisfied. In this if block the text will be fetched from the 
        # encoded audio and video file and show the encoded message to the user.
        elif request.form['action'] == 'Decode':
            # Taking input of the audio and video file.
            audio = request.files['uploadedAudio']
            video = request.files['uploadedVideo']

            if video and audio and isAllowedVideoFile(video.filename) and isAllowedAudioFile(audio.filename):
                # Getting the audio file name and save it to the local to access it.
                audioFileName = secure_filename(audio.filename)
                audioFilePath = os.path.join(app.config['UploadFolder'], audioFileName)
                audio.save(audioFilePath)

                # Getting the video file name and save it to the local to access it.
                videoFileName = secure_filename(video.filename)
                videoFilePath = os.path.join(app.config['UploadFolder'], videoFileName)
                video.save(videoFilePath)

                # Calling the function to decrypt the audio file and get the message.
                flag, audioDecodedMsg = decodeAudioData(audioFilePath)
                # Calling the function to decrypt the video file and get the message.
                videoDecodedMsg = decodeVideo(videoFilePath)
                return render_template('audioAndVideo/index.html', decodedMsg = audioDecodedMsg + ' ' + videoDecodedMsg, decoded = "")
            return render_template('audioAndVideo/index.html', decodedMsg = "Video File is not supported. Please provide another video.", decoded = "")
    return render_template('audioAndVideo/index.html')

if __name__ == '__main__':
    app.run(debug = True)