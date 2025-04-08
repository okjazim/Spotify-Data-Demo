import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from collections import Counter
from dotenv import load_dotenv
import os

load_dotenv()

# Spotify API credentials

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

# Authenticate and create Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope='user-read-recently-played'
))

def fetch_recently_played(limit):
    """Fetch the last `limit` number of recently played tracks."""
    results = []
    next_url = f'https://api.spotify.com/v1/me/player/recently-played?limit={min(limit, 50)}'

    while next_url and len(results) < limit:
        response = sp._get(next_url)
        if 'items' in response:
            results.extend(response['items'])
        if 'next' in response and len(results) < limit:
            next_url = response['next']
        else:
            next_url = None

    return results[:limit]  # Ensure only the requested number of songs are returned

def fetch_played_songs(song_count):
    """Fetch the last `song_count` played songs and save to CSV."""
    # Fetch recently played tracks
    results = fetch_recently_played(song_count)

    # Extract relevant data for each track
    song_data = []
    artist_counter = Counter()
    artist_links = {}
    for item in results:
        track = item['track']
        artist_names = [artist['name'] for artist in track['artists']]
        artist_urls = [artist['external_urls']['spotify'] for artist in track['artists']]
        song_data.append({
            'played_at': item['played_at'],
            'track_name': track['name'],
            'artist_name': ', '.join(artist_names),
            'artist_link': ', '.join(artist_urls),
            'album_name': track['album']['name'],
            'spotify_link': track['external_urls']['spotify']
        })
        for name, url in zip(artist_names, artist_urls):
            artist_counter[name] += 1
            artist_links[name] = url

    # Create DataFrame for songs
    df_songs = pd.DataFrame(song_data)

    # Create DataFrame for top 5 artists
    top_artists = artist_counter.most_common(5)
    df_artists = pd.DataFrame(top_artists, columns=['artist_name', 'play_count'])
    df_artists['artist_link'] = df_artists['artist_name'].map(artist_links)

    # Save to CSV
    df_songs.to_csv(f'last_{song_count}_played_songs.csv', index=False)
    df_artists.to_csv(f'top_5_artists_last_{song_count}_songs.csv', index=False)
    print(f"CSV files for last {song_count} played songs and top 5 artists generated successfully!")

# Fetch and generate CSV files for different song counts
fetch_played_songs(10)
fetch_played_songs(20)
fetch_played_songs(30)
fetch_played_songs(40)
fetch_played_songs(50)
