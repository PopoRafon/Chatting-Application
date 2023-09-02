# Discord Clone
Real-time communication application built using Python with Django framework and Django channels.
## Installation
1. Open up your terminal.
2. If you don't have installed Python run `sudo apt-get update` `sudo apt-get install python3` command on Linux.
3. Also if you don't have installed Redis run `sudo apt-get update` `sudo apt-get install redis` command on Linux.
4. Using `cd (directory path)` command go into directory you want your application to be installed in.
5. In your desired directory run command `git clone https://github.com/PopoRafon/Discord-Clone.git` to install this application.
6. Go into "Discord" directory in your application using `cd Discord-Clone/Discord/` command.
7. Create .env file with secret key running `echo "SECRET_KEY=$(openssl rand -base64 32)" > .env` command. - **REMEMBER TO NEVER SHARE YOUR SECRET KEY WITH ANYONE!**
## Usage
1. Go into your application directory using `cd Discord-Clone/` command.
2. Start your redis server using `sudo service redis-server start` command.
3. Compile your CSS file using `./tailwind/tailwindcss-linux-x64 -i ./static/styles/tailwind.css -o ./static/styles/main.css` command.
4. Now you can run your application using `python3 manage.py runserver` command.
## Features
* Real-time communication using WebSockets.
* Well described API using OpenAPI specifications.