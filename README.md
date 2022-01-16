# Discordfy 
## nwHacks 2022 Submission by Josh Fung, Grace Lin, and Luca Festa
`Discordfy` is a song guessing game built into a Discord bot, making use of songs from Spotify playlists.
It is built in Python and makes use of a variety of APIs and tools such as `discord.py`, `spotDL`, and, `FFmpeg`.

## Function
Given a Spotify playlist, `Discordfy` will pick 5 songs, playing a **five** second snippet for each
song. Following, you'll be given a chance to try to guess the name of the song in **ten** seconds before it
moves onto the next song.