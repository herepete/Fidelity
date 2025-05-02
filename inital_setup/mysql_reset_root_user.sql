-- This script forcefully resets the root@localhost user to use password-based login only.
DROP USER IF EXISTS 'root'@'localhost';

CREATE USER 'root'@'localhost' IDENTIFIED BY 'bla';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;

