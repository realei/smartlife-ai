# How to test the Docker version service 

`docker build -t my_image .`

`docker run -p 8000:8080 --env-file ./.env my_image`