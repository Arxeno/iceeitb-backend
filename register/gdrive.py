from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def configure_pydrive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    return drive


drive = configure_pydrive()
