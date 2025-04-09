import os

def delete_csvs():
    """Delete the CSV files for the last 10, 20, 30, 40, and 50 played songs and the top 5 artists from the csv folder."""
    song_counts = [10, 20, 30, 40, 50]
    for count in song_counts:
        song_file_name = f'csv/last_{count}_played_songs.csv'
        artist_file_name = f'csv/top_5_artists_last_{count}_songs.csv'

        if os.path.exists(song_file_name):
            os.remove(song_file_name)
            print(f"Deleted {song_file_name}")
        else:
            print(f"{song_file_name} does not exist")

        if os.path.exists(artist_file_name):
            os.remove(artist_file_name)
            print(f"Deleted {artist_file_name}")
        else:
            print(f"{artist_file_name} does not exist")

# Delete the CSV files in the csv/ folder
delete_csvs()
