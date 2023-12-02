import json
from neo4j import GraphDatabase
class SpotifyDatabaseTest:
    def __init__(self, uri, user, pwd):
        self._uri = uri
        self._user = user
        self._password = pwd
        self._driver = None

    def close(self):
        self._driver.close()

    def connect(self):
        self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))
        return self._driver
    
def createData(tx, playlists):
    #create playlist node
    for playlist in playlists:
        # Create PLAYLIST node
        tx.run(
            "MERGE (p:PLAYLIST {pid: $pid, name: $name, collaborative: $collaborative, "
            "modified_at: $modified_at, num_tracks: $num_tracks, num_albums: $num_albums, "
            "num_followers: $num_followers})",
            pid=playlist['pid'],
            name=playlist['name'],
            collaborative=playlist['collaborative'],
            modified_at=playlist['modified_at'],
            num_tracks=playlist['num_tracks'],
            num_albums=playlist['num_albums'],
            num_followers=playlist['num_followers']
        )

        # Iterate through tracks in the playlist
        for track in playlist['tracks']:
            # Create ARTIST node
            tx.run(
                "MERGE (a:ARTIST {artist_uri: $artist_uri, artist_name: $artist_name})",
                artist_uri=track['artist_uri'],
                artist_name=track['artist_name']
            )

            # Create ALBUM node
            tx.run(
                "MERGE (al:ALBUM {album_uri: $album_uri, album_name: $album_name})",
                album_uri=track['album_uri'],
                album_name=track['album_name']
            )

            # Create TRACK node
            tx.run(
                "MERGE (t:TRACK {track_uri: $track_uri, track_name: $track_name, duration_ms: $duration_ms})",
                track_uri=track['track_uri'],
                track_name=track['track_name'],
                duration_ms=track['duration_ms']
            )

            # Create relationships
            tx.run(
                "MATCH (p:PLAYLIST), (t:TRACK) "
                "WHERE p.pid = $pid AND t.track_uri = $track_uri "
                "MERGE (p)-[:CONTAINS]->(t)",
                pid=playlist['pid'],
                track_uri=track['track_uri']
            )

            tx.run(
                "MATCH (t:TRACK), (al:ALBUM) "
                "WHERE t.track_uri = $track_uri AND al.album_uri = $album_uri "
                "MERGE (t)-[:FROM_ALBUM]->(al)",
                track_uri=track['track_uri'],
                album_uri=track['album_uri']
            )

            tx.run(
                "MATCH (t:TRACK), (a:ARTIST) "
                "WHERE t.track_uri = $track_uri AND a.artist_uri = $artist_uri "
                "MERGE (t)-[:PERFORMED_BY]->(a)",
                track_uri=track['track_uri'],
                artist_uri=track['artist_uri']
            )


#filepath change this!
f = open("/Users/tingweilin/Desktop/CSDS_234_DATA/ProjectFinal/spotify_million_playlist_dataset/data/mpd.slice.0-20.json")
data = json.load(f)
connection = SpotifyDatabaseTest(uri = "bolt://localhost:7687", user="neo4j", pwd="Password")
with connection.connect() as driver:
    driver.session().write_transaction(createData, data['playlists'])