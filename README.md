# MovieBookingAPI

`Python: 3.6 to 3.7`

Movie booking system with an API and database

### How to run

1. Clone this github repository: `git clone https://github.com/John-Salmaan-School/MovieBookingAPI.git`
2. Open the cloned folder
3. In the cloned folder, open CMD or Terminal depending on your operating system
4. Install python virtual environment: `pip3 install virtualenv`
5. Run python virtual environment. Form CMD: `py -m venv venv`. For Unix: `python3 -m venv venv`
6. For CMD: `venv\Scripts\activate.bat`. For Unix: `source venv/bin/activate`. Once this is done it should say (venv) at the very left
7. Install required python packages: `pip install -r requirements.txt`
8. Configuration:
    
    If you are running on an external server, change config.py:
    
    ```python
    ...
   host = "0.0.0.0"
   ...
    ```
   Else, leave config.py
9. Run the program: `python app.py`

### Routes
* / :

    Main page to make booking

* /remove:
    
    Page to remove booking by name
    
* /update:

    Page to update booking by name 

* /register:

    Page to register new users

* /booking/submit:

    POST request to submit a movie booking
    
* /booking/remove:

    POST request to remove a booking by name
    
* /booking/update:

    POST request to update a booking by name

* /auth/register:

    POST request to register a new user to database

* /view/bookings:

    GET request to view all current bookings in database
    
* /view/users:
    
    GET request to view all current users in the database
    
* /view/booking/<string:id>:

    GET request to view a booking with a specific id
    Example: http://localhost:1234/view/booking/dfa41569-4268-49a0-9ada-335c4747aa2f
