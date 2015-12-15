-- MySQL dump 10.13  Distrib 5.7.9, for Win64 (x86_64)
--
-- Host: 192.168.237.144    Database: mystore
-- ------------------------------------------------------
-- Server version	5.5.46-0ubuntu0.14.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `secDaily`
--

DROP TABLE IF EXISTS `secDaily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `secDaily` (
  `tID` int(11) NOT NULL AUTO_INCREMENT,
  `secCode` varchar(45) NOT NULL DEFAULT '‘’',
  `secName` varchar(32) NOT NULL,
  `ns` varchar(64) NOT NULL,
  `dayNum` int(11) NOT NULL DEFAULT '0',
  `secTime` datetime NOT NULL,
  `openPrice` double DEFAULT NULL,
  `closePrice` double DEFAULT NULL,
  `highPrice` double DEFAULT NULL,
  `lowPrice` double DEFAULT NULL,
  `changeTotal` int(11) DEFAULT NULL,
  `exQty` int(11) DEFAULT NULL,
  PRIMARY KEY (`tID`),
  UNIQUE KEY `sid_UNIQUE` (`tID`),
  KEY `secCode_Index` (`secCode`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3149 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `secDetail`
--

DROP TABLE IF EXISTS `secDetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `secDetail` (
  `sdID` int(11) NOT NULL AUTO_INCREMENT,
  `secDailyID` int(11) NOT NULL,
  `seq` int(11) NOT NULL DEFAULT '0',
  `detailTime` datetime NOT NULL,
  `price` double DEFAULT NULL,
  `qty` double DEFAULT NULL,
  PRIMARY KEY (`sdID`)
) ENGINE=InnoDB AUTO_INCREMENT=7654415 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'mystore'
--
/*!50003 DROP PROCEDURE IF EXISTS `getRange` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `getRange`(codeRange varchar(45), beginTime varchar(20), endTime varchar(20),rangval int)
begin

	declare startTime datetime;
    declare closeTime datetime;
    declare minutesCount int;
    declare minutesTotal int;
    declare currentTime datetime;

	set startTime = str_to_date(beginTime,'%Y-%m-%d %H:%i:%S');
	set closeTime = str_to_date(endTime,'%Y-%m-%d %H:%i:%S');


	set minutesCount = 0; 
	set currentTime = startTime;

	set minutesTotal = TIMESTAMPDIFF(MINUTE, startTime,closeTime) ;

	DROP table IF EXISTS tbRang;

	create TEMPORARY table tbRang(baseTime datetime NOT NULL);

	WHILE minutesCount < minutesTotal DO
		insert into tbRang(baseTime) values(currentTime);
		set currentTime = DATE_ADD(currentTime, INTERVAL  rangval MINUTE );
		set minutesCount = minutesCount +  rangVal;
	end WHILE;

	
	select tbRang.baseTime,ifnull(CC.cnt,0) as cnt 
    from 
    (
		select date_format(
						concat( date_format( min_point, '%Y-%m-%d %H:') 
                        , FLOOR(date_format( min_point, '%i:00')*rangVal))
                        ,'%Y-%m-%d %H:%i:%S') as baseTime, cnt    
		from (
			select  concat( date_format( detailTime, '%Y-%m-%d %H:' ) ,  FLOOR(date_format( detailTime, '%i') /rangVal))  as min_point , count(*) as cnt 
			from secDetail
			inner join secDaily on secDetail.secDailyID = secDaily.tID
			where CHAR_LENGTH(codeRange) = 0 or secCode = codeRange
			group by min_point) as BB
     ) CC
    right join tbRang on tbRang.baseTime = CC.baseTime;
    
	drop table tbRang;
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-12-15 10:13:19
