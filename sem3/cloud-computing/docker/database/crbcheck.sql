-- MySQL dump 10.13  Distrib 8.0.30, for Linux (x86_64)
--
-- Host: localhost    Database: crbdb
-- ------------------------------------------------------
-- Server version	8.0.30-0ubuntu0.20.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE SCHEMA IF NOT EXISTS `crbdb` DEFAULT CHARACTER SET utf8 ;
USE `crbdb` ;
--
-- Table structure for table `address`
--

DROP TABLE IF EXISTS `address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `address` (
  `address_id` int NOT NULL AUTO_INCREMENT,
  `address_start_date` date DEFAULT NULL,
  `address_end_date` date DEFAULT NULL,
  `address_type` int NOT NULL,
  `address_city` varchar(32) NOT NULL,
  `address_state` varchar(32) NOT NULL,
  `address_details` varchar(128) NOT NULL,
  `address_person_id` int NOT NULL,
  PRIMARY KEY (`address_id`,`address_person_id`),
  UNIQUE KEY `address_id_UNIQUE` (`address_id`),
  KEY `fk_address_registry1_idx` (`address_person_id`),
  CONSTRAINT `fk_address_registry1` FOREIGN KEY (`address_person_id`) REFERENCES `registry` (`person_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address`
--

LOCK TABLES `address` WRITE;
/*!40000 ALTER TABLE `address` DISABLE KEYS */;
INSERT INTO `address` VALUES (6,'2021-01-01','2022-12-01',1,'Bangalore','KA','Hosa Road',6),(7,'2022-11-20','2022-11-29',1,'Bangalore','KA','Haralur Road',6),(8,'2022-11-22','2022-12-09',2,'Bangalore','KA','Sarjapura Road',6),(9,NULL,NULL,1,'Kanpur','KA','Sarjapura Road',7),(10,NULL,NULL,1,'Bangalore','KA','Sarjapura Road',8),(11,NULL,NULL,1,'Kanpur','UP','Haralur Road',9),(14,'2022-11-14','2022-11-29',1,'Ramnagar','KA','Chmabal Ghati',6),(15,'2021-01-01','2022-11-29',1,'Ramnagar','UP','Chmabal Ghati',11),(16,'1980-01-01','2000-02-01',1,'Ramnagar','UP','Chmabal Ghati',12);
/*!40000 ALTER TABLE `address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `convictions`
--

DROP TABLE IF EXISTS `convictions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `convictions` (
  `conviction_id` int NOT NULL AUTO_INCREMENT,
  `conviction_type` int NOT NULL,
  `conviction_name` varchar(64) NOT NULL,
  `conviction_desc` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`conviction_id`),
  UNIQUE KEY `conviction_id_UNIQUE` (`conviction_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `convictions`
--

LOCK TABLES `convictions` WRITE;
/*!40000 ALTER TABLE `convictions` DISABLE KEYS */;
INSERT INTO `convictions` VALUES (1,1,'DEATH PENALTY','Crimes against govt, murder, abetting suicide of minor, etc'),(2,2,'LIFE IMPRISONMENT','Imprisonment for natural life of the person'),(3,3,'RIGOROUS IMPRISONMENT','Prisoners are put to hard labour '),(4,4,'SIMPLE IMPRISIONMENT','Prisoner is merely confined in jail and is not put to any kind of work'),(5,5,'FORFEITURE OF PROPERTY','Deprecate unless committing depredations against the government of India'),(6,6,'FINE','Forfeiture of money by way of penalty');
/*!40000 ALTER TABLE `convictions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `criminal_record`
--

DROP TABLE IF EXISTS `criminal_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `criminal_record` (
  `record_id` int NOT NULL AUTO_INCREMENT,
  `conviction_date` date NOT NULL,
  `conviction_place` varchar(128) DEFAULT NULL,
  `curr_status` int DEFAULT NULL,
  `alert_flag` int DEFAULT NULL,
  `record_offense_id` int NOT NULL,
  `record_conviction_id` int NOT NULL,
  `record_person_id` int NOT NULL,
  PRIMARY KEY (`record_id`,`record_offense_id`,`record_conviction_id`,`record_person_id`),
  UNIQUE KEY `record_id_UNIQUE` (`record_id`),
  KEY `fk_criminal_record_offenses1_idx` (`record_offense_id`),
  KEY `fk_criminal_record_convictions1_idx` (`record_conviction_id`),
  KEY `fk_criminal_record_registry1_idx` (`record_person_id`),
  CONSTRAINT `fk_criminal_record_convictions1` FOREIGN KEY (`record_conviction_id`) REFERENCES `convictions` (`conviction_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_criminal_record_offenses1` FOREIGN KEY (`record_offense_id`) REFERENCES `offenses` (`offense_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_criminal_record_registry1` FOREIGN KEY (`record_person_id`) REFERENCES `registry` (`person_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `criminal_record`
--

LOCK TABLES `criminal_record` WRITE;
/*!40000 ALTER TABLE `criminal_record` DISABLE KEYS */;
INSERT INTO `criminal_record` VALUES (2,'2022-11-02','Bangalore',1,2,10,6,6),(3,'2022-11-09','',2,2,1,4,7),(4,'2022-11-02','Bangalore',3,2,7,4,8),(5,'2022-11-12','Bangalore',1,2,10,6,9),(7,'2022-11-07','Bangalore',1,1,2,2,9),(8,'2022-11-25','Lucknow',3,2,7,6,9),(10,'2000-03-01','Lucknow',3,1,1,2,12),(11,'2001-06-01','Lucknow',3,2,5,3,12);
/*!40000 ALTER TABLE `criminal_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offenses`
--

DROP TABLE IF EXISTS `offenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `offenses` (
  `offense_id` int NOT NULL AUTO_INCREMENT,
  `offense_name` varchar(64) NOT NULL,
  `offense_type` int NOT NULL,
  `offense_desc` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`offense_id`),
  UNIQUE KEY `offense_id_UNIQUE` (`offense_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offenses`
--

LOCK TABLES `offenses` WRITE;
/*!40000 ALTER TABLE `offenses` DISABLE KEYS */;
INSERT INTO `offenses` VALUES (1,'ASSAULT AND BATTERY',1,'Crime against a person'),(2,'ARSON',2,'Arson'),(3,'CHILD ABUSE',3,'Abuse against childred'),(4,'DOMESTIC ABUSE',4,'Abuse arising in a familial or relationship context'),(5,'KIDNAPPING',5,'Taking a person against his or her will'),(6,'CRIME AGAINST WOMEN',6,'Rape and statutory rape'),(7,'THEFT',7,'Burglary, larceny, robbery, auto theft, and shoplifting.'),(8,'ALCOHOL RELATED',8,'Driving under influence, public intoxication, selling drugs to minors, etc'),(9,'FINANCIAL CRIME',9,'Fraud, blackmail, embezzlement and money laundering, tax evasion'),(10,'CYBER CRIME',10,'Impersonation, fraud (can overlap with financial crime)');
/*!40000 ALTER TABLE `offenses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `query`
--

DROP TABLE IF EXISTS `query`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `query` (
  `quiery_id` int NOT NULL AUTO_INCREMENT,
  `search_firstname` varchar(32) NOT NULL,
  `search_middlename` varchar(32) DEFAULT NULL,
  `search_lastname` varchar(32) NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `search_city` varchar(64) DEFAULT NULL,
  `search_timestamp` timestamp NULL DEFAULT NULL,
  `query_type_id` int NOT NULL,
  `user_user_id` int NOT NULL,
  PRIMARY KEY (`quiery_id`,`query_type_id`,`user_user_id`),
  UNIQUE KEY `quiery_id_UNIQUE` (`quiery_id`),
  KEY `fk_query_query_type1_idx` (`query_type_id`),
  KEY `fk_query_user1_idx` (`user_user_id`),
  CONSTRAINT `fk_query_query_type1` FOREIGN KEY (`query_type_id`) REFERENCES `query_type` (`type_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_query_user1` FOREIGN KEY (`user_user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `query`
--

LOCK TABLES `query` WRITE;
/*!40000 ALTER TABLE `query` DISABLE KEYS */;
INSERT INTO `query` VALUES (5,'Shobhit','','Kumar',NULL,NULL,'2022-11-16','','2022-11-02 11:23:28',1,4),(12,'Gabbar','','Singh',NULL,'2001-08-01',NULL,'','2022-11-04 01:19:26',1,9);
/*!40000 ALTER TABLE `query` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `query_type`
--

DROP TABLE IF EXISTS `query_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `query_type` (
  `type_id` int NOT NULL AUTO_INCREMENT,
  `type_name` varchar(64) NOT NULL,
  `type_desc` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`type_id`),
  UNIQUE KEY `type_id_UNIQUE` (`type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `query_type`
--

LOCK TABLES `query_type` WRITE;
/*!40000 ALTER TABLE `query_type` DISABLE KEYS */;
INSERT INTO `query_type` VALUES (1,'SIMPLE','Simple query giving on last criminal record details with last known contact details'),(2,'DETAILED','Detailed criminal record history with all known addresses'),(3,'FLAGGED','Flagged for sexual or violent crimes');
/*!40000 ALTER TABLE `query_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registry`
--

DROP TABLE IF EXISTS `registry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registry` (
  `person_id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(64) DEFAULT NULL,
  `fisrt_name` varchar(32) NOT NULL,
  `middle_name` varchar(32) DEFAULT NULL,
  `last_name` varchar(32) NOT NULL,
  `dob` date DEFAULT NULL,
  `phone` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`person_id`),
  UNIQUE KEY `person_id_UNIQUE` (`person_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registry`
--

LOCK TABLES `registry` WRITE;
/*!40000 ALTER TABLE `registry` DISABLE KEYS */;
INSERT INTO `registry` VALUES (6,'kumar@shobhit.info','Shobhit','','Kumar','2022-11-16','9980854689'),(7,'','Shobhit','','Arora',NULL,''),(8,'praneesh@abc.com','Praneesh','','Kumar','1985-02-01','9980854689'),(9,'somebody@nobody.com','Somebody','','Nobody','2022-11-16','9980854689'),(11,'gabbar@singh.com','Gabbar','','Singh','2022-11-16','9980854689'),(12,'gabbar@singh.com','Gabbar','','Singh','1975-01-01','9980854689');
/*!40000 ALTER TABLE `registry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `role_id` int NOT NULL AUTO_INCREMENT,
  `role_name` varchar(64) NOT NULL,
  `role_desc` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`role_id`),
  UNIQUE KEY `role_id_UNIQUE` (`role_id`),
  UNIQUE KEY `role_name_UNIQUE` (`role_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'ADMIN','Admin User'),(2,'USER','Normal query user');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(64) NOT NULL,
  `last_name` varchar(64) NOT NULL,
  `email` varchar(128) NOT NULL,
  `loginname` varchar(32) NOT NULL,
  `password` varchar(64) NOT NULL,
  `phone` varchar(32) DEFAULT NULL,
  `company` varchar(128) DEFAULT NULL,
  `role_type_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`role_type_id`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`),
  UNIQUE KEY `loginname_UNIQUE` (`loginname`),
  UNIQUE KEY `company_UNIQUE` (`company`),
  KEY `fk_user_role1_idx` (`role_type_id`),
  CONSTRAINT `fk_user_role1` FOREIGN KEY (`role_type_id`) REFERENCES `role` (`role_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (4,'Shobhit','Kumar','2021mt12072@wilp.bits-pilani.ac,in','shobhit','$2y$10$qGhmIBwtvczMQodSg43N6eKJL8KIwJnV74G8z7mcsn3H.Wn6U9OVq','9980854689','Amazon',1),(9,'WILP','WILP','abx@xyz.com','wilp','$2y$10$2qNOePoMoZ7eMZuedLiLpuPmpuX9TZazttnyTpDwMhmZluYC.nVim','9980854689','WILP',2);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-11-04 12:42:31
