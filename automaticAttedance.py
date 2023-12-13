import tkinter as tk
from tkinter import *
import os
import cv2
import pandas as pd
import datetime
import time

# haarcasecade_path = "C:\\Users\\Lenovo\\Documents\\FaceData\\haarcascade_frontalface_default.xml"
# trainimagelabel_path = 'C:\\Users\\Lenovo\\Documents\\FaceData\\Label\\Trainner.yml'

# trainimage_path = 'C:\\Users\\Lenovo\\Documents\\FaceData\\Images'
# studentdetail_path = 'C:\\Users\\Lenovo\\Documents\\FaceData\\StudentDetails\\studentdetails.csv'

# attendance_path = 'C:\\Users\\Lenovo\\Documents\\FaceData\\Attendance'

haarcasecade_path = "D:\\Coding\\Minor Project\\haarcascade_frontalface_default.xml"
trainimagelabel_path = 'D:\\Coding\\Minor Project\\TrainingImageLabel\\Trainner.yml'
trainimage_path = 'D:\\Coding\\Minor Project\\TrainingImage'
studentdetail_path = 'D:\\Coding\\Minor Project\\StudentDetails\\studentdetails.csv'
attendance_path = 'D:\\Coding\\Minor Project\\Attendance'


def subjectChoose(text_to_speech):
    def FillAttendance():
        subject_name = subject_text_area.get()
        if subject_name == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            folder_name = os.path.join(attendance_path, subject_name)
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
                print(f"Folder {folder_name} created successfully!")
            else:
                print(f"Folder {folder_name} already exists.")
            try:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read(trainimagelabel_path)
                except:
                    error = "No training data found. Please train the data first."
                    text_to_speech(error)
                facecasCade = cv2.CascadeClassifier(haarcasecade_path)
                
                df = pd.read_csv(studentdetail_path)
                camera = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ["Enrollment", "Name"]
                attendance = pd.DataFrame(columns=col_names)
                while True:
                    ___, image = camera.read()
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)
                    for (x, y, w, h) in faces:
                        global Id
                        Id, conf = recognizer.predict(gray[y: y + h, x: x + w])
                        if conf < 70:
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            Subject = subject_text_area.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                            aa = df.loc[df["Enrollment"] == Id]["Name"].values
                            global tt
                            tt = str(Id) + "-" + aa
                            attendance.loc[len(attendance)] = [
                                Id,
                                aa,
                            ]
                            cv2.rectangle(
                                image, (x, y), (x + w, y + h), (0, 260, 0), 4)
                            cv2.putText(
                                image, str(tt), (x + h,y), font, 1, (255, 255, 0,), 4
                            )
                        else:
                            Id = "Unknown"
                            tt = str(Id)
                            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(image, str(tt), (x + h, y),font, 1, (0, 25, 255), 4)

                    attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                    cv2.imshow("Filling Attendance...", image)
                    key = cv2.waitKey(30) & 0xFF
                    if key == 27:
                        break

                
                ts = time.time()
                attendance[date] = 1
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                attendance = attendance.drop_duplicates( ["Enrollment"], keep="first")
                print(attendance)
                attendance.to_csv("Attendance/" + subject_name + "/" +date + ".csv", index=False)
                m = "Attendance Filled Successfully of " + Subject
                text_to_speech(m)
                camera.release()
                cv2.destroyAllWindows()

            except:
                f = "Some error"
                text_to_speech(f)
                cv2.destroyAllWindows()

    subject = Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")
    
    title = tk.Label(
        subject, 
        bg="black", 
        relief=RIDGE,
        bd=10, 
        font=("arial", 30))
    
    title.pack(fill=X)
    
    title = tk.Label(
        subject,
        text="Enter the Subject Name",
        bg="black",
        fg="white",
        font=("arial", 25),
    )
    title.place(x=160, y=12)

    subject_label = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="black",
        fg="white",
        bd=5,
        relief=RIDGE,
        font=("arial", 15),
    )
    subject_label.place(x=50, y=100)

    subject_text_area = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="black",
        fg="white",
        relief=RIDGE,
        font=("times", 30, "bold"),
    )
    subject_text_area.place(x=190, y=100)

    fill_attendance_button = tk.Button(
        subject,
        text="Fill Attendance",
        command=FillAttendance,
        bd=7,
        font=("arial", 15),
        bg="black",
        fg="white",
        height=2,
        width=25,
        relief=RIDGE,
    )
    fill_attendance_button.place(x=195, y=170)
    subject.mainloop()
