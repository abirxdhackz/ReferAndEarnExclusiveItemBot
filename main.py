# Author (C) @abirxdhackz
# Channel : https://t.me/abir_xd_bio

import telebot
from telebot import types
import time

API_TOKEN = 'API_TOKEN'  # Replace with your bot's API token
bot = telebot.TeleBot(API_TOKEN)

# Sample data storage for user data
user_data = {}
total_users = set()  # Store unique users to count total members
service_requests = {}  # Store mapping of message IDs to user chat IDs

# Define the admin group chat ID for forwarding messages and replying
GROUP_CHAT_ID = -1002263161625  # Replace with your group chat ID
ADMIN_USER_IDS = {7303810912,5442332281,6249257243}  # Replace with actual admin user IDs

# Define the point cost for each service
service_points = {
    "NETFLIX": 30,
    "PRIME VIDEO": 15,
    "CAPCUT": 20,
    "Canva": 3,
    "HoichoiChorki": 30,
    "VPN": 6,
    "WhatsApp Number": 30,
    "Apple Music": 15,
    "Chruncyroll": 10,
    "YouTube Premium": 8,
    "Telegram Number": 60
}

# List of channels to check
channels_to_check = [
    "@ModVipRM",
    "@ModviprmBackup",
    "@modDirect_download",
    "@abir_x_official"
]

# Function to create the main menu
def main_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    join_buttons = [
        types.InlineKeyboardButton("Main Channel", url="https://t.me/ModVipRM"),
        types.InlineKeyboardButton("Backup Channel", url="https://t.me/ModviprmBackup"),
        types.InlineKeyboardButton("Direct Downloads", url="https://t.me/modDirect_download"),
        types.InlineKeyboardButton("Developer", url="https://t.me/abir_x_official")
    ]
    joined_button = types.InlineKeyboardButton("Joined", callback_data="joined")
    markup.add(*join_buttons)
    markup.add(joined_button)
    bot.send_message(chat_id, "Welcome! Please join all channels before proceeding.", reply_markup=markup)

# Function to check if the user has joined all required channels
def check_joined(chat_id):
    for channel in channels_to_check:
        try:
            member = bot.get_chat_member(channel, chat_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception as e:
            return False
    return True

# Command handler for /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id
    referrer_id = message.text.split(" ")[1] if len(message.text.split(" ")) > 1 else None

    if chat_id not in total_users:
        total_users.add(chat_id)
        user_data[chat_id] = {
            'balance': 0,
            'invited_users': 0,
            'bonus_claimed': False
        }
        if referrer_id and referrer_id.isdigit() and int(referrer_id) in user_data:
            user_data[int(referrer_id)]['invited_users'] += 1
            user_data[int(referrer_id)]['balance'] += 2
            bot.send_message(int(referrer_id), "Successful referral! You earned 2 points.")

    main_menu(chat_id)

# Callback handler for the joined button
@bot.callback_query_handler(func=lambda call: call.data == "joined")
def joined_handler(call):
    chat_id = call.message.chat.id
    if check_joined(chat_id):
        options_menu(chat_id)
    else:
        bot.send_message(chat_id, "You need to join all channels to use the bot. Please join and click 'Joined' again.")

# Function to display options after joining
def options_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🧑‍🤝‍🧑 Refer", "🏆 Redeem", "🎁 Bonus", "📞 Support", "📊 Statistics", "👩‍💻 Account")
    bot.send_message(chat_id, "Choose an option:", reply_markup=markup)



# Function to handle the Redeem button
@bot.message_handler(func=lambda message: message.text == "🏆 Redeem")
def redeem_handler(message):
    chat_id = message.chat.id
    user = user_data.get(chat_id, {'balance': 0})

    # Create a 3x3 grid layout for service buttons
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    # Create buttons for each service in a 3x3 layout
    service_buttons = []
    for service, points in service_points.items():
        service_buttons.append(f"{service} ({points} points)")
    
    # Add buttons to the markup in rows
    for i in range(0, len(service_buttons), 3):
        markup.add(*service_buttons[i:i+3])

    markup.add("🔙 Back to Menu")  # Back button
    bot.send_message(chat_id, "Choose a service to redeem:", reply_markup=markup)

# Function to handle service selection in the redeem section
@bot.message_handler(func=lambda message: message.text.split(" (")[0] in service_points.keys())
def service_handler(message):
    chat_id = message.chat.id
    service = message.text.split(" (")[0]
    required_points = service_points[service]
    user = user_data.get(chat_id, {'balance': 0})

    if user['balance'] >= required_points:
        user['balance'] -= required_points
        forwarded_message_text = f"User ID: {chat_id}\nUser requested: {service}"
        sent_message = bot.send_message(GROUP_CHAT_ID, forwarded_message_text)
        service_requests[sent_message.message_id] = chat_id
        bot.send_message(chat_id, f"Your request for {service} has been forwarded to the admin. {required_points} points have been deducted from your balance.")
    else:
        bot.send_message(chat_id, f"⚠️ You need {required_points} points to redeem {service}. You currently have {user['balance']} points.")

# Function to handle the Back button in the redeem section
@bot.message_handler(func=lambda message: message.text == "🔙 Back to Menu")
def back_to_main_menu(message):
    chat_id = message.chat.id
    options_menu(chat_id)

# Function to handle the Refer button
@bot.message_handler(func=lambda message: message.text == "🧑‍🤝‍🧑 Refer")
def refer_handler(message):
    chat_id = message.chat.id

    if chat_id not in user_data:
        user_data[chat_id] = {'balance': 0, 'invited_users': 0, 'bonus_claimed': False}

    referral_link = f"https://t.me/ReferAndEarnExclusiveItemBot?start={chat_id}"
    response = (
        f"👬 Your invite link: {referral_link}\n"
        "💸 Per refer: 2 points\n"
        f"👉 Total invited users: {user_data[chat_id]['invited_users']}"
    )
    bot.send_message(chat_id, response)

# Function to handle the Bonus button
@bot.message_handler(func=lambda message: message.text == "🎁 Bonus")
def bonus_handler(message):
    chat_id = message.chat.id
    user = user_data.get(chat_id, {'balance': 0, 'bonus_claimed': False})
    if not user['bonus_claimed']:
        user['balance'] += 1  # Give bonus points
        user['bonus_claimed'] = True  # Mark bonus as claimed
        bot.send_message(chat_id, "You have received 1 bonus point!")
    else:
        bot.send_message(chat_id, "⚠️ You can claim your bonus points once every 24 hours.")

# Function to handle the Support button
@bot.message_handler(func=lambda message: message.text == "📞 Support")
def support_handler(message):
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup()
    support_button = types.InlineKeyboardButton("Support Group", url="https://t.me/ModVipRM_Discussion")
    markup.add(support_button)
    bot.send_message(chat_id, "Here is our Support Group. Join for assistance!", reply_markup=markup)

# Function to handle the Account button
@bot.message_handler(func=lambda message: message.text == "👩‍💻 Account")
def account_handler(message):
    chat_id = message.chat.id
    user = user_data.get(chat_id, {'balance': 0, 'invited_users': 0, 'bonus_claimed': False})
    response = (
        f"👤 Account Information:\n"
        f"💰 Balance: {user['balance']} points\n"
        f"👥 Invited Users: {user['invited_users']}\n"
        f"🎁 Bonus Claimed: {'Yes' if user['bonus_claimed'] else 'No'}"
    )
    bot.send_message(chat_id, response)

# Function to handle the Statistics button
@bot.message_handler(func=lambda message: message.text == "📊 Statistics")
def statistics_handler(message):
    chat_id = message.chat.id
    response = (
        "📊 Statistics of @ReferAndEarnExclusiveItemBot\n"
        f"🧑 Total members: {len(total_users)}\n"
        "👑 Bot creator: @abirxdhackz\n"
        "❤️ Join our Channel for more bots: @ModVipRM"
    )
    bot.send_message(chat_id, response)

# Admin command to add balance
@bot.message_handler(commands=['BalanceAdd'])
def balance_add_handler(message):
    if message.from_user.id not in ADMIN_USER_IDS:
        bot.send_message(message.chat.id, "⚠️ You don't have permission to use this command.")
        return

    # Ask for the amount and user ID to add balance
    msg = bot.send_message(message.chat.id, "Please enter the amount of points and user ID in this format:\n\n`points user_id`", parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_balance_add)

# Process the balance add input from the admin
def process_balance_add(message):
    try:
        # Split input into points and user ID
        points, user_id = map(str.strip, message.text.split())
        points = int(points)
        user_id = int(user_id)

        # Ensure the user ID exists in user_data, initialize if missing
        if user_id not in user_data:
            user_data[user_id] = {'balance': 0, 'invited_users': 0, 'bonus_claimed': False}

        # Add points to the user's balance
        user_data[user_id]['balance'] += points
        bot.send_message(message.chat.id, f"✅ Successfully added {points} points to user {user_id}'s balance.")
        bot.send_message(user_id, f"🎉 You have received {points} points! Your new balance is {user_data[user_id]['balance']} points.")

    except ValueError:
        bot.send_message(message.chat.id, "⚠️ Invalid input format. Please use the format `points user_id` (e.g., `10 123456789`).")
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ An error occurred: {e}")

# Admin command to broadcast a message
@bot.message_handler(commands=['broadcast'])
def broadcast_handler(message):
    if message.from_user.id not in ADMIN_USER_IDS:
        bot.send_message(message.chat.id, "⚠️ You don't have permission to use this command.")
        return

    # Ask for the message to broadcast
    msg = bot.send_message(message.chat.id, "Please enter the message or send the file to broadcast.")
    bot.register_next_step_handler(msg, process_broadcast)

# Process the broadcast message or file
def process_broadcast(message):
    # Broadcast the received message to all users in total_users
    for user_id in total_users:
        try:
            # Check if the message contains text, photo, document, or video to broadcast
            if message.content_type == 'text':
                bot.send_message(user_id, message.text)
            elif message.content_type == 'photo':
                bot.send_photo(user_id, message.photo[-1].file_id, caption=message.caption)
            elif message.content_type == 'document':
                bot.send_document(user_id, message.document.file_id, caption=message.caption)
            elif message.content_type == 'video':
                bot.send_video(user_id, message.video.file_id, caption=message.caption)
        except Exception as e:
            print(f"Could not send message to {user_id}: {e}")

    # Notify the admin that the broadcast was successful
    bot.send_message(message.chat.id, "✅ Broadcast sent to all users.")


# Admin reply handler
@bot.message_handler(func=lambda message: message.reply_to_message and message.reply_to_message.chat.id == GROUP_CHAT_ID)
def admin_reply_handler(message):
    if message.reply_to_message and message.reply_to_message.text and message.reply_to_message.text.startswith("User ID:"):
        # Extract the user ID from the forwarded message
        user_chat_id_str = message.reply_to_message.text.split(":")[1].strip().split("\n")[0]  # Only take the part before any newlines
        try:
            user_chat_id = int(user_chat_id_str)  # Convert to int
            bot.send_message(user_chat_id, message.text)  # Send the reply back to the user
        except ValueError as e:
            print(f"Error converting user ID to int: {e}")  # Log error for debugging

# Start polling for updates
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)


# Author (C) @abirxdhackz
# Channel : https://t.me/abir_xd_bio
