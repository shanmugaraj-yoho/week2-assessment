from database import engine, SessionLocal
from models import Customer, Product, Order
from sqlalchemy import select

# with SessionLocal.begin() as session:

#     customer = Customer(
#         name = "shan",
#         email = "shan@gmail.com",
#         phone = "894574365"
#     )

#     product = Product(
#         name = "Laptop",
#         price = 50000,
#         stock = 10
#     )

#     session.add_all([customer, product])

# print("Customer and Product inserted")

def place_order(customer_id, product_id, quantity, force_error = False):

    try:
        with SessionLocal.begin() as session:

            customer = session.get(Customer, customer_id)

            if not customer:
                raise ValueError("Customer not found")

            product = session.execute(select(Product).where(Product.id == product_id)
                                      .with_for_update()).scalar_one_or_none()

            if not product:
                raise ValueError("Product not found")

            if product.stock < quantity:
                raise ValueError("INsufficient stock")

            product.stock -= quantity

            if force_error:
                raise RuntimeError("Testing rollback")

            order = Order(
                customer_id = customer_id,
                product_id = product_id,
                quantity = quantity
            )

            session.add(order)

            print("Order placed successfully")

    except Exception as e:
        print("Transaction failed:",e)

place_order(customer_id=1, product_id=1, quantity= 2)