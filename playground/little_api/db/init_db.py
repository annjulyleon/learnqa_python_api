import logging
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import crud, schemas
from db.base import Base
from db.cat_data import CATS
from db.session import engine

logger = logging.getLogger(__name__)

FIRST_ADMIN = 'admin@coolcats.bla'


def init_db(db: Session):
    Base.metadata.create_all(bind=engine)
    if FIRST_ADMIN:
        user = crud.user.get_by_email(db,email=FIRST_ADMIN)
        if not user:
            user_in = schemas.UserCreate(
                first_name="Initial Admin",
                last_name="Initial",
                email=FIRST_ADMIN,
                is_superuser=True,
            )
            user = crud.user.create(db, obj_in=user_in)
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{FIRST_ADMIN} already exists. "
            )
        if not user.cats:
            for cat in CATS:
                cat_in = schemas.CatCreate(
                    age=cat["age"],
                    color=cat["color"],
                    description=cat["description"],
                    name=cat["name"],
                    status=cat["status"],
                    caretaker_id=user.id,
                )
                crud.cat.create(db, obj_in=cat_in)
        else:
            logger.warning(
                "Skipping creating superuser.  FIRST_ADMIN needs to be "
                "provided as an env variable. "
                "e.g.  FIRST_ADMIN=admin@api.coursemaker.io"
            )
