import os
import sys
import re
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from discord.ext import commands

# Load Environment Variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CID = os.getenv('SPOTIFY_CID')
SECRET = os.getenv('SPOTIFY_SECRET')
USER = os.getenv('SPOTIFY_USER')
RURI = os.getenv('SPOTIFY_RURI')
PLAYLIST = os.getenv('SPOTIFY_PLAYLIST')

# Setup Spotify
token = spotipy.util.prompt_for_user_token(
		USER, 'playlist-modify-private', client_id=CID, client_secret=SECRET, redirect_uri=RURI
)
if token:
	sp = spotipy.Spotify(auth=token)
	sp.trace = False
else:
	print("Can't get token for {:s}".format(USER))
	sys.exit()
	
# Setup Discord
bot = commands.Bot(command_prefix='+')

# Global Variables
PATTERN = re.compile(r"https:\/\/open.spotify.com\/(\w*)\/(\w+)[?=\w]*")

# Helper Functions
def add_to_playlist(uri):
	results = sp.user_playlist_add_tracks(USER, PLAYLIST, [uri])
	print(results)
	
# Event Functions
@bot.command(name='add', help='Adds a song to the community playlist.')
async def add_song(ctx, url):
	match = re.search(PATTERN, url)
	if match and match.group(1) == 'track':
		await ctx.send('Adding to playlist.')
		add_to_playlist(match.group(2))
		
		''' Possible playlist change functionality
	elif match and match.group(1) == 'playlist':
		print('This is a playlist')
		print(match.group(2))
		playlist = match.group(2)
		'''
	
	else:
		await ctx.send('Invalid track.')
	
bot.run(TOKEN)