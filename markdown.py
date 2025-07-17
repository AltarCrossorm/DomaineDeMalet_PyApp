"""Markdown types
uses a simple inheritance system from a PyObject to a MDObject
"""

class MD_Object:

    def __init__(self,
                 content:str = ""
                ) -> None:
        """MD_Object class
        Is the default object who can provide a wide range of capabilites

        Args:
            content (str, optional): the description of the object, may vary from time to time. Defaults to "".
        """
        self.content = content
        
    def __str__(self) -> str:
        return f"<neutral MD object with content \"{self.content}\">"
    
    
class MD_header(MD_Object):
    def __init__(self,
                 content: str = "",
                 header_level:int = 1
                ) -> None:
        super().__init__(content)
        
        if not header_level and header_level <6:
            self.header_level = header_level
        else:
            self.header_level = 6
            
    def __str__(self) -> str:
        return f"{"#"*self.header_level} {self.content}"
    
    
class MD_codeblock(MD_Object):
    def __init__(self,
                 content: str = "",
                 code_highlight:str = "py"
                ) -> None:
        super().__init__(content)
        
        self.highlighting = code_highlight
    
    def __str__(self) -> str:
        return \
        f"""
        ```{self.highlighting}
        {self.content}
        ```
        """


class MD_hyperlink(MD_Object):
    def __init__(self,
                 content: str = "",
                 link:str = ""
                ) -> None:
        super().__init__(content)
        self.hyperlink = link
        
    def __str__(self) -> str:
        return f"[{self.content}]({self.hyperlink})"


class MD_image(MD_hyperlink):
    def __init__(self,
                 content: str = "",
                 link: str = ""
                ) -> None:
        super().__init__(content, link)
    
    def __str__(self) -> str:
        return f"!{super().__str__()}"


class MD_separator(MD_Object):
    def __init__(self,
                 content: str = ""
                ) -> None:
        super().__init__(content)
        
    def __str__(self) -> str:
        return "---"
    
class MD_text(MD_Object):
    def __init__(self,
                 content: str = ""
                ) -> None:
        super().__init__(content)
        
    def __str__(self) -> str:
        return self.content
    
    
class MD_italic(MD_text):
    def __init__(self,
                 content: str = ""
                ) -> None:
        super().__init__(content)
        
    def __str__(self) -> str:
        return f"_{super().__str__()}_"
    

class MD_bold(MD_text):
    def __init__(self,
                 content: str = ""
                ) -> None:
        super().__init__(content)
        
    def __str__(self) -> str:
        return f"**{super().__str__()}**"


class MD_codeline(MD_text):
    def __init__(self, 
                 content: str = ""
                ) -> None:
        super().__init__(content)
        
    def __str__(self) -> str:
        return f"``{super().__str__()}``"

NEUTRAL:str = "-"
LEFT:str = ":-"
CENTER:str = ":-:"
RIGHT:str = "-:"

class MD_table_column(MD_Object):
    def __init__(self,*,
                 content: str = "",
                 values:list[MD_Object],
                 direction:str = NEUTRAL
                ) -> None:
        super().__init__(content)
        
        self.__values = values
        self.__direction = direction
        
    def __str__(self) -> str:
        return self.content # title of the column
    
    def __len__(self) -> int:
        return len(self.__values)
    
    def get_value(self, index:int = 0) -> MD_Object:
        if index < 0 or index >= len(self.__values):
            raise ValueError("wrong value enterd")
        return self.__values[index]
    
    def get_direction(self) -> str:
        return self.__direction
        
    
class MD_table(MD_Object):
    def __init__(self,*,
                 content: str = "",
                 column_list:list[MD_table_column]
                ) -> None:
        super().__init__(content)
        self.column_list = column_list
        
        
    def __str__(self) -> str:
        return \
        f"""
        |{'|'.join(str(self.column_list[i]) for i in range(len(self.column_list)))}|
        |{'|'.join(str(self.column_list[i].get_direction()) for i in range(len(self.column_list)))}|
        {'\n'.join(f"|{'|'.join(self.column_list[i].get_value(j).__str__() for i in range(len(self.column_list)))}|" for j in range(self.column_list[0].__len__()))}
        """
        


def MD_fuse(first:list[MD_Object], second:list[MD_Object]) -> list[MD_Object]:
    return first + second

def MD_Generate(final:list[MD_Object]) -> str:
    ret:str = ""
    for objects in final:
        ret += f"{objects}\n\n"
    return ret

def MD_fSpace() -> str:
    return "&nbsp;"