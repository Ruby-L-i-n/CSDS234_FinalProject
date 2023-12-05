import numpy as np
import pandas as pd
import random


def is_element_in_playlist(element, element_in_pl_matrix):
"""
A helper method to convert a list of elements into a binary list that details if that element is in the playlist or not

ARGUMENTS:

element: the element ids/names from the matrix to record if that element is in a playlist
element_in_pl_matrix: a sparse matrix that tracks which elements are in which playlists

OUTPUTS:
binary_pl: the binary list with 1's at pids corresponding to the element
"""

binary_pl = np.zeros(len(list(element_pl_df.columns)))
element_index = [list(element_in_pl_matrix).index(s) for s in element]
binary_pl[element_index] = 1
return binary_pl

# def get_titles(element_list,)


