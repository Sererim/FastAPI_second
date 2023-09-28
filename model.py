from pydantic import BaseModel, Field
from typing import Optional
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
    product_name: str = Field(..., title="Name of the product", max_length=50)
    product_description: str = Field(..., title="Description of the product.", max_length=256)
    product_price: float = Field(..., title="Price of the product.", gt=0.00, description="Must be greater than zero.")
    

class ProductOut(BaseModel):
    """
        Model for product output.
    """
    id: int = Field(..., title="Product id.", gt=0)
    product_name: str = Field(..., title="Name of the product", max_length=50)
    product_description: str = Field(..., title="Description of the product.", max_length=256)
    product_price: float = Field(..., title="Price of the product.", gt=0.00, description="Must be greater than zero.")


class OrderIn(BaseModel):
    """
        Model for order input.
    """
    user_id: int = Field(..., title="Product id.", gt=0)
    product_id: int = Field(..., title="Product id.", gt=0)
    status_of_order: bool = Field(..., title="Status of order.")
    date_of_order: datetime = Field(..., gt= datetime.now())


class OrderOut(BaseModel):
    """
    Model for order output.
    """
    id: int = Field(..., title="Product id.", gt=0)
    user_id: int = Field(..., title="Product id.", gt=0)
    product_id: int = Field(..., title="Product id.", gt=0)
    status_of_order: bool = Field(..., title="Status of order.")
    date_of_order: datetime = Field(...,)