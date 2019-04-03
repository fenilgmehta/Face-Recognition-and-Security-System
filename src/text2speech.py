# python 3
# Description: method to do offline text to speech using pyttsx3 library

# https://stackoverflow.com/questions/48438686/realistic-text-to-speech-with-python-that-doesnt-require-internet
# sudo apt-get update && sudo apt-get install espeak
# pip install pyttsx3

# offline text to speech
import pyttsx3

#####################################################################################################################


def text_to_speech(user_text):
    """
    Parameters:
    user_text (str): string message to be converted to audio and output using speakers available
    """

    try:
        engine = pyttsx3.init()
        engine.say(user_text)
        engine.runAndWait()
    except:
        print("ERROR: unknown error in text to speech")


if __name__ == "__main__":
    print(1)
    text_to_speech('Un-authorized person, access denied')
    print(2)
    text_to_speech('Welcome')

