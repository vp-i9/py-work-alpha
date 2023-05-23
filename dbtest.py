# db notes for clinic products, add to models.py later
from datetime import datetime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, create_engine, ForeignKey

Base = declarative_base()


# vendor table

class Vendor(Base):
	# identifying which table in db this class applies to
	__tablename__ = 'vendor'

	# for vendor id, give them simple autoincrementing numeric IDs (1, 2, 3, etc)
	vendor_id = Column(Integer, primary_key=True)
	vendor_abbrev = Column(String, nullable=False)
	company = Column(String, nullable=False)
	contact_name = Column(String, nullable=False)
	contact_phone = Column(Integer, nullable=False)
	contact_email = Column(String, nullable=False)
	# company_street = Column(String, nullable=True)
	# company_city = Column(String, nullable=True)
	# company_state = Column(String, nullable=True)
	# company_zip = Column(Integer, nullable=True)

# products table

class Product(Base):
	__tablename__ = 'products'
	# expiration date and reference id are most important fields, 
	expiration = Column(DateTime, nullable=False)
	reference_id = Column(String, nullable=False)
	quantity_on_hand = Column(Integer, nullable=False)
# 	quantity_on_order = Column(Integer, nullable=False, default=0)
# 	product_id = Column(String, nullable=False)
# 	category = Column(String, nullable=False)
# 	size = Column(String, nullable=False)
# 	description = Column(String, nullable=False)

# class Purchase(Base):
# 	__tablename__ = 'purchases'

# 	# add a primary key, maybe composite of vendor + product + date purchase(?)
# 	purchase_id = Column(String, ForeignKey(Product.product_id), primary_key=True)
# 	vendor_purchase_id = Column(String, ForeignKey(Vendor.vendor_id), primary_key=True)
# 	purchase_reference = Column(String, ForeignKey(f"{Vendor.vendor_abbrev}-{Product.expiration}"))

class Consignment(Base):
	__tablename__ = 'consignments'

	# add a primary key, composite as mirror of above, needs to allow similar record types as purchases


# put in examples below, one for each table ideally
examples = [
	Product(expiration=datetime(1980, 12, 12), reference_id='123ABC', quantity_on_hand=3),
]

# for below, switch to Sanjeev's postgres db record
session_maker = sessionmaker(bind=create_engine('sqlite:///models.db'))

def create_tables():
	with session_maker() as session:
		for example in examples:
			session.add(example)
		session.commit()

with session_maker() as session:
	example_records = session.query(Product).all()
	for product in example_records:
		print(product)


"""

examples = [
    Product(
        expiration_date=datetime(1980, 12, 12),
        reference_id="123ABC",
        quantity_on_hand=10,
        # quantity_on_order = Column(Integer, nullable=False, default=0),
        product_id="test-id",
        category="catheter",
        size="1x2x3",
        description="multi-system catheter",
    ),
    Product(
        expiration_date=datetime(2023, 1, 2),
        reference_id="H74939294600410",
        quantity_on_hand=5,
        product_id="090877",
        category="stent",
        size="6x40x130",
        description="drug eluting vascular stent",
    ),
]
older version=

from datetime import datetime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import Column, Integer, String, DateTime, create_engine, ForeignKey

Base = declarative_base()


class Vendor(Base):
    # identifying which table in db this class applies to
    __tablename__ = "vendor"
    # for vendor id, give them simple autoincrementing numeric IDs (1, 2, 3, etc)
    vendor_id = Column(Integer, primary_key=True)
    vendor_abbrev = Column(String, nullable=False)
    vendor_name = Column(String, nullable=False)
    # contact_name = Column(String, nullable=False)
    # contact_phone = Column(Integer, nullable=False)
    # contact_email = Column(String, nullable=False)
    # # company_street = Column(String, nullable=True)
    # company_city = Column(String, nullable=True)
    # company_state = Column(String, nullable=True)
    # company_zip = Column(Integer, nullable=True)


class Product(Base):
    __tablename__ = "products"
    # expiration date and reference id are most important fields,
    expiration_date = Column(DateTime, nullable=False, primary_key=True)
    reference_id = Column(String, nullable=False, primary_key=True)
    quantity_on_hand = Column(Integer, nullable=False)
    quantity_on_order = Column(Integer, nullable=False, default=0)
    product_id = Column(String, autoincrement=True)
    category = Column(String, nullable=False)
    size = Column(String, nullable=False)
    description = Column(String, nullable=False)

    @property
    def current(self):
        return f"""
    For {self.description}-{self.size}, we have: {self.reference_id}-{self.expiration_date}.
    """

    def __repr__(self):
        return f"""
	    Product Reference ID: {self.reference_id},
		Expiration date: {self.expiration_date},
		Quantity of product available: {self.quantity_on_hand}
	    """


class Purchase(Base):
    __tablename__ = "purchases"
    # add a primary key, maybe composite of vendor + product + date purchase(?)
    purchase_id = Column(Integer, primary_key=True)
    product_reference = Column(
        String, ForeignKey("product.reference_id"), nullable=False
    )
    vendor_reference = Column(String, ForeignKey("vendor.vendor_id"), nullable=False)
    # purchase_reference = Column(
    #     String, ForeignKey(f"{Vendor.vendor_abbrev}-{Product.expiration_date}")
    product = relationship("Product", foreign_keys=[product_reference])
    vendor = relationship("Vendor", foreign_keys=[vendor_reference])

    @property
    def current(self):
        return f"""    Purchase reference information for current item: {self.vendor_reference}-{self.product_reference}.
    """

    # def __repr__(self):
    #     return f"""


#     Product Reference ID: {self.,
# 	Expiration date: {self.expiration_date},
# 	Quantity of product available: {self.quantity_on_hand}
#     """


# class Consignment(Base):
#     __tablename__ = "consignments"


examples = [
    Product(
        expiration_date=datetime(2024, 6, 25),
        reference_id="H74939419400810",
        quantity_on_hand=2,
        product_id="090",
        category="balloon catheter",
        size="4-80-135",
        description="paclitaxel-coated PTA balloon catheter, OTW 5F (018)",
    ),
    Vendor(
        vendor_id=100,
        vendor_abbrev="BSCI",
        vendor_name="Boston Scientific",
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

engine = create_engine("sqlite://", echo=False)
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
    example_records = session.query(Product).all()
    for product in example_records:
        print(product.current)

"""


"""


"""
examples = [
    Product(
        expiration_date=datetime(2024, 6, 25),
        reference_id="H74939419400810",
        quantity_on_hand=2,
        product_id="090",
        category="balloon catheter",
        size="4-80-135",
        description="paclitaxel-coated PTA balloon catheter, OTW 5F (018)",
    ),
    Vendor(
        vendor_id=100,
        vendor_abbrev="BSCI",
        vendor_name="Boston Scientific",
    ),
]


    # def __repr__(self):
    #     return f"""


#     Product Reference ID: {self.,
# 	Expiration date: {self.expiration_date},
# 	Quantity of product available: {self.quantity_on_hand}
#     """



"""