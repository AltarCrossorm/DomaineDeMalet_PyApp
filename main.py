from gui import gui


def main() -> int:
    GUI = gui(className=" Domaine de Malet")
    GUI.mainloop()
    
    return 0


if (__name__ == '__main__'):
    main()