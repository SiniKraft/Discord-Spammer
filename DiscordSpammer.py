import keyboard  # pip install keyboard
import tkinter as tk
import tkinter.ttk as ttk
from time import sleep as time_sleep
import threading
from win10toast import ToastNotifier  # pip install win10toast
from pyperclip import copy, paste  # pip install pyperclip
import os
import urllib.request
import json
from tkinter import messagebox as mbox
from sys import exit
import webbrowser

# Init

DiscordSpammerFilesPath = os.path.expandvars(r'%APPDATA%\DiscordSpammer\\')  # Get the path
try:
    os.makedirs(DiscordSpammerFilesPath)  # If the folder does not exist, create it.
except:
    pass

if not os.path.isfile(DiscordSpammerFilesPath + "\\DiscordSpammer.ico"):  # If icon is nonexistent, downloading it
    urllib.request.urlretrieve("https://raw.githubusercontent.com/SiniKraft/Discord-Spammer/main/DiscordSpammer.ico",
                               DiscordSpammerFilesPath + "\\DiscordSpammer.ico")


# Classes


class Var:  # This class will contains all the global vars and they will be accessible everywhere.
    def __init__(self):
        super(Var, self).__init__()
        self.ThreadsNumber = 0
        self.isSpamBtnEnabled = True
        self.isWindowAlive = True
        self.ClipboardBackup = ""
        self.Delay = 0
        self.numberToSpam = 0
        self.isCheckBoxChecked = False

    def get_value(self, value_name):
        return eval("self." + value_name)

    def set_value(self, value_name, value_content):
        exec("self." + value_name + " = " + str(value_content))


# Functions


def save_settings():
    if var1.get() == 0:
        is_checkbox_checked = False
    elif var1.get() == 1:
        is_checkbox_checked = True
    dict_in = {'message': input_txt.get("1.0", tk.END)[:-1],
               "delay": input_time_txt.get("1.0", tk.END)[:-1],
               "number_to_spam": input_number_txt.get("1.0", tk.END)[:-1], 'is_checkbox_checked': is_checkbox_checked}
    write_json = json.dumps(dict_in, indent=4)
    with open(DiscordSpammerFilesPath + "settings.json", "w+") as _file:
        _file.write(write_json)
        _file.close()


def do_nothing():  # A very useful function.
    pass


def btn_state():
    while global_vars.get_value("isWindowAlive"):
        if global_vars.get_value("isSpamBtnEnabled"):
            spam_btn["state"] = tk.NORMAL
        else:  # Will enable or disable the spam btn based on a global var and stop this process if window destroyed
            spam_btn["state"] = tk.DISABLED


def notify(message, time):
    try:
        notifier.show_toast("Discord Spammer", message, duration=time,
                            icon_path=DiscordSpammerFilesPath + "DiscordSpammer.ico")
    except:
        pass  # Try to show a windows notification.


def spam_thread():  # The main script executed in a thread
    time_to_sleep = global_vars.get_value("Delay") * 0.001
    time_sleep(5)
    tt2 = threading.Thread(target=notify, args=("Spamming ...", 2), )
    try:
        tt2.start()
    except:
        pass
    time_sleep(1)
    if global_vars.get_value("isCheckBoxChecked") == 0:
        for x in range(0, global_vars.get_value("numberToSpam")):
            keyboard.press("ctrl")
            keyboard.press("v")
            keyboard.release("ctrl")
            keyboard.release("v")
            keyboard.press("enter")
            keyboard.release("enter")
            time_sleep(time_to_sleep)
    else:
        list_to_print = list(paste())
        for x in range(0, global_vars.get_value("numberToSpam")):
            for i in range(0, len(list_to_print)):
                copy(list_to_print[i])
                keyboard.press("ctrl")
                keyboard.press("v")
                keyboard.release("ctrl")
                keyboard.release("v")
                keyboard.press("enter")
                keyboard.release("enter")
                time_sleep(time_to_sleep)

    time_sleep(3)
    global_vars.set_value("isSpamBtnEnabled", True)


def spam():  # Executed when the Spam btn is clicked.
    save_settings()
    if var1.get() == 0:
        is_checkbox_checked = False
    elif var1.get() == 1:
        is_checkbox_checked = True
    global_vars.set_value("isCheckBoxChecked", is_checkbox_checked)
    global_vars.set_value("isSpamBtnEnabled", False)
    try:
        global_vars.set_value("Delay", int(str(input_time_txt.get("1.0", tk.END)[:-1]).lstrip("0")))
    except:
        mbox.showerror("Invalid input", "The delay input is invalid !")
        window.destroy()
        exit()
    try:
        global_vars.set_value("numberToSpam", int(str(input_number_txt.get("1.0", tk.END)[:-1]).lstrip("0")))
    except:
        mbox.showerror("Invalid input", "The delay input is invalid !")
        window.destroy()
        exit()
    copy(input_txt.get("1.0", tk.END)[:-1])
    t2 = threading.Thread(target=notify, args=("Spamming in 5 seconds ...", 4), )
    ttt2 = threading.Thread(target=notify, args=("Spamming in 5 seconds ...", 4), )
    exec("t" + str(global_vars.get_value("ThreadsNumber")) + " = threading.Thread(target=spam_thread,)")
    exec("t" + str(global_vars.get_value("ThreadsNumber")) + ".start()")
    global_vars.set_value("ThreadsNumber", (global_vars.get_value("ThreadsNumber") + 1))
    try:
        t2.start()
    except RuntimeError:
        ttt2.start()


def stop_window():  # Executed when the window is destroyed.
    global_vars.set_value("isWindowAlive", False)
    save_settings()
    window.destroy()


def view_source():
    webbrowser.open("https://github.com/SiniKraft/Discord-Spammer")


# Global vars

global_vars = Var()
notifier = ToastNotifier()
t1 = threading.Thread(target=spam_thread, )

# Load settings

if os.path.isfile(DiscordSpammerFilesPath + "settings.json"):
    with open(DiscordSpammerFilesPath + "settings.json", "r") as file:
        data = json.load(file)
        file.close()  # Will simply load the dict present in 'settings.json' if exists.
    delay_loaded = data["delay"]
    message_loaded = data["message"]
    number_to_spam_loaded = data["number_to_spam"]
    is_check_box_checked_loaded = data["is_checkbox_checked"]
else:
    delay_loaded = "000100"
    message_loaded = "Discord Spammer by SiniKraft"
    number_to_spam_loaded = "30"
    is_check_box_checked_loaded = False

# Window

window = tk.Tk()  # Initialising the window
win_width = 400
win_height = 210
pos_right = int(window.winfo_screenwidth() / 2 - win_width / 2)
pos_down = int(window.winfo_screenheight() / 2 - win_height / 2)  # will calculate the window first position.
window.title("Discord Spammer by SiniKraft v. Alpha 0.1")  # Set title.
window.resizable(0, 0)  # Make the window can't be resized.
window.geometry("{0}x{1}+{2}+{3}".format(win_width, win_height, pos_right, pos_down))  # Set window properties.

input_txt = tk.Text(window, height=3, width=40, font=("Segoe UI",))
input_txt.place(x=17, y=20)
input_txt.insert(tk.END, message_loaded)  # Replace the text field vy this default value.

text = ttk.Label(window, text="Delay between each line :                  ms")
text.place(x=17, y=95)
input_time_txt = tk.Text(window, height=1, width=6, font=("Segoe UI", 9))
input_time_txt.place(x=160, y=95)
input_time_txt.insert(tk.END, delay_loaded)

text_number = ttk.Label(window, text="Number of messages to spam :                  times")
text_number.place(x=17, y=120)
input_number_txt = tk.Text(window, height=1, width=6, font=("Segoe UI", 9))
input_number_txt.place(x=190, y=120)
input_number_txt.insert(tk.END, number_to_spam_loaded)

var1 = tk.IntVar()
if is_check_box_checked_loaded:
    var1.set(1)
else:
    var1.set(0)
c1 = ttk.Checkbutton(window, text='Spam each letter (beta)', variable=var1, onvalue=1, offvalue=0)
c1.place(x=17, y=145)

spam_btn = ttk.Button(text="Spam", command=spam)
spam_btn.place(x=160, y=168)

source_btn = ttk.Button(text="View Source", command=view_source)
source_btn.place(x=280, y=168)

thread = threading.Thread(target=btn_state,)
thread.start()

window.protocol('WM_DELETE_WINDOW', stop_window)  # Will execute function stop_window instead of instantly deleting it.
window.iconbitmap(DiscordSpammerFilesPath + "DiscordSpammer.ico")
window.mainloop()  # Run the window
