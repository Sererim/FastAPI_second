import databases
import sqlalchemy
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


DATABASE_URL: str = "sqlite:///shop.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

class Tables():
    
    users = sqlalchemy.Table(
        "Users",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.INTEGER, primary_key=True),
        sqlalchemy.Column("firstname", sqlalchemy.String(length=45)),
        sqlalchemy.Column("secondname", sqlalchemy.String(length=45)),
        sqlalchemy.Column("username", sqlalchemy.String(45)),
        sqlalchemy.Column("email", sqlalchemy.String()),
        sqlalchemy.Column("password", sqlalchemy.String())
    )
    
    products = sqlalchemy.Table(
        "Products",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.INTEGER, primary_key=True),
        sqlalchemy.Column("name of the product", sqlalchemy.String()),
        sqlalchemy.Column("description of the product", sqlalchemy.TEXT()),
        sqlalchemy.Column("product price", sqlalchemy.DECIMAL(precision=2))
    )

    orders = sqlalchemy.Table(
        "Orders",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.INTEGER, primary_key=True),
        sqlalchemy.Column("user_id", sqlalchemy.INTEGER, foreign_key="Users.id"),
        sqlalchemy.Column("product_id", sqlalchemy.INTEGER, foreign_key="Products.id"),
        sqlalchemy.Column()
    )

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

app = FastAPI()

