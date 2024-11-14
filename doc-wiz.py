import os
import discord
import requests
from dotenv import load_dotenv

# Replace with your credentials
DISCORD_TOKEN = os.getenv(DISCORD_TOKEN)
GOOGLE_API_KEY = os.getenv(GOOGLE_API_KEY)
SEARCH_ENGINE_ID = os.getenv(SEARCH_ENGINE_ID)

# Set up Discord bot client
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Function to search using Google Custom Search API
def search_documentation(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            # Return the first result's title and link
            return data["items"][0]["title"], data["items"][0]["link"]
        else:
            return "No results found.", None
    else:
        return "Error retrieving results.", None
    
@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")

@client.event
async def on_message(message):
    # Prevent bot from responding to its own messages
    if message.author == client.user:
        return
    
    # Check if message starts with the trigger
    if message.content.startswith("!docs"):
        query = message.content[6:]  # Get the search term after '!docs '
        title, link = search_documentation(query)
        
        if link:
            await message.channel.send(f"**{title}**\n{link}")
        else:
            await message.channel.send(title)