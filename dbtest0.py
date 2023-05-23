from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, column_property
from sqlalchemy import Column, Integer, String, DateTime, create_engine, ForeignKey

Base = declarative_base()


class Vendor(Base):
    __tablename__ = "vendors"
    id = Column(Integer, primary_key=True)
    abbrev = Column(String, nullable=False)
    name = Column(String, nullable=False)
    products = relationship("Product", back_populates="vendor")

    def __repr__(self):
        return f"""
This is vendor information: {self.name}, listed as {vendor.abbrev}.
	    """


class Product(Base):
    __tablename__ = "products"
    # id = Column(
    #     String, primary_key=True
    # )  # composed of reference + expiry date together
    id_reference = Column(String, primary_key=True)
    id_expiry_date = Column(DateTime, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    size = Column(String, nullable=False)
    quantity_on_hand = Column(Integer, nullable=False)
    quantity_on_order = Column(Integer, nullable=False, default=0)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    vendor = relationship("Vendor", back_populates="products")

    @hybrid_property
    def reference(self):
        return f"{self.id_reference} = {self.id_expiry_date}"

    @reference.expression
    def reference(cls):
        # Return the SQL expression that calculates the reference value
        return cls.id_reference + "-" + cls.id_expiry_date

    @property
    def current(self):
        return f"""
For {self.name}, size: {self.size}, we have: {self.quantity_on_hand} available, consisting of Reference/Expiry: {self.reference}."""

    def __repr__(self):
        return f"""
Product Reference Information: {self.reference},
Quantity of product available: {self.quantity_on_hand}
	    """


class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey("products.reference"))
    vendor_abbrev = Column(String, ForeignKey("vendors.abbrev"))
    reference = column_property(f"{product_id} = {vendor_abbrev}")
    quantity = Column(Integer, nullable=False, default=1)
    product = relationship("Product", foreign_keys=[product_id])
    vendor = relationship("Vendor", foreign_keys=[vendor_abbrev])

    @property
    def current(self):
        return f"""
Purchase reference information: {self.vendor_abbrev}-{self.product_id}.
    """


# class Consignment(Base):
#     __tablename__ = "consignments"

expiration_date = datetime(2024, 6, 25)
examples = [
    Vendor(
        id=100,
        abbrev="BSCI",
        name="Boston Scientific",
    ),
    Product(
        id=f"""H74939419400810={expiration_date}""",
        id_reference="H74939419400810",
        id_expiry_date=expiration_date,
        name="paclitaxel-coated PTA balloon catheter, OTW 5F (018)",
        category="balloon catheter",
        size="4-80-135",
        quantity_on_hand=2,
        vendor_id=100,
    ),
    Purchase(
        # id=f"H74939419400810={expiration_date}",
        # vendor_abbrev="BSCI",
        quantity=1,
    ),
]

"""
    Product(
        expiration_date=datetime(),
        reference_id="",
        quantity_on_hand=10,
        product_id="",
        category="",
        size="",
        description="",
    ),

    
    Vendor(
    vendor_id = 100,
    vendor_abbrev = 'BSCI',
    vendor_name = 'Boston Scientific',
    )
"""

engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)
# for below, switch to Sanjeev's postgres db record
session_maker = sessionmaker(bind=engine)


def create_tables():
    with session_maker() as session:
        for example in examples:
            session.add(example)
        session.commit()


create_tables()
# already done ^, saved to db file(if using file then change create_engine's first parameter to file)

with session_maker() as session:
    product_records = session.query(Product).all()
    vendor_records = session.query(Vendor).all()
    purchase_records = session.query(Purchase).all()
    # print(type(product_records)) # this is type list, as expected
    for product in product_records:
        print(product.current)
        print(product.reference)
    for vendor in vendor_records:
        print(vendor)
    for purchase in purchase_records:
        print(purchase.current)
        print("--- test space ---")
        # print(purchase.id)
        print(purchase.reference)
        print(purchase.product_id)
    # print("--- test space ---")
