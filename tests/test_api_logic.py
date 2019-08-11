import pytest

from app.api_logic import get_bitbucket_info, get_github_info, merge_dicts

def test_get_github_info():
    # Ideally, I wouldn't be using a pre-existing repo to test, but rather
    # use the Github API to create a repo, and then use my function to verify
    # it's pulling the data back correctly.

    # But.... we're going to be lazy and just use PyGame

    results = get_github_info('pygame')
    assert len(results) == 8
    assert results['total_original_repos'] == 8
    assert results['total_languages'] == 3
    assert len(results['repo_details']) == 8


def test_get_bitbucket_info():
    # Same note as above

    results = get_bitbucket_info('pygame')
    assert len(results) == 8
    assert results['total_original_repos'] == 7
    assert results['total_languages'] == 2
    assert len(results['repo_details']) == 7


def test_merge_dicts():
    dict1 = {
        'a': 2,
        'b': 'value1',
        'c': [1,2,3],
        'd': {
            'apple': 'red',
            'age': 25,
            'hobbies': [None]
        },
        'e': None,
        'f': 3.45,
        'g': 42,
        'h': (6, 7)
    }

    dict2 = {
        'a': 5,
        'b': 'value2',
        'c': [3, 4, 5],
        'd': {
            'banana': 'yellow',
            'age': 42,
            'carrot': 'orange',
            'hobbies': ['sleeping']
        },
        'e': None,
        'f': 2.90,
        'h': (5, 6),
        'i': 'extra'
    }

    merged_dict = merge_dicts(dict1, dict2)

    assert len(merged_dict.keys()) == 11
    assert merged_dict['a'] == 7
    assert merged_dict['b_1'] == 'value1'
    assert merged_dict['b_2'] == 'value2'
    assert merged_dict['c'] == [1,2,3,4,5]
    assert set(merged_dict['d'].keys()) == {'apple', 'age', 'hobbies', 'carrot', 'banana'}
    assert merged_dict['d']['apple'] == 'red'
    assert merged_dict['d']['age'] == 67
    assert set(merged_dict['d']['hobbies']) == {None, 'sleeping'}
    assert merged_dict['d']['carrot'] == 'orange'
    assert merged_dict['d']['banana'] == 'yellow'
    assert merged_dict['e'] == None
    assert merged_dict['f'] == 6.35
    assert merged_dict['g'] == 42
    assert merged_dict['h_1'] == (6, 7)
    assert merged_dict['h_2'] == (5, 6)
    assert merged_dict['i'] == 'extra'


