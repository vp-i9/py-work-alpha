from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import Column, Integer, String, DateTime, create_engine, ForeignKey

Base = declarative_base()


class Vendor(Base):
    __tablename__ = "vendors"
    id = Column(Integer, primary_key=True)
    abbrev = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    products = relationship("Product", back_populates="vendor")

    def __repr__(self):
        return f"This is vendor information: {self.name}, listed as {self.abbrev}"


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    id_reference = Column(String, nullable=False)
    id_expiry_date = Column(DateTime, nullable=False)
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
        return cls.id_reference + "-" + cls.id_expiry_date

    @property
    def current(self):
        return f"For {self.name}, size: {self.size}, we have: {self.quantity_on_hand} available, consisting of Reference/Expiry: {self.reference}"

    def __repr__(self):
        return f"Product Reference Information: {self.reference}, Quantity of product available: {self.quantity_on_hand}"


class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    vendor_abbrev = Column(String, ForeignKey("vendors.abbrev"))
    quantity = Column(Integer, nullable=False, default=1)
    product = relationship("Product", foreign_keys=[product_id])
    vendor = relationship("Vendor", foreign_keys=[vendor_abbrev])

    @property
    def current(self):
        return f"Purchase reference information: {self.vendor_abbrev}-{self.product_id}"


expiration_date = datetime(2024, 6, 25)
examples = [
    Vendor(
        id=100,
        abbrev="BSCI",
        name="Boston Scientific",
    ),
    Product(
        id=1,
        id_reference="H74939419400810",
        id_expiry_date=expiration_date,
        name="paclitaxel-coated PTA balloon catheter, OTW 5F (018)",
        category="balloon catheter",
        size="4-80-135",
        quantity_on_hand=2,
        vendor_id=100,
    ),
    Purchase(
        product_id=1,
        vendor_abbrev="BSCI",
        quantity=1,
    ),
]


# engine = create_engine('postgresql+psycopg2://user:password@hostname/database_name')

# engine = create_engine("postgresql+psycopg2://postgres@localhost", echo=True)
# the above works, tables created + viewed in pgadmin4

engine = create_engine("postgresql://yc:postgres@localhost:5432/clinicdb")
# can override the hardcoded pw later

# engine = create_engine("postgresql+psycopg2://clinicdb@localhost", echo=True)

# engine = create_engine("sqlite://", echo=True)
Base.metadata.create_all(engine)
session_maker = sessionmaker(bind=engine)


def create_tables():
    with session_maker() as session:
        for example in examples:
            session.add(example)
        session.commit()


# create_tables()

elements = [
    Vendor(
        id=101,
        abbrev="BSCI22",
        name="Boston Scientific2",
    ),
    Product(
        id=2,
        id_reference="H749394194008102",
        id_expiry_date=expiration_date,
        name="paclitaxel-coated PTA balloon catheter, OTW 5F (035)",
        category="stent",
        size="4-9099-135",
        quantity_on_hand=4,
        vendor_id=101,
    ),
    Purchase(
        product_id=2,
        vendor_abbrev="BSCI22",
        quantity=1,
    ),
]


def add_data():
    with session_maker() as session:
        for e in elements:
            session.add(e)
        session.commit()


# with session_maker() as session:
#     product_records = session.query(Product).all()
#     vendor_records = session.query(Vendor).all()
#     purchase_records = session.query(Purchase).all()
#     for product in product_records:
#         print(product.current)
#         print(product.reference)
#     for vendor in vendor_records:
#         print(vendor)
#     for purchase in purchase_records:
#         print(purchase.current)
#         print(purchase.product_id)
#         print(purchase.vendor_abbrev)
