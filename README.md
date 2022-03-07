# Chatroom-app #Django

simple chatroom where you can create or enter a room and chat with others .
user can create private or normal room . for private room you should add a password so each user who want to join the room should enter a password.

I use Django for this project without using websockets .
I've been working on back-end of the project so I didn't pay attention to the front end and I'm using Bootstrap for the front side.

to run the project first fork it and in the terminal cd into root directory were manage.py file is. 
then run :
```
pyhthon manage.py runserver
```
open your browser and enter : 127.0.0.1:8000

migrate changes using:
```
python manage.py makemigrations
```
then:
```
python manage.py migrate
```

make sure to create a super user first to have access to the admin panel.
in your terminal cd into root directory and enter:
```
python manage.py createsuperuser
```

Here's a Gif to see how the app is working:
<div style="width:360px;max-width:100%;"><div style="height:0;padding-bottom:56.39%;position:relative;"><iframe width="360" height="203" style="position:absolute;top:0;left:0;width:100%;height:100%;" frameBorder="0" src="https://imgflip.com/embed/67pvve"></iframe></div><p><a href="https://imgflip.com/gif/67pvve">via Imgflip</a></p></div>
