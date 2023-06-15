import discord
from discord.ext import commands
import os
import requests
import asyncio
from difflib import get_close_matches
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from io import BytesIO

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Replace <YOUR_API_KEY> with your actual Google Drive API key
API_KEY = 'AIzaSyC9_YlzFpmjACrtx0dsIStm4pxqBJp9i98'
# Replace <YOUR_FOLDER_ID> with the ID of the folder in your Google Drive where the files are located
FOLDER_ID = '1eE3uKTkHJ9pArZF1ljek6AyTQQoq4Z1o'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('------')

@bot.command(name='songs')
async def songs_command(ctx, file_name):
    service = build('drive', 'v3', developerKey=API_KEY)
    
    # Remove the file extension from the requested filename
    file_name_without_ext = os.path.splitext(file_name)[0]
    
    # Split the file name into individual words
    file_name_words = file_name_without_ext.lower().split()
    
    # Search for the file with the specified name or partial match
    matched_files = []
    response = service.files().list(q=f"'{FOLDER_ID}' in parents", fields='files(id, name, webContentLink)').execute()
    files = response.get('files', [])
    
    for file in files:
        file_name_only = os.path.splitext(file['name'])[0]
        file_name_only_words = file_name_only.lower().split()
        
        # Check if any word in the requested file name matches with any word in the actual file name
        if any(word in file_name_only_words for word in file_name_words):
            matched_files.append(file)
    
    if matched_files:
        if len(matched_files) == 1:
            selected_file = matched_files[0]
            await ctx.send(f"You chose to download '{selected_file['name']}'!")
            await ctx.send(f"Download Link: {selected_file['webContentLink']}")
        else:
            # Find the closest matching filenames for partial matches
            closest_matches = get_close_matches(file_name_without_ext, [file['name'] for file in matched_files])
            if closest_matches:
                suggestion_list = '\n'.join(closest_matches)
                await ctx.send(f"Did you mean one of the following files?\n{suggestion_list}")
            else:
                await ctx.send(f"No exact matches found for '{file_name}'.")
    else:
        await ctx.send(f"File '{file_name}' not found.")

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run('MTExMjkyOTI4NDc4NTQ1NTE3Nw.G9ukFl.WRRTh7B8OPGHj287cvtMhm1RbmkqPrfNuo7xIg')
