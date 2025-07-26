import requests
import json
import git
import webbrowser

UPDATE_API:str = r"https://api.github.com/repos/AltarCrossorm/DomaineDeMalet_PyApp/releases"
GITHUB_REPO:str = r"https://github.com/AltarCrossorm/DomaineDeMalet_PyApp"

__id:int = 0

def is_up_to_date() -> bool:
    """checks online if the version got updated

    :returns True: if the version is up to date, False otherwise
    """
    data:str = requests.get(UPDATE_API).text
    id:int = json.loads(data)[0]['id'] # collects the id of the latest release
    
    with open("./version.txt",'r') as ver:
        if ver.read() != str(id):
            __id = id
            return False
        else:
            __id = int(ver.read())
            return True


def update_version(*,new_ver:int) -> bool:
    """updates the version accordingly

    :param int new_ver: the new version to be written

    :returns True: if the version is succesfully updated
    :returns False: if any problem occur
    """
    try:
        with open("./version.txt",'w') as ver:
            ver.write(str(new_ver))
        git.Repo().remote().pull()
        print("git pull [finished]")
    except Exception as e:
        print(e)
        return False
    
    return True

def goto_repo() -> None:
    webbrowser.open_new(GITHUB_REPO)
    
if __name__ == '__main__':
    import subprocess
    import sys
    """Checks and install all the necessary libraries"""
    libs = ['webbrowser','git','md2pdf','tkinter']
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', ])