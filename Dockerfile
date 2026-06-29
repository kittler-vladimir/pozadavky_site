FROM debian:bullseye

RUN apt-get update
RUN apt-get install -y locales vim mc python3 python3-django python3-psycopg2 uwsgi uwsgi-plugin-python3 nginx
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
RUN echo "cs_CZ.UTF-8 UTF-8" >> /etc/locale.gen
RUN locale-gen

ENV LANG="cs_CZ.UTF-8"

RUN mkdir -p /www/dp2_site
COPY dp2_site /www/dp2_site/dp2_site
COPY static /www/dp2_site/static
COPY templates /www/dp2_site/templates
COPY manage.py /www/dp2_site
COPY conf/uwsgi/dp2_site.ini /etc/uwsgi/apps-available/dp2_site.ini
RUN ln -s /etc/uwsgi/apps-available/dp2_site.ini /etc/uwsgi/apps-enabled/dp2_site.ini
COPY conf/nginx/dp2_site.conf /etc/nginx/sites-available/dp2_site
RUN ln -s /etc/nginx/sites-available/dp2_site /etc/nginx/sites-enabled/dp2_site
RUN rm -f /etc/nginx/sites-enabled/default
RUN ln -s /www/dp2_site/manage.py /usr/bin/manage-dp2_site

RUN mkdir /www/dp2_site/static_all
RUN manage-dp2_site collectstatic

# Zajistit spusteni uwsgi a nginx po restartu (mel by Debian udelat sam)