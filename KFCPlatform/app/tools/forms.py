# -*- coding: utf-8 -*-
from wtforms import Form
from wtforms.fields import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Regexp, Email, EqualTo, ValidationError

class LoginForm(Form):
    name = StringField(
        "name",
        validators=[
            DataRequired(u"Name can't be empty.")
        ]
    )

    pwd = PasswordField(
        "password",
        validators=[
            DataRequired(u"Password can't be empty.")
        ]
    )

    def validate_name(self, field):
        data = CRUD.user_unique(field.data)
        if not data:
            raise ValidationError("This account name doesn't exist.")

    def validate_pwd(self, field):
        if not CRUD.check_login(self.name.data, field.data):
            raise ValidationError("The password is incorrect.")
