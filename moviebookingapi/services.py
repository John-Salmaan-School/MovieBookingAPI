from .models import Booking

class BookingService(object):
    @classmethod
    def create(cls, name, show, date,
               adult_num, child_num,
               discount, cost):
        return Booking(
            name=name, show=show, date=date,
            adult_num=adult_num, child_num=child_num,
            discount=discount, cost=cost
        )

    @classmethod
    def remove(cls, name):
        Booking.get(name=name).delete()

    @classmethod
    def list_bookings(cls):
        bookings_list = []

        for booking in Booking.select():
            booking_detail = []
            name = booking.name
            show = booking.show
            date = booking.date
            adult_num = booking.adult_num
            child_num = booking.child_num
            discount = booking.discount
            cost = booking.cost

            booking_detail.append(name)
            booking_detail.append(show)
            booking_detail.append(date)
            booking_detail.append(adult_num)
            booking_detail.append(child_num)
            booking_detail.append(discount)
            booking_detail.append(cost)

            bookings_list.append(booking_detail)

        return bookings_list

    @classmethod
    def get_booking(cls, name):
        booking_list = []
        for booking in Booking.select(lambda x: x.name == name):
            book_name = booking.name
            book_show = booking.show
            book_date = booking.date
            book_adult_num = booking.adult_num
            book_child_num = booking.child_num
            book_discount = booking.discount
            book_cost = booking.cost

            booking_list.append(book_name)
            booking_list.append(book_show)
            booking_list.append(book_date)
            booking_list.append(book_adult_num)
            booking_list.append(book_child_num)
            booking_list.append(book_discount)
            booking_list.append(book_cost)

        return booking_list

