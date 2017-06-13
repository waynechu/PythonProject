import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(expand = 0)
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self, text = "Hello World", command = self.say_hi)
#        self.hi_there["text"] = "Hello World\n(click me)"
#        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="left")

        self.quit = tk.Button(self, text = "QUIT", fg = "white", bg = "red", command = root.destroy)
        self.quit.pack(side="right")

    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
