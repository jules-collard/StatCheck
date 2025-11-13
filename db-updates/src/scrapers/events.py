import requests

from .. import BACKEND_URL

def post_event_types():
    event_type_dicts = [
        {'typeCode': 502, 'typeDescKey': 'faceoff'},
        {'typeCode': 503, 'typeDescKey': 'hit'},
        {'typeCode': 504, 'typeDescKey': 'giveaway'},
        {'typeCode': 505, 'typeDescKey': 'goal'},
        {'typeCode': 506, 'typeDescKey': 'shot-on-goal'},
        {'typeCode': 507, 'typeDescKey': 'missed-shot'},
        {'typeCode': 508, 'typeDescKey': 'blocked-shot'},
        {'typeCode': 509, 'typeDescKey': 'penalty'},
        {'typeCode': 516, 'typeDescKey': 'stoppage'},
        {'typeCode': 520, 'typeDescKey': 'period-start'},
        {'typeCode': 521, 'typeDescKey': 'period-end'},
        {'typeCode': 523, 'typeDescKey': 'shootout-complete'},
        {'typeCode': 524, 'typeDescKey': 'game-end'},
        {'typeCode': 525, 'typeDescKey': 'takeaway'},
        {'typeCode': 535, 'typeDescKey': 'delayed-penalty'},
        {'typeCode': 537, 'typeDescKey': 'failed-shot-attempt'}
    ]
    r = requests.post(f"{BACKEND_URL}/games/event-types", json=event_type_dicts)
    print(r.status_code)

if __name__ == "__main__":
    post_event_types()