#!/usr/bin/env bash
cp -Rf /home/abi/development/ICOM5016/CoquiGames/Client/CGWebApp/* /home/abi/development/production/coquigames/
cd /home/abi/development/production/coquigames/
git add --all
git commit -m "Deploy"
git push heroku master
heroku ps