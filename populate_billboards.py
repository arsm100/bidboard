from bidboard.billboards.model import Billboard, db

SQLALCHEMY_DATABASE_URI = "postgres://localhost:5432/bidboard"

s = db.session()
objects = [
    Billboard('coolcompany', 'Jalan Cheras, Bulatan Billion', "10' x 40'", 650),
    Billboard('poolcompany', 'Jalan Cendiakawan, Taman Connaught', "10' x 40'", 900),
    Billboard('toolcompany', 'Taman Connaught, Jalan Bandar Tun Razak', "10' x 40'", 1300),
    Billboard('boolcompany', 'Jalan Cheras berhampiran Stesen BHP', "10' x 40'", 100),
    Billboard('woolcompany', 'Jalan Damansara, Pusat Sains Negara', "10' x 40'", 750),
    Billboard('nutri.ly', 'Jalan Loke Yew, Bulatan Cheras', "10' x 40'", 800),
    Billboard('bitly', 'Bulatan Pahang,berhampiran HKL', "10' x 40'", 850),
    Billboard('nutly', 'Bulatan Pahang, berdekatan Maktab Perguruan Sri Kota', "10' x 40'", 700),
    Billboard('butly', 'Jalan Sri Amar', "10' x 40'", 800),
    Billboard('cutly', 'Jalan Tun Razak, laluan bertingkat Lebuhraya Prolintas', "20' x 60'", 1000),
    Billboard('dutly', 'Jalan Mergastua', "10' x 40'", 600),
    Billboard('gutly', 'Jalan Wangsa Maju berhampiran AEON', "10' x 40'", 500),
    Billboard('jutly', 'Jalan Bangsar / Jalan Travers', "10' x 40'", 900),
    Billboard('kutly', 'Jalan Ipoh/Kampung Batu Berhampiran Bulatan Kepong', "10' x 40'", 450),
    Billboard('lutly', 'Jalan Ipoh / Taman Wahyu', "10' x 40'", 500),

]
s.bulk_save_objects(objects)
s.commit()