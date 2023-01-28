import requests
import jsonlines
import json

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}


def run_requests(request_file : str):
    with jsonlines.open('data/requests.json') as reader:
        for register in reader:
            response = requests.post('http://0.0.0.0:80/predict',data=json.dumps(register),headers=headers)
            print(response.status_code)


if __name__ == '__main__':
    run_requests('data/requests.json')