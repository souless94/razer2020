The future of credit scoring has arrived
==================================================
This repository contains the code for the whole PowerUp project, from experiments on internal and external APIs to the fully functioning app, deployed by AWS Elastic Beanstalk and AWS CloudFormation.

What's here
-----------

The repo contains:

* README.md - this file
* ebdjando - Django configuration files for the front- and back-end
* metascorer - test notebooks for calling game publishers' API and metascore building
* powerup - Django project files
* manage.py - script to start the Django app files

Files provided by the AWS CodeStar platform (copied)

* .ebextensions/ - this directory contains the Django configuration file that
  allows AWS Elastic Beanstalk to deploy the Django app
* buildspec.yml - this file is used by AWS CodeBuild to build and test
  the application
* requirements.txt - this file is used to install Python dependencies needed by
  the Django application
* template.yml - this file contains the description of AWS resources used by AWS
  CloudFormation to deploy the app infrastructure
* template-configuration.json - this file contains the project ARN with placeholders used for tagging resources with the project ID

App URL
-------

**[IMPORTANT] Best viewed on Chrome's inspect tool, with iPhone X view (375px x 812px) (sorry we wanted to replicate the experience of the Razer app).
<br>
It works really well when you inspect it with the iPhone X view**
<br>
http://razer2020app.eba-ppfnb2xn.ap-southeast-1.elasticbeanstalk.com/
