import discord
from discord.ext import commands, tasks
from datetime import datetime
import pytz
import os

# Set your timezone and 5:30 PM time
IST = pytz.timezone('Asia/Kolkata')
CHECK_TIME = datetime.now(IST).replace(hour=17, minute=30, second=0, microsecond=0)

# Initialize the bot
bot = commands.Bot(command_prefix="!")

# Define the channel ID and role ID for tagging
DAILY_REPORT_CHANNEL_ID = 1292700286707699824  # Replace with your #daily-report channel ID brahma - 1266320212299612262
TEAM_ROLE_ID = 1292702831190478881  # Replace with the role ID for your team if you want to tag a specific role brahma - 892357106701848576

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    check_daily_reports.start()

@tasks.loop(minutes=1)
async def check_daily_reports():
    now = datetime.now(IST)
    if now.hour == CHECK_TIME.hour and now.minute == CHECK_TIME.minute:
        channel = bot.get_channel(DAILY_REPORT_CHANNEL_ID)
        if channel is None:
            print("Could not find the #daily-report channel.")
            return

        # Set of users who have sent messages today
        today = now.date()
        reported_users = set()
        
        # Check messages from today only
        async for message in channel.history(limit=100):  # You can adjust limit as needed
            if message.created_at.astimezone(IST).date() == today:
                reported_users.add(message.author.id)

        # Check all team members in the role and DM/tag those who haven't posted
        guild = channel.guild
        role = guild.get_role(TEAM_ROLE_ID)
        for member in role.members:
            if member.id not in reported_users:
                await channel.send(f"{member.mention} Please send your daily report!")
                await member.send("Hey! Please remember to send your daily report in #daily-report!")

# Run the bot
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
