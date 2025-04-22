# GUI for T2S Converter
# Imports
import os
import sys
import boto3
from tkinter import *
from tkinter import messagebox
from contextlib import closing
from tempfile import gettempdir
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter.filedialog import askopenfile

# Create an instance of tkinter frame or window
root = Tk()

# Path
# Translate asset paths to useable format for PyInstaller


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# Create five frames in the window
Mul_App = Frame(root)
Sentiment_analysis = Frame(root)
Text_to_Speech = Frame(root)
Extract_Text = Frame(root)
Text_Translator = Frame(root)

# set title
root.title("Multi-Tasking Desktop Application")
root.iconbitmap(resource_path('chat1.ico'))                    # set icon
root.geometry("1000x600+100+50")                        # set geometry
# Disable the resizable Property
root.resizable(False, False)
root.configure(bg="#fbfbfb")                            # set bg color

# Start/Main Function


def Multi_tasking_app():
    # Menubar Function

    def backToBack():
        root.title("Multi-Tasking Desktop Application")
        Mul_App.pack(fill='both', expand=1)
        Sentiment_analysis.pack_forget()
        Text_to_Speech.pack_forget()
        Extract_Text.pack_forget()
        Text_Translator.pack_forget()

    def exitWindow():
        root.destroy()

    # Create Menubar
    menubar = Menu(root)
    root.config(menu=menubar)
    user_menu = Menu(menubar, tearoff=0)

    # add menu items to the File menu
    menubar.add_cascade(label='EXIT', command=exitWindow)
    menubar.add_cascade(label='BACK', command=backToBack)

    Mul_App.pack(fill='both', expand=1)
    # root.pack_forget()
    Mul_App.configure(bg="#fbfbfb")                            # set bg color
    # Insert GIF
    file = resource_path('chat3_test.gif')
    info = Image.open(file)
    # n_frames method calculate total no. of frames in the gif
    frameCnt = info.n_frames
    # print(frameCnt)
    # frameCnt = 110
    frames = [PhotoImage(file=resource_path('chat3_test.gif'), format='gif -index %i' % (i))
              for i in range(frameCnt)]

    def update(count):

        frame = frames[count]
        count += 1
        if count == frameCnt:
            count = 0
        label.configure(image=frame)
        Mul_App.after(100, update, count)

    label = Label(Mul_App)
    label.place(height=360, width=500, y=90, x=10)
    Mul_App.after(0, update, 0)


Multi_tasking_app()

# Button
btn_1 = Button(Mul_App, text="Analyze Sentiment", command=lambda: change_ToSentiment(), foreground="#09263a",
               activebackground="#547c84", bg='#71e4c0', cursor="hand2", width=24, height=1, font=("times new roman", 18, "bold"))
btn_1.place(x=540, y=110)
btn_2 = Button(Mul_App, text="Convert Text to Speech", command=lambda: change_ToTextSpeech(), foreground="#09263a",
               activebackground="#547c84", bg='#71e4c0', cursor="hand2", width=24, height=1, font=("times new roman", 18, "bold"))
btn_2.place(x=540, y=210)
btn_3 = Button(Mul_App, text="Text Translator", command=lambda: change_ToText_Translator(), foreground="#09263a",
               activebackground="#547c84", bg='#71e4c0', cursor="hand2", width=24, height=1, font=("times new roman", 18, "bold"))
btn_3.place(x=540, y=310)
btn_4 = Button(Mul_App, text="Extract Text From Image", command=lambda: change_ToExtract_Text(), foreground="#09263a",
               activebackground="#547c84", bg='#71e4c0', cursor="hand2", width=24, height=1, font=("times new roman", 18, "bold"))
btn_4.place(x=540, y=410)


# Analyze Sentiment Button Function
def change_ToSentiment():
    root.title("Analyze Sentiment and KeyPhrase")
    Sentiment_analysis.pack(fill='both', expand=2)
    Mul_App.pack_forget()
    # set bg color
    Sentiment_analysis.configure(bg="#ffffff")

    # Insert GIF
    file = resource_path('Sentiment_test.gif')
    info = Image.open(file)
    # n_frames method calculate total no. of frames in the gif
    frameCnt = info.n_frames
    # frameCnt = 110
    frames = [PhotoImage(file=resource_path('Sentiment_test.gif'), format='gif -index %i' % (i))
              for i in range(frameCnt)]

    def update(count):

        frame = frames[count]
        count += 1
        if count == frameCnt:
            count = 0
        label.configure(image=frame)
        Sentiment_analysis.after(100, update, count)

    label = Label(Sentiment_analysis)
    label.place(height=200, width=400, x=80, y=220)
    Sentiment_analysis.after(0, update, 0)

    # Text Lable
    label_0 = Label(Sentiment_analysis, text="Enter Text To Analyze", font=(
        "times new roman", 45, "bold"), fg="#cc5454", bg="#ffffff")
    label_0.place(x=360, y=40)

    # TextBox
    textExample = Text(Sentiment_analysis, font=(
        "times new roman", 15), bg="lightgray")
    textExample.place(x=569, y=180, width=370, height=245)

    # TextBox/Button Function
    # Now Send result to comprehend

    def btn1_sentiment():
        aws_mng_con = boto3.session.Session(
            profile_name='demo1')                       # Create session
        client = aws_mng_con.client(
            service_name='comprehend', region_name='us-east-1')      # Create client
        result = textExample.get("1.0", "end")  # Get text from textbox from start to end
        # print(result)
        response = client.detect_sentiment(Text=result, LanguageCode='en')
        messagebox.showinfo(
            "Sentiment", "The prominant sentiment is: "
            + response['Sentiment']+"\n\nThe SentimentScore is:"
            + "\nPositive:" + str(response['SentimentScore']['Positive'])
            + "\nNegative:" + str(response['SentimentScore']['Negative'])
            + "\nNeutral:" + str(response['SentimentScore']['Neutral'])
            + "\nMixed:" + str(response['SentimentScore']['Mixed']))

    def btn2_KeyPhrase():
        aws_mng_con = boto3.session.Session(
            profile_name='demo1')                       # Create session
        client = aws_mng_con.client(
            service_name='comprehend', region_name='us-east-1')      # Create client
        result = textExample.get("1.0", "end")
        # print(result)
        response2 = client.detect_key_phrases(Text=result, LanguageCode='en')

        Keyph = [ph['Text'] for ph in response2['KeyPhrases']]
        anKeyph = ", ".join(Keyph)
        messagebox.showinfo("KeyPrases", "Key phrases are:\n\n"+anKeyph)

    # Button
    btn1 = Button(Sentiment_analysis, text="Analyze Sentiment", command=btn1_sentiment, foreground="#ffffff",
                  activebackground="#547c84", bg='#a93b44', cursor="hand2", width=16, height=1, font=("times new roman", 12, "bold"))
    btn1.place(x=580, y=480)

    btn2 = Button(Sentiment_analysis, text="Analyze KeyPhrase", command=btn2_KeyPhrase, foreground="#ffffff",
                  activebackground="#547c84", bg='#a93b44', cursor="hand2", width=16, height=1, font=("times new roman", 12, "bold"))
    btn2.place(x=765, y=480)

# Text2Speech Btn Function


def change_ToTextSpeech():

    root.title("Text-to-Speech")
    Text_to_Speech.pack(fill='both', expand=1)
    Mul_App.pack_forget()
    # set bg color
    Text_to_Speech.configure(bg="#fcfefc")

    # Insert GIF
    file = resource_path('chat1_test.gif')
    info = Image.open(file)
    # n_frames method calculate total no. of frames in the gif
    frameCnt = info.n_frames
    # print(frameCnt)
    # frameCnt = 110
    frames = [PhotoImage(file=resource_path('chat1_test.gif'), format='gif -index %i' % (i))
              for i in range(frameCnt)]

    def update(count):

        frame = frames[count]
        count += 1
        if count == frameCnt:
            count = 0
        label.configure(image=frame)
        Text_to_Speech.after(100, update, count)

    label = Label(Text_to_Speech)
    label.place(height=360, width=300, y=90)
    Text_to_Speech.after(0, update, 0)

    # Text Lable
    label_0 = Label(Text_to_Speech, text="Enter Text To Listen", font=(
        "times new roman", 45, "bold"), fg="#242244", bg="#fcfefc")
    label_0.place(x=390, y=20)

    # TextBox
    textExample = Text(Text_to_Speech, font=(
        "times new roman", 15), bg="lightgray")
    textExample.place(x=389, y=180, width=550, height=145)

    # TextBox/LISTEN Button Function

    def getText():
        aws_mng_con = boto3.session.Session(
            profile_name='demo1')                       # Create session
        client = aws_mng_con.client(
            service_name='polly', region_name='us-east-1')      # Create client
        result = textExample.get("1.0", "end")
        # print(result)
        response = client.synthesize_speech(
            VoiceId='Joanna', OutputFormat='mp3', Text=result, Engine='neural')
        # print(response)

        # Extracting audiostream from the dictionary
        if "AudioStream" in response:
            # Extract the 'AudioStream' from 'response' as a 'stream' and in the output
            # we gave the complete 'path' of the 'temporary directory' where complete speech
            # is stored along with the name 'speech.mp3'
            with closing(response['AudioStream']) as stream:
                # output is complete path to downloaded speech
                output = os.path.join(gettempdir(), "speech.mp3")
                try:
                    with open(output, "wb") as file:
                        # Write the o/p as a binary stream
                        file.write(stream.read())
                except IOError as error:
                    # print(error)
                    sys.exit(-1)
        else:
            # print("Could not find the stream!")
            sys.exit(-1)

        # Now opening Media Player
        if sys.platform == 'win32':
            os.startfile(output)

    # Button
    btnRead = Button(Text_to_Speech, text="LISTEN", command=getText, foreground="#84d2c0",
                     activebackground="#547c84", bg='#242244', cursor="hand2", width=14, height=1, font=("times new roman", 18, "bold"))
    btnRead.place(x=540, y=410)


# change_ToText_Translator

def change_ToText_Translator():
    root.title("Text Translator")
    Text_Translator.pack(fill='both', expand=1)
    Mul_App.pack_forget()
    # set bg color
    Text_Translator.configure(bg="#ffffff")

    # Text Lable
    label_0 = Label(Text_Translator, text="Enter Text To Translate", font=(
        "times new roman", 45, "bold"), fg="#a93b44", bg="#fcfefc")
    label_0.place(x=200, y=20)

    # TextBox
    textExample = Text(Text_Translator, font=(
        "times new roman", 15), bg="lightgray")
    textExample.place(x=100, y=150, width=815, height=175)

    aws_mng_con = boto3.session.Session(
        profile_name='demo1')                       # Create session

    def getHindi():
        client = aws_mng_con.client(
            service_name='translate', region_name='us-east-1')      # Create client
        result = textExample.get("1.0", "end")
        response = client.translate_text(
            Text=result, SourceLanguageCode='en', TargetLanguageCode='hi')
        messagebox.showinfo(
            "Translated Text", "Translated Text is:\n\n" +
            response.get('TranslatedText')
            + "\nSource Language Code: " + response.get('SourceLanguageCode')
            + "\nTarget Language Code: " + response.get('TargetLanguageCode'))

    def getJapenese():
        client = aws_mng_con.client(
            service_name='translate', region_name='us-east-1')      # Create client
        result = textExample.get("1.0", "end")
        response = client.translate_text(
            Text=result, SourceLanguageCode='en', TargetLanguageCode='ja')
        messagebox.showinfo(
            "Translated Text", "Translated Text is:\n\n" +
            response.get('TranslatedText')
            + "\nSource Language Code: " + response.get('SourceLanguageCode')
            + "\nTarget Language Code: " + response.get('TargetLanguageCode'))

    def getGerman():
        client = aws_mng_con.client(
            service_name='translate', region_name='us-east-1')      # Create client
        result = textExample.get("1.0", "end")
        response = client.translate_text(
            Text=result, SourceLanguageCode='en', TargetLanguageCode='de')
        messagebox.showinfo(
            "Translated Text", "Translated Text is:\n\n" +
            response.get('TranslatedText')
            + "\nSource Language Code: " + response.get('SourceLanguageCode')
            + "\nTarget Language Code: " + response.get('TargetLanguageCode'))

    def getChinese():
        client = aws_mng_con.client(
            service_name='translate', region_name='us-east-1')      # Create client
        result = textExample.get("1.0", "end")
        response = client.translate_text(
            Text=result, SourceLanguageCode='en', TargetLanguageCode='zh')
        messagebox.showinfo(
            "Translated Text", "Translated Text is:\n\n" +
            response.get('TranslatedText')
            + "\nSource Language Code: " + response.get('SourceLanguageCode')
            + "\nTarget Language Code: " + response.get('TargetLanguageCode'))

    def getSpanish():
        client = aws_mng_con.client(
            service_name='translate', region_name='us-east-1')      # Create client
        result = textExample.get("1.0", "end")
        response = client.translate_text(
            Text=result, SourceLanguageCode='en', TargetLanguageCode='es')
        messagebox.showinfo(
            "Translated Text", "Translated Text is:\n\n" +
            response.get('TranslatedText')
            + "\nSource Language Code: " + response.get('SourceLanguageCode')
            + "\nTarget Language Code: " + response.get('TargetLanguageCode'))

    def getFrench():
        client = aws_mng_con.client(
            service_name='translate', region_name='us-east-1')      # Create client
        result = textExample.get("1.0", "end")
        response = client.translate_text(
            Text=result, SourceLanguageCode='en', TargetLanguageCode='fr')

        messagebox.showinfo(
            "Translated Text", "Translated Text is:\n\n" +
            response.get('TranslatedText')
            + "\nSource Language Code: " + response.get('SourceLanguageCode')
            + "\nTarget Language Code: " + response.get('TargetLanguageCode'))

    # Button
    btn_Hindi = Button(Text_Translator, text="Hindi", command=getHindi, foreground="#ffffff",
                       activebackground="#547c84", bg='#a93b44', cursor="hand2", width=8, height=1, font=("times new roman", 18, "bold"))
    btn_Hindi.place(x=250, y=390)
    btn_Japenese = Button(Text_Translator, text="Japenese", command=getJapenese, foreground="#ffffff",
                          activebackground="#547c84", bg='#a93b44', cursor="hand2", width=8, height=1, font=("times new roman", 18, "bold"))
    btn_Japenese.place(x=420, y=390)
    btn_German = Button(Text_Translator, text="German", command=getGerman, foreground="#ffffff",
                        activebackground="#547c84", bg='#a93b44', cursor="hand2", width=8, height=1, font=("times new roman", 18, "bold"))
    btn_German.place(x=590, y=390)
    btn_Chinese = Button(Text_Translator, text="Chinese", command=getChinese, foreground="#ffffff",
                         activebackground="#547c84", bg='#a93b44', cursor="hand2", width=8, height=1, font=("times new roman", 18, "bold"))
    btn_Chinese.place(x=250, y=470)
    btn_Spanish = Button(Text_Translator, text="Spanish", command=getSpanish, foreground="#ffffff",
                         activebackground="#547c84", bg='#a93b44', cursor="hand2", width=8, height=1, font=("times new roman", 18, "bold"))
    btn_Spanish.place(x=420, y=470)
    btn_French = Button(Text_Translator, text="French", command=getFrench, foreground="#ffffff",
                        activebackground="#547c84", bg='#a93b44', cursor="hand2", width=8, height=1, font=("times new roman", 18, "bold"))
    btn_French.place(x=590, y=470)


def change_ToExtract_Text():
    root.title("Extract Text from Image")
    Extract_Text.pack(fill='both', expand=1)
    Mul_App.pack_forget()
    # set bg color
    Extract_Text.configure(bg="#ffffff")


# Insert GIF
    file = resource_path('ImageText3.gif')
    info = Image.open(file)
    # n_frames method calculate total no. of frames in the gif
    frameCnt = info.n_frames
    # print(frameCnt)
    # frameCnt = 110
    frames = [PhotoImage(file=resource_path('ImageText3.gif'), format='gif -index %i' % (i))
              for i in range(frameCnt)]

    def update(count):

        frame = frames[count]
        count += 1
        if count == frameCnt:
            count = 0
        label.configure(image=frame)
        Extract_Text.after(100, update, count)

    label = Label(Extract_Text)
    label.place(height=400, width=800, y=40, x=100)
    Extract_Text.after(0, update, 0)

    # Button Function

    def upload_file():
        aws_mng_con = boto3.session.Session(
            profile_name='demo1')                       # Create session
        client = aws_mng_con.client(
            service_name='textract', region_name='us-east-1')      # Create client

        global img
        f_types = [('Png Files', '*.png')]
        filename = filedialog.askopenfilename(filetypes=f_types)
        img = ImageTk.PhotoImage(file=filename)

        img_bytes = get_img_byte(filename)
        b2 = Button(Extract_Text, image=img)  # using Button
        b2.place(height=340, width=900, x=50, y=100)

        response = client.detect_document_text(Document={'Bytes': img_bytes})

        a = [item['Text']
             for item in response['Blocks'] if item['BlockType'] == 'LINE']

        extractedText = " ".join(a)
        with open("extractedText.txt", 'w') as f:
            f.write(extractedText)

        messagebox.showinfo(
            "Extracted Text", "Extracted Text is:\n\n"+extractedText)

        # def open_extractedText():
        #     with open("extractedText.txt", 'r') as f:
        #         f.read(extractedText)

    # Function for getting binary code

    def get_img_byte(filename):
        with open(filename, 'rb') as imgfile:
            return imgfile.read()

    # Button
    btn_Upload = Button(Extract_Text, text=" [ + ] Upload File & See what it has!!!", command=upload_file, foreground="#ffffff",
                        activebackground="#547c84", bg='#57d495', cursor="hand2", width=30, height=1, font=("times new roman", 18, "bold"))
    btn_Upload.place(x=270, y=40)


# Add Copyright
copyright_symbol = u"\u00A9"
label_1 = Label(root, text=u"Copyright{copyright_symbol} 2022, Divyanshu Gupta, All rights reserved. 0905CS191069".format(copyright_symbol=copyright_symbol), font=(
    "times new roman", 10, "bold"), fg="#635e70", bg="#fcfefc")
label_1.place(x=560, y=550)
# a = Multi_tasking_app()
root.mainloop()  # mainloop() is used to load the GUI Window
