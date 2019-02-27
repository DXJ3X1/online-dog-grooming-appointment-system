/*
 * DogGrooming database example data
 * SWEN90016 S1 2018
 * For PostgreSQL
 *
 * NOTE: Do not repeatedly run this script, as it is rather big and will be a burden on the server.
 */

SET search_path = DogGrooming, "$user", public;


BEGIN TRANSACTION;

-- Clean out the old data
-- WARNING: This will remove any existing data
DELETE FROM Member;
DELETE FROM Dog;
DELETE FROM Booking;

COMMIT;


BEGIN TRANSACTION;
--
-- Data for Name: Member; Schema: DogGrooming;
INSERT INTO Member VALUES (0, 'tom@admin.com', 'admin', '', '', '', '', '', '', '');
INSERT INTO Member VALUES (1, 'zihuaxue7@gmail.com', 'puddle', '', 'Jacob', 'Foster', '23 Punchs Creek Road,MOUNT TULLY QLD 4380', '042325358', '042325359', '042325360');
INSERT INTO Member VALUES (2, 'zivahsueh@gmail.com', 'quantum', '', 'Albert', 'Einstein', '56 Wynyard Street,KILLIMICAT NSW 2720', '0420150508', '0418790314', '0420110901');

--
-- Data for Name: Dog; Schema: DogGrooming;
INSERT INTO Dog VALUES (0, '', '', '0001-01-01');
INSERT INTO Dog VALUES (1, 'David', 'Labrador', '2014-06-30');
INSERT INTO Dog VALUES (1, 'Tom', 'Golden Retriever', '2015-01-16');
INSERT INTO Dog VALUES (2, 'Lucy', 'Golden Retriever', '2015-08-16');

COMMIT;