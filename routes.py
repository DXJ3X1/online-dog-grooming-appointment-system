# Importing the frameworks

from modules import *
from flask import *
from flask_mail import Mail, Message
import database
import configparser

ERROR_CODE = database.ERROR_CODE    # Error code
ADMIN_NO = 0                        # Admin's member_no 
user_details = {}                   # User details kept for us
session = {}
page = {}
dogs_details = []

# Initialise the application
app = Flask(__name__)
app.secret_key = 'aab12124d346928d14710610f'

# Initialise mail applicaton
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'zoexue3@gmail.com'
app.config['MAIL_PASSWORD'] = 'gyuh0308@'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

#####################################################
##  ADMIN
#####################################################

@app.route('/admin')
def admin():
    # Check if the user is logged in
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))
    page['title'] = 'Tom\'s Dog Grooming'
    val = database.get_all_bookings(user_details['member_no'])
    return render_template('admin.html', 
        bookings=val, session=session, page=page)

#####################################################
##  REMINDER EMAIL
#####################################################

@app.route('/reminder')
def reminder():
    # Check if the user is logged in
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))
    # Check if the user is admin
    if(user_details['member_no'] != ADMIN_NO):
        return redirect(url_for('index'))
    rs = []
    for recipient in database.get_reminder_recipients():
        rs += recipient
    msg = Message('Dog Grooming Appointment', sender = 'zoexue3@gmail.com', recipients = rs)
    msg.body = "Hi, You have an appointment with Tom's Dog Grooming in 24 hours."
    mail.send(msg)
    
    page['bar'] = True
    flash('Reminders have been sent successfully')
    return redirect(url_for('admin'))

#####################################################
##  INDEX
#####################################################

@app.route('/')
def index():
    # Check if the user is logged in
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))
    page['title'] = 'Tom\'s Dog Grooming'
    return render_template('index.html',
        session=session,
        page=page,
        user=user_details,
        dogs=dogs_details)

#####################################################
##  LOGIN
#####################################################

@app.route('/login', methods=['POST', 'GET'])
def login():
    # Check if they are submitting details, or they are just logging in
    if(request.method == 'POST'):
        # submitting details
        val = database.check_login(request.form['email'], request.form['password'])

        # Check if the database gave an error
        if(val == ERROR_CODE):
            page['bar'] = False
            flash("""There was an error with the database.""")
            return redirect(url_for('login'))

        # If it's null, saying they have incorrect details
        if(val is None or len(val) < 1):
            page['bar'] = False
            flash("Incorrect user/password, please try again")
            return redirect(url_for('login'))

        # If there was no error, log them in
        page['bar'] = True
        flash('You have been logged in successfully')
        session['logged_in'] = True

        user_details['member_no'] = val[0][0]

        # check if it's admin
        if(user_details['member_no'] == ADMIN_NO):
            return redirect(url_for('admin'))

        # Store the user details for us to use throughout
        user_details['email'] = val[0][1]
        user_details['first'] = val[0][2]
        user_details['family'] = val[0][3]
        user_details['address'] = val[0][4]
        user_details['mobile_phone'] = val[0][5]
        user_details['work_phone'] = val[0][6]
        user_details['home_phone'] = val[0][7]

        # Store dogs' details
        dogs_details.clear()
        for i in range(len(val)):
            dogs_details.append({})
            dogs_details[-1]['name'] = val[i][8]
            dogs_details[-1]['breed'] = val[i][9]
            dogs_details[-1]['birthdate'] = val[i][10]
        return redirect(url_for('index'))

    elif(request.method == 'GET'):
        return(render_template('login.html', page=page))

#####################################################
##  LOGOUT
#####################################################

@app.route('/logout')
def logout():
    session['logged_in'] = False
    page['bar'] = True
    flash('You have been logged out')
    return redirect(url_for('index'))

#####################################################
##  PROFILE
#####################################################

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if( 'logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    if(request.method == 'POST'):
        # submitting details
        outcome = database.edit_profile(user_details['email'],
                                    request.form['first'],
                                    request.form['family'],
                                    request.form['address'],
                                    request.form['mobile_phone'],
                                    request.form['work_phone'],
                                    request.form['home_phone'])
        
        # Check if the outcome is successful
        if(outcome):
            # Update the user details
            user_details['first'] = request.form['first']
            user_details['family'] = request.form['family']
            user_details['address'] = request.form['address']
            user_details['mobile_phone'] = request.form['mobile_phone']
            user_details['work_phone'] = request.form['work_phone']
            user_details['home_phone'] = request.form['home_phone']
            page['bar'] = True
            flash("You have updated user profile successfully")
            return redirect(url_for('index'))

        # if there war error
        page['bar'] = False
        flash("""There was an error with the database.""")
        return redirect(url_for('profile'))

    elif(request.method == 'GET'):
        return(render_template('profile.html', 
            page=page, 
            user=user_details))

#####################################################
##  LIST DOGS
#####################################################

@app.route('/list_dogs', methods=['GET', 'POST'])
def list_dogs():
    if( 'logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    if(request.method == 'POST'):
        # submitting details
        outcome = database.add_dog(user_details['member_no'],
                                   request.form['name'],
                                   request.form['breed'],
                                   request.form['birthdate'])
        
        # Check if the outcome is successful
        if(outcome):
            dogs_details.append({})
            dogs_details[-1]['name'] = request.form['name']
            dogs_details[-1]['breed'] = request.form['breed']
            dogs_details[-1]['birthdate'] = request.form['birthdate']
            page['bar'] = True
            flash("You have added the dog successfully.")
            return redirect(url_for('index'))

        # if there war error
        page['bar'] = False
        flash("""There was an error with the database.""")
        return redirect(url_for('profile'))

    elif(request.method == 'GET'):
        return render_template('dog_list.html', 
            dogs=dogs_details, 
            page=page, 
            session=session)

#####################################################
## DOG
#####################################################
@app.route('/dog')
def dog():
    if( 'logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    action = request.args.get('action', '')
    dog_name = request.args.get('dog', '')

    # Handle if the user didn't give a dog or an action
    # Action can only be remove
    if(action == '' or dog_name == ''):
        page['bar'] = False
        flash("Error, no dog or action submitted.")
        return(redirect(url_for('index')))

    if(action == 'remove'):
        # Remove the dog
        outcome = database.remove_dog(user_details['member_no'], dog_name)

        # Is it successful?
        if(outcome):
            # Fresh dogs' details every time users go to the home page
            for dog_details in dogs_details:
                if dog_details['name'] == dog_name:
                    dogs_details.remove(dog_details)
                    break
            page['bar'] = True
            flash("You have removed the dog successfully.")
        else:
            page['bar'] = False
            flash("There was an error removing the dog.")

    else:
        page['bar'] = False
        flash("Error, invalid action.")

    return(redirect(url_for('index')))

#####################################################
##  MAKE BOOKING
#####################################################

@app.route('/new_booking', methods=['GET', 'POST'])
def new_booking():
    if( 'logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    b_date = request.args.get('b_date', '')

    if(request.method == 'GET'):
        if(b_date != ''):
            times = ["09:00", "10:30", "12:00", "13:30", "15:00", "16:30"]
            grooming_options = ["wash only", "wash and nail clipping", "deluxe grooming"]
            booked_times = list(database.get_booked_times(b_date))
            for i in range(len(booked_times)):
                booked_times[i] = str(booked_times[i][0])
            return render_template('new_booking.html', 
                b_date=b_date,
                dogs=dogs_details, 
                times=[time for time in times if (time + ':00') not in booked_times], 
                options=grooming_options,
                session=session, 
                page=page)

        return render_template('booking_date.html',
            session=session, 
            page=page)

    # If we're making the booking
    outcome = database.make_booking(user_details['member_no'],
                                request.form['dog_name'],
                                request.form['book_date'],
                                request.form['book_hour'],
                                request.form['duration'],
                                request.form['grooming_type'],
                                request.form['description'])
    if(outcome):
        page['bar'] = True
        flash("You have made a booking successfully.")
        return(redirect(url_for('my_bookings')))
    else:
        page['bar'] = False
        flash("There was an error making your booking.")
        return(redirect(url_for('new_booking')))

#####################################################
##  RESCHEDULE BOOKING
#####################################################

@app.route('/reschedule_booking', methods=['GET', 'POST'])
def reschedule_booking():
    if( 'logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    if(request.method == 'GET'):
        b_date = request.args.get('b_date', '')
        booking_id = request.args.get('booking', '')

        # Handle if the user didn't give a booking
        if(booking_id == ''):
            page['bar'] = False
            flash("Error, no booking submitted.")
            return(redirect(url_for('index')))

        if(b_date != ''):
            times = ["09:00", "10:30", "12:00", "13:30", "15:00", "16:30"]
            booked_times = list(database.get_other_booked_times(b_date, booking_id))
            for i in range(len(booked_times)):
                booked_times[i] = str(booked_times[i][0])
            return render_template('reschedule_booking.html', 
                booking_id=booking_id,
                b_date=b_date,
                times=[time for time in times if (time + ':00') not in booked_times], 
                session=session, 
                page=page)
        
        return render_template('booking_date.html',
            booking_id=booking_id,
            session=session, 
            page=page)

    # If we're making the booking
    outcome = database.reschedule_booking(request.form['booking_id'],
                                request.form['book_date'],
                                request.form['book_hour'])
    if(outcome):
        page['bar'] = True
        flash("You have rescheduled a booking successfully.")

    else:
        page['bar'] = False
        flash("There was an error rescheduling your booking.")
    
    return(redirect(url_for('my_bookings')))

#####################################################
##  SHOW MY BOOKINGS
#####################################################

@app.route('/my_bookings')
def my_bookings():
    if( 'logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    # Check if viewing a booking detail
    booking_id = request.args.get('booking', '')

    if(booking_id != ''):
        # Booking details
        val = database.get_booking(booking_id)
        return render_template('booking_detail.html', 
            booking=val, session=session, page=page)

    # If no booking, then get all the bookings made by the user
    val = database.get_all_bookings(user_details['member_no'])
    return render_template('bookings_list.html', 
        bookings=val, session=session, page=page)


#####################################################
## CANCEL BOOKING
#####################################################
@app.route('/booking')
def booking():
    if( 'logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    action = request.args.get('action', '')
    booking_id = request.args.get('booking', '')

    # Handle if the user didn't give a booking or an action
    # Action can only be cancel
    if(action == '' or booking_id == ''):
        page['bar'] = False
        flash("Error, no booking or action submitted.")

    elif(action == 'cancel'):
        # Cancel the booking
        outcome = database.cancel_booking(booking_id)

        # Is it successful?
        if(outcome):
            page['bar'] = True
            flash("You have cancelled the booking successfully.")
            return(redirect(url_for('my_bookings')))
        else:
            page['bar'] = False
            flash("There was an error cancelling the booking.")

    else:
        page['bar'] = False
        flash("Error, invalid action.")

    return(redirect(url_for('index')))
