"""Main module."""

from tkinter import Tk

from academic.project.views.pages import Application

root = Tk()
Application(root)
root.mainloop()
