#From project root directory
cd Client/deploy
git init
git add .
git commit -m "deploy 1"
heroku git:remote -a coquigames
git config --global push.default simple
git push --set-upstream heroku master
rm -fr .git
