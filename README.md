SecRes
=====

SecRes - site monitor and security profile tool

Install on LAMP stack server to help monitor app and directory contents for
unwanted changes and additions as well as monitor logs for web site performance 
and security issues. 

SETUP INSTRUCTIONS
==================
--TESTED ENVIRONMENT--
Python 2.7.2
djangorestframework-2.3.7
django.VERSION (1, 4, 3, 'final', 0)

--DEPENDENCIES INSTALL INSTRUCTIONS--
easy_install djangorestframework
easy_install django-extensions
easy_install pygments
easy_install django-filter
easy_install mysql-python

Cron
====
Cron Job needs to set up to run JSON script to upload consolidated country data
python manage.py runscript directory_structure