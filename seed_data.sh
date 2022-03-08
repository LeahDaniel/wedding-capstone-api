rm db.sqlite3
./manage.py migrate
./manage.py loaddata vendorTypes
./manage.py loaddata weddingSizes
./manage.py seed_db