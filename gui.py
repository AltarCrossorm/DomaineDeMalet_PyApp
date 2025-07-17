import tkinter
from tkinter.ttk import Frame, Label, Button
import sqlite3
import markdown as md
from md2pdf.core import md2pdf # type: ignore
from datetime import datetime

TABLE_EX:md.MD_table = md.MD_table(
    column_list=[md.MD_table_column(content="truc",direction=md.RIGHT,values=[md.MD_text("Machin"),md.MD_text("chose")])]
)
    


class gui(tkinter.Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
    
        self.con = sqlite3.connect("./database.db",autocommit=True)
        self.cur = self.con.cursor()
        self.md_list:list[md.MD_Object] = [TABLE_EX]
        self.mainframe:Frame = Frame(self,padding=10)
        self.mainframe.grid()
        Label(self.mainframe,text="Application du Domaine de Malet").grid(column=0,row=0)
        Button(self.mainframe,text="générer markdown",command=self.print_Markdown).grid(column=0,row=1)
        self.maxsize(1000,1000)
        
    def print_Markdown(self) -> None:
        print(self.md_list)
        if len(self.md_list) == 0:
            self.md_list.append(md.MD_header("<center>blank page</center>",6))
            
        md2pdf(pdf_file_path=f"./pdf/{datetime.today().date()}_DdM_mkdwn.pdf",
               md_content=md.MD_Generate(self.md_list),
               css_file_path="./md_DdM.css",
               base_url="./img")
        print("Document generated")