/*
 * SWEN90016
 *
 * Reference Schema for SWEN90016 Group Assignment - Dog-Grooming Database
 * version 1.0
 *
 * PostgreSQL version...
 *
 * IMPORTANT!
 * You need to replace <your-login> with your PostgreSQL user name in line 311
 * of this file (the ALTER USER  command)
 */

/* clean-up to make script idempotent */
BEGIN TRANSACTION;
SET search_Path = DogGrooming, '$user', public;
DROP TABLE IF EXISTS Member         CASCADE;
DROP TABLE IF EXISTS Dog            CASCADE;
DROP TABLE IF EXISTS Booking;
DROP SCHEMA IF EXISTS DogGrooming   CASCADE;
COMMIT;


/* schema starts here */
CREATE SCHEMA DogGrooming;

/* this line will ensure that all following CREATE statements use the DogGrooming schema */
SET search_Path = DogGrooming, '$user', public;


/* for Member table */
CREATE DOMAIN EMailType AS VARCHAR(50) CHECK (value SIMILAR TO '[[:alnum:]_]+@[[:alnum:]]+%.[[:alnum:]]+');


CREATE TABLE Member (
   memberNo      INTEGER,                      -- new surrogate key to allow changeable email
   email         EMailType    NOT NULL UNIQUE, -- original key from E-R diagram
   password      VARCHAR(20)  NOT NULL,        -- better store just a hash value of the password
   pw_salt       VARCHAR(10),                  -- newly added for better security (not needed when bcrypt used)
   nameGiven     VARCHAR(100),
   nameFamily    VARCHAR(100),
   address       VARCHAR(200),
   mobilePhone   VARCHAR(15),
   workPhone     VARCHAR(15),
   homePhone     VARCHAR(15),
   CONSTRAINT Member_PK PRIMARY KEY (memberNo)
);

CREATE TABLE Dog (
   memberNo   INTEGER,
   name       VARCHAR(100) NOT NULL UNIQUE,
   breed      VARCHAR(100),
   birthdate  DATE,
   CONSTRAINT Dog_PK PRIMARY KEY (memberNo,name),
   CONSTRAINT Dog_Member_FK FOREIGN KEY (memberNo) REFERENCES Member(memberNo) ON DELETE CASCADE
);

CREATE TABLE Booking (
   bookingID    SERIAL,              -- new surrogate key; automatic increased integer ID
   dogName      VARCHAR(100) NOT NULL,
   madeBy       INTEGER      NOT NULL,
   startTime    TIMESTAMP    NOT NULL UNIQUE, -- start time is inclusive
   duration     TIME         NOT NULL,
   type         VARCHAR(100) NOT NULL,
   description  VARCHAR(1000),
   CONSTRAINT Booking_PK          PRIMARY KEY (bookingID),
   CONSTRAINT Booking_Dog_FK      FOREIGN KEY (dogName)    REFERENCES Dog(name) ON DELETE CASCADE,
   CONSTRAINT Booking_Member_FK   FOREIGN KEY (madeBy) REFERENCES Member(memberNo) ON DELETE CASCADE
);

/* end schema definition */


/* IMPORTANT TODO: */
/* please replace <your-login> with the name of your PostgreSQL login */
/* in the following ALTER USER username SET search_path ... command   */
/* this ensures that the DogGrooming schema is automatically used when you query one of its tables */
ALTER USER zihuaxue SET search_Path = '$user', public, DogGrooming;
