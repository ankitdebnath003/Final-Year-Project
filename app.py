from flask import Flask, render_template, request, session
from audio import *
from image import *
import os
from werkzeug.utils import secure_filename

# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name for template path
# The default folder name for static files should be "static" else need to mention custom folder for static path
app = Flask(__name__, template_folder = 'template', static_folder = '/')

# Defining upload folder path.
uploadFolder = "upload/"

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

                    filename = "encodedaudio.wav"
                    return render_template('audio/index.html', filename = filename, encoded = "")
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
This Route is used to redirect the user to the image page according to the user's
choice to either encrypt or decrypt the image file and according to that the respective
options are available. 
"""
@app.route('/image/<select>', methods = ["POST", "GET"])
@app.route('/image', defaults = {'select': 'default'}, methods = ["POST", "GET"])
def uploadImageFile(select):
    decodedMsg = None

    # When the user selects to encrypt the audio file then the respective options
    # will be shown on the html page.
    if select == "encrypt":
        return render_template('image/index.html', value = "encode")
        
    # When the user selects to decrypt the audio file then the respective options
    # will be shown on the html page.
    elif select == "decrypt":
        return render_template('image/index.html', value = "decode")

    # When the user submit the encode or decode button then this will be worked.
    if (request.method == 'POST'):

        # If the user wants to encode the audio file with text message then this
        # condition will be satisfied. In this if block the data are taken from 
        # the form and embedded the text message in the audio file and show the 
        # user to download the encrypted audio file.
        if request.form['action'] == 'Encode':
            # Taking input of the message and audio file.
            msg = request.form['inputText']
            image = request.files['uploadedImage']

            if image and isAllowedImageFile(image.filename):
                imageFileName = secure_filename(image.filename)
                imageFilePath = os.path.join(app.config['UploadFolder'], imageFileName)
                image.save(imageFilePath)

                # if isValidWavFile(imageFilePath):
                outputName = "encodedimage.bmp"

                # Calling the function to encrypt the text message in the audio file.
                encodeImageData(imageFilePath, msg, outputName)

                fileName = "encodedimage.bmp"
                return render_template('image/index.html', filename = fileName, encoded = "")
            return "Invalid file format. Please upload a BMP Image file."

        # If the user wants to decode the audio file then this condition will be 
        # satisfied. In this if block the text will be fetched from the encoded 
        # audio file and show the encoded message to the user.
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

if __name__ == '__main__':
    app.run(debug = True)