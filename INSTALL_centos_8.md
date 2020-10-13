Based on the instructions from 
```
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-centos-7
```

# Install dependant packages for Centos 8
```
sudo dnf install epel-release -y
sudo dnf install python3-virtualenv nginx mysql-server python3-pip mysql-devel gcc ufw git unzip -y
```

# For development
## get sigma and runserver
```
git clone https://github.com/charlesflannery73/sigma
cd sigma
python3 -m venv .venv --prompt sigma
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata groups
python manage.py createsuperuser
python manage.py installtasks
python manage.py runserver
```
# For deployment
## Setup MySql
```
sudo systemctl enable mysqld
sudo systemctl start mysqld

# secure installation unnecessary for mysql 5.7 and later. it installs secure by default with no root password, auth_socket login only
# sudo mysql_secure_installation
```
+ validate password component
+ set root password
+ remove anonymous users
+ disallow root login remotely
+ remove test database
+ reload privileges
```
sudo mysql -p

CREATE DATABASE sigma;
CREATE USER 'sigmauser'@'localhost' IDENTIFIED BY 'password_change_me';
GRANT ALL ON sigma.* TO 'sigmauser'@'localhost';
ALTER DATABASE sigma CHARACTER SET 'utf8';
exit;
```
## Create sigmauser
```
sudo adduser sigmauser -g nginx
cat /dev/urandom | tr -dc a-zA-Z0-9 | fold -w 32 | head -n 1 | sudo passwd --stdin sigmauser
sudo chmod 710 /home/sigmauser
sudo su - sigmauser
```

## Install sigma
```
# copy sigma_bundle.zip to sigmauser home dir
unzip sigma_bundle.zip
cd sigma
python3 -m venv .venv --prompt sigma
source .venv/bin/activate
pip install --upgrade pip

# if connected to internet
pip install --upgrade pip
pip install -r requirements.txt

# if offline
pip install --no-index --find-links="~/sigma_packages" -r requirements.txt
```

create .env file
---
```
# create .env file in same dir as sigma/sigma/settings.py

SECRET_KEY=my-super-secret-key-erlksduhiuyhwnci4nu9576w7vtysueh-change-me
DEBUG=False
ALLOWED_HOSTS='*'
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

DB_ENGINE=django.db.backends.mysql
DB_NAME=sigma
DB_USER=sigmauser
DB_PASSWORD=password_change_me
DB_HOST=127.0.0.1
DB_PORT=3306
```

# setup database
```
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata groups
python manage.py collectstatic
python manage.py createsuperuser
```

# setup gunicorn
 switch to root user
## create daemon file
/etc/systemd/system/gunicorn.service
 
suggested number of workers is 2 * n + 1 where n = number of cores

```
[Unit]
Description=gunicorn service
After=network.target

[Service]
User=sigmauser
Group=nginx
WorkingDirectory=/home/sigmauser/sigma/sigma
ExecStart=/home/sigmauser/sigma/.venv/bin/gunicorn --access-logfile - --workers 5 --chdir /home/sigmauser/sigma --bind unix:/home/sigmauser/sigma/sigma.sock sigma.wsgi:application

[Install]
WantedBy=multi-user.target
```
# selinux
edit /etc/selinux/config

set to permissive. Or if you are game, configure it properly to use selinux
````
SELINUX=permissive
````

To change selinux without a reboot run
```
setenforce 0
```

## start gunicorn daemon
```
systemctl daemon-reload
systemctl enable gunicorn
systemctl start gunicorn
systemctl status gunicorn
```

# create self-signed certificate
```
sudo mkdir /etc/ssl/private
sudo chmod 700 /etc/ssl/private
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt
openssl dhparam -out /etc/pki/tls/certs/dhparam.pem 2048
```

# nginx setup
create file /etc/nginx/conf.d/ssl.conf
```
server {
       listen 80 default_server;
       server_name 127.0.0.1;
       return 301 https://$server_name$request_uri;
}

server {
    listen 443 http2 ssl;
    listen [::]:443 http2 ssl;

    server_name 127.0.0.1;

    ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
    ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;
    ssl_dhparam /etc/ssl/certs/dhparam.pem;

    ########################################################################
    # from https://cipherli.st/                                            #
    # and https://raymii.org/s/tutorials/Strong_SSL_Security_On_nginx.html #
    ########################################################################

    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;
    ssl_ciphers "EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH";
    ssl_ecdh_curve secp384r1;
    ssl_session_cache shared:SSL:10m;
    ssl_session_tickets off;
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;
    # Disable preloading HSTS for now.  You can use the commented out header line that includes
    # the "preload" directive if you understand the implications.
    #add_header Strict-Transport-Security "max-age=63072000; includeSubdomains; preload";
    add_header Strict-Transport-Security "max-age=63072000; includeSubdomains";
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;

    ##################################
    # END https://cipherli.st/ BLOCK #
    ##################################

    location /static/ {
         root /home/sigmauser/sigma;
    }

    location /media/ {
         root /home/sigmauser/sigma;
    }

    location / {
         proxy_set_header Host $http_host;
         proxy_set_header X-Real-IP $remote_addr;
         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
         proxy_set_header X-Forwarded-Proto $scheme;
         proxy_pass http://unix:/home/sigmauser/sigma/sigma.sock;
    }
}

```


# comment out the default server block
edit /etc/nginx/nginx.conf
```
#    server {
#        listen       80 default_server;
#        listen       [::]:80 default_server;
#        server_name  _;
#        root         /usr/share/nginx/html;
#
#        # Load configuration files for the default server block.
#        include /etc/nginx/default.d/*.conf;
#
#        location / {
#        }
#
#        error_page 404 /404.html;
#            location = /40x.html {
#        }
#
#        error_page 500 502 503 504 /50x.html;
#            location = /50x.html {
#        }
#    }

```

```
nginx -t
systemctl enable nginx
systemctl start nginx
```

# firewall - allow http/s
```
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --list-all
sudo firewall-cmd --reload
```


Reboot
```
sudo reboot
```
