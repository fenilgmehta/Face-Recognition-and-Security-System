# Import the required module for text  
# to speech conversion 
from gtts import gTTS 
  
# This module is imported so that we can  
# play the converted audio 
import os 

def text_to_speech(user_text):
	# str: the text that you want to convert to audio 
		  
	# Language in which you want to convert 
	language = 'en'
	  
	# Passing the text and language to the engine,  
	# here we have marked slow=False. Which tells  
	# the module that the converted audio should  
	# have a high speed 
	myobj = gTTS(text=user_text, lang=language, slow=False) 
	  
	# Saving the converted audio in a mp3 file named 
	# welcome  
	myobj.save(".temp_audio.mp3") 
	  
	# Playing the converted file 
	os.system("mpg321 .temp_audio.mp3")

if __name__ == "__main__":
    print(1)
    text_to_speech('Un-authorized person, access denied')
    print(2)
    text_to_speech('Welcome')

