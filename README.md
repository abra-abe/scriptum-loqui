# scriptum-loqui
Converts written text from an image or video (live feed) into speech
It makes use of cv2 for image and video processing
Tesseract OCR, for text detection
gTTS for text to speech conversion
Playsound for playing the converted audio
 
It has two modes:
1. Text detection from image
2. Text detection from video feed

For text detection from image, simply the text 
Will be detected from the image, then the text 
Will be stored in a text document which will
Later on be converted into a .mp3 file 

For text detection from video, a live video feed
Will be set up using ip camera app on the phone
and the video will record for 2.5 seconds and 
Then the detected text from the video will be stored
in a text document which will be converted to a
.mp3 file
