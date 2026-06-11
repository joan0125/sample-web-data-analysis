import mysql.connector
import os
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt

load_dotenv()

with mysql.connector.connect(
    host = os.environ.get("DB_HOST", "localhost"),
    user = "root",
    password = os.environ.get("DB_PASSWORD"),
    database = "web_data",
) as conn:
    os.makedirs("output", exist_ok=True)

    # 첫번째 쿼리: 이벤트 타입별 발생 횟수
    events_count = pd.read_sql("""
        SELECT event_type, COUNT(*) AS count
        FROM events
        GROUP BY event_type
        ORDER BY count DESC
    """, conn).set_index("event_type")["count"]
    plt.figure()
    events_count.plot(kind = "bar")
    plt.title("Event Occurrence Count")
    plt.xlabel("Event Type")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("output/events_count.png")

    # 두번째 쿼리: 수업별 구매 개수 / 비율
    purchases = pd.read_sql("""
        SELECT purchase, COUNT(*) AS count
        FROM events
        WHERE event_type = 'buy'
        GROUP BY purchase
        ORDER BY count DESC
    """, conn).set_index("purchase")["count"]
    plt.figure()
    purchases.plot(kind = "bar")
    plt.title("Class Purchase Count")
    plt.xlabel("Class Number")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("output/purchases_count.png")

    plt.figure()
    plt.pie(purchases, 
            labels = purchases.index, 
            autopct = "%1.1f%%", 
            startangle = 90)
    plt.axis("equal")
    plt.title("Class Purchase Proportions")
    plt.savefig("output/purchases_ratio.png")

    # 세번째 쿼리: 시간대별 이벤트 추이
    hourly = pd.read_sql("""
        SELECT HOUR(created_at) AS hour, COUNT(*) AS count
        FROM events
        GROUP BY hour
        ORDER BY hour
    """, conn).set_index("hour")["count"].reindex(range(24), fill_value=0)
    plt.figure()
    hourly.plot(kind = "line")
    plt.title("Hourly Event Count")
    plt.xlabel("Hour (0-23)")
    plt.ylabel("Count")
    plt.xticks(range(24))
    plt.tight_layout()
    plt.savefig("output/hourly_events.png")

    # 네번째 쿼리: 페이지별 조회 횟수
    viewed = pd.read_sql("""
        SELECT page_name, COUNT(*) AS count
        FROM events
        WHERE event_type = 'view'
        GROUP BY page_name
        ORDER BY count DESC
    """, conn).set_index("page_name")["count"]
    plt.figure()
    viewed.plot(kind = "bar")
    plt.title("Views per Page")
    plt.xlabel("Pages")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("output/page_views.png")


