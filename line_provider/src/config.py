import os

# PostgreSQL
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_NAME = os.environ['DB_NAME']

# RabbitMQ
RMQ_LOGIN = os.environ['RMQ_LOGIN']
RMQ_PASSWORD = os.environ['RMQ_PASSWORD']
RMQ_HOST = os.environ['RMQ_HOST']
RMQ_PORT = os.environ['RMQ_PORT']