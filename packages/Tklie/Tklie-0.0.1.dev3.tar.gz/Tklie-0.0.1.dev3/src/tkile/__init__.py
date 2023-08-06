from tkile.Constant import *
from tkinter import TclError
from functools import singledispatch

__all__ = [
    "Application",
    "Widget",
    "Window",
    "Button"
]


def Error(en_strings):
    from colorama import Fore
    print(Fore.RED+f"tkile Error : {en_strings}"+Fore.RESET)


def Empty():
    pass


class Application(object):
    __name__ = "tkile.Application"

    def __init__(self):
        super(Application, self).__init__()
        self.applicationInit()

    def applicationInit(self):
        pass

    def Run(self, Window):
        Window.Class.mainloop()

    def Exit(self, Window):
        Window.Class.quit()


class Event(object):
    def __init__(self):
        super(Event, self).__init__()
        self.Class = None

    def bindEvent(self, eventName: str = None, eventFunc=None, handlerName=None):
        id = self.Class.bind(eventName, eventFunc)
        if handlerName is not None:
            self.setEvent(handlerName, id)

    def bindEventAll(self, eventName: str = None, eventFunc=None, handlerName=None):
        id = self.Class.bind_all(eventName, eventFunc)
        if handlerName is not None:
            self.setEvent(handlerName, id)

    def bindEventClass(self, className, eventName: str = None, eventFunc=None, handlerName=None):
        id = self.Class.bind_class(className, eventName, eventFunc)
        if handlerName is not None:
            self.setEvent(handlerName, id)

    def bindEventCanel(self, eventName, id):
        self.Class.unbind(eventName, id)

    def waitTime(self, waitMs, waitFunc=None, handlerName=None):
        id = self.Class.after(waitMs, waitFunc)
        if handlerName is not None:
            self.setEvent(handlerName, id)


class EventHandler(object):
    def __init__(self):
        super(EventHandler, self).__init__()

        self.Class = None
        self.events = {}

    def getEvents(self):
        return self.events

    def setEvent(self, eventName, eventId):
        self.events[eventName] = eventId

    def getEvent(self, eventName):
        try:
            return self.events[eventName]
        except KeyError:
            Error("eventName not found")


class WindowEvent(Event):
    def __init__(self):
        super(WindowEvent, self).__init__()


class WidgetEvent(Event):
    def __init__(self):
        super(WidgetEvent, self).__init__()

    def onSizeChange(self, func, handlerName=None):
        self.bindEvent("<Configure>", func, handlerName)

    def onWidgetDestory(self, func, handlerName):
        self.bindEvent("<Destroy>", func, handlerName)


class Attribute(object):
    def __init__(self):
        super(Attribute, self).__init__()
        self.Class = None

    def getWidth(self):
        return self.Class.winfo_width()

    def getHeight(self):
        return self.Class.winfo_height()

    def getX(self):
        return self.Class.winfo_x()

    def getY(self):
        return self.Class.winfo_y()

    def getId(self):
        return self.Class.winfo_id()

    def getHwnd(self):
        try:
            from ctypes import windll
        except AttributeError:
            return 0
        else:
            return windll.user32.GetParent(self.getId())


class Widget(WidgetEvent, EventHandler, Attribute):
    def __init__(self):
        try:
            super(Widget, self).__init__()
            from tkinter import Widget
            self.Class = Widget()
        except UnboundLocalError:
            pass
        self.events = {}

    def bell(self):
        self.Class.bell()

    def getRGB(self, red: int, green: int, blue: int):
        from ctypes.wintypes import RGB
        return RGB(red, green, blue)

    def getHex(self, hex: int):
        from PIL import ImageColor
        return ImageColor.getcolor(hex, "RGB")

    def configure(self, name, var):
        eval(f"self.Class.configure({name}={var})")

    def destroy(self):
        self.Class.destroy()

    def upDate(self):
        self.Class.update()

    def setBackground(self, color):
        self.configure("background", f"'{color}'")

    def getBackground(self):
        return self.Class.cget("background")

    def setForeground(self, color):
        try:
            self.configure("foreground", f"'{color}'")
        except TclError:
            Error("This property does not support this component")

    def getForeground(self):
        return self.Class.cget("foreground")

    def setPos(self, x: int or float, y: int or float):
        self.Class.place(x=x, y=y)

    def setSize(self, width: int or float, height: int or float):
        self.Class.place(width=width, height=height)


class Window(Widget):
    __name__ = "tkile.Window"

    def __init__(self):
        super(Window, self).__init__()
        try:
            from tkdev4 import DevWindow
            self.Class = DevWindow()
        except NameError:
            from tkinter import Tk
            self.Class = Tk()
        try:
            from tkdev4 import DevManage
            self.Manage = DevManage(self.Class)
        except NameError:
            pass
        self.theme = Light
        self.usemica = False
        self.useacrylic = False
        self.windowInit()

    def windowInit(self):
        from src.tkile.Icons import getIconPath
        self.setIcon(getIconPath())
        self.setTitle("tkile")
        self.setCaptionStyle(Auto)

    def setMaximizeBox(self):
        self.Manage.add_window_maximizebox()

    def setMinimizeBox(self):
        self.Manage.add_window_minimizebox()

    def setBorder(self, border):
        from sys import platform, getwindowsversion
        if platform == "win32" and getwindowsversion().build >= 22621:
            if border == Default:
                try:
                    self.Manage.dwm_set_window_round_default()
                except AttributeError:
                    pass
            elif border == Round:
                try:
                    self.Manage.dwm_set_window_round_round()
                except AttributeError:
                    pass
            elif border == RoundSmall:
                try:
                    self.Manage.dwm_set_window_round_round_small()
                except AttributeError:
                    pass
            elif border == RoundNone:
                try:
                    self.Manage.dwm_set_window_round_donot_round()
                except AttributeError:
                    pass

    def setSize(self, width: int, height: int):
        self.Class.geometry(f"{width}x{height}")

    def getSize(self):
        return self.getWidth(), self.getHeight()

    def setPos(self, x: int, y: int):
        self.Class.geometry(f"+{x}+{y}")

    def getPos(self):
        return self.getX(), self.getY()

    def setTitle(self, title: str):
        self.Class.title(title)

    def getTitle(self):
        return self.Class.title

    def setTheme(self, theme: str):
        from sys import platform, getwindowsversion
        if platform == "win32" and getwindowsversion().build >= 22000:
            if theme == "auto":
                from darkdetect import isDark, isLight
                if isLight():
                    try:
                        self.Manage.dwm_set_window_attribute_use_light_mode()
                    except AttributeError:
                        pass
                    else:
                        self.theme = Light
                        self.Class.configure(background="#ffffff")
                elif isDark():
                    try:
                        self.Manage.dwm_set_window_attribute_use_dark_mode()
                    except AttributeError:
                        pass
                    else:
                        self.theme = Dark
                        self.Class.configure(background="#111317")
            elif theme == "light":
                try:
                    self.Manage.dwm_set_window_attribute_use_light_mode()
                except AttributeError:
                    pass
                else:
                    self.theme = Light
                    self.Class.configure(background="#ffffff")
            elif theme == "dark":
                try:
                    self.Manage.dwm_set_window_attribute_use_dark_mode()
                except AttributeError:
                    pass
                else:
                    self.theme = Dark
                    self.Class.configure(background="#111317")

    def getTheme(self):
        return self.theme

    def setIcon(self, path):
        self.Class.iconbitmap(path)

    def getIcon(self):
        return self.Class.iconbitmap

    def setCaptionStyle(self, style):
        from sys import platform, getwindowsversion
        if platform == "win32" and getwindowsversion().build >= 22621:
            if self == Auto:
                try:
                    self.Manage.dwm_set_window_attribute_systembackdrop_type_auto()
                except AttributeError:
                    pass
            elif style is None:
                try:
                    self.Manage.dwm_set_window_attribute_systembackdrop_type_none()
                except AttributeError:
                    pass
            elif style == MainWindow:
                try:
                    self.Manage.dwm_set_window_attribute_systembackdrop_type_mainwindow()
                except AttributeError:
                    pass
            elif style == TabbedWindow:
                try:
                    self.Manage.dwm_set_window_attribute_systembackdrop_type_tabbed_window()
                except AttributeError:
                    pass
            elif style == TransientWindow:
                try:
                    self.Manage.dwm_set_window_attribute_systembackdrop_type_transient_window()
                except AttributeError:
                    pass

    def setSysMenu(self):
        self.Manage.add_window_sysmenu()

    @singledispatch
    def setTitleColor(self, red: int, green: int, blue: int):
        self.Manage.dwm_set_window_attribute_text_color(self.getRGB(red, green, blue))

    @setTitleColor.register
    def setTitleColor(self, hex: str):
        Hex = self.getHex(hex)
        self.Manage.dwm_set_window_attribute_text_color(self.getRGB(Hex[0], Hex[1], Hex[2]))

    @singledispatch
    def setCaptionColor(self, red: int, green: int, blue: int):
        self.Manage.dwm_set_window_attribute_caption_color(self.getRGB(red, green, blue))

    @setCaptionColor.register
    def setCaptionColor(self, hex: str):
        Hex = self.getHex(hex)
        self.Manage.dwm_set_window_attribute_caption_color(self.getRGB(Hex[0], Hex[1], Hex[2]))

    @singledispatch
    def setBorderColor(self, red: int, green: int, blue: int):
        self.Manage.dwm_set_window_attribute_border_color(self.getRGB(red, green, blue))

    @setBorderColor.register
    def setBorderColor(self, hex: str):
        Hex = self.getHex(hex)
        self.Manage.dwm_set_window_attribute_border_color(self.getRGB(Hex[0], Hex[1], Hex[2]))

    def useMica(self, theme=Auto):
        from sys import platform, getwindowsversion
        if platform == "win32" and getwindowsversion().build >= 22600:
            if theme == Auto:
                try:
                    self.Manage.use_mica_mode_auto()
                except AttributeError:
                    pass
                else:
                    self.usemica = True
            if theme == Light:
                try:
                    self.Manage.use_mica_mode_light()
                except AttributeError:
                    pass
                else:
                    self.usemica = True
            elif theme == Dark:
                try:
                    self.Manage.use_mica_mode_dark()
                except AttributeError:
                    pass
                else:
                    self.usemica = True

    def isUseMica(self):
        return self.usemica

    def useHighDPI(self):
        self.Manage.high_dpi()

    def useAcrylic(self, theme=Auto):
        if theme == Auto:
            try:
                self.Manage.use_acrylic_mode_auto()
            except AttributeError:
                pass
            else:
                self.useacrylic = True
        if theme == Light:
            try:
                self.Manage.use_acrylic_mode_light()
            except AttributeError:
                pass
            else:
                self.useacrylic = True
        elif theme == Dark:
            try:
                self.Manage.use_acrylic_mode_dark()
            except AttributeError:
                pass
            else:
                self.useacrylic = True

    def isUseAcrylic(self):
        return self.useacrylic

    def center(self):
        try:
            self.Manage.set_window_pos_center()
        except AttributeError:
            pass


class Button(Widget):
    def __init__(self, parent, text: str = "", onClick=Empty):
        super(Button, self).__init__()
        import tkinter
        self.Class = tkinter.Button(parent.Class, command=onClick, text=text)

        self.parent = parent

        self.buttonInit()

    def setRelief(self, relief):
        self.configure("relief", f"'{relief}'")

    def setBorder(self, width):
        self.configure("border", f"{width}")

    def buttonInit(self):
        self.setBackground("#fcfcfc")
        self.setRelief("ridge")
        self.setBorder(1)


if __name__ == '__main__':
    from ctypes.wintypes import RGB

    Application = Application()
    Window = Window()
    Button = Button(Window, text="Hello")
    Button.setPos(10, 10)
    Application.Run(Window)
