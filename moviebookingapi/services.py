# Holds services that interact with the sqlite database
from .models import Booking, User, Show

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
        Show.get(name=show).count += 1

    @classmethod
    def remove(cls, bid):
        Booking.get(bid=bid).delete()

    @classmethod
    def update(cls, bid, user, show, date,
               adult_num, child_num,
               discount, cost):

        for booking in user.bookings.select(lambda x: x.bid == bid):
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
        return User.select()

class ShowService(object):
    @classmethod
    def create(cls, name, cost_child, cost_adult,
               image, count=0):
        return Show(
            name=name, cost_child=cost_child,
            cost_adult=cost_adult, image=image,
            count=count
        )

    @classmethod
    def remove(cls, name):
        Show.get(name=name).delete()

        for booking in Booking.select():
            if booking.show == name:
                Booking.get(show=name).delete()

    @classmethod
    def update(cls, name, cost_child, cost_adult,
               image):
        for show in Show.select(lambda x: x.name == name):
            show.name = name if show.name != name else show.name
            show.cost_child = cost_child if show.cost_child != cost_child else show.cost_child
            show.cost_adult = cost_adult if show.cost_adult != cost_adult else show.cost_adult
            show.image = image if show.image != image else show.image

    @classmethod
    def get_show(cls, name):
        return Show.get(name=name)

    @classmethod
    def list_shows(cls):
        return Show.select()
