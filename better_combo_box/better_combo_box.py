from tkinter import Tk, StringVar, OptionMenu, Button
import sys

OPTIONS = sys.argv[1].split("|")

root = Tk()

variable = StringVar(root)
variable.set(OPTIONS[0])  # default value

w = OptionMenu(root, variable, *OPTIONS)
w.pack()


def ok():
    sys.stdout.write(variable.get())
    sys.stdout.flush()
    root.destroy()


button = Button(root, text="OK", command=ok)
button.pack()

root.mainloop()
