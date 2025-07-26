from datetime import datetime as date
import os

def get_date_directory(base_file:str) -> str:
    ret:str = f"{date.today().year}/{date.today().month}/{date.today().day}"
    if not os.path.exists(f"{base_file}/{ret}/"):
        os.makedirs(f"{base_file}/{ret}/")
    return ret

def get_file_hour() -> str:
    ret:str = f"{date.today().hour}_{date.today().minute}_{date.today().second}"
    
    return ret