import os
import ormar
from sqlalchemy import func
from app.database.database import metadata, database


class MainMeta(ormar.ModelMeta):
    """
    Class with main Metadata
    """
    database = database
    metadata = metadata


class User(ormar.Model):
    """
    User model
    """
    class Meta(MainMeta):
        pass

    id = ormar.Integer(primary_key=True, autoincrement=True)
    username = ormar.String(max_length=64)
    password = ormar.String(max_length=256, encrypt_backend=ormar.EncryptBackends.HASH,
                            encrypt_secret=os.getenv("SECRET_KEY"))
    created_at = ormar.DateTime(server_default=func.now())
    updated_at = ormar.DateTime(server_default=func.now())

