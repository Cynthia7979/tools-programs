import Tkinter
root = Tkinter.Tk()
label = Tkinter.Label(root, text='0')
def count():
    t = label['text']
    label['text'] = str(int(t) + 1)
	
button = Tkinter.Button(root, text='click me!', command=count)
label.pack()
button.pack()
root.mainloop()
