# Talkie – communication trainer telegram bot
There are hundreds of thousands of people around the world with social anxiety and difficulties in handling social situations. I did this project to help people practice their communication skills in safe and comfortable environment.

*Note: this project was done for Russian audience, so all messages in bot are written in Cyrillic. However, all notes and comments in code are in English.*

![image](https://user-images.githubusercontent.com/88551054/196945000-11a31071-314d-4cf1-a4a4-62294705bbcd.png)

## Idea
I created Takie telegram bot to help people practice their communication skills. 

After short questionnaire you will be offered to learn a little bit about how communication works. For this purpose I created website and post articles on the topic. Site no longer exist because project is frozen. But I did a [few screenshots](https://drive.google.com/drive/folders/1UiNLm9lwTIG04UrI05R_vW0fhDo5Ue3M?usp=sharing) to show you the idea.

When you read theory and get some advices bot will offer you to arrange meeting to another user of bot to practice your skills on online meeting with some interesting tasks. And that is the key: you practice your communication skills in safe environment with a person who is also interested in the topic and do some tasks created by psychologist supervisor.

## Implementation
To create the bot I used aiogram library - asynchrome Telegram API library written over asyncio.

To store the data I used SQLite database and SQLite3 python library (note: this was my very first python project, so database structure and logic are written very poorly. Now I see it 😅).

## Project structure
**Handlers** All message handlers are stored in /handlers directory. They are devided by bot modules and menus.

**Midlewares** There is only one middleware which helps to run online support chat with admin of the bot right in bot interface.

**algorithm.py** There is algorithm which match users into pairs everyday in 7 p.m. Idea is to firstly match users with smaller amount of availible matches, then users this lot's of mathes. So everybody will have a pair.

**app.py** Runs bot, scheduler and creates database

**loader.py** Defines the key entities of the bot

**bot_commands.py** Set user's command for bot

**config.py** Gets credentials from .env

**keyboards.py** Store all keyboards

**sqkite.py** Code for operating SQLite database

## To sum up
This was my first Python project, I did it a year ago. I got almost 100 of users, but only few of them were active weekly. So I stopped the project for some time. I hope somebody will find this code useful for themselves.

Oh, and there is [mindmap of bot's logic](https://miro.com/app/board/o9J_kyNTfhM=/) after user have a match for better understanding the structure (it's in Cyrillyc, but nevertheless).

