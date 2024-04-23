## How to test the Docker version service 

`docker build -t my_image .`

`docker run -p 8000:8080 --env-file ./.env my_image`

## Poetry Dependence Management

1. update the latest `requirements.txt` to pyproject.toml

`cat requirements.txt | xargs poetry add`