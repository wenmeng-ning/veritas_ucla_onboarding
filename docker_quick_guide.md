# Docker Quick Guide

Docker is a very lightweight yet powerful tool to help create completely isolate units (docker containers), each of which encapsulates the entire environment along with all the needed applications and their dependencies. Docker helps eliminate the problems caused by difference in versions and operation systems and make sure everything runs under consistent conditions.



## Docker Images

There are docker images that are ready to use on the UCLA gamma cluster! You can check the docker images by running 

```shell
docker images
```



You can refer to these docker images by either the image ID or the repo and tag. For example, you can both refer to the docker image by `333121b9bc36` or by `vegas_nancy:v2510`.



You can also check what is inside the docker image by

```shell
docker inspect <imageid>
```





## Running Docker

You can go into each docker image and run things inside the container by running

````shell
docker run -it <imageid> bash
````



Or you can run it in command line by running

```shell
docker run --rm --user `id -u`:`id -g` -v <path_to_data>:<path_in_container> <imageid> /bin/bash -c ‘command’
```

