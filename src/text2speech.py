# python 3

# https://stackoverflow.com/questions/48438686/realistic-text-to-speech-with-python-that-doesnt-require-internet
# sudo apt-get update && sudo apt-get install espeak
# pip install pyttsx3

# offline text to speech
import pyttsx3

#####################################################################################################################


def text_to_speech(user_text):
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

