import os
import tkinter as tk
import sys
import glob
import serial
import time
import shutil

class OptionMenu(tk.OptionMenu):
    def __init__(self, *args, **kw):
        self._command = kw.get("command")
        self.variable = args
        tk.OptionMenu.__init__(self, *self.variable, **kw)
        
    def addOption(self, label):
        self["menu"].add_command(label=label,
            command=tk._setit(self.variable[1], label, self._command))
    def deleteAll(self):
        self["menu"].delete(0, "end")
        
def refresh(commMenu, moduleMenu):
    refreshModules(moduleMenu)
    refreshPorts(commMenu)
        
def refreshModules(menu):
    modules = []
    try:
        modules = os.listdir("./modules/Highlanders")
    except OSError as e:
        print("No Modules Found", e)    
    
    menu.deleteAll()
    for mod in modules:
        menu.addOption(mod)
        
def refreshPorts(menu):
    comms = serial_ports()

    if (len(comms) == 0):
        comms = ['']

    menu.deleteAll()
    for comm in comms:
        menu.addOption(comm)
    
def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
    
    
def deploy(port, module):
    moduleFile = "./modules/Highlanders/" + module + "/" + module + ".py"
    scriptFile = "./modules/Highlanders/" + module + "/" + "script.cfg"
    dstDir = "D:/modules/Highlanders/" + module

    sendCommand(port, b'streamoff\rusbsd\r')
    time.sleep(3)

    copyFile(port, moduleFile, dstDir)
    copyFile(port, scriptFile, dstDir)
    
    sendCommand(port, b'restart\r')
        
def sendConfig(port, file):
    srcFile = "./config/" + file
    dstDir = "D:/config"
    
    sendCommand(port, b'streamoff\rusbsd\r')
    time.sleep(3)

    copyFile(port, srcFile, dstDir)
    sendCommand(port, b'restart\r')

def copyFile(port, srcFile, dstDir):
    try:
        if not os.path.exists(dstDir):
            os.makedirs(dstDir)
        
        shutil.copy2(srcFile, dstDir)
        time.sleep(1)
    except (serial.SerialException) as e:
        print("Could not connect to", port, e)
    except (OSError) as e:
        print(e)

def sendCommand(port, cmd):
    try:
        com = serial.Serial(port)
        com.write(cmd)
        com.close()
    except (serial.SerialException) as e:
        print("Could not connect to", port, e)
    except (OSError) as e:
        print(e)        


if __name__ == '__main__':  
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    
    main = tk.Tk()
    main.title("Jevois Deploy")
    
    lbl = tk.Label(main, text="Module:") 
    lbl.grid(column=0, row=0)
    lbl = tk.Label(main, text="Comm Port:")
    lbl.grid(column=0, row=1)
    
    
    moduleString = tk.StringVar(main)
    moduleString.set([''])
    moduleMenu = OptionMenu(main, moduleString, "")
    moduleMenu.grid(column=1, row=0)
    
    commString = tk.StringVar(main)
    commString.set([''])
    commMenu = OptionMenu(main, commString, "")
    commMenu.grid(column=1, row=1)
    
    refresh(commMenu, moduleMenu)
    
    
    buttonWidth = 16
    button = tk.Button(main, text='Deploy', width=buttonWidth, command=lambda : deploy(commString.get(), moduleString.get()))
    button.grid(column=1, row=2)
    
    button = tk.Button(main, text='Refresh', width=buttonWidth, command=lambda : refresh(commMenu, moduleMenu))
    button.grid(column=0, row=2)
    
    button = tk.Button(main, text='initscript', width=buttonWidth, command=lambda : sendConfig(commString.get(), "initscript.cfg"))
    button.grid(column=1, row=3)
    
    button = tk.Button(main, text='videomappings', width=buttonWidth, command=lambda : sendConfig(commString.get(), "videomappings.cfg"))
    button.grid(column=0, row=3)
    
    main.mainloop()
