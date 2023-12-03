# Chatting Application
Real-time chatting application to chat with your friends built with Python and Django.
## Requirements
1. You need to have git installed if you don't run `apt-get install git` command in your console on Linux or download git from official page https://git-scm.com/downloads.
2. You also need to have Python >= 3.6 installed if you don't run `sudo apt-get update` `sudo apt-get install python3` command in your console on Linux or download python from official page https://www.python.org/downloads/.
3. (**OPTIONAL**) If you want to have Redis as your channel layer (**RECOMMENDED**) run `sudo apt-get update` `sudo apt-get install redis` command in your console on Linux or download redis from official page https://redis.io/download/.
4. (**OPTIONAL**) If you want to use MySQL as your database install it from mysql official page https://dev.mysql.com/downloads/.
## Installation and Configuration
1. Open up your console.
2. Using `cd (directory path)` command go into directory you want your application to be installed in.
3. In your desired directory run command `git clone https://github.com/PopoRafon/Chatting-Application.git` to install this application.
4. Run command `cd Chatting-Application/` to go into your application directory.
5. In your application directory run `python3 -m venv env` command to create virtual environment for your Python modules.
6. Open your virtual environment by running command `source env/bin/activate` on Linux or `env\scripts\activate.bat` on Windows.
7. In your virtual environment install all dependencies by running command `pip install -r requirements.txt`.
8. Go into "Chatting" directory in your application using `cd Chatting/` command.
9. Create `.env` file with secret key running `echo "SECRET_KEY=$(openssl rand -base64 32)" > .env` command. **REMEMBER TO NEVER SHARE YOUR SECRET KEY WITH ANYONE!**
10. If you are using MySQL in your "Chatting" directory rename `myexample.cnf` file to `my.cnf`.
11. Edit your `my.cnf` file **BE CAREFUL NOT TO EXPOSE YOUR CREDENTIALS!**
- set `database` to your database name
- set `user` to your MySQL username
- set `password` to your database password
12. If you are using Redis or MySQL you need to open `settings.py` file in your "Chatting" directory and change settings in section `Django Channels` and `Database` with information provided there.
13. Install Tailwind standalone CLI to be able to compile your CSS file from https://github.com/tailwindlabs/tailwindcss/releases/tag/v3.3.3 and put it in tailwind directory.
14. Go into tailwind directory using `cd (directory path)` and run `./(tailwind executable file name) -i ../static/styles/tailwind.css -o ../static/styles/main.css` command to compile your CSS file.
15. Go into your main directory with `manage.py` file using `cd (directory path)` command.
16. In your main directory with `manage.py` file run commands `python3 manage.py makemigrations` and `python3 manage.py migrate` to apply necessary changes to your database.
17. To ensure everything works fine in your main directory with `manage.py` file run command `python3 manage.py runserver` to start server.
18. If no error messages appear in your console then everything works fine.
## Usage
1. Go into your application directory using `cd (directory path)` command.
2. If you are using Redis as channel layer run `sudo service redis-server start` command.
3. Now you can run your application using `python3 manage.py runserver` command.
## Features
* Real-time communication using WebSockets.
* Well described API using OpenAPI specifications with many endpoints to play with.
* Tests providing convenient way to debug your application.
* Fully responsive user interface. 
## Testing
If you want to test your application you can run `python3 manage.py test` command in your application main directory. Also you can create your own tests in each of the "tests" directories.
## Author
* [PopoRafon](https://github.com/PopoRafon)