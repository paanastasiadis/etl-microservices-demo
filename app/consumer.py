import json
from kafka import KafkaConsumer
import mysql.connector
from flask import Flask, jsonify, request, make_response
from dotenv import load_dotenv
import os
import topics

# enable reading from .env
load_dotenv()

# insertion queries
PRODUCTS_QUERY = "INSERT IGNORE INTO Products (ProductID, Description) VALUES (%s, %s)"
USERS_QUERY = "INSERT IGNORE INTO Transactions (Name, ProductID) VALUES (%s, %s)"


# creates Flask instance
app = Flask(__name__)

# establish a connection with MySQL
cnx = mysql.connector.connect(user=os.getenv("MYSQL_USR"),
                              password=os.getenv("MYSQL_PSWD"),
                              host=os.getenv("MYSQL_URL"),
                              database='relational_db')
# creates a mysql cursor
cursor = cnx.cursor()

# stores user and his products to mysql db


def add_transaction(user, products):
    for product in products:
        values = (user, product)
        cursor.execute(USERS_QUERY, values)
    cnx.commit()

# stores users to mysql Transactions table


def store_users(user):
    print(user["user"])

    # store user to db
    add_transaction(user["user"]["name"], user["user"]["products"])
    # store the friends of user to db
    for friend in user["friends"]:
        add_transaction(friend["name"], friend["products"])


# stores collection to mysql Products table
def store_products(products):
    print(products)
    values = (products["productID"], products["description"])
    cursor.execute(PRODUCTS_QUERY, values)
    cnx.commit()

# search in kafka topics for the specified user
# and collection and store them to mysql db


@app.route('/store_data', methods=['POST'])
def store_data():

    request_data = request.get_json()

    requested_topic = topics.get_collection_topic(request_data["collection"])

    # create a kafka consumer
    consumer = KafkaConsumer(
        requested_topic,
        topics.USERS_TOPIC,
        bootstrap_servers=os.getenv("KAFKA_URL"),
        auto_offset_reset="earliest",
        # enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')))


    # poll messages from the subscribed topics
    msg = consumer.poll(1000)

    if not msg:
        return make_response("No data were streamed", 400)

    for topic_partition, messages in msg.items():
        if topic_partition.topic == requested_topic:
            # search inside the specified topic
            for message in messages:
                store_products(json.loads(message.value))
        elif topic_partition.topic == topics.USERS_TOPIC:
            # search inside users topic for the specified user
            for message in messages:
                if request_data["user"] == message.value["user"]["name"]:
                    store_users(message.value)

    consumer.close()
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(port=os.getenv("CONSUMER_PORT"))
