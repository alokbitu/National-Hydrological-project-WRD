/*
SQLyog Community v12.12 (64 bit)
MySQL - 5.6.5-m8 : Database - wrd_dash
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`wrd_dash` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin */;

USE `wrd_dash`;

/*Table structure for table `arg` */

DROP TABLE IF EXISTS `arg`;

CREATE TABLE `arg` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stn_id` varchar(40) COLLATE utf8mb4_bin DEFAULT NULL,
  `stn_type` varchar(10) COLLATE utf8mb4_bin DEFAULT NULL,
  `stn_nm` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `location` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `hourly_rainfall` float DEFAULT NULL,
  `daily_rainfall` float DEFAULT NULL,
  `rainfall_value_8am` float DEFAULT NULL,
  `battery_voltage` float DEFAULT NULL,
  `solar_voltage` float DEFAULT NULL,
  `datetime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31087 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

/*Data for the table `arg` */

/*Table structure for table `awlr` */

DROP TABLE IF EXISTS `awlr`;

CREATE TABLE `awlr` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stn_id` varchar(40) COLLATE utf8mb4_bin DEFAULT NULL,
  `stn_type` varchar(10) COLLATE utf8mb4_bin DEFAULT NULL,
  `stn_nm` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `location` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `water_level_value` float DEFAULT NULL,
  `water_level_8am` float DEFAULT NULL,
  `battery_voltage` float DEFAULT NULL,
  `solar_voltage` float DEFAULT NULL,
  `datetime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=156921 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

/*Data for the table `awlr` */

/*Table structure for table `combine_station` */

DROP TABLE IF EXISTS `combine_station`;

CREATE TABLE `combine_station` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stn_id` varchar(40) COLLATE utf8mb4_bin DEFAULT NULL,
  `stn_type` varchar(10) COLLATE utf8mb4_bin DEFAULT NULL,
  `stn_nm` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `location` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `hourly_rainfall_value` float DEFAULT NULL,
  `daily_rainfall_value` float DEFAULT NULL,
  `water_level_value` float DEFAULT NULL,
  `battery_voltage` float DEFAULT NULL,
  `solar_voltage` float DEFAULT NULL,
  `datetime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45606 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

/*Data for the table `combine_station` */

/*Table structure for table `realtime_data_query_table` */

DROP TABLE IF EXISTS `realtime_data_query_table`;

CREATE TABLE `realtime_data_query_table` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stn_id` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `stn_location` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `stn_type` varchar(20) COLLATE utf8mb4_bin DEFAULT NULL,
  `stn_nm` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `sim_no` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `datetime` timestamp NULL DEFAULT NULL,
  `water_level_value` float DEFAULT NULL,
  `hourly_rainfall_value` float DEFAULT NULL,
  `daily_rainfall_value` float DEFAULT NULL,
  `battery_voltage` float DEFAULT NULL,
  `solar_voltage` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=304673 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

/*Data for the table `realtime_data_query_table` */

/*Table structure for table `realtime_data_update_table` */

DROP TABLE IF EXISTS `realtime_data_update_table`;

CREATE TABLE `realtime_data_update_table` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stn_id` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `stn_location` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `stn_type` varchar(20) COLLATE utf8mb4_bin DEFAULT NULL,
  `sim_no` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `datetime` timestamp NULL DEFAULT NULL,
  `water_level_value` float DEFAULT NULL,
  `hourly_rainfall_value` float DEFAULT NULL,
  `daily_rainfall_value` float DEFAULT NULL,
  `battery_voltage` float DEFAULT NULL,
  `solar_voltage` float DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

/*Data for the table `realtime_data_update_table` */

/*Table structure for table `stn_master` */

DROP TABLE IF EXISTS `stn_master`;

CREATE TABLE `stn_master` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stn_id` varchar(20) COLLATE utf8mb4_bin DEFAULT NULL,
  `stn_type` varchar(10) COLLATE utf8mb4_bin DEFAULT NULL,
  `stn_location` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `stn_nm` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `district` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `river` varchar(60) COLLATE utf8mb4_bin DEFAULT NULL,
  `basin` varchar(60) COLLATE utf8mb4_bin DEFAULT NULL,
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

/*Data for the table `stn_master` */

insert  into `stn_master`(`id`,`stn_id`,`stn_type`,`stn_location`,`stn_nm`,`district`,`river`,`basin`) values (1,'20101051','AWL','Singarimunda Rd Bridge,SH-62,Singarimunda','AWL_051','Angul','Manjhor','Mahanadi'),(2,'20102052','AWL','Deulabeda Rd Brodge,SH-62,Deulabeda','AWL_052','Angul','Barabankia','Mahanadi'),(3,'20401018','AWL','Barsar Rd Bridge,Barsar','AWL_018','Bhadrak','salandi','Baitarani'),(4,'20601045','AWL','Khaeramal Rd Bridge,NH-57,Khaeramal','AWL_045','Boudh','Meherani jhor','Mahanadi'),(5,'20602046','AWL','Jamatangi Rd Bridge,NH-57,Maheswar Pinda','AWL_046','Boudh','Bagh','Mahanadi'),(6,'20602050','AWL','Marjadpur Rd Bridge,NH-57,Marjadpur','AWL_050','Boudh','Salki','Mahanadi'),(7,'20701054','AWL','Talabasta Rd Bridge,Talabasta','AWL_054','Cuttack','Rana','Mahanadi'),(8,'20702055','AWL','Keutapada Rd Bridge,Ketupada','AWL_055','Cuttack','Sapua','Mahanadi'),(9,'20903031','AWL','Motunga Rd Bridge,Motunga','AWL_031','Dhenkanal','Niagara','Brahmani'),(10,'20902037','AWL','Dandadhar Dam','AWL_037','Dhenkanal','Ramial','Brahmani'),(11,'30901017','ARG+AWL','Sapua Badjore Dam','ARG+AWL_017','Dhenkanal','Sapua','Mahanadi'),(12,'11001002','ARG','Harbhangi','ARG_002','Gajapati','Harbhangi','Vansadhara'),(13,'21002098','AWL','Harbhangi Dam,Bebiri','AWL_098','Gajapati','Harbhangi','Vansadhara'),(14,'21202070','AWL','Bilaspur Rd Bridge,Bilaspur','AWL_070','Jagatsinghpur','Mahanadi','Mahanadi'),(15,'21201071','AWL','Kulashree Bridge,Mundilo-kulasri Rd,Mundilo','AWL_071','Jagatsinghpur','Devi','Mahanadi'),(16,'21603056','AWL','Orata Gobari Rd Bridge,Babor Bijaynagar Kendrapada Rd,Alailo','AWL_056','kendrapada','Gobari','Mahanadi'),(17,'21602021','AWL','Kanjhari Dam','AWL_021','Keonjhar','kanjhari','Baitarani'),(18,'31601005','ARG+AWL','Remal Dam','ARG+AWL_005','Keonjhar','Remal','Baitarani'),(19,'31801040','ARG+AWL','Salia Dam ','ARG+AWL_040','Khordha','Salia','Rushikulya'),(20,'22202053','AWL','Ostia Rd Bridge,Ostia','AWL_053','Nayagarh','Brutanga','Mahanadi'),(21,'32201035','ARG+AWL','Baghua Dam','ARG+AWL_035','Nayagarh','Baghua','Rushikulya'),(22,'31313131','ARG','Saipala','ARG_001','Nuapada','Ong','Mahanadi'),(23,'22302058','AWL','Sundar Dam','AWL_058','Nuapada','Sundar','Mahanadi'),(24,'22303082','AWL','Dumerbahal Dam','AWL_082','Nuapada','Ong','Mahanadi'),(25,'12401003','ARG','Badanalla','ARG_003','Rayagada','Badanalla','Vansadhara'),(26,'22501039','AWL','Remal-Rairakhol Rd Bridgge,SH-24,Kendumunda','AWL_039','Sambalpur','Tikra Nadi','Bramhani'),(27,'22502042','AWL','Govindtola Rd Bridge,Hans Nagar','AWL_042','Sambalpur','Harad','Mahanadi'),(28,'22503049','AWL','Bolangir Sonepur Rairakhol Rd Bridge,Dhaurakhaman','AWL_049','Sambalpur','Suraball','Mahanadi'),(29,'22601044','AWL','Arigaon Rd Bridge,SH-55,Arigaon','AWL_044','Sonepur','Jira','Mahanadi'),(30,'22602047','AWL','Bolangir Sonepur Rairakhol Rd Bridge,Kuapada','AWL_047','Sonepur','Harihar Jhor','Mahanadi'),(31,'22603048','AWL','Bolangir Sonepur Rairakhol Rd Bridge,kamira','AWL_048','Sonepur','Bauri Jhor','Mahanadi'),(32,'20103030','AWL','Talcher-Kaniha Rd Bridge,Balangi','AWL_030','Angul','Singhara River','Brahmani'),(33,'21101085','AWL','Asika Rd Bridge,Asika','AWL_085','Ganjam','Barha','Rushikulya'),(34,'21102086','AWL','Ambailapali Rd Bridge,Brahmanachal','AWL_086','Ganjam','Baghua','Rushikulya'),(35,'21103087','AWL','Daringbadi Gopalpur Rd Bridge,NH-59,Hinjilicut','AWL_087','Ganjam','Ghodahado','Rushikulya'),(36,'21104088','AWL','Kainchapur Rd Bridge,Poinasi','AWL_088','Ganjam','Kharkhai','Rushikulya'),(37,'21105089','AWL','Kusaraba Rd Bridge,Kusabara','AWL_089','Ganjam','Rushikulya','Rushikulya'),(38,'21106090','AWL','Kandhanuaapalli Road Bridge,Kandhanuaapalli','AWL_090','Ganjam','Burha Nadi','Rushikulya'),(39,'21107091','AWL','Badangi Rd Bridge,Badangi','AWL_091','Ganjam','Barha Nadi','Rushikulya'),(40,'21108105','AWL','Chikit Main Rd Bridge, Dabarasingi','AWL_105','Ganjam','kantajura','Bahuda'),(41,'21109116','AWL','Kelua Bridge,Kelua','AWL_106','Ganjam','Bagi','Bahuda');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) COLLATE utf8mb4_bin NOT NULL,
  `email` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  `password` varchar(80) COLLATE utf8mb4_bin NOT NULL,
  `admin` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username_UNIQUE` (`username`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

/*Data for the table `user` */

insert  into `user`(`id`,`username`,`email`,`password`,`admin`) values (6,'sunjray','sunjraywebmail@gmail.com','123456',1);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
