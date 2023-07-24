# -*- coding: utf-8 -*-
from app.tools.orm import ORM
from app.models.models import User, Msg

class CRUD(object):
    @staticmethod
    # Certify uniqueness of user name, phone, and email
    def user_unique(data, method=1):
        session = ORM.db()
        user = None
        try:
            #crud
            model = session.query(User)
            if method == 1:
                user = model.filter_by(name=data).first()
            if method == 2:
                user = model.filter_by(email=data).first()
            if method == 3:
                user = model.filter_by(phone=data).first()
        except Exception as e:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()

        if user:
            return True
        else:
            return False