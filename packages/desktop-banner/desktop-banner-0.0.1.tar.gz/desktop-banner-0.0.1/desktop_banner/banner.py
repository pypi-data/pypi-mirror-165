from tkinter import *
from screeninfo import get_monitors
import configparser
import os

class Banner:
    def __init__(self, master, monitor):
        # Define default settings 
        self.settings = {}
        self.settings["message"] = "Create /etc/banner.conf with permissions 644" 
        self.settings["color"] = "#4cbb17"
        self.settings["opacity"] = 0.8
        self.settings["width"] = 0.85

        self.window = master
        self.monitor = monitor
        self.getSettings()
        self.configureBanner()

    def getSettings(self):
        if os.access('/etc/banner.conf',os.R_OK):
            self.parser = configparser.ConfigParser()
            self.parser.read('/etc/banner.conf')
            for key in self.settings:
                if self.parser.has_option('settings',key):
                    self.settings[key] = self.parser['settings'][key]
    
    def printBannerConfig(self):
        for item in self.__dict__:
            print(str(item) + " : " + str(self.__dict__[item]))

    def configureBanner(self):
        # Calculate banner width from screen dimensions
        self.banner_width = int(self.monitor.width * float(self.settings['width']))
        self.banner_height = 20

        # x and y positioning of the banner
        # x should be centered and y is always at the top (which is 0)
        self.x = int( self.monitor.x + (self.monitor.width - self.banner_width)/2)
        self.y = 0

        # Configure the box that houses message text
        self.banner_message = Text(self.window, bg=self.settings['color'], width=self.banner_width)
        self.banner_message.tag_configure("center", justify='center')
        self.banner_message.insert("1.0", self.settings['message'])
        self.banner_message.tag_add("center", "1.0", "end")
        self.banner_message["state"]=DISABLED
        self.banner_message.pack(expand=True)

        # Configure window dimensions and attributes
        self.window.geometry("%dx%d+%d+%d" % (self.banner_width,self.banner_height,self.x,self.y))     
        self.window.wm_attributes('-type', 'splash')
        self.window.wm_attributes('-alpha', self.settings["opacity"])
        self.window.attributes('-topmost', 'true')


def main():
    # Create Tk main window and hide it in background / no system tray
    root = Tk()
    root.wm_attributes('-type','splash')
    root.withdraw()

    for monitor in get_monitors():
        new_banner=Toplevel(root)
        Banner(new_banner, monitor)

    root.mainloop()

if __name__ == "__main__":
    main()
