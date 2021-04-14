# Holds services that interact with the sqlite database
from .models import Booking, User

# This service is used to manage bookings, such as creating
# updating, removing, listing and getting a specific
# booking.
class BookingService(object):
    @classmethod
    def create(cls, bid, user, show, date,
               adult_num, child_num,
               discount, cost):
        Booking(
            bid=bid, user=user, show=show, date=date,
            adult_num=adult_num, child_num=child_num,
            discount=discount, cost=cost
        )

    @classmethod
    def remove(cls, bid):
        Booking.get(bid=bid).delete()

    @classmethod
    def update(cls, bid, show, date,
               adult_num, child_num,
               discount, cost):
        for booking in Booking.select(lambda x: x.bid == bid):
            booking.show = show if booking.show != show else booking.show
            booking.date = date if booking.date != date else booking.date
            booking.adult_num = adult_num if booking.adult_num != adult_num else booking.adult_num
            booking.child_num = child_num if booking.child_num != child_num else booking.child_num
            booking.discount = discount if booking.discount != discount else booking.discount
            booking.cost = cost if booking.cost != cost else booking.cost

    @classmethod
    def list_bookings(cls):
        return Booking.select()

    @classmethod
    def get_booking(cls, bid):
        return Booking.get(bid=bid)

    @classmethod
    def get_booking_by_name(cls, name):
        return Booking.get(name=name)

# This service is used to manage users, such as creating
# listing and getting users.
class UserService(object):
    @classmethod
    def create(cls, name, email, password,
               phone_num, admin=False,
               manager=False):
        return User(name=name, email=email, password=password,
                    phone=phone_num, admin=admin,
                    manager=manager)

    @classmethod
    def get_by_email(cls, email):
        return User.get(email=email)

    @classmethod
    def list_users(cls):
        result = {"data": []}
        for user in User.select():
            user_detail = {
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
                "admin": user.admin,
                "manager": user.manager
            }

            result["data"].append(user_detail)

        return result


