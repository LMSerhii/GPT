import json
import os

from base64 import b64decode

import openai

from dotenv import dotenv_values, load_dotenv

config = {
    **dotenv_values('.env.secret')
}

openai.api_key = config.get('GPT_KEY')


def generate_text(text):
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=text,
        max_tokens=200,
        temperature=0.7,
        n=1,
        stop=None,
        timeout=15
    )
    if response and response.choices:
        return response.choices[0].text.strip()

    return 'Text was not created'


def generate_images(text):
    response = openai.Image.create(
        prompt=text,
        n=1,
        size='256x256',
        response_format='b64_json'
    )

    with open('data.json', 'w') as file:
        json.dump(response, file, indent=4, ensure_ascii=False)

    result = b64decode(response.get('data')[0].get('b64_json'))

    with open(f'output.png', 'wb') as file:
        file.write(result)

    return 'Successfully'


def main():
    text = input()
    print(generate_text(text))
    # print(generate_images(text))
    # print(os.getenv('GPT_KEY'))
    # print(config.get('GPT_KEY'))


if __name__ == '__main__':
    main()
