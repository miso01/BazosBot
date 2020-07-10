from bazos_http import BazosHttp
from models import User, db, Advertisement
from datetime import datetime


date = datetime.utcnow()
print("heroku script run at time " + date.strftime("%d/%m/%Y %H:%M:%S"))
all_users = User.query.all()
print("all_users length is " + str(len(all_users)))

for user_index, user in enumerate(all_users):
    if user.cookie and user.ad_password:
        user_ads = Advertisement.query.filter_by(user_id=user.id).all()
        print("user with index " + str(user_index) +
              ", cookie is " + user.cookie +
              ", ad_password is " + user.ad_password +
              " and email " + user.email +
              " has " + str(len(user_ads)) + "advertisements")
        for ad_index, ad in enumerate(user_ads):
            print("ad with index " + str(ad_index) + ", ad_id " + ad.id + " and email " + user.email + "posted")
            bh = BazosHttp(user.cookie)
            result = bh.post_advertisement(ad=ad, user=user, advertisement=Advertisement, db=db)
            print("result is " + result)
