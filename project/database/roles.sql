use TaskTracker;
show tables;

DROP ROLE IF EXISTS Viewer;

DROP ROLE IF EXISTS Worker;
CREATE ROLE Worker;
GRANT SELECT ON Assignments TO Worker; 
GRANT SELECT ON Tasks TO Worker; 
GRANT SELECT ON Users TO Worker; 

DROP ROLE IF EXISTS Manager;
CREATE ROLE Manager;
GRANT SELECT, INSERT, UPDATE ON Assignments TO Manager; 
GRANT SELECT, INSERT, UPDATE ON Tasks TO Manager; 
GRANT SELECT, INSERT, UPDATE ON Users TO Manager; 

DROP ROLE IF EXISTS Moderator;
CREATE ROLE Moderator;
GRANT ALL ON Assignments TO Moderator;
GRANT ALL ON Tasks TO Moderator;
GRANT ALL ON Users TO Moderator;

SELECT user AS role_name
FROM mysql.user
WHERE host = '%'
  AND NOT LENGTH(authentication_string);