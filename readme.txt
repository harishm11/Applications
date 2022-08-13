install python3, nginx, postgresql, postgresql-contrib
pip install django, gunicorn, postgresql, psycopg2, pgadmin

===================webserver and wsgi===================w

gunicorn -c  /Users/harishmurali/Pythonprojects/Project/conf/gunicorn_congig.py myproj.wsgi &


brew install nginx
      brew services start nginx        --to start webserver
      brew services stop nginx        --to stop webserver


which nginx --to get path and use it below
export PATH=$PATH:/usr/local/bin/nginx

brew services start nginx        --to start webserver

mkdir -p /usr/local/etc/nginx/sites-{enabled,available}
cd /usr/local/etc/nginx/sites-enabled
ln -s ../sites-available/default.conf
ln -s ../sites-available/default-ssl.conf

brew services restart nginx

ps ax|grep gunicorn
kill -9 <pid>

===================dbserver===================

brew install postgresql
install pgadmin
create server group and server in pgadmin

brew services start postgresql  - --to start dbserver

