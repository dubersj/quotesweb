# Quotes CRUD Application

This is a Python Flask application that includes everything working up through topic-09-sessions in KSU's Web Development I. Two features added are a show-all ability, and a quote deletion confirmation. The front-end has been redeveloped in Bootstrap 5. Some additional functionality is included in code but not currently used, such as the functions needed to hash and check passwords worked on in class. To prepare the application to accept password logins, I had CertBot install a SSL certificate issued by LetsEncrypt. This application is served off an Ubuntu-Server in my home, accessable through:

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
    listen 443 ssl; # managed by Certbot
    server_name quotes.steveduber.com;

    ssl_certificate /etc/letsencrypt/live/quotes.steveduber.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/quotes.steveduber.com/privkey.pem; # managed by Certbot

	location / {
        include proxy_params;
        proxy_pass http://unix:/home/dubersj/quotesweb/quotesweb.sock;
    }

    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

    }
    server {
        if ($host = quotes.steveduber.com) {
            return 301 https://$host$request_uri;
        } # managed by Certbot

	    listen      80;
        server_name quotes.steveduber.com;
        return 404; # managed by Certbot
    }
