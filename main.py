import os.path
import requests

DOWNLOAD_PATH = "/home/caio/documents/software-engineering/books/"
SUBJECTS_URL = "https://studeoapi.unicesumar.edu.br/ambiente-api-controller/api/aluno/disciplina"
SUBJECT_URL = "https://studeoapi.unicesumar.edu.br/objeto-ensino-api-controller/api/material-estudo/"
SUBJECT_FILE_URL = "https://conteudoava.unicesumar.edu.br/download/apostila/"
AUTH_TOKEN = "YOUR_AWESOME_AUTH_TOKEN"
FILE_TOKEN = "YOUR_AWESOME_FILE_TOKEN"

HEADERS = {
    "Accept": "application/json; text/plain; */*",
    "Authorization": AUTH_TOKEN}

subjects = requests.get(SUBJECTS_URL, headers=HEADERS).json()

for subject in subjects:
    if subject['flCurricular']:
        subject_code = subject['cdShortname']
        subject_name = subject['nmDisciplina']
        subject_year = subject['ano']
        subject_semester = subject['semestre']

        subject_data = requests.get(SUBJECT_URL + subject_code, headers=HEADERS).json()

        if subject_data:
            file_hash = subject_data[0]['nomeArquivoHash']
            full_file_name = f'{DOWNLOAD_PATH}{subject_name} {subject_year}-{subject_semester}.pdf'

            if not os.path.exists(full_file_name):
                with open(full_file_name, 'wb') as file:
                    print("Downloading:", full_file_name)
                    response = requests.get(f'{SUBJECT_FILE_URL}{file_hash}/{FILE_TOKEN}', headers=HEADERS)
                    file.write(response.content)
