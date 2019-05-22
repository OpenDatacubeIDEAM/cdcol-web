# Ariflow Container Server

Build the Docker file to get a Airflow Docker Image.

```sh
docker build -t airflow .
```

Run the container and create a shared volumen to the *airflow* folder in your current directory.

```sh
docker run -it -v ${PWD}/airflow:/home/airflow --name airflow airflow
```

Exit from within container (this proceduce will stop the container)

```sh
exit
```

Once the contianer was created you can start it again with

```sh
docker start -ia airflow
```