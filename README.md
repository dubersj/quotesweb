# Quotes CRUD Application

This is a Flask application that includes everything working up through topic-09-sessions in KSU's Web Development I. One additional feature added is a show-all ability. The front-end has been redeveloped in Bootstrap 5. Some additional functionality is included in code but not currently used, such as the functions needed to hash and check passwords worked on in class. This application is served off an Ubuntu-Server in my home, accessable through:

**http://quotes.steveduber.com**

A lot of time was spent avoiding codespaces to set up a virtual python environment with Flask, Mongita, and Gunicorn as the Web Server Gateway Interface. Traffic is first passed through the Nginx reverse proxy before it reaches the WSGI socket. This is also enabled as a system service.

## quotesweb.service

    [Unit]
    Description=Gunicorn instance to serve quotesweb(flask)
    After=network.target

    [Service]
    User=dubersj
    Group=www-data
    WorkingDirectory=/home/dubersj/quotesweb
    Environment="PATH=/home/dubersj/quotesweb/quoteswebvenv/bin"
    ExecStart=/home/dubersj/quotesweb/quoteswebvenv/bin/gunicorn --workers 4 --bind unix:quotesweb.sock -m 007 --access-  logfile /home/dubersj/gunilog/quotesaccess.log --error-logfile /home/dubersj/gunilog/quoteserror.log wsgi:app

    [Install]
    WantedBy=multi-user.target

## nginx configuration

    server {
      listen      80;
      server_name quotes.steveduber.com;
  
      location / {
        include proxy_params;
        proxy_pass http://unix:/home/dubersj/quotesweb/quotesweb.sock;
      }
    }
