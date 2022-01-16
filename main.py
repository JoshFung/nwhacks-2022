# from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import random

import spotipy
from spotdl.search import SpotifyClient
from spotipy.oauth2 import SpotifyOAuth

from spotdl.search.song_gatherer import from_playlist

GUESSING = False
SONG_TITLE = ""
GUESSING_AUTHOR = ""

SpotifyClient.init(
    os.getenv('SPOTIPY_CLIENT_ID'),
    os.getenv('SPOTIPY_CLIENT_SECRET'),
    False
)


def from_url(spotify_url: str):
    if "open.spotify.com" not in spotify_url or "track" not in spotify_url:
        raise Exception(f"passed URL is not that of a track: {spotify_url}")

    # query spotify for song, artist, album details
    spotify_client = SpotifyClient()

    raw_track_meta = spotify_client.track(spotify_url)

    if raw_track_meta is None:
        raise Exception(
            "Couldn't get metadata, check if you have passed correct track id"
        )

    return raw_track_meta


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=str(os.environ.get('SPOTIPY_CLIENT_ID')),
        client_secret=str(os.environ.get('SPOTIPY_CLIENT_SECRET')),
        redirect_uri="http://example.com"
    )
)

# load_dotenv()
bot = commands.Bot(command_prefix='.')


@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Guessing "
                                                                                       "songs..."
                                                                                       "!"))
    print(f'Successfully logged in and booted...!')


# bot ignores own messages
# if message.author == bot.user:
#    return

@bot.command()
async def download(ctx, arg):
    # command to convert song into downloadable .mp3
    url = arg
    raw_track_meta = from_url(url)
    song_name = raw_track_meta["name"]
    contributing_artists = ", ".join([artist["name"] for artist in raw_track_meta["artists"]])
    file_name = f"{contributing_artists} - {song_name}.mp3"
    await ctx.send("Downloading song...")
    os.system(f"spotdl {url}")
    os.rename(file_name, file_name.replace(" ", ""))
    file_name = file_name.replace(" ", "")
    await ctx.send('Here is your song:', file=discord.File(file_name))
    os.remove(file_name)

@bot.command()
async def playlist(ctx, arg):
    global GUESSING, SONG_TITLE, GUESSING_AUTHOR

    url = arg
    await ctx.send("Getting tracks...")
    lst_of_name_link = playlist_songs_url(url)
    await ctx.send("Picking a song...")
    song_tuple = random.choice(lst_of_name_link)
    raw_track_meta = from_url(song_tuple[1])
    contributing_artists = ", ".join([artist["name"] for artist in raw_track_meta["artists"]])
    song_name = raw_track_meta["name"]
    file_name = f"{contributing_artists} - {song_name}.mp3"
    await ctx.send("Loading song...")
    os.system(f"spotdl {song_tuple[1]}")
    os.rename(file_name, "full.mp3")
    os.system('ffmpeg -i full.mp3 -ss 00:00:30 -t 00:00:05.0 -c copy song.mp3')
    await ctx.send('Guess the song title', file=discord.File("song.mp3"))
    os.remove("song.mp3")
    os.remove("full.mp3")
    GUESSING = True
    SONG_TITLE = song_tuple[0]
    GUESSING_AUTHOR = ctx.author
    guess = await bot.wait_for('message')

    if GUESSING and guess.author == GUESSING_AUTHOR:
        if guess.content == SONG_TITLE:
            await ctx.send("You guessed right!")
        else:
            await ctx.send(f"Wrong answer! The song was {SONG_TITLE}")
        GUESSING = False


def playlist_songs_url(playlist_url: str) -> list:
    return [(song._raw_track_meta['name'], song._raw_track_meta['external_urls']['spotify']) for
            song in from_playlist(playlist_url)]


bot.run(os.environ.get('TOKEN'))