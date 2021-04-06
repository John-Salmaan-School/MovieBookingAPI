from pony import orm

db = orm.Database("sqlite", "../booking.db", create_db=True)

class Booking(db.Entity):
    _table_ = "bookings"

    name = orm.Required(str)
    show = orm.Required(str)
    date = orm.Required(str)
    adult_num = orm.Required(str)
    child_num = orm.Optional(str)
    discount = orm.Required(str)
    cost = orm.Required(str)


db.generate_mapping(create_tables=True)

