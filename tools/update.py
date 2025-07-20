import requests
import json
import git


UPDATE_API:str = r"https://api.github.com/repos/AltarCrossorm/DomaineDeMalet_PyApp/releases"

__id:int = 0

def is_up_to_date() -> bool:
    """checks online if the version got updated

    :returns True: if the version is up to date, False otherwise
    """
    data:str = requests.get(UPDATE_API).text
    id:int = json.loads(data)[0]['id'] # collects the id of the latest release
    
    with open("./version.txt",'r') as ver:
        if ver.read() != str(id):
            global __id
            __id = id
            return False
        else:
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


update_version(new_ver=0x0001)