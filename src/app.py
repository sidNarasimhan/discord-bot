import discord
from discord.ext import commands, tasks
import pytz
from datetime import datetime
import os

# Replace with your actual token and channel/role IDs
TOKEN = os.getenv("DISCORD_TOKEN")
DAILY_REPORT_CHANNEL_ID = 1292700286707699824    # Replace with your channel ID
TEAM_ROLE_ID = 1292702831190478881    # Replace with your role ID
OWNER_USER_ID = 758367646101536799  # Replace with your Discord user ID

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
    # Check if it's time to send the summary
    now = datetime.now(pytz.timezone("Asia/Kolkata"))  # Set to your timezone
    if now.hour == 17 and now.minute == 30:  # 5:30 PM IST
        user = await bot.fetch_user(OWNER_USER_ID)  # Fetch the user by ID
        summary = "Daily Reports Summary:\n"
        for member_id, report in reports.items():
            member = bot.get_user(member_id)  # Get the member object
            summary += f"{member.name}: {report}\n"
        
        await user.send(summary)  # Send the summary as a DM
        reports.clear()  # Clear the reports for the next day

@daily_report.before_loop
async def before_daily_report():
    await bot.wait_until_ready()

bot.run(TOKEN)
