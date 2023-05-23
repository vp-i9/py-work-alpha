from sqlalchemy import inspect
from sqlalchemy import create_engine


# engine = create_engine("postgresql://u:p@host/database")

# now works below
# engine = create_engine("postgresql://yc:postgres@localhost:5432/clinicdb")

engine = create_engine("postgresql://postgres@localhost:5432/postgres")

inspector = inspect(engine)

for table_name in inspector.get_table_names():
    for column in inspector.get_columns(table_name):
        print("Column: %s" % column["name"])
