# ETL Microservices

This project consists of a set of microservices that handle the ETL process for data ingestion and storage. These services can be deployed independently, scaled horizontally, and be easily integrated into larger pipelines.

## Microservices

The following microservices are included in this project:

- `producer.py`: Streams data from MongoDB and Neo4j to Kafka topics.
- `consumer.py`: Reads data from Kafka topics and stores it in MySQL.

### Python Requirements

- Flask
- kafka-python
- py2neo
- pymongo
- mysql-connector-python
- python-dotenv

## Populate the Databases (MongoDB, Neo4j, MySQL)

Before running the application, you'll need to initialize and populate the databases.

### For MongoDB

Install MongoDB. After installation, you can create a database named `etl_products` and use the `insert_products.mongodb` (inside input directory) file to populate the database with sample data.

### For Neo4j

Install Neo4J. After installation, use the script `insert_users.cypher` (inside input directory) to insert the sample user data and create friendship relationships between them.

### For MySQL

Install MySQL. Then, create a database `relational_db` containing two tables:

- One table named `Products` with columns `ProductID` (varchar, primary key) and `Description` (varchar).
- One table named `Transactions` with columns `Name` (varchar) and `ProductID` (varchar, foreign key).

## Environment Variables

In order to run the application locally, create a .env file inside the project app's directory, which will contain sensitive data such as database credentials, API keys, etc.

For the app to work, it is necessary to add the credentials for neo4j, mongodb, kafka, mysql and the producer and consumer ports. Here's a demonstration example of how the `.env` file should look like:

```
NEO4J_URL = "bolt://127.0.0.1:7687"
NEO4J_USR = "neo4j"
NEO4J_PSWD = "12341234"

KAFKA_URL = "localhost:9092"

MONGODB_URL = "mongodb+srv://your-username:your-password@cluster0.b8y0nwn.mongodb.net/?retryWrites=true&w=majority"

PRODUCER_PORT = 5001
CONSUMER_PORT = 5002

MYSQL_USR = "root"
MYSQL_PSWD = "your-mysql-password"
MYSQL_URL = "localhost"
```

## Usage

### Running the Producer

The producer can be started by running the following command in the root directory of the project:

```
python producer.py
```

The producer exposes two endpoints that stream data to Kafka topics:

- `POST /stream_collection`: Streams all documents from a specified collection in MongoDB to the corresponding Kafka topic.
- `POST /stream_user`: Streams a user and their friends from Neo4j to the users Kafka topic.

### Running the Consumer

The consumer can be started by running the following command in the root directory of the project:

```
python consumer.py
```

The consumer exposes an endpoint that reads data from Kafka topics and stores it in MySQL:

- `POST /store_data`: Reads data from a specified Kafka topic and stores it in the corresponding table in MySQL.

### Making the Requests

You can use Postman to make requests to the exposed endpoints. The body of each request should be in JSON format and look like the following examples:

Example request for `/stream_collection`:

```
{
    "collection": "Laptops"
}
```

Example request for `/stream_user`:

```
{
    "user": "Igor"
}
```

Example request for `/store_data`:

```
{
    "user": "Alice",
    "collection": "Wearables"
}
```
