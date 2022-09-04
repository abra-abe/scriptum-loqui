# project: reading assistance for the visually impaired
# This mini project is a proof of concept, the actual project might be possible
# to perform using a device such as a RaspberryPi, or creating a mobile phone application
import cv2
import pytesseract
from gtts import gTTS
from playsound import playsound
from googletrans import Translator

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def imagedetection():
    # ________________For Image Detection______________________
    img = cv2.imread("img2.png")

    # detecting the text from the image
    print(pytesseract.image_to_string(img))

    hImg, wImg, _ = img.shape

    # converting the image into readable data
    data = pytesseract.image_to_data(img)

    # opening the file in writing mode to write the detected text into a text file/document
    file1 = open("stringFromImg.txt", "w")

    for z, a in enumerate(data.splitlines()):
        if z != 0:
            a = a.split()
            if len(a) == 12:
                x, y = int(a[6]), int(a[7])
                h, w = int(a[8]), int(a[9])

                # displaying rectangles around each detected word
                cv2.rectangle(img, (x, y), (x + h, y + w), (0, 255, 0), 1)

                # displaying the detected text on top of the word on the image
                cv2.putText(img, a[11], (x - 15, y), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 1)
                file1.write(a[11] + " ")
    file1.close()

    # open the file in reading mode, to convert the text into speech
    file1read = open("stringFromImg.txt", "r")

    line = file1read.read()
    if line != " ":
        file1read.close()
        speech = gTTS(text=line, lang="en", slow=False, tld="com")
        speech.save("test01.mp3")

    # for displaying the image with the surrounding boxes
    cv2.imshow('image', img)

    cv2.waitKey(0)

    # for playing the sound after the image window is closed
    playsound("test01.mp3")


def videodetection():
    # _________________For Live Video Feed______________________
    video = cv2.VideoCapture("https://192.168.43.1:8080/video")

    #for the video width and height
    video.set(3, 640)
    video.set(4, 480)


    file2 = open("StringFromVid.txt", "w")

# NOTE:: The code below will record a continuous/live feed video, the video will only stop when the user presses the 'x'
# button to cancel the video feed. But this will lead to the same text to be detected and recorded in the text document
# multiple times, thus the audio will only be the same words being repeated over and over again.
# In order to solve this, I have decided to incorporate a timeout, thus after 2500 millliseconds (2.5 seconds),
# the video feed will be terminated, and the detected text will be recorded in the text document
# ready to be converted into audio format.

    # while True:
    #     extra, frames = video.read()
    #     data3 = pytesseract.image_to_data(frames)
    #     for z, a in enumerate(data3.splitlines()):
    #         if z != 0:
    #             a = a.split()
    #             if len(a) == 12:
    #                 x, y = int(a[6]), int(a[7])
    #                 w, h = int(a[8]), int(a[9])
    #
    #                 # This below will display bounding boxes for each word that is detected in the video feed
    #                 cv2.rectangle(frames, (x, y), (x + w, y + h), (0, 255, 0), 1)
    #
    #                 # The code below will be used to display the text that has been detected
    #                 # on top of the image
    #
    #                 cv2.putText(frames, a[11], (x, y + 25), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)
    #                 file2.write(a[11] + " ")
    #
    #     cv2.imshow('Video capture', frames)
    #     # in order to break out of the while loop, we can use the following
    #     # the code below means that if the waitKey is more than 1 and the user presses the q key
    #     # the video window will close
    #     if cv2.waitKey(1) & 0xFF == ord('x'):
    #         video.release()
    #         cv2.destroyAllWindows()
    #         break

# NOTE:: The code below is the fix for the above code, which incorporates the use of a timeout

    while True:
        extra, frames = video.read()
        data3 = pytesseract.image_to_data(frames)
        for z, a in enumerate(data3.splitlines()):
            if z != 0:
                a = a.split()
                if len(a) == 12:
                    x, y = int(a[6]), int(a[7])
                    w, h = int(a[8]), int(a[9])

                    # This below will display bounding boxes for each word that is detected in the video feed
                    cv2.rectangle(frames, (x, y), (x + w, y + h), (0, 255, 0), 1)

                    # The code below will be used to display the text that has been detected
                    # on top of the image

                    cv2.putText(frames, a[11], (x, y + 25), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)
                    file2.write(a[11] + " ")

        cv2.imshow('Video capture', frames)
        # in order to break out of the while loop, we can use the following
        # the code below means that if the waitKey is more than 1 and the user presses the q key
        # the video window will close
        if cv2.waitKey(2500):
            video.release()
            cv2.destroyAllWindows()
            break

    file2.close()

    file2read = open("StringFromVid.txt", "r")

    line = file2read.read()

    if line != " ":
        file2read.close()
        speech = gTTS(text=line, lang='en', slow=False, tld="com")
        speech.save("test02.mp3")


    playsound("test02.mp3")


def texttranslation():
    # _____________________For Translating detected text from a video____________
    video = cv2.VideoCapture("https://192.168.43.1:8080/video")

    # for the video width and height
    video.set(3, 640)
    video.set(4, 480)

    fileTranslate = open("StringFromVid.txt", "w")


    while True:
        extra, frames = video.read()
        data3 = pytesseract.image_to_data(frames)
        for z, a in enumerate(data3.splitlines()):
            if z != 0:
                a = a.split()
                if len(a) == 12:
                    x, y = int(a[6]), int(a[7])
                    w, h = int(a[8]), int(a[9])

                    # This below will display bounding boxes for each word that is detected in the video feed
                    cv2.rectangle(frames, (x, y), (x + w, y + h), (0, 255, 0), 1)

                    # The code below will be used to display the text that has been detected
                    # on top of the image

                    cv2.putText(frames, a[11], (x, y + 25), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)
                    fileTranslate.write(a[11] + " ")

        cv2.imshow('Video capture', frames)
        # in order to break out of the while loop, we can use the following
        # the code below means that if the waitKey is more than 1 and the user presses the q key
        # the video window will close
        if cv2.waitKey(2500):
            video.release()
            cv2.destroyAllWindows()
            break

    fileTranslate.close()

    fileTranslate2 = open("StringFromVid.txt", "r")
    contents = fileTranslate2.read()

    translation = Translator()

    output = translation.translate(contents, dest="en")

    fileTranslate3 = open("translatedText.txt", "w")
    fileTranslate3.write(output.text)
    fileTranslate3.close()

    fileReadTranslate = open("translatedText.txt", "r")

    line2 = fileReadTranslate.read()

    if line2 != " ":
        fileReadTranslate.close()
        speech2 = gTTS(text=line2, lang='en', slow=False, tld="com")
        speech2.save("test03.mp3")


    playsound("test03.mp3")

# using else if ladder to select which of the three modes to use
while True:
    line3 = "welcome, which mode do you want to use, mode 1 for testing the program, mode 2 for live text detection or mode 3 for translation"

    question = gTTS(text=line3, lang='en', slow=False, tld="com")
    question.save("question.mp3")

    playsound("question.mp3")

    option = input("Which mode do you want to use? (1, 2 or 3)")
    print("\n")
    if option == '1':
        imagedetection()
    elif option == '2':
        videodetection()
    elif option == '3':
        texttranslation()
    else:
        print("Incorrect Input...")
        break
