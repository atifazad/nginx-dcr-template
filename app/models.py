from . import db

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )

    email = db.Column(
        db.String(80),
        index=False,
        unique=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        index=False,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        index=False,
        nullable=False
    )

    auth_tokens = db.relationship('AuthToken', backref='user')

    def __repr(self):
        return '<User {}>'.format(self.username)

class AuthToken(db.Model):

    __tablename__ = 'auth_tokens'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    token = db.Column(
        db.String(64),
        nullable=False,
        unique=True
    )

    expires_at = db.Column(
        db.DateTime,
        index=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        index=False,
        nullable=False
    )
