from random import randint

from tinydb import TinyDB, Query
import itertools
import re

from tinydb.operations import increment

CATS = [
    {"name": "Grisha",
     "gender": "male",
     "color": "red",
     "age": 2.5,
     "description": "calm gentle friendly",
     "mood": 3,
     "petted": 0,
     "hugged": 0,
     "status": "inhouse"
     },
    {"name": "Kora",
     "gender": "female",
     "color": "white",
     "age": 1.5,
     "description": "shy intelligent gentle",
     "mood": 3,
     "petted": 0,
     "hugged": 0,
     "status": "inhouse"
     },
    {"name": "Drozd",
     "gender": "male",
     "color": "black",
     "age": 1.5,
     "description": "playful friendly",
     "mood": 3,
     "petted": 0,
     "hugged": 0,
     "status": "inhouse"
     }
]

USERS = [
    {"login": "admin",
     "password": "123456",
     "fullname": "Mary Shnider",
     "role": "admin"},
    {"login": "lora_grown",
     "password": "123478",
     "fullname": "Lora Grown",
     "role": "caretaker"},
    {"login": "jeremy_fox",
     "password": "543478",
     "fullname": "Jeremy Fox",
     "role": "guest"}
]


def init_db(db: TinyDB):
    db.drop_tables()
    cats = db.table('cats')
    users = db.table('users')

    for cat in CATS:
        cats.insert(cat)
    for user in USERS:
        users.insert(user)


def get_cats(db: TinyDB):
    cats = db.table('cats')
    cats_with_id = []
    for cat in cats.all():
        cat["id"] = cat.doc_id
        cats_with_id.append(cat)
    return cats_with_id


def get_cats_by_description(db: TinyDB, *keywords):
    cats = db.table('cats')
    Cat = Query()
    cats_found = []
    cats_found_with_id = []
    for keyword in keywords:
        cats_found.append(cats.search(
            Cat.description.search(keyword,flags=re.IGNORECASE))
        )

    cats_found = list(itertools.chain(*cats_found))
    for cat in cats_found:
        cat['id'] = cat.doc_id
        if not any(d['id'] == cat.doc_id for d in cats_found_with_id):
            cats_found_with_id.append(cat)
    return cats_found_with_id


def get_cat_by_id(db: TinyDB, cat_id):
    cats = db.table('cats')
    if cats.contains(doc_id=cat_id):
        return cats.get(doc_id=cat_id)
    else:
        return False


def create_cat(db: TinyDB, cat: dict):
    cats = db.table('cats')
    default_fields = {
        "mood": 3,
        "petted": 0,
        "hugged": 0,
        "status": "inhouse"
    }
    doc_id = cats.insert(cat|default_fields)
    return doc_id


def pet_cat(db:TinyDB, cat_id):
    cats = db.table('cats')
    if cats.contains(doc_id=cat_id):
        cats.update(increment("mood"), doc_ids=[cat_id])
        cats.update(increment("petted"), doc_ids=[cat_id])
    else:
        return False


def hug_cat(db:TinyDB, cat_id):
    cats = db.table('cats')
    if cats.contains(doc_id=cat_id):
        cats.update(increment("mood"), doc_ids=[cat_id])
        cats.update(increment("hugged"), doc_ids=[cat_id])
    else:
        return False


def update_cat(db: TinyDB, cat_id, cat: dict):
    cats = db.table('cats')
    if cats.contains(doc_id=cat_id):
        cats.update(cat,doc_ids=[cat_id])
        return True
    else:
        return False


def delete_cat(db:TinyDB, cat_id):
    cats = db.table('cats')
    removed_cat = cats.remove(doc_ids=[cat_id])
    return removed_cat


def get_user_by_id(db: TinyDB, user_id):
    users = db.table('cats')
    if user_id.contains(doc_id=user_id):
        user = users.get(doc_id=user_id)
        user.pop("password", None)
        return user
    else:
        return {"msg": f"There is no user with provided id '{user_id}"}


def create_user(db: TinyDB, user: dict):
    pass


def update_user(db: TinyDB, user: dict):
    pass


def random_mood(db: TinyDB):
    cats = db.table("cats")
    ids = [cat.doc_id for cat in cats.all()]
    for id in ids:
        mood = randint(1, 5)
        cats.update({"mood": mood}, doc_ids=[id])


if __name__ == '__main__':
    db = TinyDB('db.json')
    #init_db(db)
    new_cat = {"name": "Krokus",
     "gender": "male",
     "color": "mixed",
     "age": 3.5,
     "description": "serious shy clever"}

    #print(get_cat_by_id(db,1))
    #print(get_cats(db))
    #print(get_cats_by_description(db,"gentle","friendly"))
    #print(create_cat(db, new_cat))
    #print(delete_cat(db,4))
    #print(type(get_cats(db)))
    #update_cat(db,1,{"age": 2.5})
    #pet_cat(db,1)
    #cats = db.table('cats')
    #cats.update({"mood": 2})
    #print(random_mood(db))
