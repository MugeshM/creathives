#!/bin/bash
set -e
clear
echo -e "\nEnter Virtual Environment path (Default is /media/mugesh/Extra/STUDIES/Internship/newenv): ";
read env;
env=${env:-"/media/mugesh/Extra/STUDIES/Internship/newenv"};
echo $env/bin/activate;
source $env/bin/activate;

echo -e  "\nLets remove existing enabled sites : ";
sudo rm -v /etc/nginx/sites-enabled/* || true;

echo -e "\nList of available sites : ";
ls /etc/nginx/sites-available/;

echo -e "\nEnter a site name to activate it (Default is creathives): ";
read site;
site=${site:-"creathives"};

cd /etc/nginx/sites-available/;

if [ -e "$site" ]
then
	sudo rm /etc/nginx/sites-available/$site || true;
else
  echo "";
fi
cd;
echo -e "\nEnter project path (Default is /media/mugesh/Extra/STUDIES/Internship/Django/Creathives): ";
read project_path;
project_path=${project_path:-"/media/mugesh/Extra/STUDIES/Internship/Django/Creathives"};
sudo sh -c "echo '127.0.0.1 $site.com' >> /etc/hosts";
sudo sh -c "echo 'server {
  listen 80;
  server_name $site.com;
  location = /favicon.ico { access_log off; log_not_found off; }
  location /static/ {
      alias $project_path/static/;
  }

  location / {
      proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
      proxy_set_header Host \$http_host;
      proxy_redirect off;
      proxy_pass http://127.0.0.1:8000;
  }
}' >> /etc/nginx/sites-available/$site";

echo -e "\nSite domain is $site.com";
sudo ln -s /etc/nginx/sites-available/$site /etc/nginx/sites-enabled/;

echo -e "\nSite enabled is :";
ls /etc/nginx/sites-enabled/;

echo -e "\nExporting path for poject : ";
export PYTHONPATH=$project_path;
export DJANGO_SETTINGS_MODULE=main.settings.development;

sudo service nginx restart;
gunicorn --timeout=7200 --bind 127.0.0.1:8000 main.wsgi:application --reload;
