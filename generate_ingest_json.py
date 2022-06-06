from datetime import datetime, timedelta, timezone
from pprint import pprint
import random
import uuid
import json

import requests

token = '<API Token>'
MacrohardId = '<Macrohard Customer ID>'
HamPotId = '<Ham Pot Customer ID>'
CustomerIds = [MacrohardId, HamPotId]


def ingest(events):
    remainder = events
    with open('ingest.json', 'w') as f:
        json.dump(events, f)
    f.close()
    print('success')

def random_monthly_target(n):
    return random.randint(90*n // 720, 110*n // 720)

events = []
for cid in CustomerIds: 
    customerId = cid
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
        if cid == HamPotId:
                append_event('gb_logs_ingested', {
                    "gb_ingested":random_monthly_target(130)
                })
        if cid == MacrohardId:
                user_id = uuid.uuid1().fields[1]
                append_event('user_login', {
                    "user_id": f'"{user_id}"'
                })

        t += timedelta(hours=1)

ingest(events)