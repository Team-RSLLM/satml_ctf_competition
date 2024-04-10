# Competition Attack Script

import requests
import argparse
from termcolor import colored

# The base URL for the API
BASE_URL = "https://ctf.spylab.ai/api/v1"

def create_attack_chat(submission_id: str, ctf_api_key: str, evaluation: bool = False):
    endpoint = f"{BASE_URL}/chat/attack/create"
    headers = {"accept": "application/json", "X-API-Key": ctf_api_key, "Content-Type": "application/json"}
    payload = {"submission_id": submission_id, "evaluation": evaluation}
    response = requests.post(endpoint, json=payload, headers=headers)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
        raise e
    return response.json()


def get_remaining_guesses(secret_id: str, ctf_api_key: str):
    endpoint = f"{BASE_URL}/secret/{secret_id}/remaining_guesses"
    headers = {"accept": "application/json", "X-API-Key": ctf_api_key, "Content-Type": "application/json"}
    response = requests.get(endpoint, headers=headers)
    return response.json()

    
def new_message(chat_id: str, message: str, ctf_api_key: str, api_keys: dict = None):
    endpoint = f"{BASE_URL}/chat/attack/{chat_id}/new_message"
    headers = {"accept": "application/json", "X-API-Key": ctf_api_key, "Content-Type": "application/json"}
    payload = {"new_message": message}
    if api_keys:
        payload["api_keys"] = api_keys
    response = requests.post(endpoint, headers=headers, json=payload)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # print(e)
        raise e
    return response.json()


def guess_secret(secret_id: str, chat_id: str, guess: str, ctf_api_key: str):
    endpoint = f"{BASE_URL}/secret/{secret_id}/guess?guess={guess}"
    payload = {"chat_id": chat_id, "guess": guess}
    headers = {"accept": "application/json", "X-API-Key": ctf_api_key, "Content-Type": "application/json"}
    response = requests.post(endpoint, headers=headers, json=payload)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if not e.response.status_code == 403:
            print(e)
            raise e
        else:
            print("Guesses exhausted")
    return response.json()


def main():
    parser = argparse.ArgumentParser(description='Attack a defense.')
    parser.add_argument('--api_key', required=True, help='Your actual CTF API key')
    parser.add_argument('--defense_id', required=True, help='ID of the defense you want to attack')
    parser.add_argument('--evaluate', required=False, default=False, type=bool, help='Set evaluation to true')
    parser.add_argument('--chat_id', required=False, default=None, help='ID of the chat to resume')
    args = parser.parse_args()

    while True:
        chat_info = create_attack_chat(submission_id=args.defense_id, ctf_api_key=args.api_key, evaluation=args.evaluate)

        print("\n")
        print("-" * 50)
        for key, value in chat_info.items():
            print(f"{key}: {value}")
        print("Evaluation: ", args.evaluate)
        print("-" * 50)
        print("\n")

        while True:
            while True:
                message = input(colored("Enter your message: ", 'blue'))
                print(colored("Message: ", "blue"), colored(message, "green"))
                confirm = input("Is the message correct? (yes/no): ")
                if confirm.lower() == 'yes':
                    break
            print("\n")
            print("-" * 50)
            print("Sending message...")
            print("-" * 50)
            for i in range(10):
                try:
                    response = new_message(chat_id=chat_info["chat_id"], message=message, ctf_api_key=args.api_key)
                    break
                except requests.exceptions.HTTPError as e:
                    print(e)
                    print("Retrying...")
                    continue

            print(colored('Model:', 'blue'), colored(response['model'], 'green'))
            print(colored('Submission ID:', 'blue'), colored(response['submission_id'], 'green'))
            print(colored('History:', 'blue'))
            for i, item in enumerate(response['history']):
                print(colored(f"Message {i+1}:", 'yellow'))
                print(colored('Role:', 'blue'), colored(item['role'], 'green'))
                print(colored('Content:', 'blue'), colored(item['content'], 'white'))
                print(colored('Timestamp:', 'blue'), colored(item['timestamp'], 'green'))

            while True:
                print("-" * 50)
                print("Remaining guesses: ", get_remaining_guesses(secret_id=chat_info["secret_id"], ctf_api_key=args.api_key))
                print("-" * 50)
                guess = input(colored("Do you want to guess the secret? (yes/no): ", 'blue'))
                if guess.lower() == 'yes':
                    guess_value = input("Enter your guess: ")
                    guess_response = guess_secret(secret_id=chat_info["secret_id"], chat_id=chat_info["chat_id"], guess=guess_value, ctf_api_key=args.api_key)
                    print(colored('Guess Response:', 'blue'))
                    print(colored('Correct:', 'blue'), colored(guess_response['correct'], 'green' if guess_response['correct'] else 'red'))
                    print(colored('Guesses Remaining:', 'blue'), colored(guess_response['guesses_remaining'], 'green'))
                    if guess_response['correct']:
                        print(colored('Congratulations! Your guess is correct!', 'green'))
                        exit()
                else:
                    break

            new_chat = input("Do you want to start a new chat? (yes/no): ")
            if new_chat.lower() != 'yes':
                break

            finish = input("Do you want to finish the chat? (yes/no): ")
            if finish.lower() == 'yes':
                print("Chat ID: ", chat_info["chat_id"])
                print("Remaining guesses: ", get_remaining_guesses(secret_id=chat_info["secret_id"], ctf_api_key=args.api_key))
                exit()

        print(get_remaining_guesses(secret_id=chat_info["secret_id"], ctf_api_key=args.api_key))


if __name__ == "__main__":
    main()