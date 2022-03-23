rm db.sqlite3
./manage.py migrate
./manage.py loaddata vendorTypes weddingSizes
./manage.py seed_db
./manage.py loaddata visionPhotos exampleImages