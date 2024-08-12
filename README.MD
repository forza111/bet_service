## Start of microservices

docker-compose -f rabbitmq/docker-compose.yaml up   
docker-compose -f line_provider/docker-compose.yaml up  
docker-compose -f bet_maker/docker-compose.yaml up  

## Usage

line_provider SWAGGER: http://127.0.0.1:8000/docs  
bet_maker SWAGGER: http://127.0.0.1:8001/docs