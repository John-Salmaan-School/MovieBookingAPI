from .models import Booking, User

class BookingService(object):
    @classmethod
    def create(cls, bid, name, show, date,
               adult_num, child_num,
               discount, cost):
        Booking(
            bid=bid, name=name, show=show, date=date,
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
        result = {"data": []}

        for booking in Booking.select():
            booking_detail = {
                "id": booking.bid,
                "name": booking.name,
                "show": booking.show,
                "date": booking.date,
                "adult": booking.adult_num,
                "child": booking.child_num,
                "discount": booking.discount,
                "cost": booking.cost
            }

            result["data"].append(booking_detail)

        return result

    @classmethod
    def get_booking(cls, bid):
        result = {"data": {}}
        for booking in Booking.select(lambda x: x.bid == bid):
            result["data"]["id"] = booking.bid
            result["data"]["name"] = booking.name
            result["data"]["show"] = booking.show
            result["data"]["date"] = booking.date
            result["data"]["adult"] = booking.adult_num
            result["data"]["child"] = booking.child_num
            result["data"]["discount"] = booking.discount
            result["data"]["cost"] = booking.cost

        return result

    @classmethod
    def get_booking_by_name(cls, name):
        result = {"data": {}}
        for booking in Booking.select(lambda x: x.name == name):
            result["data"]["id"] = booking.bid
            result["data"]["name"] = booking.name
            result["data"]["show"] = booking.show
            result["data"]["date"] = booking.date
            result["data"]["adult"] = booking.adult_num
            result["data"]["child"] = booking.child_num
            result["data"]["discount"] = booking.discount
            result["data"]["cost"] = booking.cost

        return result


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


