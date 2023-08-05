import cv2
from playsound import playsound
from pybot import PyBot
from pygame import mixer
import time
def main():
    #os.chdir(os.path.dirname(os.path.abspath(__file__)))
    window_name = 'Leaf Blower Revolution'
    #window_name = 'areasxx.jpg - Paint'
    # initialize bot
    #bot = bothandler.BotHandler(window_name)
    debug = 'debug'
    print("""Hold shift + ESC to stop
Hold shift + P to pause/unpause.
Hold shift + F to show FPS
Program is running.
    """)


    # Input an existing wav filename

    bot = PyBot(window_name, debug)
    bot.resize(640,380)
    bot.run()
    print('Program is closed.')
    i = input("Press any key to end program.\n")


# Driver code
if __name__ == '__main__':
    main()