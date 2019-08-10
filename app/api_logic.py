import requests
import copy
import numbers

GITHUB_API = 'https://api.github.com' # currently v3
BITBUCKET_API = 'https://api.bitbucket.org/2.0'

# I'm not completely sure on the requirements for this results dict.
# At first, I just included all the aggregated data, but then decided to include the repo details as well
RESULTS_TEMPLATE = {
    'total_original_repos': 0,
    'total_forked_repos': 0,
    'total_watchers': 0,
    'total_languages': 0,
    'languages': {},
    'total_topics': 0,
    'topics': {},
    'repo_details': []
}

REPO_DETAILS_TEMPLATE = {
    'remote_host': None,
    'name': None,
    'number_of_watchers': 0,
    'language': None,
    'topics': []
}

def get_github_info(org):
    response = requests.get('{}/orgs/{}/repos'.format(GITHUB_API, org))
    if response.ok:
        results = copy.deepcopy(RESULTS_TEMPLATE)
        repos = response.json()
        for repo in repos:

            # fork info
            if repo.get('fork'):
                results['total_forked_repos'] += 1
            else:
                results['total_original_repos'] += 1

            # watchers info
            results['total_watchers'] += repo.get('watchers_count')

            # language info
            if repo.get('language'):
                if results['languages'].get(repo.get('language')):
                    results['languages'][repo.get('language')] += 1
                else:
                    results['languages'][repo.get('language')] = 1

            # topics info
            if repo.get('topics'):
                for topic in repo.get('topics'):
                    if results['topics'].get(topic):
                        results['languages'][topic] += 1
                    else:
                        results['languages'][topic] = 1

            # repo details info
            repo_details = copy.deepcopy(REPO_DETAILS_TEMPLATE)
            repo_details['remote_host'] = 'GitHub'
            repo_details['name'] = repo.get('name')
            repo_details['number_of_watchers'] = repo.get('watchers_count')
            repo_details['language'] = repo.get('language')
            repo_details['topics'] = repo.get('topics')

            results['repo_details'].append(repo_details)

        results['total_languages'] = len(results['languages'].keys())
        results['total_topics'] = len(results['topics'].keys())

        return results
    else:
        # Response not ok
        return 'Error'


def get_bitbucket_info(team):
    response = requests.get('{}/repositories/{}'.format(BITBUCKET_API, team))
    if response.ok:
        results = copy.deepcopy(RESULTS_TEMPLATE)
        data = response.json()
        repos = data.get('values')
        if repos:
            for repo in repos:
                repo_details = copy.deepcopy(REPO_DETAILS_TEMPLATE)
                repo_details['remote_host'] = 'BitBucket'
                repo_details['name'] = repo.get('name')

                # api response doesn't seem to contain fork v original information
                results['total_original_repos'] += 1

                # language info
                if repo.get('language'):
                    repo_details['language'] = repo.get('language')
                    if results['languages'].get(repo.get('language')):
                        results['languages'][repo.get('language')] += 1
                    else:
                        results['languages'][repo.get('language')] = 1

                # watchers info
                watchers_link = repo['links'].get('watchers')
                if watchers_link:
                    watchers_response = requests.get(watchers_link['href'])
                    if watchers_response.ok:
                        watchers_data = watchers_response.json()
                        results['total_watchers'] += watchers_data.get('size')
                        repo_details['number_of_watchers'] = watchers_data.get('size')

                # topics info
                # I don't see anything about topics or an equivalent

                results['repo_details'].append(repo_details)

        results['total_languages'] = len(results['languages'].keys())

        return results
    else:
        # Response not ok
        return 'Error'

    # There's another api call to get a team's followers. This number is different from the total
    #   watchers count I got above. I assume followers are team-level, while watchers are repo-level.
    #   Going to stick with returning watchers since it seems more similar to Github watchers.
    #   response = requests.get('{}/teams/{}/followers'.format(BITBUCKET_API, team))


def merge_dicts(dict1, dict2, exclude_extra_keys=False):
    '''
    Merge two dictionaries with similar/same keys
    :param dict1:
    :param dict2:
    :param exclude_extra_keys: Only include matching keys between two dictionaries
    :return:
    '''
    result = {}
    for key, item1 in dict1.items():
        item2 = dict2.get(key)
        if item2 != None:
            if (type(item1) != type(item2)) or (type(item1) == 'str'):
                result['{}_1'.format(key)] = item1
                result['{}_2'.format(key)] = item2
            elif isinstance(item1, numbers.Number):
                result[key] = item1 + item2
            elif isinstance(item1, dict):
                result[key] = merge_dicts(item1, item2)
            elif isinstance(item1, list):
                try:
                    result[key] = list(set(item1 + item2))
                except TypeError:
                    # This will be thrown when the list items are dictionaries
                    result[key] = item1 + item2
        else:
            result[key] = item1
    if not exclude_extra_keys:
        remaining_dict2_keys = list(set(dict2.keys()) - set(dict1.keys()))
        for key in remaining_dict2_keys:
            result[key] = dict2.get(key)

    return result
