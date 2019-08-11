# Coding Challenge App

A simple flask app which fetches and merges repository details for similar profiles on GitHub and BitBucket.

## Environment Setup:

Use a Python version 3.6 or higher. (I used Python 3.7.4)

Create and activate virtual environment in project root:
```
python3 -m venv venv
source venv/bin/activate
```

Pip install from the requirements file:
``` 
pip install -r requirements.txt
```

## Starting the Server

In the root directory:
```
python3 -m run
```


## Making Requests

```
curl -i "http://127.0.0.1:5000/health-check"
```

(Or my preferred method, open Chrome and enter the URL there.)


### Available Endpoints

```/health-check``` : Sanity check to make sure server is functioning

```/merge/<github-org>/<bitbucket-team>```
```/merge/<profile>``` : Two endpoints that provide the same information. In the case of differing names
between GitHub and BitBucket, use the first endpoint. In the names are the same, use the latter.

This call will provide a jSON response with at least 4 keys:

```github_org```: Organization name that was queried for Github

```bitbucket_team```: Team name that was queried for BitBucket

```github_results```: Profile results from GitHub. If API call was successful, results will be a 
dictionary with aggregated profile data as well as data about each individual repository. If call was
not successful, results will be a dictionary containing information about the error.

```bitbucket_results```: Profile results from BitBucket. Format same as for ```github_results```.

```merge```: This will only be included in jSON response if both API calls were successful. This will
contain a dictionary with the merged profile data from both API's.

###Example Request & Response

```curl -i "http://127.0.0.1:5000/merge/pygame"```

(Response truncated to conserve space)
```
{
    "bitbucket_results": {
        "languages": {
            "c++": 1,
            "python": 5
        },
        "repo_details": [
            {
                "language": "python",
                "name": "pygame",
                "number_of_watchers": 225,
                "remote_host": "BitBucket",
                "topics": []
            },
            {
                "language": "python",
                "name": "pygamegsoc12",
                "number_of_watchers": 4,
                "remote_host": "BitBucket",
                "topics": []
            }
        ],
        "topics": {},
        "total_forked_repos": 0,
        "total_languages": 2,
        "total_original_repos": 7,
        "total_topics": 0,
        "total_watchers": 245
    },
    "bitbucket_team": "pygame",
    "github_org": "pygame",
    "github_results": {
        "languages": {
            "c": 3,
            "python": 4,
            "ruby": 1
        },
        "repo_details": [
            {
                "language": "C",
                "name": "pygamemirror",
                "number_of_watchers": 2,
                "remote_host": "GitHub",
                "topics": null
            },
            {
                "language": "C",
                "name": "pygamefullmirror",
                "number_of_watchers": 3,
                "remote_host": "GitHub",
                "topics": null
            },
        ],
        "topics": {},
        "total_forked_repos": 0,
        "total_languages": 3,
        "total_original_repos": 8,
        "total_topics": 0,
        "total_watchers": 1415
    },
    "merge": {
        "topics": {},
        "total_forked_repos": 0,
        "total_languages": 5,
        "total_original_repos": 15,
        "total_topics": 0,
        "total_watchers": 1660
        "languages": {
            "c": 3,
            "c++": 1,
            "python": 9,
            "ruby": 1
        },
        "repo_details": [
            {
                "language": "python",
                "name": "pygame",
                "number_of_watchers": 225,
                "remote_host": "BitBucket",
                "topics": []
            },
            {
                "language": "python",
                "name": "pygamegsoc12",
                "number_of_watchers": 4,
                "remote_host": "BitBucket",
                "topics": []
            },
            {
                "language": "C",
                "name": "pygamemirror",
                "number_of_watchers": 2,
                "remote_host": "GitHub",
                "topics": null
            },
            {
                "language": "C",
                "name": "pygamefullmirror",
                "number_of_watchers": 3,
                "remote_host": "GitHub",
                "topics": null
            }
        ]
}
```



## Running Tests

In the root directory:

```pytest```

## What'd I'd like to improve on...

The Bitbucket API doesn't seem to provide information on forked v. original repos, so
I just categorized every repo as original by default. It would be interesting to see if
there's another API (or just something in the existing API that I missed) which provides
this information.

Currently, the ```/merge``` call just returns every repo from both remote sources, and it's up
to the end user to look through the results and figure out the similarities/differences
between the sources. Logic could be added to do this comparison automatically (e.g. these two 
repos have the same name - therefore, maybe they should be merged together).

I added a Blueprint just so I could get the test_client to work; however, in the 
app's current state, Blueprints aren't really necessary. Find a way to setup the test_client
without using a Blueprint.

Add Logging back in (I lost it when I had to restructure routes.py due to aforementioned Blueprint experiment).

Improve unit tests so that they aren't dependent on a static API call.