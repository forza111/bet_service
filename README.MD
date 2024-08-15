## Start of microservices

terminal_1: `docker-compose -f rabbitmq/docker-compose.yaml up`  
terminal_2: `docker-compose -f line_provider/docker-compose.yaml up`  
terminal_3: `docker-compose -f bet_maker/docker-compose.yaml up`  

## Usage

line_provider SWAGGER: http://127.0.0.1:8000/docs  
bet_maker SWAGGER: http://127.0.0.1:8001/docs