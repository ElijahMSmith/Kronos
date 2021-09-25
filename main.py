import tkinter as tk
import daily

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.renderView()

    def renderView(self):
        daily.createButtons(self)

root = tk.Tk()
app = Application(master=root)
app.mainloop()