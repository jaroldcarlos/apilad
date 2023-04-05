#!/bin/bash
echo
echo Pulling git changes
echo
cd src
git reset --hard
git pull origin master
echo
echo Restarting GUNICORN
echo
sudo systemctl restart gunicorn
echo Done
