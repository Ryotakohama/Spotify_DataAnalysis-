import mysql.connector
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import re

# set up client credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials
    (client_id='6c38f93c66da4d96907ff1cd678683bf',
     client_secret='6ffc2f425eec482ebd9ac94f133e3eba'
))

# MySql Database Connection
db_config = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : 'root',
    'database' : 'spotify_db'
}

# Connect to database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Read track url from file
file_path = 'spotify_url.txt'
with open(file_path, 'r') as file:
    spotify_url = file.readlines()

# Process each url
for track_url in spotify_url:
    track_url = track_url.strip()
    try:

        # Extract track ID from track URL using Regex
        track_id = re.search(r'track/([a-zA-Z0-9]+)', track_url).group(1)

        # Fetch track details
        track = sp.track(track_id)

        # Extract meta data
        track_data = {
            'track_name' : track['name'],
            'artist_name': track['artists'][0]['name'],
            'album_name': track['album']['name'],
            'release_date' : track["album"]["release_date"],
            'popularity': track['popularity'],
            'duration_minutes': track['duration_ms'] / 60000,
            'track_url' : track["external_urls"]["spotify"]
        }

        # Insert data into SQL
        insert_query = """
        insert into spotify_tracks(track_name,artist_name,album_name,release_date,duration_minutes,popularity)
        values (%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(insert_query, (
            track_data['track_name'],
            track_data['artist_name'],
            track_data['album_name'],
            track_data['release_date'],
            track_data['duration_minutes'],
            track_data['popularity']
        ))
        connection.commit()

        print(f"Track '{track_data['track_name']}' by {track_data['artist_name']} inserted into the database.")
    except Exception as e:
        print(f"Error Processing  URL: {track_url}, Error: {e}")

# Close the connection
cursor.close()
connection.close()

print("All the tracks have been processed and inserted into the database")
