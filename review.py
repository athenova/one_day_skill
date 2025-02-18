import os
import telebot
import json
import requests
import glob

from datetime import date
from datetime import timedelta
from openai import OpenAI
from PIL import Image

BOT_TOKEN_NAME = "ATHE_BOT_TOKEN"
BOT_TOKEN = os.environ.get(BOT_TOKEN_NAME)
CHAT_ID = -1002374309134
AI_TEXT_MODEL = 'chatgpt-4o-latest'
AI_IMAGE_MODEL = 'dall-e-3'

check_date = date.today() + timedelta(days=1)

tasks = json.load(open('files/in_progress.json', 'rt', encoding='UTF-8'))

for i, task in enumerate(tasks):
    if task["date"] == check_date.strftime('%Y-%m-%d'):
        folder_name = glob.escape(f"files/data/{task['group'].replace('/', ',')}")
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        folder_name = glob.escape(f"{folder_name}/{task['name'].replace('/', ',')}")
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        text_file_name = f"{folder_name}/text.txt"
        temp_image_file = f"{folder_name}/image.webp"
        image_file_name = f"{folder_name}/image.png"

        client = OpenAI()
        if not os.path.exists(text_file_name):
            text_prompt = task["text_prompt"]
            text = client.chat.completions.create(
                        model=AI_TEXT_MODEL,
                        messages=[
                            { "role": "system", "content": f"Ты - блогер с 1000000 миллионном подписчиков" },
                            { "role": "user", "content": text_prompt },
                        ]
                    ).choices[0].message.content
            open(text_file_name, 'wt', encoding="UTF-8").write(text)

        if not os.path.exists(temp_image_file):
            image_prompt = task["image_prompt"]
            image_url = client.images.generate(
                model=AI_IMAGE_MODEL,
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            ).data[0].url
            response = requests.get(image_url)
            with open(temp_image_file, 'wb') as f:
                f.write(response.content)
            
        if os.path.exists(temp_image_file) and not os.path.exists(image_file_name):
            webp_image = Image.open(temp_image_file)
            png_image = webp_image.convert("RGBA")
            png_image.save(image_file_name)
            
        bot = telebot.TeleBot(BOT_TOKEN)
        if os.path.exists(image_file_name):
            bot.send_photo(chat_id=CHAT_ID, photo=open(image_file_name, 'rb'), parse_mode="Markdown")

        if os.path.exists(text_file_name):
            bot.send_message(chat_id=CHAT_ID, text=open(text_file_name, 'rt', encoding='UTF-8').read(), parse_mode="Markdown")