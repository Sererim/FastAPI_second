from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime


class UserIn(BaseModel):
    """
    Model for input data for user table.
    """
    firstname: str = Field(..., title="First name.", min_length=2, max_length=45)
    secondname: str = Field(..., title="Second name.", min_length=2, max_length=45)
    username: str = Field(..., title="User name", min_length=3, max_length=45)
    email: str = Field(..., title="User email", min_length=8)
    password: str = Field(..., title="User password.", min_length=8)
    

class UserOut(BaseModel):
    """
    Model for output data for user table.
    """
    id: int = Field(..., title="User id.", gt=0)
    firstname: str = Field(..., title="First name.", min_length=2, max_length=45)
    secondname: str = Field(..., title="Second name.", min_length=2, max_length=45)
    username: str = Field(..., title="User name", min_length=3, max_length=45)
    email: str = Field(..., title="User email", min_length=8)
    password: str = Field(..., title="User password.", min_length=8)


class ProductIn(BaseModel):
    """
    Model for product input.
    """
    product_name: str = Field(..., title="Name of the product")
    description: str = Field(..., title="Description of the product.")
    price: Decimal = Field(..., title="Price of the product.", gt=0.00, decimal_places=2, description="Must be greater than zero.")
    

class ProductOut(BaseModel):
    """
    Model for product output.
    Args:
        BaseModel (_type_): _description_
    """
    id: int = Field(..., title="Product id.", gt=0)
    product_name: str = Field(..., title="Name of the product")
    description: str = Field(..., title="Description of the product.")
    price: Decimal = Field(..., title="Price of the product.", gt=0.00, decimal_places=2, description="Must be greater than zero.")


class OrderIn(BaseModel):
    """
    Model for order input.
    Args:
        BaseModel (_type_): _description_
    """
    user_id: int = Field(..., title="Product id.", gt=0)
    product_id: int = Field(..., title="Product id.", gt=0)
    date: datetime = Field(..., gt= datetime.now())


class OrderOut(BaseModel):
    """
    Model for order output.
    """
    id: int = Field(..., title="Product id.", gt=0)
    user_id: int = Field(..., title="Product id.", gt=0)
    product_id: int = Field(..., title="Product id.", gt=0)
    date: datetime = Field(..., gt= datetime.now())
