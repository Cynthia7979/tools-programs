# https://stackoverflow.com/questions/4055267/tkinter-mouse-drag-a-window-without-borders-eg-overridedirect1
# https://stackoverflow.com/questions/19080499/transparent-background-in-a-tkinter-window
import tkinter as tk


TEXT_COLOR = 'white'
TRANSPARENT_COLOR = ('black', 'white')[TEXT_COLOR == 'black']
BORDER_COLOR = 'red'
ALPHA = 0.3

FONT_NAME = 'Microsoft YaHei'
FONT_SIZE = 36
TEXT = '你好世界！'


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.floater = FloatingWindow(self)
        self.withdraw()


class FloatingWindow(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.overrideredirect(True)
        self.x = 0
        self.y = 0

        self.label = tk.Label(self, text=TEXT, font=(FONT_NAME, FONT_SIZE), background=TRANSPARENT_COLOR,
                              foreground=TEXT_COLOR,)
        self.label_border = tk.Label(self, text=TEXT, font=(FONT_NAME, FONT_SIZE+10), background=TRANSPARENT_COLOR,
                              foreground=BORDER_COLOR,)
        # self.grip = tk.Label(self, bitmap="gray25")
        # self.grip.pack(side="left", fill="y")

        self.label.pack()

        self.lift()
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-transparentcolor", TRANSPARENT_COLOR)
        self.wm_attributes('-alpha', ALPHA)

        self.label.bind("<ButtonPress-1>", self.start_move)
        self.label.bind("<ButtonRelease-1>", self.stop_move)
        self.label.bind("<B1-Motion>", self.do_move)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")


class FloatingWindow(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.overrideredirect(True)
        self.x = 0
        self.y = 0

        self.canvas = tk.Canvas(self, bg=TRANSPARENT_COLOR, bd=1)
        self.canvas.create_text(100, 100, font=(FONT_NAME, FONT_SIZE+2), text=TEXT, fill=BORDER_COLOR)
        self.canvas.create_text(100, 100, font=(FONT_NAME, FONT_SIZE), text=TEXT, fill=TEXT_COLOR)
        self.canvas.pack()

        self.lift()
        self.wm_attributes("-topmost", True)
        self.wm_attributes("-transparentcolor", TRANSPARENT_COLOR)
        self.wm_attributes('-alpha', ALPHA)

        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<ButtonRelease-1>", self.stop_move)
        self.canvas.bind("<B1-Motion>", self.do_move)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

app = App()
app.floater.mainloop()
