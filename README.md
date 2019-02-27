## Introduction

The online dog grooming appointment system has features including user authentication, searching, making new appointment, rescheduling existing appointments, viewing appointment history, and upcoming appointment reminder.

Used PostgresSQL for database, Flask for web framework, Python library pg8000 for connecting database and fetching data.

## How to run?

1. Make sure python3 is installed
2. Set up your postgresSQL database server at localhost:5430
3. Edit config.ini with your database server username and password
4. Load DogGrooming_db.sql and DogGrooming_SampleData.sql into your database
5. Windows: open run.bat
   Mac: open run.command
   Unix/Linux/Terminal: run "python3 main.py"

## Use Case

As a client, I can login the system with my registered username and password, edit my information, get a reminder email in the 24 hours before appointment time, book dog grooming reservation online and cancel or re-schedule appointments. As a groomer, I can view a list of bookings. The use case diagram is shown as following.

![Use Case Diagram](https://github.com/DXJ3X1/online-dog-grooming-appointment-system/blob/master/screenshots/use%20case%20diagram.png?raw=true)

## Screenshots

### Login

![Login](https://github.com/DXJ3X1/online-dog-grooming-appointment-system/blob/master/screenshots/Week%209/Login.png?raw=true)

### Edit and View User Profile

![Edit profile](https://github.com/DXJ3X1/online-dog-grooming-appointment-system/blob/master/screenshots/Week%209/profile.png?raw=true)
![View profile](https://github.com/DXJ3X1/online-dog-grooming-appointment-system/blob/master/screenshots/Week%209/Update%20Profile%20Result.png?raw=true)

### View Dog List

![Dog list](https://github.com/DXJ3X1/online-dog-grooming-appointment-system/blob/master/screenshots/Week%209/Dog%20List.png?raw=true)

### Make New Booking

![Make new booking](https://github.com/DXJ3X1/online-dog-grooming-appointment-system/blob/master/screenshots/Week%2010/new_booking.png?raw=true)

### My Bookings

![My bookings](https://github.com/DXJ3X1/online-dog-grooming-appointment-system/blob/master/screenshots/Week%2010/my_bookings.png?raw=true)

### Shop Owner View Upcoming Bookings

![Upcoming bookings](https://github.com/DXJ3X1/online-dog-grooming-appointment-system/blob/master/screenshots/Week%2011/sending%20reminder.png?raw=true)
