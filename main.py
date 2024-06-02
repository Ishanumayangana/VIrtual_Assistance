import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

# Initialize recognizer and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Listen for a command from the microphone and return it as text"""
    command = ""
    try:
        with sr.Microphone() as source:
            print('listening...')
            listener.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'ali' in command:
                command = command.replace('ali', '')
                print(command)
    except Exception as e:
        print(f"Error: {e}")
    return command

def run_alexa():
    """Process the command and perform the requested action"""
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '').strip()
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'who the heck is' in command:
        person = command.replace('who the heck is', '').strip()
        try:
            info = wikipedia.summary(person, sentences=1)
            print(info)
            talk(info)
        except wikipedia.exceptions.DisambiguationError as e:
            talk(f"There are multiple entries for {person}, please be more specific.")
            print(f"DisambiguationError: {e.options}")
        except wikipedia.exceptions.PageError:
            talk(f"I couldn't find any information on {person}.")
            print("PageError: No page found for the query.")
        except Exception as e:
            talk(f"An error occurred while retrieving information.")
            print(f"Unexpected error: {e}")
    elif 'date' in command:
        talk('sorry, I have a headache')
    elif 'are you single' in command:
        talk('I am in a relationship with wifi')
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    else:
        talk('Please say the command again.')

try:
    while True:
        run_alexa()
except KeyboardInterrupt:
    print("Program terminated by user")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    print("Cleaning up resources...")
    engine.stop()
