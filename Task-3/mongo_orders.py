from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URL"))

db = client["week2-task-3"]

collection = db["order_events"]

events = [
    { "customer_id":1, "product":"Laptop", "quantity": 2, "total_amount": 100000 },
    { "customer_id":2, "product":"Mobile", "quantity": 5, "total_amount": 200000 },
    { "customer_id":3, "product":"Mouse", "quantity": 3, "total_amount": 10000 },
    { "customer_id":4, "product":"Laptop", "quantity": 2, "total_amount": 150000 },
    { "customer_id":5, "product":"Keyboard", "quantity": 1, "total_amount": 100000 }
]

result = collection.insert_many(events)

print("Inserted:", len(result.inserted_ids))

pipeline = [
    {
        "$group":{
            "_id":"$customer_id",
            "total_sales":{
                "$sum": "$total_amount"
            },
            "total_orders":{
                "$sum": 1
            }
        }
    },
    {
        "$sort":{
            "_id":1
        }
    }
]

result = collection.aggregate(pipeline)

print("\nTotal per customer")

for data in result:
    print(data)

client.close()