import numpy as np
import pandas as pd
import random


def is_song_in_playlist(songs, song_in_pl_matrix):
"""
A helper method to convert a list of songs into a binary list that details if the song is in the playlist or not

ARGUMENTS:

songs: the song titles from the matrix that tracks if songs are in playlists
song_in_pl_matrix: a sparse matrix that tracks which songs are in which playlists

OUTPUTS:
binary_pl: the binary list with 1's at pids corresponding to the songs
"""

binary_pl = np.zeros(len(list(song_pl_df.columns)))
song_index = [list(song_in_pl_matrix).index(s) for s in songs]
binary_pl[song_index] = 1
return binary_pl

# def get_titles(song_list,)


