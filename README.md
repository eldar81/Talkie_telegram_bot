# Talkie – communication trainer telegram bot
There are hundreds of thousands of people around the world with social anxiety and difficulties in handling social situations. I did this project to help people practice their communication skills in a safe and comfortable environment.

*Note: this project was done for a Russian audience, so all messages in the bot are written in Cyrillic. However, all notes and comments in the code are in English.*

![image](https://user-images.githubusercontent.com/88551054/196945000-11a31071-314d-4cf1-a4a4-62294705bbcd.png)

## Idea
I created a Takie telegram bot to help people practice their communication skills. 

After a short questionnaire, you will be offered to learn a little bit about how communication works. For this purpose, I created a website and posted articles on the topic. The site no longer exists because the project is frozen. But I did a [few screenshots](https://drive.google.com/drive/folders/1UiNLm9lwTIG04UrI05R_vW0fhDo5Ue3M?usp=sharing) to show you the idea.

When you read the theory and get some advice bot will offer you to arrange a meeting with another user of the bot to practice your skills in an online meeting with some interesting tasks. And that is the key: you practice your communication skills in a safe environment with a person who is also interested in the topic and do some tasks created by the psychologist supervisor.

## Implementation
To create the bot I used the aiogram library - asynchronous Telegram API library written over asyncio.

To store the data I used SQLite database and SQLite3 python library (note: this was my very first python project, so database structure and logic are written very poorly. Now I see it 😅).

## Project structure
**Handlers** All message handlers are stored in /handlers directory. They are divided by bot modules and menus.

**Midlewares** There is only one middleware that helps to run online support chat with the admin of the bot right in the bot interface.

**algorithm.py** There is an algorithm that matches users into pairs every day at 7 p.m. Idea is to first match users with a smaller amount of available matches, then users this lots of matches. So everybody will have a pair.

**app.py** Runs bot, and scheduler and creates a database

**loader.py** Defines the key entities of the bot

**bot_commands.py** Set the user's command for the bot

**config.py** Gets credentials from .env

**keyboards.py** Store all keyboards

**sqkite.py** Code for operating SQLite database

## To sum up
This was my first Python project, I did it a year ago. I got almost 100 users, but only a few of them were active weekly. So I stopped the project for some time. I hope somebody will find this code useful themselves.

Oh, and there is [mindmap of bot's logic](https://miro.com/app/board/o9J_kyNTfhM=/) after the user has a match for a better understanding of the structure (it's in Cyrillic, but).
