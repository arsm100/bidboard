from bidboard.billboards.model import Billboard, db

SQLALCHEMY_DATABASE_URI = "postgres://localhost:5432/bidboard"

s = db.session()
objects = [
    Billboard('coolcompany', 'Jalan Cheras, Bulatan Billion', "10' x 40'", 650),
    Billboard('poolcompany', 'Jalan Cendiakawan, Taman Connaught', "10' x 40'", 900)
]
s.bulk_save_objects(objects)
s.commit()
