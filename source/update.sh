git submodule update --init --recursive
git submodule foreach --recursive git fetch
git submodule foreach git merge origin master
git pull origin master
python ../source/update_populations_un.py
