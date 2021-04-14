# Holds the database schema of all the objects that will be
# in the database
from pony import orm

# Initiate connection with the the database. If it doesn't
# exist, then create an sqlite database.
db = orm.Database("sqlite", "../booking.db", create_db=True)

# Class that holds the Booking object. Holds values that
# are in the Booking object such as the booking ID, the cost,
# etc.
class Booking(db.Entity):
    _table_ = "bookings"

    bid = orm.Required(str)
    user = orm.Required("User")
    show = orm.Required(str)
    date = orm.Required(str)
    adult_num = orm.Required(str)
    child_num = orm.Optional(str)
    discount = orm.Required(str)
    cost = orm.Required(str)

# Class that holds the User object. Holds values that
# are in the User object, such as email and password.
class User(db.Entity):
    _table_ = "users"

    name = orm.Required(str)
    email = orm.Required(str)
    password = orm.Required(str)
    phone = orm.Required(str)
    bookings = orm.Set("Booking")
    manager = orm.Optional(bool)
    admin = orm.Optional(bool)


# Once the objects have been defined, a method is invoked
# to generate the schema while also creating all the needed
# tables
db.generate_mapping(create_tables=True)

