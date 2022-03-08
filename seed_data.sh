rm db.sqlite3
./manage.py migrate
./manage.py loaddata users
./manage.py loaddata vendorTypes weddingSizes tokens 
./manage.py loaddata hosts vendors
./manage.py seed_db