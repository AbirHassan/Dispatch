# delete existing values
DELETE FROM person;
DELETE FROM friendgroup;
DELETE FROM member;
DELETE FROM comment;
DELETE FROM content;
DELETE FROM share;
DELETE FROM tag;

#Initial user creation
INSERT INTO person VALUES ('AA', md5('AA'), 'Ann', 'Anderson');
INSERT INTO person VALUES ('BB', md5('BB'), 'Bob', 'Baker');
INSERT INTO person VALUES ('CC', md5('CC'), 'Cathy', 'Chang');
INSERT INTO person VALUES ('DD', md5('DD'), 'David', 'Davidson');
INSERT INTO person VALUES ('EE', md5('EE'), 'Ellen', 'Ellenberg');
INSERT INTO person VALUES ('FF', md5('FF'), 'Fred', 'Fox');
INSERT INTO person VALUES ('GG', md5('GG'), 'Gina', 'Gupta');
INSERT INTO person VALUES ('HH', md5('HH'), 'Helen', 'Harper');

#inserting ann into family
INSERT INTO friendgroup VALUES ('family', 'AA', NULL);
INSERT INTO member VALUES ('CC', 'family', 'AA');
INSERT INTO member VALUES ('DD', 'family', 'AA');
INSERT INTO member VALUES ('EE', 'family', 'AA');

# inserting bob into family
INSERT INTO friendgroup VALUES 	('family', 'BB', NULL);
INSERT INTO member VALUES 		('FF','family', 'BB');
INSERT INTO member VALUES 		('EE','family', 'BB');

# inserting ann into besties
INSERT INTO friendgroup VALUES 	('besties', 'AA', NULL);
INSERT INTO member VALUES 		('GG','besties','AA');
INSERT INTO member VALUES 		('HH','besties','AA');

# creating friends and friend requests

INSERT INTO friends VALUES ('AA', 'BB', TRUE);
INSERT INTO friends VALUES ('CC', 'AA', FALSE);
INSERT INTO friends VALUES ('EE', 'AA', FALSE);
INSERT INTO friends VALUES ('DD', 'AA', TRUE);
INSERT INTO friends VALUES ('AA', 'FF', TRUE);
INSERT INTO friends VALUES ('GG', 'AA', TRUE);
# Saving HH to demonstrate sending a friend request

#Testing for Tag
INSERT INTO content VALUES (1,'BB',NULL,NULL,"ASS",1)
INSERT INTO tag VALUES (1,'BB','AA', NULL,NULL)


-- # Ann​ ​posted​ ​a​ ​content​ ​item​ ​with​ ​ID=1,​ ​caption​ ​=​ ​“Whiskers”,​ ​
-- # is​ ​pub​ ​=​ ​False,​ ​and​ ​shared​ ​it with​ ​her​ ​“family”​ ​FriendGroup.
-- INSERT INTO content VALUES 
-- 	(1, '2017-11-3', NULL, 'Whiskers', FALSE, 'AA');

-- INSERT INTO share VALUES (1, 'family', 'AA');


-- # Ann​ ​posted​ ​a​ ​content​ ​item​ ​with​ ​ID=2,​ ​caption​ ​=​ ​“My​ ​birthday​ ​party”,​ ​
-- # is​ ​pub​ ​=​ ​False,​ ​and shared​ ​it​ ​with​ ​her​ ​“besties”​ ​FriendGroup.
-- INSERT INTO content VALUES 
-- 	(2, '2017-11-3', NULL,'My​ ​birthday​ ​party', FALSE, 'AA');

-- INSERT INTO share VALUES (2, 'besties', 'AA');


-- # Bob​ ​posted​ ​a​ ​content​ ​item​ ​with​ ​ID=3,​ ​caption​ ​=​ ​“Rover”,​ ​
-- # is​ ​pub​ ​=​ ​False,​ ​and​ ​shared​ ​it with​ ​his​ ​“family”​ ​FriendGroup.
-- INSERT INTO content VALUES 
-- 	(3, '2017-11-3', NULL, 'Rover', FALSE, 'BB');

-- INSERT INTO share VALUES (3, 'family', 'BB');



