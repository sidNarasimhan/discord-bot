import discord
from discord.ext import commands, tasks
from datetime import datetime
import pytz

# Set your timezone and 5:30 PM time
IST = pytz.timezone('Asia/Kolkata')
CHECK_TIME = datetime.now(IST).replace(hour=17, minute=30, second=0, microsecond=0)

# Initialize the bot
bot = commands.Bot(command_prefix="!")

# Define the channel ID and role ID for tagging
DAILY_REPORT_CHANNEL_ID = 1234567890  # Replace with your #daily-report channel ID
TEAM_ROLE_ID = 9876543210  # Replace with the role ID for your team if you want to tag a specific role

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
bot.run('YOUR_BOT_TOKEN')
