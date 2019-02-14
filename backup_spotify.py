#!python3
import sys
import spotipy
import spotipy.util as util

scope = 'user-library-read'
BACKUP_DIR = "C:/Users/Trevor/Music/SpotifyBackups"

def tracks_to_text(tracks):
    track_infos = []
    for i, item in enumerate(tracks['items']):
        track = item['track']
        track_infos.append(str(i+1) + ' ' + track['artists'][0]['name'] + ' - ' + track['name'])
    return '\n'.join(track_infos)

# right now this just overwrites everything, which is inefficient.
def fill_txt_file(backup_dir, playlist, tracks):
    playlist_name = playlist['name'].replace('/', '_')
    fullpath = backup_dir + "/" + playlist_name + ".txt"
    print("Saving " + playlist['name'] + " in " + fullpath)
    playlist_file = open(fullpath, 'w', encoding="utf8")
    playlist_file.write(tracks_to_text(tracks))
    playlist_file.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage:", sys.argv[0], "username")
        sys.exit()

    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        for playlist in playlists['items']:
            if playlist['owner']['id'] == username:
                results = sp.user_playlist(username, playlist['id'],
                    fields="tracks,next")
                tracks = results['tracks']
                fill_txt_file(BACKUP_DIR, playlist, tracks)
    else:
        print("Can't get token for", username)