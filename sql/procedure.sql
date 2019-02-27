-- Procedure to Insert slots into table. Once a new room is added Change the insert query to Room #2
CREATE DEFINER=`soen344`@`%` PROCEDURE `INIT_ROOM_SLOTS`()
BEGIN
 DECLARE x  INT;
 DECLARE str  VARCHAR(255);
 
 SET x = 1;

 WHILE x  <= 13608 DO
	INSERT INTO ROOM_SLOTS VALUES (NULL, 1, 1, FALSE, FALSE, NULL, NULL);
    SET x = x + 1;
 END WHILE;
 

 END