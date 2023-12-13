import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import pyttsx3
import takeImage
import trainImage
import automaticAttedance

global screen

# add voice command
def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()

# validates value (should be string)
def testVal(inStr, acttyp):
    if acttyp == "1":
        if not inStr.isdigit():
            return False
    return True

# take image UI configuration
def TakeImageUI():
    ImageUI = Tk()
    ImageUI.title("Take Student Image..")
    ImageUI.geometry("780x480")
    ImageUI.configure(background="black")
    ImageUI.resizable(0, 0)
    title = tk.Label(ImageUI, bg="black", relief=RIDGE,
                     bd=10, font=("arial", 35))
    title.pack(fill=X)
    title = tk.Label(ImageUI, text="Register Your Face",
                     bg="black", fg="white", font=("arial", 30),)
    title.place(x=270, y=12)

    header = tk.Label(
        ImageUI,
        text="Enter the details",
        bg="black",
        fg="white",
        bd=10,
        font=("arial", 24),
    )
    header.place(x=280, y=75)

    er_no = tk.Label(
        ImageUI,
        text="Enrollment No",
        width=10,
        height=2,
        bg="black",
        fg="white",
        bd=5,
        relief=RIDGE,
        font=("arial", 12),
    )
    er_no.place(x=120, y=130)
    text_area_er_no = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        bg="black",
        fg="white",
        relief=RIDGE,
        font=("times", 25, "bold"),
    )
    text_area_er_no.place(x=250, y=130)
    text_area_er_no["validatecommand"] = (
        text_area_er_no.register(testVal), "%P", "%d")

    name = tk.Label(
        ImageUI,
        text="Name",
        width=10,
        height=2,
        bg="black",
        fg="white",
        bd=5,
        relief=RIDGE,
        font=("arial", 12),
    )
    name.place(x=120, y=200)
    text_area_name = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        bg="black",
        fg="white",
        relief=RIDGE,
        font=("times", 25, "bold"),
    )
    text_area_name.place(x=250, y=200)

    def take_image():
        er_no = text_area_er_no.get()
        name = text_area_name.get()
        takeImage.TakeImage(
            er_no,
            name,
            haarcasecade_path,
            trainimage_path,
            text_to_speech,
        )
        text_area_er_no.delete(0, "end")
        text_area_name.delete(0, "end")

    take_img_button = tk.Button(
        ImageUI,
        text="Take Image",
        command=take_image,
        bd=10,
        font=("arial", 18),
        bg="black",
        fg="white",
        height=2,
        width=12,
        relief=RIDGE,
    )
    take_img_button.place(x=130, y=350)

    def train_image():
        trainImage.TrainImage(
            trainimage_path,
            trainimagelabel_path,
            text_to_speech,
        )

    train_image_button = tk.Button(
        ImageUI,
        text="Train Image",
        command=train_image,
        bd=10,
        font=("arial", 18),
        bg="black",
        fg="white",
        height=2,
        width=12,
        relief=RIDGE,
    )
    train_image_button.place(x=360, y=350)

def automatic_attedance():
    automaticAttedance.subjectChoose(text_to_speech)

haarcasecade_path = "D:\\Coding\\Minor Project\\haarcascade_frontalface_default.xml"
trainimagelabel_path = 'D:\\Coding\\Minor Project\\TrainingImageLabel\\Trainner.yml'
trainimage_path = 'D:\\Coding\\Minor Project\\TrainingImage'
studentdetail_path = 'D:\\Coding\\Minor Project\\StudentDetails\\studentdetails.csv'
attendance_path = 'D:\\Coding\\Minor Project\\Attendance'

# App configuration
window = Tk()
window.title("Face recognizer")
window.geometry("1280x720")
window.configure(background="black")

App = tk.Label(
    window,
    text="Welcome to the Face Recognition Based\nAttendance Management System",
    bg="black",
    fg="white",
    bd=5,
    pady=10,
    font=("arial", 35),
)
App.pack()

register_icon = Image.open("Icons/register.png")
register_box = ImageTk.PhotoImage(register_icon)
register_label = Label(window, image=register_box)
register_label.image = register_box
register_label.place(x=350, y=170)

attendance_icon = Image.open("Icons/attendance.png")
App = ImageTk.PhotoImage(attendance_icon)
attendance_label = Label(window, image=App)
attendance_label.image = App
attendance_label.place(x=650, y=170)

register_box = tk.Button(
    window,
    text="Register a new student",
    command=TakeImageUI,
    bd=10,
    font=("arial", 16),
    bg="black",
    fg="white",
    height=2,
    width=17,
)
register_box.place(x=350, y=420)

attendance_box = tk.Button(
    window,
    text="Take Attendance",
    command=automatic_attedance,
    bd=10,
    font=("arial", 16),
    bg="black",
    fg="white",
    height=2,
    width=21,
)
attendance_box.place(x=650, y=420)

exit_box = tk.Button(
    window,
    text="EXIT",
    bd=10,
    command=quit,
    font=("arial", 16),
    bg="black",
    fg="white",
    height=2,
    width=17,
)
exit_box.place(x=500, y=560)

window.mainloop()
