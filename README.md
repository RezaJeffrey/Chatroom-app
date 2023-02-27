# Chatroom-app #Django
Note: this project is being updated so the clip showing below is a previouse version of the project. Check feature/websockets branch in order to see the new changes.


Real-time chat app where you can create or enter a room and chat with others.
user can create private or normal room . for private room you should add a password so each user who want to join the room should enter a password.

using django channels and websockets makes it possible to display new messages without any need to reload.

<div style="width:720px;max-width:100%;">
  <p><img align="left" alt="gif" src="https://github.com/RezaJeffrey/Chatroom-app/blob/master/ezgif.com-gif-maker%20(1).gif" width="560" height="360"  frameBorder="0" /></p>
  </div>
  

I've been working on back-end of the project so didn't pay attention to the front end and I'm using Bootstrap for the front side.

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


  
