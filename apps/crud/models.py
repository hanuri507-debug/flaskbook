from datetime import datetime
import uuid

from apps.app import db
from werkzeug.security import generate_password_hash


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    uuid = db.Column(
        db.String(36),
        unique=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    username = db.Column(db.String, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now
    )

    @property
    def password(self):
        raise AttributeError("읽어 들일 수 없음")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)