echo "Updating COVID data."
git submodule update --init --recursive
git submodule foreach --recursive git fetch
git submodule foreach git merge origin master
#git pull origin master
echo "Done."
