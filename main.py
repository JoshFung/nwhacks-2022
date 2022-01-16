import os
import discord
import random

import spotipy
from spotdl.search import SpotifyClient
from spotipy.oauth2 import SpotifyOAuth

from spotdl.search.song_gatherer import from_playlist

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

client = discord.Client()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.download') and ' ' in message.content:
        url = message.content.split(" ")[1]
        raw_track_meta = from_url(url)
        song_name = raw_track_meta["name"]
        contributing_artists = ", ".join([artist["name"] for artist in raw_track_meta["artists"]])
        file_name = f"{contributing_artists} - {song_name}.mp3"
        await message.channel.send("Downloading song...")
        os.system(f"spotdl {url}")
        os.rename(file_name, file_name.replace(" ", ""))
        file_name = file_name.replace(" ", "")
        await message.channel.send('Here is your song:', file=discord.File(file_name))
        os.remove(file_name)

    if message.content.startswith('.playlist'):
        url = message.content.split(" ")[1]
        lst_of_name_link = playlist_songs_url(url)
        song_tuple = random.choice(lst_of_name_link)

def playlist_songs_url(playlist_url: str) -> list:
    return [(song._raw_track_meta['name'], song._raw_track_meta['external_urls']['spotify']) for
            song in from_playlist(playlist_url)]

client.run(os.environ.get('TOKEN'))
