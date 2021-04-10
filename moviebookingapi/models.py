from pony import orm
from jwt import jwt

db = orm.Database("sqlite", "../booking.db", create_db=True)

class Booking(db.Entity):
    _table_ = "bookings"

    bid = orm.Required(str)
    name = orm.Required(str)
    show = orm.Required(str)
    date = orm.Required(str)
    adult_num = orm.Required(str)
    child_num = orm.Optional(str)
    discount = orm.Required(str)
    cost = orm.Required(str)

class User(db.Entity):
    _table_ = "users"

    name = orm.Required(str)
    email = orm.Required(str)
    password = orm.Required(str)
    phone = orm.Required(str)
    manager = orm.Optional(bool)
    admin = orm.Optional(bool)


db.generate_mapping(create_tables=True)

