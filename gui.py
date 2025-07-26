import tkinter as tk
from tkinter.ttk import Frame, Label, Button, Combobox, Entry
import sqlite3
from tools import markdown as md, update as up

class gui(tk.Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
    
        self.con = sqlite3.connect("./database.db",autocommit=True)
        self.cur = self.con.cursor()
        self.md_list:list[md.MD_Object] = []
        
        self.mainframe:Frame = Frame(self,padding=10)
        self.geometry("800x500")
        self.resizable(False, False)
        self.mainframe.grid()
        
        self.setup()

        self.cuisine_ingredients() # must end by this
    
    def setup(self) -> None:
        self.menubar = tk.Menu(self)
        self.menubar.add_command(label="Acceuil", command=self.menu_main)

        self.menubar_cuisine = tk.Menu(self.menubar)
        self.menubar_cuisine.add_command(label="Ajouter plat", command=self.cuisine_ajouter)
        self.menubar_cuisine.add_command(label="Creer plat", command=self.cuisine_creer)
        self.menubar_cuisine.add_command(label="Ajouter ingredients", command=self.cuisine_ingredients)
        self.menubar.add_cascade(label="Cuisine", menu=self.menubar_cuisine)
        
        
        self.menubar.add_command(label="Courses", command=self.menu_courses)
        self.menubar.add_command(label="Code source et aides", command=self.menu_aide)
        
        self.config(menu=self.menubar)
        
    def clear_frame(self) -> None:
        for children in self.mainframe.winfo_children():
            children.destroy()
        
    def menu_main(self) -> None:
        self.clear_frame()
        Label(self.mainframe,text="Application du Domaine de Malet").grid(column=0, row=0)
        self.mainframe.grid()
    
    def cuisine_ajouter(self) -> None:
        self.clear_frame()
        self.cuisine:list[tuple[int, int, int]] = []
        
        self.cuisine_ajouter_codes_plats = tk.StringVar()
        
        Combobox(
            self.mainframe, 
            state="readonly",
            values=self.cur.execute(
                f"SELECT DISTINCT code FROM menu_codes;"
                ).fetchall(),
            textvariable=self.cuisine_ajouter_codes_plats,
        ).grid(
            column=0, row=0, ipadx=10
        )
        
        self.mainframe.grid_slaves(0,0)[0].bind('<<ComboboxSelected>>',self.ajouter_update_plates)

        Combobox(
            self.mainframe,
            state="disabled",
            values=[]
        ).grid(
            column=1, row=0, ipadx=40
        )
                
        Button(
            self.mainframe,
            text="Ajouter plat",
            command=self.add_new_plate
        ).grid(
            column=6, row=0
        )
        
        Button(
            self.mainframe, 
            text="Générer Markdown",
            command=lambda:md.print_Markdown(self.md_list)
        ).grid(
            column=0, row=1
        )
            
    def ajouter_update_plates(self,event:tk.Event) -> None:
        sql = self.cur.execute(
                f"SELECT DISTINCT P.name FROM plats P JOIN menu_codes C ON C.ID_menu_code = P.code_menu WHERE C.code = '{self.cuisine_ajouter_codes_plats.get()}';"
            ).fetchall()
        if(sql):
            self.mainframe.grid_slaves(0,1)[0]["state"] = 'readonly'
            self.mainframe.grid_slaves(0,1)[0]["values"] = [x[0] for x in sql]
        else:
            self.mainframe.grid_slaves(0,1)[0]["state"] = 'disabled'
            self.mainframe.grid_slaves(0,1)[0]["values"] = []
    
    def cuisine_creer(self) -> None:
        self.clear_frame()
        
        self.cuisine_creer_code_plat = tk.StringVar()
        
        Combobox(
            self.mainframe, 
            state="readonly",
            values=self.cur.execute(
                f"SELECT DISTINCT code FROM menu_codes;"
                ).fetchall(),
            textvariable=self.cuisine_creer_code_plat,
        ).grid(
            column=0, row=0, ipadx=10
        )
        
        self.mainframe.grid_slaves(0,0)[0].bind('<<ComboboxSelected>>',self.creer_update_plates)
        
        Entry(
            self.mainframe,
            state='disabled',
            validate='focusout'
        ).grid(
            column=1, row=0, ipadx=30
        )
        
    def creer_update_plates(self, event:tk.Event) -> None:
        pass
    
    def cuisine_ingredients(self) -> None:
        self.clear_frame()
        
        cuisine_ingredients_name = tk.StringVar()
        cuisine_ingredients_value_1 = tk.StringVar()
        cuisine_ingredients_value_2 = tk.StringVar()
        
        Entry(
            self.mainframe,
            textvariable=cuisine_ingredients_name,
        ).grid(
            column=0, row=1, ipadx=10
        )
        
        Entry(
            self.mainframe,
            textvariable=tk.StringVar(self.mainframe,value="Ingrédient")
        ).grid(
            column=1, row=1, ipadx=10
        )
        
        Entry(
            self.mainframe
        )
        
        Button(
            self.mainframe,
            text="Ajouter ingrédient à la BD",
            command=lambda:self.cur.execute(f"insert into META_Ingredients(name,cook_unit,buying_unit,fournisseur) values({cuisine_ingredients_name.get()},{cuisine_ingredients_value_1.get()},{cuisine_ingredients_value_2.get()},{""})")
        ).grid(
            column=0, row=2, ipadx=40
        )
        
        
        
        self.mainframe.grid_slaves(1,0)[0].bind('<<ComboboxSelected>>',self.ingredients_update_plates)
    
    def ingredients_update_plates(self, event:tk.Event) -> None:
        pass
    
    def add_new_plate(self) -> None:
        pass
    
    def menu_courses(self) -> None:
        self.clear_frame()
        
    
    def menu_aide(self) -> None:
        up.goto_repo()