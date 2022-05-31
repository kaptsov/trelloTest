import requests
import json
from dotenv import load_dotenv
import os
from os.path import join, dirname

'''
Свои ключи генерируются тут:
https://trello.com/app-key
'''


def main():
    teams = (

    {
        'pm': 'Толстоногов Алексей',
        'pm_color': 'green',
        'student1': 'Толсторуков Максим',
        'student2': 'Толстолапов Александр',
        'student3': 'Толстосуева Олеся',
        'call_time': '20:30',
    },
    {
        'pm':'Кривоногов Алексей',
        'pm_color':'purple',
        'student1':'Криворуков Максим',
        'student2':'Косолапов Александр',
        'student3':'Мимосуева Олеся',
        'call_time':'19:30',
    },
    {
        'pm': 'Сухоногов Алексей',
        'pm_color': 'lime',
        'student1': 'Сухоруков Максим',
        'student2': 'Сухолапов Александр',
        'student3': 'Сухосуева Олеся',
        'call_time': '20:00',
    },
    )

    create_trello(teams=teams, project_name='Test API', project_start_date='01.11.2011', project_end_date='03.03.2023')


def create_trello(teams, project_name, project_start_date, project_end_date):

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    API_KEY = os.environ.get("API_KEY")
    TOKEN = os.environ.get("TOKEN")

    project_full_name = f'Проект {project_name}, [{project_start_date}-{project_end_date}]'

    url = "https://api.trello.com/1/organizations"

    headers = {
        "Accept": "application/json"
    }

    query = {
        'displayName': project_full_name,
        'key': API_KEY,
        'token': TOKEN
    }

    response = requests.request(
        "POST",
        url,
        headers=headers,
        params=query
    )

    org = json.loads(response.text)
    print(org)

    for team in teams:

        board_name=f'{team["call_time"]} - {team["student1"]}, {team["student2"]}, {team["student3"]}'

        url = "https://api.trello.com/1/boards/"

        query = {
            'name': board_name,
            'key': API_KEY,
            'token': TOKEN,
            'idOrganization':org['id'],
            'prefs_background':team['pm_color'],
            'desc':f'PM команды: {team["pm"]}',
            'prefs_permissionLevel':'private',

        }

        response = requests.request(
            "POST",
            url,
            params=query
        )

        board = json.loads(response.text)
        print(board['url'])

        url = f"https://api.trello.com/1/boards/{board['id']}"

        query = {
            'key': API_KEY,
            'token': TOKEN,
            'closed':'false'
        }

        response = requests.request(
            "PUT",
            url,
            params=query
        )

    return True


if __name__ == '__main__':
    main()
