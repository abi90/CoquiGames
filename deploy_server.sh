#!/usr/bin/env bash
cp -Rf /home/abi/development/ICOM5016/CoquiGames/Server/CGWebServiceApi/* ~/development/production/cgwsapi/
cd /home/abi/development/production/cgwsapi
rm -r *.pyc
git add --all
git commit -m "Deploy"
git push heroku master
heroku ps