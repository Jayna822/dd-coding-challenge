import json

def test_healthcheck(test_client):
    response = test_client.get('/health-check')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'All Good!'


def test_successful_merge(test_client):
    response = test_client.get('/merge/pygame')

    assert response.status_code == 200

    data = json.loads(response.data)
    assert len(data.keys()) == 5
    assert data['github_org'] == 'pygame'
    assert data['bitbucket_team'] == 'pygame'
    assert data['github_results'].get('total_original_repos') != None
    assert data['bitbucket_results'].get('total_original_repos') != None
    assert data.get('merge') != None


def test_both_failed_call(test_client):
    '''
    Calls to both API's have failed
    '''
    response = test_client.get('/merge/fake78567')

    assert response.status_code == 200

    data = json.loads(response.data)
    assert len(data.keys()) == 4
    assert data['github_org'] == 'fake78567'
    assert data['bitbucket_team'] == 'fake78567'
    assert data['github_results']['error'] == True
    assert data['bitbucket_results']['error'] == True

def test_github_failed_call(test_client):
    '''
    Call to just Github API fails
    '''
    response = test_client.get('/merge/fake78567/mailchimp')

    assert response.status_code == 200

    data = json.loads(response.data)
    assert len(data.keys()) == 4
    assert data['github_org'] == 'fake78567'
    assert data['bitbucket_team'] == 'mailchimp'
    assert data['github_results']['error'] == True
    assert data['bitbucket_results'].get('total_original_repos') != None