from datetime import datetime, timedelta, timezone
from pprint import pprint
import random
import uuid

import requests

token = '<API_TOKEN>'
customerId = '<Customer ID>'

def ingest(events):
    remainder = events
    while len(remainder) > 0:
        pprint(remainder[:100])

        response = requests.post(
            "https://api.metronome.com/v1/ingest",
            headers={
                "Authorization": f"Bearer {token}",
            },
            json=remainder[:100]
        )

        if response.status_code != 200:
            print(f'ERROR {response.status_code}: {response.text}')
        remainder = remainder[100:]

def random_monthly_target(n):
    return random.randint(90*n // 720, 110*n // 720) / 100

events = []
t = datetime.now(timezone.utc) - timedelta(days=33)
while t < datetime.now(timezone.utc):
    def append_event(event_type, properties):
        events.append({
            "transaction_id": uuid.uuid4().hex,
            "timestamp": t.isoformat(),
            "event_type": event_type,
            "customer_id": customerId,
            "properties": properties,
        })

    append_event('user_activity', { # SUM(run_time_hrs)
        "machine_type": random.choice(["m5.4xlarge", "m5.8xlarge", "c5n.9xlarge","c5n.4xlarge"]),
        "run_time_hrs":random_monthly_target(300)
    })

    append_event('dataset_heartbeat', { # SUM(dataset_num)
        "dataset_num":random_monthly_target(130)
    })
    
    append_event('cloud_storage_heartbeat', { # MAX(gigabyte_months)
        "gigabyte_months":random_monthly_target(100)
    })

    append_event('query', { # COUNT()
    })

    append_event('user_login', { # COUNT()
        "user_id": random.choice(["OliveYew@metronome.com", "AidaBugg@metronome.com", "MaureenBiologist@metronome.com"])   
    })

    t += timedelta(hours=1)

ingest(events)