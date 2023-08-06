from ..utils import format_adj_matrix_from_standard, format_channel_location_dict, format_adj_matrix_from_adj_list
from ..standard_1020 import STANDARD_1020_CHANNEL_LOCATION_DICT

AMIGOS_CHANNEL_LIST = ['AF3', 'F7', 'F3', 'FC5', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'FC6', 'F4', 'F8', 'AF4']

AMIGOS_LOCATION_LIST = [['-', '-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', 'AF3', '-', 'AF4', '-', '-', '-'],
                        ['F7', '-', 'F3', '-', '-', '-', 'F4', '-', 'F8'],
                        ['-', 'FC5', '-', '-', '-', '-', '-', 'FC6', '-'],
                        ['T7', '-', '-', '-', '-', '-', '-', '-', 'T8'], ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
                        ['P7', '-', '-', '-', '-', '-', '-', '-', 'P8'], ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', 'O1', '-', 'O2', '-', '-', '-']]

AMIGOS_CHANNEL_LOCATION_DICT = format_channel_location_dict(AMIGOS_CHANNEL_LIST, AMIGOS_LOCATION_LIST)

AMIGOS_ADJACENCY_LIST = {
    'AF3': ['F3', 'AF4'],
    'AF4': ['AF3', 'F4'],
    'F7': ['F3', 'FC5', 'T7'],
    'F3': ['AF3', 'F7', 'FC5'],
    'F4': ['AF4', 'F8', 'FC6'],
    'F8': ['F4', 'FC6', 'T8'],
    'FC5': ['F7', 'F3', 'T7'],
    'FC6': ['F4', 'F8', 'T8'],
    'T7': ['F7', 'FC5', 'P7'],
    'T8': ['F8', 'FC6', 'P8'],
    'P7': ['T7'],
    'P8': ['T8'],
    'O1': ['O2'],
    'O2': ['O1']
}

AMIGOS_ADJACENCY_MATRIX = format_adj_matrix_from_adj_list(AMIGOS_CHANNEL_LIST, AMIGOS_ADJACENCY_LIST)

AMIGOS_STANDARD_ADJACENCY_MATRIX = format_adj_matrix_from_standard(AMIGOS_CHANNEL_LIST,
                                                                 STANDARD_1020_CHANNEL_LOCATION_DICT,
                                                                 delta=0.00035)
