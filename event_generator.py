from datetime import datetime
import random
import uuid
import json

events = ["view", "buy", "error"]
pages = ["home", "about", "classes", "careers"]
error_codes = [400, 401, 403, 404, 500, 502, 503, 504]


def make_one_event():
    timestamp = datetime.now()
    e = random.choice(events)
    user_id = str(uuid.uuid1())
    event = {"created_at": timestamp,
             "user_id":  user_id,
             "event_type": e}
    if e == "view":
        page = random.choice(pages)
        if page == "classes":
            class_n = random.randint(1,10)
            page = f"class_{str(class_n)}"
        event["page"] = page
    elif e == "buy":
        class_n = random.randint(1,10)
        purchase = f"class_{str(class_n)}"
        event["purchase"] = purchase
    elif e == "error":
        event["code"] = random.choice(error_codes)

    return event

def make_events(n: int) -> list[dict]:
    return [make_one_event() for _ in range(n)]

def main():
    from db import insert_events
    events = make_events(100)
    insert_events(events)

if __name__ == "__main__":
    main()