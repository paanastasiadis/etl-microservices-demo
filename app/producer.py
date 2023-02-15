from kafka import KafkaProducer
from pymongo import MongoClient
from flask import Flask, jsonify, request, make_response
from py2neo import Graph
from bson import json_util
import json
from dotenv import load_dotenv
import os
import topics
# enable reading from .env
load_dotenv()


# establish a connection with mongo db
client = MongoClient(
    os.getenv("MONGODB_URL"), serverSelectionTimeoutMS=5000)

# get access to our database
db = client.get_database("etl_products")

# get access to neo4j
graph = Graph(os.getenv("NEO4J_URL"), auth=(
    os.getenv("NEO4J_USR"), os.getenv("NEO4J_PSWD")))

# create a Kafka producer
producer = KafkaProducer(bootstrap_servers=os.getenv("KAFKA_URL"),
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# creates Flask instance
app = Flask(__name__)

# streams the documents of a requested collection to specific topic using Kafka producer
@app.route('/stream_collection', methods=['POST'])
def stream_products():
    request_json = request.get_json()
    collection_name = request_json['collection']

    # get the kafka topic which corresponds to the requested collection name
    topic = topics.get_collection_topic(collection_name)

    response_data = []

    if topic is not None:
        collection = db[collection_name]
        for doc in collection.find():
            # convert document to json format
            json_data = json_util.dumps(doc)
            # fill the response array
            response_data.append(json_data)
            print(json_data)

            # send document to the topic
            producer.send(topic, json_data)
            # producer.flush()
    else:
        return make_response("404 No such collection found", 404)
    return jsonify(response_data)

# streams requested user and their friends to specific topic using Kafka producer


@app.route('/stream_user', methods=['POST'])
def stream_users():
    request_data = request.get_json()

    # query that gets the requested user and their friends from neo4j db
    result = graph.run(
        "MATCH (u:User { name: $name })-[:FRIEND_WITH]->(f) RETURN u, f", name=request_data['user'])

    users = {}
    users["friends"] = []
    
    # var to ensure seperation from user and the friends
    isUserAdded = False
    for record in result:
        # append user to the array
        if isUserAdded is False:
            users["user"] = {"name": record["u"].get(
                'name'), "products": record["u"].get('products')}
            isUserAdded = True
        # append the friends to the array
        if record.get("f"):
            users["friends"].append({"name": record["f"].get(
                'name'), "products": record["f"].get('products')})
    
            
    if isUserAdded == False:
        return make_response("404 No user found", 404)    
    print(users)

    # stream the data
    producer.send(topics.USERS_TOPIC, users)
    # producer.flush()

    return jsonify(users)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PRODUCER_PORT"))