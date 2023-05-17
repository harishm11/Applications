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


====================DB backup in json==========

dumpdata command:

Usage: python manage.py dumpdata [app_label] [options]
Description: This command serializes the data from the database into JSON format and prints it to the console or writes it to a file.
Arguments:
[app_label]: Optional. Specifies the app label of the app whose data you want to dump. If not provided, all installed apps' data will be dumped.
Options:
--output: Specifies the output file to write the serialized data. Example: --output=data.json.
--indent: Specifies the number of spaces used for indentation in the output. Example: --indent=4.


loaddata command:

Usage: python manage.py loaddata fixture [fixture ...]
Description: This command reads the serialized data from JSON fixture files and loads it into the database.
Arguments:
fixture: The path to one or more fixture files to load into the database.
Options:
--database: Specifies the database to load the data into, if you have multiple databases configured.
--ignorenonexistent: Ignores fixture files that don't exist, instead of raising an error.
Example usage:

Dumping data:

Dump all data to the console: python manage.py dumpdata
Dump data for a specific app: python manage.py dumpdata myapp
Dump data to a file: python manage.py dumpdata --output=data.json
Dump data with indentation: python manage.py dumpdata --indent=4
Loading data:

Load data from a fixture file: python manage.py loaddata data.json
Load data into a specific database: python manage.py loaddata data.json --database=mydb
Ignore nonexistent fixture files: python manage.py loaddata data.json --ignorenonexistent
Note: The dumpdata command serializes data in JSON format by default, but you can use the --format option to specify other formats like XML or YAML if you have the required dependencies installed.

==================Django application =========

Repository : https://github.com/harishm11/Applications.git


-	git clone https://github.com/harishm11/Applications.git
-	cd Applications

	 Create Virtual Env 
-	virtualenv myenv 
Activate Virtual Env
-	source env/bin/activate
-	pip install <packages>


-	python manage.py makemigrations
-	python manage.py migrate
-	python manage.py runserver
-	
Ratemanager – 


PDF – excel – exhibts and ROC

1.	Transformation of exhibits into required format 
2.	Upload the file with exhibits based on state and company( PDF can different company’s/carriers and states ) – reuse current. 
3.	Put these exhibits into tables (create the models and push the data) – reuse current
4.	We should be able to view these tables – UI 
 
This should have filter by 
a.	State.
b.	Product
c.	Exhibits


===============Django project setup:

a.	Create a project 
– django-admin startproject <projectname>
b.	Make the project a git repository and push to github.
c.	Create apps 
– manage.py startapp <appname>
d.	Create the folders as needed and as shown in the project structure.
e.	Create superuser 
– manage.py createsuper 
f.	Update project settings to link to postgressql DB

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'NAME' :,
        'USER' :,
        'PASSWORD':,
        'HOST':,
        'PORT' :,

    }
}
g.	Migrate admin tables in Django to postgres 
– manage.py migrate
h.	Start the application 
– manange.py runserver

=============React App setup:
a.	Create a React app 
– npx create-react-app frontend
b.	Create react app build
-- npm run build
c.	Copy the app into Django project and integrate following
a.	Templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [BASE_DIR / 'templates'],
        'DIRS': [
            os.path.join(BASE_DIR,'frontend/build')
        ],

b.	static files.
	STATICFILES_DIRS =[
    	os.path.join(BASE_DIR,'frontend/build/static'),]
