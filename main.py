import databases
import sqlalchemy
import model
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import ValidationError
from datetime import datetime


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
        sqlalchemy.Column("product_name", sqlalchemy.String(50), nullable=False, unique=True),
        sqlalchemy.Column("product_description", sqlalchemy.String(256), nullable=False),
        sqlalchemy.Column("product_price", sqlalchemy.Float(precision=2), nullable=False)
    )

    orders = sqlalchemy.Table(
        "Orders",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.INTEGER, primary_key=True, nullable=False),
        sqlalchemy.Column("user_id", sqlalchemy.INTEGER, sqlalchemy.ForeignKey(column="Users.id"), nullable=False),
        sqlalchemy.Column("product_id", sqlalchemy.INTEGER, sqlalchemy.ForeignKey(column="Products.id"), nullable=False),
        sqlalchemy.Column("date_of_order", sqlalchemy.DATE, nullable=False),
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
        user_id).values(**user.dict())
    await database.execute(query)
    return {**user.dict(), "id": user_id}


@app.delete("/users/{id}")
async def delete_user(user_id: int):
    """
        Delete a user from the db.
    """
    query = Tables.users.delete().where(Tables.users.c.id == user_id)
    await database.execute(query)
    return {f'User with id {user_id}' : 'Was deleted'}


@app.post("/products/", response_model=model.ProductIn)
async def create_product(product: model.ProductIn):
    """
        Add one product to db.
    """
    query = Tables.products.insert().values(product_name=product.product_name, 
        product_description=product.description, product_price=product.price)
    last_record_id = await database.execute(query)
    return {**product.dict(), "id": last_record_id}


@app.get("/products/{id}")
async def get_product(product_id: int):
    """
        Get one product.
    """
    query = Tables.products.select(Tables.products.c.id == product_id)
    return await database.fetch_one(query)


@app.get("/products/")
async def get_all_products():
    """
        Get all products.
    """
    query = Tables.products.select()
    return await database.fetch_all(query)


@app.put("/products/{id}", response_model=model.ProductIn)
async def update_product(product_id: int, product: model.ProductIn):
    """
        Update a product.
    """
    query = Tables.products.update().where(Tables.products.c.id == 
        product_id).values(**product.dict())
    await database.execute(query)
    return {**product.dict(), "id" : product_id}


@app.delete("/products/{id}")
async def delete_prodcut(product_id: int):
    """
        Delete a product.
    """
    query = Tables.products.delete().where(Tables.products.c.id == product_id)
    await database.execute(query)
    return {f'Product with id {product_id}' : 'Was deleted'}


@app.post("/orders/", response_model=model.OrderIn)
async def create_order(order: model.OrderIn):
    """
        Add one order to db.
    """
    query = Tables.orders.insert().values(user_id=order.user_id, product_id=order.product_id, 
        date_of_order=order.date_of_order, status_of_order=order.status_of_order)
    last_record_id = await database.execute(query)
    return {**order.dict(), "id": last_record_id}


@app.get("/orders/{id}", response_model=model.OrderOut)
async def get_order(order_id: int):
    """
        Get one order out of the db.
    """
    query = Tables.orders.select(Tables.orders.c.id == order_id)
    return await database.fetch_one(query)


@app.get("/orders/")
async def get_all_orders():
    """
        Shows all orders in db.⌈
    """
    query = Tables.orders.select()
    return await database.fetch_all(query)


@app.put("/orders/{id}", response_model=model.OrderIn)
async def update_order(order_id: int, order: model.OrderIn):
    """
        Update an order in the db.
    """
    query = Tables.orders.update().where(Tables.orders.c.id ==
        order_id).values(**order.dict())
    await database.execute(query)
    return {**order.dict(), "id": order_id}


@app.delete("/orders/{id}")
async def delete_order(order_id: int):
    """
        Delete an order from the db.
    """
    query = Tables.orders.delete().where(Tables.orders.c.id == order_id)
    await database.execute(query)
    return {f'Order with id {order_id}' : 'Was deleted'}


# @app.get("/fake_users/{count}")
# async def create_note(count: int):
#     for i in range(count):
#         query = Tables.users.insert().values(firstname=f'user{i}', secondname=f'usersecond{i}', username=f'username{i}',
#         email=f'mail{i}@mail.ru', password=f'user{i}user')
#         await database.execute(query)
#     return {'message': f'{count} fake users create'}