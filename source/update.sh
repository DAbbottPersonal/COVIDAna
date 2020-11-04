git submodule update --init --recursive
git submodule foreach --recursive git fetch
git submodule foreach git merge origin master
#git pull origin master
python $DABBOTTCOVID/source/update/update_populations_un.py
python $DABBOTTCOVID/source/update/update_economy_un.py
python $DABBOTTCOVID/source/update/update_education_un.py
