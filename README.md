# Minecraft servers

## Description

This is a neat little project to run multiple Minecraft servers on one machine using docker.

Each container keeps the server in an off state, listening for connections. Once a user sends a request (by joining the server or using the web service), the main Minecraft server is turned on, so the user needs to wait 1-2 minutes to join the loaded world. The server shuts down automatically when no players are online to save power and resources.

## How to use

Bellow is a step-by-step guide on how create your own Minecraft server.

### Prerequisites

#### IDE

Whole process can be done in terminal, but it is recommended to use IDE like [Visual Studio Code](https://code.visualstudio.com/).

#### Directory structure

Create a directory for your server and create `docker-compose.yml` file in it. This file will be used to configure your server. You can also create `files` directory in your server directory, but it is not required - it will be created automatically.

```bash
mkdir myserver
cd myserver
touch docker-compose.yml
```

### Docker

#### Images

Main Dockerfile is located in `docker` directory. It is used to create base image for Minecraft server. You can use it to create your own image using commands in `docker/README.md` file. Make sure you aren't overriding existing images. Do only if you know what you are doing!

#### Compose file

It is recommended to use `docker-compose` to run your server. It can be done using `docker run` command, but it is not recommended. Compose file is more readable and easier to use.

Here is an example of `docker-compose.yml` file for base Minecraft server.

```yaml
services:
  mc: 
    image: minecraft # Image name - make sure you create it first
    ports:
      - 25565:25565 # Minecraft server port
      - 8080:80 # Web service port
    environment:
      VERSION: 1.20.1
      MEMORY: 5G
      DIFFICULTY: normal
      WEBPORT: 80 # Web service port - must be the same as in ports, if you want to use web service
    tty: true
    stdin_open: true
    restart: unless-stopped
    volumes:
      - ./files:/data # Server files
```

For more examples, visit examples directory.

For more information about `docker-compose` file, visit [docker-compose reference](https://docs.docker.com/compose/compose-file/).

### Start server

To start server, run `docker-compose up -d` command in your server directory. 

But before that, you need to make sure that your server is working properly. To do that, run `docker-compose up` command. Container will start, and you will see logs in your terminal. If everything is working properly, you can stop the container using `Ctrl+C` and start it in background using `docker-compose up -d` command. For better debug is recommended to use web service to start your server.

### Possible problems

#### Port already in use

Make sure that you don't have any other Minecraft server running on this port. If you do, you can change ports in `docker-compose.yml` file. You can check used ports using `docker ps` command.

#### Wrong java version

Older or modded servers may require older java version. You can change java version in `Dockerfile` file. Make sure you are using image with correct java version. If you need java, but its image is not build, you can create it using commands in `docker/README.md` file.

#### Missing or not working mods

When using `AUTO_CURSEFORGE` option, it's possible that's some mods going to be missing (some authors forbid downloading their mods automatically). After first startup, there's going to be a file that contains all missing mods. You can download them manually and put them in `files/mods` directory. After that, you can relaunch your server, and it should work.

When mod is not working, it's possible that it's not compatible with server. Check if mod isn't client-side only. If it's not, change java version or try to remove the mod. But remember, that some mods are required for server to work properly.

#### Cannot access a files directory

Check your directory permissions using `ls -l` - it should look like `drwxrwxrwx` - if not use `sudo chmod 777 -R directory_name`


#### Other problems

If you have any other problems, please read documentations of used projects, it may help you. If not, contact me.

## Console

To open server console, run `console.py` script.

```bash
sudo python3 config/console.py
```

You can pass container name as argument, or you will be asked to choose one.

## Sources

All credits go to these projects:

- [mcsleepingserverstarter](https://github.com/vincss/mcsleepingserverstarter)
- [docker-minecraft-server](https://github.com/itzg/docker-minecraft-server)
- [docker-autoheal](https://github.com/willfarrell/docker-autoheal)