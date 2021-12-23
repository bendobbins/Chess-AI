from tkinter import *

# Create window
window = Tk()
window.title("Upgrade")
window.geometry("125x100+10+20")

def get_upgrade(piece):
    window.destroy()
    return piece

def upgrade():
    piece = IntVar()
    Radiobutton(window, text="Queen", value=0, variable=piece, command=lambda:get_upgrade(piece.get())).pack(anchor=W)
    Radiobutton(window, text="Rook", value=1, variable=piece, command=lambda:get_upgrade(piece.get())).pack(anchor=W)
    Radiobutton(window, text="Bishop", value=2, variable=piece, command=lambda:get_upgrade(piece.get())).pack(anchor=W)
    Radiobutton(window, text="Knight", value=3, variable=piece, command=lambda:get_upgrade(piece.get())).pack(anchor=W)
    window.mainloop()


def main():
    upgrade()


if __name__ == "__main__":
    main()