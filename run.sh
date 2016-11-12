echo Removing existing docker images:

docker rm -f $(docker ps -a | grep decipher | awk -F" " '{print $1}')

echo Building and launching new images:

docker build -t decipher:v1 .
docker run -d -p 8080:8080 decipher:v1