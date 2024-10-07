import discord
from discord.ext import commands, tasks
from flask import Flask
import pytz
from datetime import datetime
import os

# Initialize Flask app
flask_app = Flask(__name__)

# Replace with your actual token and channel/role IDs
TOKEN = os.getenv("DISCORD_TOKEN")
DAILY_REPORT_CHANNEL_ID = 1292700286707699824    # Replace with your channel ID
TEAM_ROLE_ID = 1292702831190478881    # Replace with your role ID
OWNER_USER_ID = 758367646101536799 

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Dictionary to store member reports
reports = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    daily_report.start()

@bot.event
async def on_message(message):
    if message.channel.id == DAILY_REPORT_CHANNEL_ID and not message.author.bot:
        reports[message.author.id] = message.content  # Store the report
    await bot.process_commands(message)

@tasks.loop(hours=24)
async def daily_report():
    now = datetime.now(pytz.timezone("Asia/Kolkata"))
    if now.hour == 17 and now.minute == 30:
        user = await bot.fetch_user(OWNER_USER_ID)
        summary = "Daily Reports Summary:\n"
        for member_id, report in reports.items():
            member = bot.get_user(member_id)
            summary += f"{member.name}: {report}\n"
        
        await user.send(summary)
        reports.clear()

@flask_app.route('/')
def index():
    return "Discord Bot is Running!", 200

@flask_app.route('/health')
def health():
    return "Bot is healthy!", 200

@flask_app.before_first_request
def start_bot():
    # Start the Discord bot
    bot.loop.create_task(bot.start(TOKEN))

if __name__ == "__main__":
    flask_app.run(host='0.0.0.0', port=5000)  # Listen on all interfaces
