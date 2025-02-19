#!/usr/bin/env python3
'''
Guide for usage:
In your terminal, run the command:

python download_gdrive.py GoogleFileID /path/for/this/file/to/download/file.type

Credited to 
https://stackoverflow.com/questions/25010369/wget-curl-large-file-from-google-drive
author: https://stackoverflow.com/users/1475331/user115202
'''

import requests

def download_file_from_google_drive(id, destination):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    


if __name__ == "__main__":
    from sys import argv
    if len(argv) is not 3:
        print(f"[+] Usage: {argv[0]} drive_file_id destination_file_path")
    else:
        # TAKE ID FROM SHAREABLE LINK
        file_id = argv[1]
        # DESTINATION FILE ON YOUR DISK
        destination = argv[2]
        download_file_from_google_drive(file_id, destination)
