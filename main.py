import databases
import sqlalchemy
import model
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import ValidationError

DATABASE_URL: str = "sqlite:///shop.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

class Tables():
    
    users = sqlalchemy.Table(
        "Users",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.INTEGER, primary_key=True, nullable=False),
        sqlalchemy.Column("firstname", sqlalchemy.String(length=45), nullable=False),
        sqlalchemy.Column("secondname", sqlalchemy.String(length=45), nullable=False),
        sqlalchemy.Column("username", sqlalchemy.String(45), nullable=False, unique=True),
        sqlalchemy.Column("email", sqlalchemy.String(), nullable=False, unique=True),
        sqlalchemy.Column("password", sqlalchemy.String(), nullable=False)
    )
    
    products = sqlalchemy.Table(
        "Products",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.INTEGER, primary_key=True, nullable=False),
        sqlalchemy.Column("product_name", sqlalchemy.String(), nullable=False, unique=True),
        sqlalchemy.Column("product_description", sqlalchemy.TEXT(), nullable=False),
        sqlalchemy.Column("product_price", sqlalchemy.DECIMAL(precision=2), nullable=False)
    )

    orders = sqlalchemy.Table(
        "Orders",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.INTEGER, primary_key=True, nullable=False),
        sqlalchemy.Column("user_id", sqlalchemy.INTEGER, sqlalchemy.ForeignKey(column="Users.id"), nullable=False),
        sqlalchemy.Column("product_id", sqlalchemy.INTEGER, sqlalchemy.ForeignKey(column="Products.id"), nullable=False),
        sqlalchemy.Column("date_of_order", sqlalchemy.Time, nullable=False),
        sqlalchemy.Column("status_of_order", sqlalchemy.Boolean, nullable=False)
    )

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

app = FastAPI()


@app.post("/users/", response_model=model.UserIn)
async def create_user(user: model.UserIn):
    """
        Add one user to db.
    """
    query = Tables.users.insert().values(firstname=user.firstname, secondname=user.secondname, username=user.username,
        email=user.email, password=user.password)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@app.get("/users/{id}", response_model=model.UserOut)
async def get_user(user_id: int):
    """
        Get one user out of db
    """
    query = Tables.users.select(Tables.users.c.id == user_id)
    return await database.fetch_one(query)


@app.get("/users/")
async def get_all_users():
    """
    Shows all users in db.
    """
    query = Tables.users.select()
    return await database.fetch_all(query)


@app.put("/users/{id}", response_model=model.UserIn)
async def update_user(user_id: int, user: model.UserIn):
    """
        Update a user in the db.
    """
    query = Tables.users.update().where(Tables.users.c.id ==
        user_id).values(**user.model_dump)
    await database.execute(query)
    return {**user.model_dump, "id": user_id}


@app.delete("/users/{id}")
async def delete_user(user_id: int):
    """
        Delete a user from the db.
    """


@app.post("/products/", response_model=model.ProductIn)
async def create_product(product: model.ProductIn):
    """
    Add one product to db.
    """
    query = Tables.products.insert().values(product_name=product.product_name, 
        product_description=product.description, product_price=product.price)
    last_record_id = await database.execute(query)
    return {**product.dict(), "id": last_record_id}





# @app.get("/fake_users/{count}")
# async def create_note(count: int):
#     for i in range(count):
#         query = Tables.users.insert().values(firstname=f'user{i}', secondname=f'usersecond{i}', username=f'username{i}',
#         email=f'mail{i}@mail.ru', password=f'user{i}user')
#         await database.execute(query)
#     return {'message': f'{count} fake users create'}