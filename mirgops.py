import os
import sys
from datetime import datetime, timedelta
import json
from pprint import pprint
from random import randint

import psycopg2


def create_user(conn, username, nickname, town, region, is_staff):
    cur = conn.cursor()
    l_username = nickname
    try:
        cur.execute(
            """INSERT INTO auth_user (password, last_login, is_superuser, date_joined, username, first_name, last_name, email, is_staff, is_active) 
            VALUES ('pbkdf2_sha256$100000$pNHyPkONkUD1$0GChRwjHWIrU3nSicwyEnkgog0ymyda7G7E9WlU5Brs=', null, FALSE, %(tmstmp)s , %(username)s, %(nickname)s, %(nickname)s, null, %(staff)s, TRUE) 
            returning id """,
            {'nickname': nickname, 'tmstmp': datetime.utcnow(), 'username': username, 'town': town, 'region': region,
             'staff': is_staff})
        user = cur.fetchone()[0]
        cur.execute(
            """insert into core_cms.public.core_profile (nickname, avatar, user_id, experience, level_id)
            values (%(nickname)s , null, %(user)s, 1, 1)""",
            {'nickname': nickname, 'user': user}
        )
    except:
        pass
    return cur.fetchone()[0]


def get_category(conn, categoryname):
    cur = conn.cursor()
    cur.execute("""SELECT * FROM django_cms.public.core_category WHERE v_name = %(name)s """, {'name': categoryname})
    rows = cur.fetchall()
    if len(rows) > 0:
        return rows[0][0]
    else:
        cur.execute("""INSERT INTO django_cms.public.core_category (v_name, image)
        values (%(category)s, null) returning id_category """,
                    {'category': categoryname})
        return cur.fetchone()[0]


def create_offer(conn, offer_name, offer_text, phone, datecreated, category, town, region, author, ext_ident):
    cur = conn.cursor()
    cur.execute(
        """ INSERT INTO django_cms.public.core_offers (v_name_offer, v_text_offer, v_phone_number, is_new, is_discount, html_content, time_work, dt_updated, dt_stop, id_author_id, id_category, id_discount, id_region, id_town, is_fake, ext_ident) 
        values (%(offer_name)s, null, %(phone)s, FALSE, FALSE, %(offer_text)s, '24/7', %(datecreated)s, %(datestop)s, %(author)s, %(category)s, null, %(region)s, %(town)s, TRUE, %(ext_ident)s) returning id_offer_inst """,
        {'offer_name': offer_name, 'offer_text': offer_text, 'phone': phone, 'ext_ident': ext_ident,
         'datestop': datetime.utcnow() + timedelta(days=30), 'datecreated': datecreated, 'author': author,
         'category': category, 'town': town, 'region': region}
    )
    return cur.fetchone()[0]


def create_comment(conn, author, html, date, offer):
    cur = conn.cursor()
    cur.execute(
        """ INSERT INTO django_cms.public.core_offerscomment (parent_comment, text_comment, dt_created, offer, "user") 
        values (null, %(html)s, %(date)s, %(offer)s, %(author)s) returning id """,
        {'html': html, 'date': date, 'offer': offer, 'author': author}
    )
    return cur.fetchone()[0]


def create_review(conn, html, date, offer, user, title):
    cur = conn.cursor()
    cur.execute(
        """ INSERT INTO django_cms.public.core_offerreviews (text_review, dt_created, offer, "user", title) 
        values (%(html)s, %(date)s, %(offer)s, %(user)s, %(title)s) returning id """,
        {'html': html, 'date': date, 'offer': offer, 'user': user, 'title': title}
    )
    return cur.fetchone()[0]


def create_review_comment(conn, author, html, date, review):
    cur = conn.cursor()
    cur.execute(
        """ INSERT INTO django_cms.public.core_offerreviewscomments (text_comment, dt_created, review, "user", parent_comment_id) 
        values (%(html)s, %(date)s, %(review)s, %(author)s, null) returning id """,
        {'html': html, 'date': date, 'review': review, 'author': author}
    )
    return cur.fetchone()[0]


def check_user(conn, nickname):
    cur = conn.cursor()
    cur.execute("""SELECT * FROM core_customuser WHERE nickname = %(nickname)s """, {'nickname': nickname})
    rows = cur.fetchall()
    if len(rows) > 0:
        return rows[0][0]
    else:
        return False


def migr_town_regions(conn):
    with open('output_town.json', 'r', encoding='utf-8') as data_file:
        data = json.load(data_file)
    for rec in data:
        cur = conn.cursor()
        cur.execute("""INSERT INTO django_cms.public.core_towns (v_name_town)
            VALUES (%(town)s) RETURNING id_town """, {'town': rec['name']})
        town = cur.fetchone()[0]
        for reg in rec['regions']:
            cur = conn.cursor()
            cur.execute("""INSERT INTO django_cms.public.core_regions (v_name_region, id_town_id)
                VALUES (%(region)s, %(town)s) """, {'region': reg, 'town': town})


def get_town(conn, town):
    cur = conn.cursor()
    cur.execute(
        """SELECT id_town FROM django_cms.public.core_towns WHERE v_name_town = %(town)s """,
        {'town': town})
    row = cur.fetchall()[0]
    return row['id_town']


def get_town_region(conn, town, region):
    cur = conn.cursor()
    cur.execute(
        """SELECT id_town_id as id_town, id_region as id_region FROM django_cms.public.core_regions r join core_towns t on r.id_town_id = t.id_town WHERE v_name_region = %(region)s and v_name_town = %(town)s """,
        {'region': region, 'town': town})
    row = cur.fetchall()
    return row


def get_offer_by_ext(conn, ext):
    cur = conn.cursor()
    cur.execute(
        """SELECT id_offer_inst FROM django_cms.public.core_offers r WHERE r.ext_ident = %(ext_ident)s """,
        {'ext_ident': ext})
    return cur.fetchone()


def save_rate(conn, n_rate, rate, review):
    cur = conn.cursor()
    cur.execute(
        """ INSERT INTO django_cms.public.core_offerreviewsrates (n_rate, rate_type, review) 
        values (%(n_rate)s, %(rate)s, %(review)s) returning id """,
        {'n_rate': n_rate, 'rate': rate, 'review': review}
    )
    return cur.fetchone()[0]


def main():
    conn = psycopg2.connect(host="localhost", database="core_cms", user="django", password="db")
    conn.autocommit = True
    cur = conn.cursor()

    # migr_town_regions(conn))
    # data = None

    # idx = 10000
    # with open('output.json', 'r', encoding='utf-8') as data_file:
    #     data = json.load(data_file)
    # for record in data:
    #     idx = idx + 1
    #     town_region = get_town_region(conn, record['town'], record['region'])
    #     if len(town_region) > 0:
    #         category = get_category(conn, record['category'])
    #         usr_c = check_user(conn, record['author'])
    #         if type(usr_c) == bool:
    #             user = create_user(conn, 'sagin%s' % idx, record['author'], town_region[0][0],
    #                                town_region[0][1], True)
    #             html = ''.join(record['html'])
    #             offer = create_offer(conn, record['name'], html, record['phone'], record['date'], category,
    #                                  town_region[0][0], town_region[0][1], user, record['id'])
    #         else:
    #             html = ''.join(record['html'])
    #             offer = create_offer(conn, record['name'], html, record['phone'], record['date'], category,
    #                                  town_region[0][0], town_region[0][1], usr_c, record['id'])
    #
    #         print(offer)
    #         for com in record['comments']:
    #             usr_c = check_user(conn, com['author'])
    #             if type(usr_c) == bool:
    #                 idx = idx + 1
    #                 user = create_user(conn, 'cmmtusr%s' % idx, com['author'], None, None, False)
    #                 create_comment(conn, user, ''.join(com['html']), com['date'], offer)
    #             else:
    #                 create_comment(conn, usr_c, ''.join(com['html']), com['date'], offer)

    idx = 10000
    with open('output.json', 'r', encoding='utf-8') as data_file:
        data = json.load(data_file)
    for record in data:
        idx = idx + 1
        usr_c = check_user(conn, record['author'])
        if record['offer'] != '':
            offer = get_offer_by_ext(conn, record['offer'])
            if offer is not None:
                if type(usr_c) == bool:
                    user = create_user(conn, 'rwview%s' % idx, record['author'], None, None, True)
                    html = ''.join(record['html'])
                    review = create_review(conn, html, record['date'], offer, user, record['name'])
                else:
                    html = ''.join(record['html'])
                    review = create_review(conn, html, record['date'], offer, usr_c, record['name'])
                save_rate(conn, randint(3, 5), 1, review)
                save_rate(conn, randint(3, 5), 2, review)
                save_rate(conn, randint(3, 5), 3, review)
                print(offer)
                for com in record['comments']:
                    usr_c = check_user(conn, com['author'])
                    if type(usr_c) == bool:
                        idx = idx + 1
                        user = create_user(conn, 'rwviewcmt%s' % idx, com['author'], None, None, False)
                        create_review_comment(conn, user, ''.join(com['html']), com['date'], review)
                    else:
                        create_review_comment(conn, usr_c, ''.join(com['html']), com['date'], review)


if __name__ == '__main__':
    main()
