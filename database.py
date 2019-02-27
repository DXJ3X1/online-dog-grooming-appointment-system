#!/usr/bin/env python3

from modules import pg8000
import configparser


# Define some useful variables
ERROR_CODE = 55929
ADMIN_NO = 0    

#####################################################
##  Database Connect
#####################################################

def database_connect():
    # Read the config file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Create a connection to the database
    connection = None
    try:
        connection = pg8000.connect(database=config['DATABASE']['user'],
            user=config['DATABASE']['user'],
            port=5430,
            password=config['DATABASE']['password'],
            host=config['DATABASE']['host'])
    except pg8000.OperationalError as e:
        print("""Error, you haven't updated your config.ini or you have a bad
        connection, please try again. (Update your files first, then check
        internet connection)
        """)
        print(e)
    #return the connection to use
    return connection

#####################################################
##  Login
#####################################################

def check_login(email, password):
    # Ask for the database connection, and get the cursor set up
    conn = database_connect()
    if (conn is None):
        return ERROR_CODE
    cur = conn.cursor()
    try:
        # Try executing the query
        cur.execute("""SELECT memberNo, email, nameGiven, nameFamily, 
                              address, mobilePhone, workPhone, homePhone,
                              name, breed, birthdate
                      FROM DogGrooming.Member NATURAL JOIN DogGrooming.Dog
                     WHERE email = %s AND password = %s""",
                    (email, password))
        val = cur.fetchall()
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return val
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Error checking login")
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None

#####################################################
##  Edit Profile
#####################################################
def edit_profile(email, first, family, address, mobile_phone, work_phone, home_phone):
    # Get the database connection and set up the cursor
    conn = database_connect()
    if (conn is None):
        return ERROR_CODE
    cur = conn.cursor()
    try:
        # Try executing the query
        cur.execute("""UPDATE DogGrooming.Member
                         SET nameGiven = %s, 
                             nameFamily = %s, 
                             address = %s, 
                             mobilePhone = %s,
                             workPhone = %s, 
                             homePhone = %s
                       WHERE email = %s""",
                    (first, family, address, mobile_phone, work_phone, home_phone, email))
        conn.commit()
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return True
    except:
        conn.rollback()
        # If there were any errors, we print something nice and return a NULL value
        print("Error editing profile")

    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return False

#####################################################
##  Remove Dog
#####################################################
def remove_dog(member_no, dog_name):
    # Get the database connection and set up the cursor
    conn = database_connect()
    if (conn is None):
        return ERROR_CODE
    cur = conn.cursor()
    try:
        # Try executing the query
        cur.execute("""DELETE FROM DogGrooming.Dog
                       WHERE memberNo = %s AND name = %s""",
                    (member_no, dog_name))
        conn.commit()
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return True
    except:
        conn.rollback()
        # If there were any errors, we print something nice and return a NULL value
        print("Error removing dog")

    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return False

#####################################################
##  Add Dog
#####################################################
def add_dog(member_no, name, breed, birthdate):
    # Get the database connection and set up the cursor
    conn = database_connect()
    if (conn is None):
        return ERROR_CODE
    cur = conn.cursor()
    try:
        # Try executing the query
        cur.execute("""INSERT INTO DogGrooming.Dog VALUES (%s, %s, %s, %s)""",
                    (member_no, name, breed, birthdate))
        conn.commit()
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return True
    except:
        conn.rollback()
        # If there were any errors, we print something nice and return a NULL value
        print("Error adding dog")

    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return False

#####################################################
##  Get Booked Timeslots
#####################################################

def get_booked_times(date):
    # Ask for the database connection, and get the cursor set up
    conn = database_connect()
    if (conn is None):
        return ERROR_CODE
    cur = conn.cursor()
    try:
        # Try executing the query
        cur.execute("""SELECT startTime::time
                      FROM DogGrooming.Booking
                     WHERE date(startTime) = %s""",
                    (date, ))
        val = cur.fetchall()
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return val
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Error getting booked timeslots")
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None

def get_other_booked_times(date, booking_id):
    # Ask for the database connection, and get the cursor set up
    conn = database_connect()
    if (conn is None):
        return ERROR_CODE
    cur = conn.cursor()
    try:
        # Try executing the query
        cur.execute("""SELECT startTime::time
                      FROM DogGrooming.Booking
                     WHERE date(startTime) = %s AND bookingID != %s""",
                    (date, booking_id))
        val = cur.fetchall()
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return val
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Error getting other booked timeslots")
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None

#####################################################
##  Booking (make, get all, get details, cancel)
#####################################################

def make_booking(member_no, dog_name, date, hour, duration, grooming_option, description):
    # Get the database connection and set up the cursor
    conn = database_connect()
    if (conn is None):
        return ERROR_CODE
    cur = conn.cursor()
    try:
        # Try executing the query
        cur.execute("""INSERT INTO DogGrooming.Booking VALUES (DEFAULT, %s, %s, %s, %s, %s, %s)""",
                    (dog_name, member_no, date + ' ' + hour, duration, grooming_option, description))
        conn.commit()
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return True
    except:
        conn.rollback()
        # If there were any errors, we print something nice and return a NULL value
        print("Error making new booking")

    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return False

def get_all_bookings(member_no):
    # Get the database connection and set up the cursor
    conn = database_connect()
    if (conn is None):
        return ERROR_CODE
    cur = conn.cursor()
    val = None
    try:
        # Try getting all the information returned from the query
        if (member_no == ADMIN_NO):
            cur.execute("""SELECT nameGiven, address, mobilePhone, dogName, type, date(startTime), startTime::time, duration
                      FROM DogGrooming.Booking JOIN DogGrooming.Member ON (Booking.madeBy = Member.memberNo)
                     WHERE startTime > CURRENT_TIMESTAMP
                  ORDER BY date(startTime), startTime::time""")
        else:
            cur.execute("""SELECT dogName, type, date(startTime), startTime::time, duration, bookingID
                          FROM DogGrooming.Booking
                         WHERE madeBy=%s
                      ORDER BY startTime""", (member_no,))
        val = cur.fetchall()
    except:
        # If there were any errors, we print something nice and return a NULL value
        print("Error getting all bookings")

    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return val

def get_reminder_recipients():
    # Get the database connection and set up the cursor
    conn = database_connect()
    if (conn is None):
        return ERROR_CODE
    cur = conn.cursor()
    val = None
    try:
        # Try getting all the information returned from the query
        cur.execute("""SELECT email
                  FROM DogGrooming.Booking JOIN DogGrooming.Member ON (Booking.madeBy = Member.memberNo)
                 WHERE startTime > CURRENT_TIMESTAMP AND startTime - CURRENT_TIMESTAMP < interval '1 day'
              ORDER BY date(startTime), startTime::time""")
        val = cur.fetchall()
    except:
        # If there were any errors, we print something nice and return a NULL value
        print("Error getting emails")

    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return val

def get_booking(booking_id):
    # Get the database connection and set up the cursor
    conn = database_connect()
    if (conn is None):
        return ERROR_CODE
    cur = conn.cursor()
    val = None
    try:
        cur.execute("""SELECT nameGiven, nameFamily, dogName, breed, type, description, date(startTime), startTime::time, duration, bookingID
                      FROM DogGrooming.Booking NATURAL JOIN DogGrooming.Member NATURAL JOIN DogGrooming.Dog
                     WHERE bookingID = %s""",
                    (booking_id, ))
        # Only grab one row of results (there should only be one anyway)
        val = cur.fetchone()
    except:
        # If there were any errors, we print something nice and return a NULL value
        print("Error getting booking details")

    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return val

def cancel_booking(booking_id):
    # Get the database connection and set up the cursor
    conn = database_connect()
    if (conn is None):
        return ERROR_CODE
    cur = conn.cursor()
    try:
        # Try executing the query
        cur.execute("""DELETE FROM DogGrooming.Booking
                       WHERE bookingID = %s""",
                    (booking_id, ))
        conn.commit()
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return True
    except:
        conn.rollback()
        # If there were any errors, we print something nice and return a NULL value
        print("Error cancelling booking")

    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return False

def reschedule_booking(booking_id, date, hour):
    # Get the database connection and set up the cursor
    conn = database_connect()
    if (conn is None):
        return ERROR_CODE
    cur = conn.cursor()
    try:
        # Try executing the query
        cur.execute("""UPDATE DogGrooming.Booking
                         SET startTime = %s
                       WHERE bookingID = %s""",
                    (date + ' ' + hour, booking_id))
        conn.commit()
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return True
    except:
        conn.rollback()
        # If there were any errors, we print something nice and return a NULL value
        print("Error rescheduling booking")

    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return False


