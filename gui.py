import tkinter as tk
from tkinter.ttk import Frame, Label, Button, Combobox
import sqlite3
import markdown as md
from md2pdf.core import md2pdf # type: ignore
from datetime import datetime
import webbrowser

class gui(tk.Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
    
        self.con = sqlite3.connect("./database.db",autocommit=True)
        self.cur = self.con.cursor()
        self.md_list:list[md.MD_Object] = []
        
        self.mainframe:Frame = Frame(self,padding=10)
        self.geometry("800x500")
        self.mainframe.grid()
        self.menubar = tk.Menu(self)
        self.menubar.add_command(label="Acceuil", command=self.menu_main)
        self.menubar.add_command(label="Cuisine", command=self.menu_cuisine)
        self.menubar.add_command(label="Courses", command=self.menu_courses)
        self.menubar.add_command(label="Code source et aides", command=self.menu_aide)
        
        self.config(menu=self.menubar)

        self.menu_main() # must end by this
        
    def clear_frame(self) -> None:
        for children in self.mainframe.winfo_children():
            children.destroy()
        
    def menu_main(self) -> None:
        self.clear_frame()
        Label(self.mainframe,text="Application du Domaine de Malet").grid(column=0, row=0)
        self.mainframe.grid()
    
     
    def menu_cuisine(self) -> None:
        self.clear_frame()
        self.cuisine = []
        Combobox(
            self.mainframe, 
            values=self.cur.execute(
                f"SELECT DISTINCT type_plat FROM plats"
                ).fetchall()[0]).grid(
                    column=0, row=0
                    )
        Button(
            self.mainframe, 
            text="Générer Markdown",
            command=self.print_Markdown
            ).grid(
                column=0, 
                row=1
                )
    
    def menu_courses(self) -> None:
        self.clear_frame()
    
    def menu_aide(self) -> None:
        webbrowser.open_new("https://github.com/AltarCrossorm/DomaineDeMalet_PyApp")
        
    def print_Markdown(self) -> None:
        print(self.md_list)
        if len(self.md_list) == 0:
            self.md_list.append(md.MD_header("<center>blank page</center>",6))
            
        md2pdf(pdf_file_path=f"./pdf/{datetime.today().date()}_DdM_mkdwn.pdf",
               md_content=md.MD_Generate(self.md_list),
               css_file_path="./md_DdM.css",
               base_url="./img")
        
        print("Document generated")