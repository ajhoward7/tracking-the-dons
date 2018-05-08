import json

from constants import ALL_ACTS_JSON


def get_ids():
    ''' gets list of ids from all the activities '''
    with open(ALL_ACTS_JSON) as f:
        activities = json.load(f)
    return [a['id'] for a in activities]