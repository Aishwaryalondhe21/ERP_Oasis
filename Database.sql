CREATE DATABASE  IF NOT EXISTS `oasis` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `oasis`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: oasis
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `logistics`
--

DROP TABLE IF EXISTS `logistics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logistics` (
  `date` date DEFAULT NULL,
  `expense_name` varchar(45) DEFAULT NULL,
  `expense_amt` float DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logistics`
--
/*
LOCK TABLES `logistics` WRITE;
/*!40000 ALTER TABLE `logistics` DISABLE KEYS */;
INSERT INTO `logistics` VALUES ('2024-06-13','logistics1',500,'Paid'),('2024-06-24','logi1',500,'UNPAID'),('2024-07-01','logi1',500,'UNPAID');
/*!40000 ALTER TABLE `logistics` ENABLE KEYS */;
UNLOCK TABLES;
*/
--
-- Table structure for table `managetrucks`
--

DROP TABLE IF EXISTS `managetrucks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `managetrucks` (
  `tkdate` date DEFAULT NULL,
  `truckNo` varchar(10) DEFAULT NULL,
  `driverName` varchar(45) DEFAULT NULL,
  `source` varchar(45) DEFAULT NULL,
  `destination` varchar(45) DEFAULT NULL,
  `truckModel` varchar(45) DEFAULT NULL,
  `kilometers` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `managetrucks`
--
/*
LOCK TABLES `managetrucks` WRITE;
/*!40000 ALTER TABLE `managetrucks` DISABLE KEYS */;
INSERT INTO `managetrucks` VALUES ('2024-07-01','1234','Aishwarya','Pune','Mumbai','Truck123','345');
/*!40000 ALTER TABLE `managetrucks` ENABLE KEYS */;
UNLOCK TABLES;
*/
--
-- Table structure for table `milk_bifurcation`
--

DROP TABLE IF EXISTS `milk_bifurcation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `milk_bifurcation` (
  `date` date DEFAULT NULL,
  `loose_milk` float DEFAULT NULL,
  `milk_for_product` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `milk_bifurcation`
--
/*
LOCK TABLES `milk_bifurcation` WRITE;
/*!40000 ALTER TABLE `milk_bifurcation` DISABLE KEYS */;
INSERT INTO `milk_bifurcation` VALUES ('2024-06-13',2.12,5.3),('2024-06-13',2.12,5.3),('2024-06-13',2.1,3.2),('2024-07-01',2.12,5.3);
/*!40000 ALTER TABLE `milk_bifurcation` ENABLE KEYS */;
UNLOCK TABLES;
*/
--
-- Table structure for table `overhead`
--

DROP TABLE IF EXISTS `overhead`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `overhead` (
  `date` date DEFAULT NULL,
  `expense_name` varchar(45) DEFAULT NULL,
  `expense_amt` float DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `overhead`
--
/*
LOCK TABLES `overhead` WRITE;
/*!40000 ALTER TABLE `overhead` DISABLE KEYS */;
INSERT INTO `overhead` VALUES ('2024-06-13','overhead1',2000,'Paid'),('2024-06-25','ov1',2000,'Paid'),('2024-07-01','ov1',2000,'Paid');
/*!40000 ALTER TABLE `overhead` ENABLE KEYS */;
UNLOCK TABLES;
*/
--
-- Table structure for table `pay_farmer`
--

DROP TABLE IF EXISTS `pay_farmer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pay_farmer` (
  `token_id` int NOT NULL,
  `amount_paid` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pay_farmer`
--
/*
LOCK TABLES `pay_farmer` WRITE;
/*!40000 ALTER TABLE `pay_farmer` DISABLE KEYS */;
INSERT INTO `pay_farmer` VALUES (5001,5000.00),(5001,5000.00),(5001,1001.00),(5001,1001.00),(5005,2000.00);
/*!40000 ALTER TABLE `pay_farmer` ENABLE KEYS */;
UNLOCK TABLES;
*/
--
-- Table structure for table `product_prices`
--

DROP TABLE IF EXISTS `product_prices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_prices` (
  `vendorId` bigint NOT NULL,
  `MilkCM500Price` float DEFAULT NULL,
  `MilkCM200Price` float DEFAULT NULL,
  `MilkTM500Price` float DEFAULT NULL,
  `MilkTM200Price` float DEFAULT NULL,
  `Lassi200Price` float DEFAULT NULL,
  `LassiCUP200Price` float DEFAULT NULL,
  `LassiMANGOCUP200Price` float DEFAULT NULL,
  `Dahi200Price` float DEFAULT NULL,
  `Dahi500Price` float DEFAULT NULL,
  `Dahi2LTPrice` float DEFAULT NULL,
  `Dahi5LTPrice` float DEFAULT NULL,
  `Dahi10LTPrice` float DEFAULT NULL,
  `Dahi2LTPrice15` float DEFAULT NULL,
  `Dahi5LTPrice15` float DEFAULT NULL,
  `Dahi10LTPrice15` float DEFAULT NULL,
  `ButtermilkPrice` float DEFAULT NULL,
  `Khova500Price` float DEFAULT NULL,
  `Khoya1000Price` float DEFAULT NULL,
  `Shrikhand100Price` float DEFAULT NULL,
  `Shrikhand250Price` float DEFAULT NULL,
  `Ghee200Price` float DEFAULT NULL,
  `Ghee500Price` float DEFAULT NULL,
  `Ghee15LTPrice` float DEFAULT NULL,
  `PaneerloosePrice` float DEFAULT NULL,
  `khovaloosePrice` float DEFAULT NULL,
  PRIMARY KEY (`vendorId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_prices`
--
/*
LOCK TABLES `product_prices` WRITE;
/*!40000 ALTER TABLE `product_prices` DISABLE KEYS */;
INSERT INTO `product_prices` VALUES (1019,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250),(1020,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250),(1021,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250),(1022,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20),(1023,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340,350,360,370,380,390,400,410,420,430,440),(1024,350,340,330,320,310,300,290,280,270,260,250,240,230,220,210,200,190,180,170,160,150,140,130,120,110),(1025,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340),(1027,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,300,310,320,330,340),(1033,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250),(1034,350,240,330,320,310,300,290,280,270,89,200,240,130,140,150,160,170,180,190,200,210,140,230,240,10);
/*!40000 ALTER TABLE `product_prices` ENABLE KEYS */;
UNLOCK TABLES;
*/
--
-- Table structure for table `raw_materials`
--

DROP TABLE IF EXISTS `raw_materials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `raw_materials` (
  `buydate` date DEFAULT NULL,
  `MilkCM500RoleQuan` int DEFAULT '0',
  `MilkCM500RolePrice` int DEFAULT '0',
  `MilkCM200RoleQuan` int DEFAULT '0',
  `MilkCM200RolePrice` int DEFAULT '0',
  `MilkTM500RoleQuan` int DEFAULT '0',
  `MilkTM500RolePrice` int DEFAULT '0',
  `MilkTM200RoleQuan` int DEFAULT '0',
  `MilkTM200RolePrice` int DEFAULT '0',
  `Lassi200RoleQuan` int DEFAULT '0',
  `Lassi200RolePrice` int DEFAULT '0',
  `LassiCUP200cupQuan` int DEFAULT '0',
  `LassiCUP200cupPrice` int DEFAULT '0',
  `LassiMANGOCUP200cupQuan` int DEFAULT '0',
  `LassiMANGOCUP200cupPrice` int DEFAULT '0',
  `Dahi200MLRoleQuan` int DEFAULT '0',
  `Dahi200MLRolePrice` int DEFAULT '0',
  `Dahi500MLRoleQuan` int DEFAULT '0',
  `Dahi500MLRolePrice` int DEFAULT '0',
  `Dahi2LTBucketQuan` int DEFAULT '0',
  `Dahi2LTBucketPrice` int DEFAULT '0',
  `Dahi5LTBucketQuan` int DEFAULT '0',
  `Dahi5LTBucketPrice` int DEFAULT '0',
  `Dahi10LTBucketQuan` int DEFAULT '0',
  `Dahi10LTBucketPrice` int DEFAULT '0',
  `Dahi2LT1_5BucketQuan` int DEFAULT '0',
  `Dahi2LT1_5BucketPrice` int DEFAULT '0',
  `Dahi5LT1_5BucketQuan` int DEFAULT '0',
  `Dahi5LT1_5BucketPrice` int DEFAULT '0',
  `Dahi10LT1_5BucketQuan` int DEFAULT '0',
  `Dahi10LT1_5BucketPrice` int DEFAULT '0',
  `ButtermilkRoleQuan` int DEFAULT '0',
  `ButtermilkRolePrice` int DEFAULT '0',
  `Khova500TinQuan` int DEFAULT '0',
  `Khova500TinPrice` int DEFAULT '0',
  `Khoya1000TinQuan` int DEFAULT '0',
  `Khoya1000TinPrice` int DEFAULT '0',
  `Shrikhand100TinQuan` int DEFAULT '0',
  `Shrikhand100TinPrice` int DEFAULT '0',
  `Shrikhand250TinQuan` int DEFAULT '0',
  `Shrikhand250TinPrice` int DEFAULT '0',
  `Ghee200TinQuan` int DEFAULT '0',
  `Ghee200TinPrice` int DEFAULT '0',
  `Ghee500TinQuan` int DEFAULT '0',
  `Ghee500TinPrice` int DEFAULT '0',
  `Ghee15LTTinQuan` int DEFAULT '0',
  `Ghee15LTTinPrice` int DEFAULT '0',
  `PaneerlooseQuan` int DEFAULT '0',
  `PaneerloosePrice` int DEFAULT '0',
  `khovalooseQuan` int DEFAULT '0',
  `khovaloosePrice` int DEFAULT '0',
  `LASSICUPFOILQuan` int DEFAULT '0',
  `LASSICUPFOILPrice` int DEFAULT '0',
  `IFFFLAVERMANGOQuan` int DEFAULT '0',
  `IFFFLAVERMANGOPrice` int DEFAULT '0',
  `IFFFLAVERVANILLAQuan` int DEFAULT '0',
  `IFFFLAVERVANILLAPrice` int DEFAULT '0',
  `CULTUREAMAZIKAQuan` int DEFAULT '0',
  `CULTUREAMAZIKAPrice` int DEFAULT '0',
  `CULTUREDANISKOQuan` int DEFAULT '0',
  `CULTUREDANISKOPrice` int DEFAULT '0',
  `CULTUREHRQuan` int DEFAULT '0',
  `CULTUREHRPrice` int DEFAULT '0',
  `LIQUIDSOAPQuan` int DEFAULT '0',
  `LIQUIDSOAPPrice` int DEFAULT '0',
  `COSSODAQuan` int DEFAULT '0',
  `COSSODAPrice` int DEFAULT '0',
  `KAOHQuan` int DEFAULT '0',
  `KAOHPrice` int DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `raw_materials`
--
/*
LOCK TABLES `raw_materials` WRITE;
/*!40000 ALTER TABLE `raw_materials` DISABLE KEYS */;
/*!40000 ALTER TABLE `raw_materials` ENABLE KEYS */;
UNLOCK TABLES;
*/
--
-- Table structure for table `register_farmer`
--

DROP TABLE IF EXISTS `register_farmer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `register_farmer` (
  `name` varchar(50) NOT NULL,
  `mobno` varchar(15) NOT NULL,
  `accno` varchar(20) NOT NULL,
  `ifsc` char(11) NOT NULL,
  `branch` varchar(25) NOT NULL,
  `token_id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`token_id`),
  UNIQUE KEY `accno_UNIQUE` (`accno`)
) ENGINE=InnoDB AUTO_INCREMENT=5006 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `register_farmer`
--
/*
LOCK TABLES `register_farmer` WRITE;
/*!40000 ALTER TABLE `register_farmer` DISABLE KEYS */;
INSERT INTO `register_farmer` VALUES ('Sahil Ranadive','8459175434','556484506566','12341234123','Viman Nagar',5001),('Samarth Londhe','7512388822','43214321321','UBIN0060060','Sangli',5002),('Aishwarya Londhe','9307393578','12341234123','UBIN223200','Yerawada',5003),('Samarth Londhe','8459175434','1234123412321','UBIN0060060','Viman Nagar',5005);
/*!40000 ALTER TABLE `register_farmer` ENABLE KEYS */;
UNLOCK TABLES;
*/
--
-- Table structure for table `total_rawmaterials`
--

DROP TABLE IF EXISTS `total_rawmaterials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `total_rawmaterials` (
  `date` date NOT NULL,
  `MilkCM500RoleQuan` int DEFAULT '0',
  `MilkCM200RoleQuan` int DEFAULT '0',
  `MilkTM500RoleQuan` int DEFAULT '0',
  `MilkTM200RoleQuan` int DEFAULT '0',
  `Lassi200RoleQuan` int DEFAULT '0',
  `LassiCUP200cupQuan` int DEFAULT '0',
  `LassiMANGOCUP200cupQuan` int DEFAULT '0',
  `Dahi200MLRoleQuan` int DEFAULT '0',
  `Dahi500MLRoleQuan` int DEFAULT '0',
  `Dahi2LTBucketQuan` int DEFAULT '0',
  `Dahi5LTBucketQuan` int DEFAULT '0',
  `Dahi10LTBucketQuan` int DEFAULT '0',
  `Dahi2LT1_5BucketQuan` int DEFAULT '0',
  `Dahi5LT1_5BucketQuan` int DEFAULT '0',
  `Dahi10LT1_5BucketQuan` int DEFAULT '0',
  `ButtermilkRoleQuan` int DEFAULT '0',
  `Khova500TinQuan` int DEFAULT '0',
  `Khoya1000TinQuan` int DEFAULT '0',
  `Shrikhand100TinQuan` int DEFAULT '0',
  `Shrikhand250TinQuan` int DEFAULT '0',
  `Ghee200TinQuan` int DEFAULT '0',
  `Ghee500TinQuan` int DEFAULT '0',
  `Ghee15LTTinQuan` int DEFAULT '0',
  `PaneerlooseQuan` int DEFAULT '0',
  `khovalooseQuan` int DEFAULT '0',
  `LASSICUPFOILQuan` int DEFAULT '0',
  `IFFFLAVERMANGOQuan` int DEFAULT '0',
  `IFFFLAVERVANILLAQuan` int DEFAULT '0',
  `CULTUREAMAZIKAQuan` int DEFAULT '0',
  `CULTUREDANISKOQuan` int DEFAULT '0',
  `CULTUREHRQuan` int DEFAULT '0',
  `LIQUIDSOAPQuan` int DEFAULT '0',
  `COSSODAQuan` int DEFAULT '0',
  `KAOHQuan` int DEFAULT '0',
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `total_rawmaterials`
--
/*
LOCK TABLES `total_rawmaterials` WRITE;
/*!40000 ALTER TABLE `total_rawmaterials` DISABLE KEYS */;
INSERT INTO `total_rawmaterials` VALUES ('2024-03-30',60,20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2024-06-30',120,40,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2024-07-01',120,29,34,45,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
/*!40000 ALTER TABLE `total_rawmaterials` ENABLE KEYS */;
UNLOCK TABLES;

*/--
-- Table structure for table `use_raw_materials`
--

DROP TABLE IF EXISTS `use_raw_materials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `use_raw_materials` (
  `usedate` date DEFAULT NULL,
  `MilkCM500RoleQuan` int DEFAULT '0',
  `MilkCM200RoleQuan` int DEFAULT '0',
  `MilkTM500RoleQuan` int DEFAULT '0',
  `MilkTM200RoleQuan` int DEFAULT '0',
  `Lassi200RoleQuan` int DEFAULT '0',
  `LassiCUP200cupQuan` int DEFAULT '0',
  `LassiMANGOCUP200cupQuan` int DEFAULT '0',
  `Dahi200MLRoleQuan` int DEFAULT '0',
  `Dahi500MLRoleQuan` int DEFAULT '0',
  `Dahi2LTBucketQuan` int DEFAULT '0',
  `Dahi5LTBucketQuan` int DEFAULT '0',
  `Dahi10LTBucketQuan` int DEFAULT '0',
  `Dahi2LT1_5BucketQuan` int DEFAULT '0',
  `Dahi5LT1_5BucketQuan` int DEFAULT '0',
  `Dahi10LT1_5BucketQuan` int DEFAULT '0',
  `ButtermilkRoleQuan` int DEFAULT '0',
  `Khova500TinQuan` int DEFAULT '0',
  `Khoya1000TinQuan` int DEFAULT '0',
  `Shrikhand100TinQuan` int DEFAULT '0',
  `Shrikhand250TinQuan` int DEFAULT '0',
  `Ghee200TinQuan` int DEFAULT '0',
  `Ghee500TinQuan` int DEFAULT '0',
  `Ghee15LTTinQuan` int DEFAULT '0',
  `PaneerlooseQuan` int DEFAULT '0',
  `khovalooseQuan` int DEFAULT '0',
  `LASSICUPFOILQuan` int DEFAULT '0',
  `IFFFLAVERMANGOQuan` int DEFAULT '0',
  `IFFFLAVERVANILLAQuan` int DEFAULT '0',
  `CULTUREAMAZIKAQuan` int DEFAULT '0',
  `CULTUREDANISKOQuan` int DEFAULT '0',
  `CULTUREHRQuan` int DEFAULT '0',
  `LIQUIDSOAPQuan` int DEFAULT '0',
  `COSSODAQuan` int DEFAULT '0',
  `KAOHQuan` int DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `use_raw_materials`
--
/*
LOCK TABLES `use_raw_materials` WRITE;
/*!40000 ALTER TABLE `use_raw_materials` DISABLE KEYS */;
INSERT INTO `use_raw_materials` VALUES ('2024-06-29',6,21,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2024-06-30',150,116,170,270,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2024-06-30',30,10,34,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),('2024-07-01',30,21,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
/*!40000 ALTER TABLE `use_raw_materials` ENABLE KEYS */;
UNLOCK TABLES;
*/
--
-- Table structure for table `vendor`
--

DROP TABLE IF EXISTS `vendor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendor` (
  `token` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `enterprise` varchar(45) DEFAULT NULL,
  `gstno` varchar(45) DEFAULT NULL,
  `address` varchar(45) DEFAULT NULL,
  `mobno` varchar(45) DEFAULT NULL,
  `amount` float DEFAULT NULL,
  PRIMARY KEY (`token`)
) ENGINE=InnoDB AUTO_INCREMENT=1035 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendor`
--

/*LOCK TABLES `vendor` WRITE;
/*!40000 ALTER TABLE `vendor` DISABLE KEYS */;
INSERT INTO `vendor` VALUES (1019,'alpha','alpha enterprises','143CDE1234F1Z9','Phulenagar','9881179750',NULL),(1020,'Bravo','Bravo Enterprises','12ABCDE1234F1Z9','Gujarat','8618451685',NULL),(1021,'Charlie','Charlie Enterprises','hqsb79t497rp9ehc','dhanori','7058609753',NULL),(1022,'delta','delta enterprises','15ABC6969NINE','Viman Nagar','992268953',NULL),(1023,'elephant','elephant enterprises','16ELE4567PHA','Delhi','8378805737',NULL),(1024,'Ferirra','Ferirra enterprises','25FER456RIA','Malegaon, Pakistan','992268953',46250),(1025,'Golf','Golf enterprises','24GO789LF','Satara','9527413353',NULL),(1026,'Hotel','Hotel Enterprises','24HOT123EL','Tamil Nadu','0202592266',0),(1027,'India ','India Enterprises','240IND987IA','Satara','8855334477',180000),(1033,'Siddhi Moze',' Mother Dairy','fh398rbf9qp24uegfb98','Satara','9881179750',0),(1034,'Siddhi Moze',' Mother Dairy','143CDE1434F1Z9','Phulenagar','7058609753',0);
/*!40000 ALTER TABLE `vendor` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-02 13:36:28
*/