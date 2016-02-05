#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,TextAreaField,SelectField,BooleanField,ValidationError
from wtforms.validators import required,Length,Regexp,Email
from ..models import Role,User
from flask.ext.pagedown.fields import PageDownField

class NameForm(Form):
    name=StringField('你的名字是?',validators=[required()])
    submit=SubmitField('提交')

class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[required(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class PostForm(Form):
    # body = TextAreaField("What's on your mind?", validators=[required()])
    #启用Markdown的文章表单
    body=PageDownField("What's on your mind?",validators=[required()])
    submit = SubmitField('Submit')

class CommentForm(Form):
    body = StringField('Enter your comment', validators=[required()])
    submit = SubmitField('Submit')