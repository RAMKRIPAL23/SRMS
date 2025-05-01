from tkinter import*
from PIL import Image, ImageTk, ImageDraw  # For image handling and drawing
from datetime import*  # For current time
import time
from math import*  # For sin, cos, radians
import pymysql  # Not used here, but probably used elsewhere in your app
from tkinter import messagebox, ttk  # For popup messages and widgets
import sqlite3  # For database interaction
import os  # To run system commands


class Login_window:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#021e2f")

        #--- Left background section ---
        left_lbl = Label(self.root, bg="#08A3D2", bd=0)
        left_lbl.place(x=0, y=0, relheight=1, width=600)

        #--- Right background section ---
        right_lbl = Label(self.root, bg="#031F3C", bd=0)
        right_lbl.place(x=600, y=0, relheight=1, relwidth=1)

        #--- Login Frame ---
        login_frame = Frame(self.root, bg="white")
        login_frame.place(x=250, y=100, width=800, height=500)

        #--- Title ---
        title = Label(login_frame, text="LOGIN HERE", font=("times new roman", 30, "bold"), bg="white", fg="#08A3D2").place(x=250, y=50)

        #--- Email Field ---
        email = Label(login_frame, text="EMAIL ADDRESS", font=("times new roman", 18, "bold"), bg="white", fg="gray").place(x=250, y=150)
        self.txt_email = Entry(login_frame, font=("times new roman", 15), bg="lightgray")
        self.txt_email.place(x=250, y=180, width=350, height=35)

        #--- Password Field ---
        pass_ = Label(login_frame, text="PASSWORD", font=("times new roman", 18, "bold"), bg="white", fg="gray").place(x=250, y=250)
        self.txt_pass_ = Entry(login_frame, font=("times new roman", 15), bg="lightgray")
        self.txt_pass_.place(x=250, y=280, width=350, height=35)

        #--- Buttons ---
        btn_reg = Button(login_frame, text="Register new Account?", font=("times new roman", 14), bg="white", bd=0, fg="#B00857", cursor="hand2", command=self.register_windows).place(x=250, y=320)
        btn_forget = Button(login_frame, text="Forget Password", font=("times new roman", 14), bg="white", bd=0, fg="red", cursor="hand2", command=self.foget_password_window).place(x=450, y=320)
        btn_login = Button(login_frame, text="Login", font=("times new roman", 20), bg="#B00857", bd=0, fg="white", cursor="hand2", command=self.login).place(x=250, y=380, width=180, height=40)

        #--- Clock Display ---
        self.lbl = Label(self.root, text="R Singh Clock", font=("Book antiqua", 25, "bold"), fg="white", compound=BOTTOM, bg="#081923", bd=0)
        self.lbl.place(x=90, y=120, height=450, width=350)
        self.working()  # Start the clock animation

    #--- Reset all input fields ---
    def reset(self):
        self.cmb_quest.current(0)
        self.txt_new_pass.delete(0, END)
        self.txt_answer.delete(0, END)
        self.txt_pass_.delete(0, END)
        self.txt_email.delete(0, END)

    #--- Forget Password Handler ---
    def foget_password(self):
        if self.cmb_quest.get() == "select" or self.txt_answer.get() == "" or self.txt_new_pass.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root2)
        else:
            try:
                con = sqlite3.connect(database="rms.db")
                cur = con.cursor()
                cur.execute("select * from employee where email=? and question=? and answer=?", (self.txt_email.get(), self.cmb_quest.get(), self.txt_answer.get()))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Incorrect Security Question or Answer", parent=self.root2)
                else:
                    cur.execute("update employee set password=? where email=?", (self.txt_new_pass.get(), self.txt_email.get()))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success", "Password has been reset. Please login with new password", parent=self.root2)
                    self.reset()
                    self.root2.destroy()
            except Exception as es:
                messagebox.showerror("Error", f"Error Due to {str(es)}", parent=self.root)

    #--- Open Forget Password Popup ---
    def foget_password_window(self):
        if self.txt_email.get() == "":
            messagebox.showerror("Error", "Please enter the email address to reset your password", parent=self.root)
        else:
            try:
                con = sqlite3.connect(database="rms.db")
                cur = con.cursor()
                cur.execute("select * from employee where email=?", (self.txt_email.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid email address", parent=self.root)
                else:
                    con.close()
                    # Create reset password popup
                    self.root2 = Toplevel()
                    self.root2.title("Forget Password")
                    self.root2.geometry("350x400+495+150")
                    self.root2.config(bg="white")
                    self.root2.focus_force()
                    self.root2.grab_set()

                    t = Label(self.root2, text="Forget Password", font=("times new roman", 20, "bold"), bg="white", fg="red").place(x=0, y=10, relwidth=1)

                    # Security Question
                    question = Label(self.root2, text="Security Question", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=100)
                    self.cmb_quest = ttk.Combobox(self.root2, font=("times new roman", 13), state='readonly', justify=CENTER)
                    self.cmb_quest['values'] = ("Select", "Your first pet name", "Yourr Birth Place", "Your Best Friend")
                    self.cmb_quest.place(x=50, y=130, width=250)
                    self.cmb_quest.current(0)

                    # Answer
                    answer = Label(self.root2, text="Answer", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=180)
                    self.txt_answer = Entry(self.root2, font=("times new roman", 15), bg="lightgray")
                    self.txt_answer.place(x=50, y=210, width=250)

                    # New Password
                    new_password = Label(self.root2, text="New Password", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=260)
                    self.txt_new_pass = Entry(self.root2, font=("times new roman", 15), bg="lightgray")
                    self.txt_new_pass.place(x=50, y=290, width=250)

                    # Reset Button
                    btn_change_password = Button(self.root2, text="Reset Password", bg="green", fg="white", command=self.foget_password, font=("times new roman", 15, "bold")).place(x=90, y=340)

            except Exception as es:
                messagebox.showerror("Error", f"Error Due to {str(es)}", parent=self.root)

    #--- Switch to registration window ---
    def register_windows(self):
        self.root.destroy()
        import userreg  # Imports and runs registration script

    #--- Login Authentication ---
    def login(self):
        if self.txt_email.get() == "" or self.txt_pass_.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
        else:
            try:
                con = sqlite3.connect(database="rms.db")
                cur = con.cursor()
                cur.execute("select * from employee where email=? and password=?", (self.txt_email.get(), self.txt_pass_.get()))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Username & Password", parent=self.root)
                else:
                    messagebox.showinfo("Success", f"Welcome: {self.txt_email.get()}", parent=self.root)
                    self.root.destroy()
                    os.system("python userdash.py")  # Load dashboard
                con.close()
            except Exception as es:
                messagebox.showerror("Error", f"Error Due to {str(es)}", parent=self.root)

    #--- Draw Clock Image ---
    def clock_image(self, hr, min_, sec_):
        clock = Image.new("RGB", (400, 400), (8, 25, 35))
        draw = ImageDraw.Draw(clock)

        # Load and paste clock face
        bg = Image.open("images/c.png")
        bg = bg.resize((300, 300), Image.LANCZOS)
        clock.paste(bg, (50, 50))

        origin = 200, 200

        # Hour hand
        draw.line((origin, 200 + 50 * sin(radians(hr)), 200 - 50 * cos(radians(hr))), fill="#DF005E", width=4)
        # Minute hand
        draw.line((origin, 200 + 80 * sin(radians(min_)), 200 - 80 * cos(radians(min_))), fill="white", width=3)
        # Second hand
        draw.line((origin, 200 + 100 * sin(radians(sec_)), 200 - 100 * cos(radians(sec_))), fill="yellow", width=2)
        # Center circle
        draw.ellipse((195, 195, 210, 210), fill="#1AD5D5")

        clock.save("images/clock_new.png")  # Save image

    #--- Clock Updater ---
    def working(self):
        h = datetime.now().time().hour
        m = datetime.now().time().minute
        s = datetime.now().time().second
        hr = (h / 12) * 360
        min_ = (m / 60) * 360
        sec_ = (s / 60) * 360
        self.clock_image(hr, min_, sec_)
        self.img = ImageTk.PhotoImage(file="images/clock_new.png")
        self.lbl.config(image=self.img)
        self.lbl.after(200, self.working)  # Refresh clock every 200 ms


#--- Run the Application ---
root = Tk()
obj = Login_window(root)
root.mainloop()
