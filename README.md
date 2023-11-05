# quickLister
webApp to list files in directory

---

To run:

1. build image:

> docker build -f dockerfiles/Dockerfile -t list-app .

2. run container with directory mounted to _stuff_:

> docker run -p 8501:8501 -v PATH_TO_DIRECTORY:/code/listerApp/stuff/ list-app

3. open browser at localhost:8501
