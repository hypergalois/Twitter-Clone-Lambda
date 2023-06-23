-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: twitter-clone.cndejnjkpsl8.us-east-1.rds.amazonaws.com    Database: twitter
-- ------------------------------------------------------
-- Server version	8.0.32

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '';

--
-- Table structure for table `adjuntos`
--

DROP TABLE IF EXISTS `adjuntos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adjuntos` (
  `attachment_id` int NOT NULL AUTO_INCREMENT,
  `url` varchar(255) DEFAULT NULL,
  `type` enum('image','video') DEFAULT NULL,
  PRIMARY KEY (`attachment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adjuntos`
--

LOCK TABLES `adjuntos` WRITE;
/*!40000 ALTER TABLE `adjuntos` DISABLE KEYS */;
INSERT INTO `adjuntos` VALUES (1,'89df8s9hello.png','image'),(2,'1687553616529fundamental.png','image');
/*!40000 ALTER TABLE `adjuntos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mensajes`
--

DROP TABLE IF EXISTS `mensajes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mensajes` (
  `message_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `message` varchar(255) DEFAULT NULL,
  `attachment_id` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`message_id`),
  KEY `mensajes_FK` (`user_id`),
  KEY `mensajes_FK_1` (`attachment_id`),
  CONSTRAINT `mensajes_FK` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`user_id`),
  CONSTRAINT `mensajes_FK_1` FOREIGN KEY (`attachment_id`) REFERENCES `adjuntos` (`attachment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mensajes`
--

LOCK TABLES `mensajes` WRITE;
/*!40000 ALTER TABLE `mensajes` DISABLE KEYS */;
INSERT INTO `mensajes` VALUES (1,3,'hola',NULL,NULL),(2,2,'hola',1,NULL),(3,3,'hhhhhhhhh',NULL,NULL),(4,3,'hola bebe',2,NULL);
/*!40000 ALTER TABLE `mensajes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `respuestas`
--

DROP TABLE IF EXISTS `respuestas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `respuestas` (
  `response_id` int NOT NULL AUTO_INCREMENT,
  `message_id` int NOT NULL,
  `user_id` int NOT NULL,
  `response` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`response_id`),
  KEY `respuestas_FK` (`message_id`),
  KEY `respuestas_FK_1` (`user_id`),
  CONSTRAINT `respuestas_FK` FOREIGN KEY (`message_id`) REFERENCES `mensajes` (`message_id`),
  CONSTRAINT `respuestas_FK_1` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `respuestas`
--

LOCK TABLES `respuestas` WRITE;
/*!40000 ALTER TABLE `respuestas` DISABLE KEYS */;
/*!40000 ALTER TABLE `respuestas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seguidores`
--

DROP TABLE IF EXISTS `seguidores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seguidores` (
  `follower_id` int NOT NULL,
  `following_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  KEY `seguidores_FK` (`follower_id`),
  KEY `seguidores_FK_1` (`following_id`),
  CONSTRAINT `seguidores_FK` FOREIGN KEY (`follower_id`) REFERENCES `usuarios` (`user_id`),
  CONSTRAINT `seguidores_FK_1` FOREIGN KEY (`following_id`) REFERENCES `usuarios` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seguidores`
--

LOCK TABLES `seguidores` WRITE;
/*!40000 ALTER TABLE `seguidores` DISABLE KEYS */;
/*!40000 ALTER TABLE `seguidores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `recovery_phrase` varchar(255) DEFAULT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `biography` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `usuarios_UN1` (`username`),
  UNIQUE KEY `usuarios_UN2` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'username','email','password','hola',NULL,'aqui estamos',NULL,NULL,'name'),(2,'user','email@email.com','$2a$10$LF/37kTg0dZloHkyjc0DQeIXsZ0WT4ixhvoiT/gQJEx0uqK.XIp1i','frase',NULL,NULL,NULL,NULL,'prueba'),(3,'johndoe','johndoe@example.com','$2a$10$z3oV0fAXkOQYTPFZMfc.dOOuq5Bp39sS2J01XwkE4MKt10W7mPvnC','My secret phrase',NULL,NULL,NULL,NULL,'John Doe'),(4,'joselito','jose@gmail.com','$2a$10$oxmGWUrAca2ksPRoKGx44uuVpjGpf5kfH3xGnC3N48vmJJMxjox4G','hola',NULL,NULL,NULL,NULL,'jose'),(5,'laporta','jan@gmial.com','$2a$10$DHWsa5XBJbpyX/RYw0sa8efShdfwuhN/3zqcyHsud6FAwOalfVZmm','hola',NULL,NULL,NULL,NULL,'jan'),(6,'sdfds','dfsf','$2a$10$wusgI9b.KhD8W34WBwfxOeFHdMlTQFvts4J0/18PZzlh3TDzKoWCq','dfdfd',NULL,NULL,NULL,NULL,'dfdd'),(7,'mal','vitas','$2a$10$oTPOQM5TRKFU1zvrkxZBC.laXHi8gymT5ExtuBQoSBUFs13j8sB0K','4wr234',NULL,NULL,NULL,NULL,'todossabe'),(8,'df34','sff','$2a$10$/ruZND5/iVunX3AAEasOa.pZyPIv/h9i7rCHrgYOkkwUdqvgbXtBG','df',NULL,NULL,NULL,NULL,'dfsd34'),(9,'joselito55','jose55@gmail.com','$2a$10$QEROfRie0QlIYMdp.CthlOd3b.46EG7dAVGr3Au13Rw3pRplz39.G','hola',NULL,NULL,NULL,NULL,'jose55'),(10,'qdfs','9dsf88','$2a$10$etZj5DsnnXsDy5hLmj03/.6VYJyiCm2ljShvTSu06EoVdqqqPD20G','d89fs8',NULL,NULL,NULL,NULL,'898'),(11,'redfgisd','dfsjj','$2a$10$BObfZYDod1Ke3guGsUaGu.LAVZd891upJmBfBrJob.68zKk7anigO','dff',NULL,NULL,NULL,NULL,'reddgi'),(13,'red6fgisd','df4sjj','$2a$10$4f2xhL48XhRFbUCqiV.rHeLiCBprSMbsP/GT4MksLVHMqXrcJy3Su','dff',NULL,NULL,NULL,NULL,'red4dgi'),(14,'dsffsdf9','dfsf89sdf8','$2a$10$/ByuCpohzCJjkcrhe0SXzuyMVrs/FQ3ha1IhsnJhPeiml84/1EjB6','d8sf908f',NULL,NULL,NULL,NULL,'dsjflksjd'),(15,'djslfjdj','dfsjlfkdsj','$2a$10$DLQXhJH0BjNGq/uJzEaNTO8Jv4LQUCvyz8WP8n5Bx0I1bp6Sebx2q','dfs9f89',NULL,NULL,NULL,NULL,'jdfkljl'),(16,'sdfsf','sdff','$2a$10$w8NLa3sKcmuzGMlCiNj5w.s/w0Yw.ApvQr3dZ.ZLldr9Re5KL7Ob6','sdfdsf',NULL,NULL,NULL,NULL,'dsfdf'),(17,'juansito','jusantuº','$2a$10$M/JtEBxzYOxxgpLQGOgX9.MAlS1eTmZAxGdUWgzk1B4.dqh2tppN.','df',NULL,NULL,NULL,NULL,'juansito'),(18,'loler','loler','$2a$10$Lj3CEDKbfYL2FGGqv6oev.hzPRcrQautO0qWX2PRW/A0zeM/BNFn2','lol',NULL,NULL,NULL,NULL,'loler');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `votaciones`
--

DROP TABLE IF EXISTS `votaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `votaciones` (
  `user_id` int NOT NULL,
  `message_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  KEY `votaciones_FK` (`user_id`),
  KEY `votaciones_FK_1` (`message_id`),
  CONSTRAINT `votaciones_FK` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`user_id`),
  CONSTRAINT `votaciones_FK_1` FOREIGN KEY (`message_id`) REFERENCES `mensajes` (`message_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `votaciones`
--

LOCK TABLES `votaciones` WRITE;
/*!40000 ALTER TABLE `votaciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `votaciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'twitter'
--
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-23 22:57:17
