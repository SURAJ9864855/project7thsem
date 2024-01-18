-- phpMyAdmin SQL Dump
-- version 3.2.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jan 08, 2024 at 08:57 PM
-- Server version: 5.1.41
-- PHP Version: 5.3.1

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `productionplaning`
--
CREATE DATABASE `productionplaning` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `productionplaning`;

-- --------------------------------------------------------

--
-- Table structure for table `admindetails`
--

CREATE TABLE IF NOT EXISTS `admindetails` (
  `AdminId` int(11) NOT NULL AUTO_INCREMENT,
  `Username` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  `AdminName` varchar(250) NOT NULL,
  PRIMARY KEY (`AdminId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3001 ;

--
-- Dumping data for table `admindetails`
--

INSERT INTO `admindetails` (`AdminId`, `Username`, `Password`, `AdminName`) VALUES
(3000, 'admin', 'admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `categorydetails`
--

CREATE TABLE IF NOT EXISTS `categorydetails` (
  `CategoryId` int(11) NOT NULL AUTO_INCREMENT,
  `Code` varchar(10) NOT NULL,
  `Name` varchar(250) NOT NULL,
  `Status` tinyint(1) NOT NULL,
  `Recorded_Date` datetime NOT NULL,
  PRIMARY KEY (`CategoryId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `categorydetails`
--

INSERT INTO `categorydetails` (`CategoryId`, `Code`, `Name`, `Status`, `Recorded_Date`) VALUES
(1, 'Standard', '0.45 mm TCT (Standard)', 1, '2023-11-28 14:30:51'),
(2, 'Premium', '0.50 mm TCT (Premium)', 1, '2023-11-28 14:30:54');

-- --------------------------------------------------------

--
-- Table structure for table `configdetails`
--

CREATE TABLE IF NOT EXISTS `configdetails` (
  `ConfigId` int(11) NOT NULL AUTO_INCREMENT,
  `UserId` int(11) NOT NULL,
  `CategoryId` int(11) NOT NULL,
  `Size_Id` int(11) NOT NULL,
  `Min_Quantity` int(11) NOT NULL,
  `Max_Quantity` int(11) NOT NULL,
  `Recorded_Date` datetime NOT NULL,
  PRIMARY KEY (`ConfigId`),
  KEY `CategoryId` (`CategoryId`),
  KEY `Size_Id` (`Size_Id`),
  KEY `UserId` (`UserId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=16 ;

--
-- Dumping data for table `configdetails`
--

INSERT INTO `configdetails` (`ConfigId`, `UserId`, `CategoryId`, `Size_Id`, `Min_Quantity`, `Max_Quantity`, `Recorded_Date`) VALUES
(1, 1, 1, 1, 100, 200, '2023-11-28 14:35:41'),
(2, 1, 1, 2, 100, 200, '2023-11-28 14:35:55'),
(3, 1, 1, 3, 100, 200, '2023-11-28 14:35:41'),
(4, 1, 1, 4, 100, 200, '2023-11-28 14:35:55'),
(5, 1, 1, 5, 100, 200, '2023-11-28 14:35:55'),
(6, 1, 1, 6, 100, 200, '2023-11-28 14:35:55'),
(7, 1, 2, 7, 100, 200, '2023-11-28 14:35:41'),
(8, 1, 2, 8, 100, 200, '2023-11-28 14:35:55'),
(9, 1, 2, 9, 100, 200, '2023-11-28 14:35:41'),
(10, 1, 2, 10, 100, 200, '2023-11-28 14:35:55'),
(11, 1, 2, 11, 100, 200, '2023-11-28 14:35:55'),
(15, 1, 2, 12, 100, 200, '2023-12-20 17:34:01');

-- --------------------------------------------------------

--
-- Table structure for table `dataownerdetails`
--

CREATE TABLE IF NOT EXISTS `dataownerdetails` (
  `UserId` int(11) NOT NULL AUTO_INCREMENT,
  `Firstname` varchar(250) NOT NULL,
  `Lastname` varchar(250) NOT NULL,
  `Phoneno` bigint(250) NOT NULL,
  `Emailid` varchar(250) NOT NULL,
  `Address` varchar(250) NOT NULL,
  `Username` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  `Recorded_Date` date NOT NULL,
  PRIMARY KEY (`UserId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `dataownerdetails`
--

INSERT INTO `dataownerdetails` (`UserId`, `Firstname`, `Lastname`, `Phoneno`, `Emailid`, `Address`, `Username`, `Password`, `Recorded_Date`) VALUES
(1, 'Roofing Technologies', '-', 9043963074, 'kirubakarans2009@gmail.com', 'chennai', 'test', 'test', '2023-11-28');

-- --------------------------------------------------------

--
-- Table structure for table `orderdetails`
--

CREATE TABLE IF NOT EXISTS `orderdetails` (
  `OrderId` int(11) NOT NULL AUTO_INCREMENT,
  `PersonId` int(11) NOT NULL,
  `UserId` int(11) NOT NULL,
  `Product_Id` int(11) NOT NULL,
  `Size_Id` varchar(250) NOT NULL,
  `Quantity` varchar(250) NOT NULL,
  `Production_Date` datetime DEFAULT NULL,
  `Updated_Date` datetime DEFAULT NULL,
  `Delivered` tinyint(1) DEFAULT NULL,
  `Delivered_Date` datetime DEFAULT NULL,
  `Recorded_Date` datetime NOT NULL,
  PRIMARY KEY (`OrderId`),
  KEY `PersonId` (`PersonId`),
  KEY `Product_Id` (`Product_Id`),
  KEY `UserId` (`UserId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=28 ;

--
-- Dumping data for table `orderdetails`
--

INSERT INTO `orderdetails` (`OrderId`, `PersonId`, `UserId`, `Product_Id`, `Size_Id`, `Quantity`, `Production_Date`, `Updated_Date`, `Delivered`, `Delivered_Date`, `Recorded_Date`) VALUES
(23, 6, 1, 2, '6', '°…©]ÒyHþOG/áŒ', '2023-12-24 00:00:00', '2023-12-21 00:00:00', 1, '2024-01-08 00:00:00', '2023-12-21 20:20:14'),
(24, 6, 1, 2, '5', '°…©]ÒyHþOG/áŒ', '2023-12-27 00:00:00', '2023-12-21 00:00:00', 1, '2024-01-08 00:00:00', '2023-12-21 20:20:15'),
(25, 6, 1, 2, '1', '*â{ü¢¸Ç„$;áŸ¼Œ', '2023-12-28 00:00:00', '2024-01-08 00:00:00', 1, '2023-12-29 00:00:00', '2024-01-08 19:24:10'),
(26, 6, 1, 2, '4', '™ä@Ú+*õŸ~ëõµik', '2023-12-29 00:00:00', '2024-01-08 00:00:00', 1, '2023-12-30 00:00:00', '2024-01-08 20:40:08'),
(27, 6, 1, 2, '3', '™ä@Ú+*õŸ~ëõµik', '2023-12-30 00:00:00', '2024-01-08 00:00:00', 1, '2023-12-31 00:00:00', '2024-01-08 20:40:09');

-- --------------------------------------------------------

--
-- Table structure for table `personaldetails`
--

CREATE TABLE IF NOT EXISTS `personaldetails` (
  `PersonId` int(11) NOT NULL AUTO_INCREMENT,
  `Firstname` varchar(250) NOT NULL,
  `Lastname` varchar(250) NOT NULL,
  `Phoneno` bigint(250) NOT NULL,
  `Emailid` varchar(250) NOT NULL,
  `Address` varchar(250) NOT NULL,
  `Username` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  `Recorded_Date` date NOT NULL,
  PRIMARY KEY (`PersonId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

--
-- Dumping data for table `personaldetails`
--

INSERT INTO `personaldetails` (`PersonId`, `Firstname`, `Lastname`, `Phoneno`, `Emailid`, `Address`, `Username`, `Password`, `Recorded_Date`) VALUES
(6, 'kiruba', 's', 9043963074, 'kirubakarans2009@gmail.com', 'chennai', 'kiruba', 'kiruba', '2023-11-28');

-- --------------------------------------------------------

--
-- Table structure for table `productdetails`
--

CREATE TABLE IF NOT EXISTS `productdetails` (
  `Product_Id` int(11) NOT NULL AUTO_INCREMENT,
  `UserId` int(11) NOT NULL,
  `Name` varchar(250) NOT NULL,
  `Description` text NOT NULL,
  `Price` int(11) NOT NULL,
  `Image` varchar(250) DEFAULT NULL,
  `Size_Id` varchar(250) NOT NULL,
  `Status` tinyint(1) NOT NULL,
  `Recorded_Date` datetime NOT NULL,
  PRIMARY KEY (`Product_Id`),
  KEY `UserId` (`UserId`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `productdetails`
--

INSERT INTO `productdetails` (`Product_Id`, `UserId`, `Name`, `Description`, `Price`, `Image`, `Size_Id`, `Status`, `Recorded_Date`) VALUES
(1, 1, 'Plastic Roofing Sheets', 'Plastic sheet is the least preferred roofing option available in the market. Being less durable, they are suitable only for the construction of garden sheds and temporary structures. In case you are planning to build a structure that falls under the said categories, plastic could be a suitable choice. Precisely, the durability of plastic sheets depends on the choice of plastic. However, good quality plastic also elevates the overall cost of the structure.', 400, 'Plastic-Roofing-Sheets.png', '1,2,3,4,7,8,10', 1, '2023-11-28 10:48:10'),
(2, 1, 'Metal Roofing Sheets', 'Metal roofing sheets comprise tin, zinc, aluminium, and copper sheets that help customise rooftops based on factors such as style and price. Besides offering longevity and durability, metal sheets are also energy-efficient. It is available in a wide array of colours, styles, and textures. Though these are somewhat similar to corrugated roofing sheets in terms of composition, they have significantly lesser curves.', 1200, 'Metal-Roofing-Sheets.png', '1,2,3,4,5,6,7,8,9,10,11,12', 1, '2023-11-28 10:50:48'),
(3, 1, 'Galvanized Iron Roofing Sheet', 'The galvanized iron coating has a unique metallurgical structure that protects against abrasion and mechanical damage during shipment, installation, and service. Galvanized iron roofing sheets are designed to automatically protect any damaged areas of the sheet. The sheets serve as a cathode or sacrificial layer of protection for any small areas that may be damaged during shipping. As a result, the covering protects the full length of the sheets.', 1500, 'Galvanized-Iron-Roofing-Sheets.png', '4,5,6,11,12', 0, '2023-11-28 10:54:08');

-- --------------------------------------------------------

--
-- Table structure for table `sizedetails`
--

CREATE TABLE IF NOT EXISTS `sizedetails` (
  `Size_Id` int(11) NOT NULL AUTO_INCREMENT,
  `Sheet_Thickness` varchar(250) NOT NULL,
  `Standard_Sheet_Length` varchar(250) NOT NULL,
  `Overall_Profile_Width` varchar(250) NOT NULL,
  `Effective_Cover_Width` varchar(250) NOT NULL,
  `Minimum_Roof_Slope` varchar(250) NOT NULL,
  `Status` tinyint(1) NOT NULL,
  `Recorded_Date` datetime NOT NULL,
  PRIMARY KEY (`Size_Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=13 ;

--
-- Dumping data for table `sizedetails`
--

INSERT INTO `sizedetails` (`Size_Id`, `Sheet_Thickness`, `Standard_Sheet_Length`, `Overall_Profile_Width`, `Effective_Cover_Width`, `Minimum_Roof_Slope`, `Status`, `Recorded_Date`) VALUES
(1, '0.45 mm TCT (Standard)', '1830 mm (6 ft)', '1090 mm', '1000 mm', '15 degrees', 1, '2023-11-28 00:00:00'),
(2, '0.45 mm TCT (Standard)', '2440 mm (8 ft)', '1090 mm', '1000 mm', '15 degrees', 1, '2023-11-28 00:00:00'),
(3, '0.45 mm TCT (Standard)', '3050 mm (10 ft)', '1090 mm', '1000 mm', '15 degrees', 1, '2023-11-28 00:00:00'),
(4, '0.45 mm TCT (Standard)', '3660 mm (12 ft)', '1090 mm', '1000 mm', '15 degrees', 1, '2023-11-28 00:00:00'),
(5, '0.45 mm TCT (Standard)', '4270 mm (14 ft)', '1090 mm', '1000 mm', '15 degrees', 1, '2023-11-28 00:00:00'),
(6, '0.45 mm TCT (Standard)', '4880 mm (16ft)', '1090 mm', '1000 mm', '15 degrees', 1, '2023-11-28 00:00:00'),
(7, '0.50 mm TCT (Premium)', '1830 mm (6 ft)', '1090 mm', '1000 mm', '15 degrees', 1, '2023-11-28 00:00:00'),
(8, '0.50 mm TCT (Premium)', '2440 mm (8 ft)', '1090 mm', '1000 mm', '15 degrees', 1, '2023-11-28 00:00:00'),
(9, '0.50 mm TCT (Premium)', '3050 mm (10 ft)', '1090 mm', '1000 mm', '15 degrees', 1, '2023-11-28 00:00:00'),
(10, '0.50 mm TCT (Premium)', '3660 mm (12 ft)', '1090 mm', '1000 mm', '15 degrees', 1, '2023-11-28 00:00:00'),
(11, '0.50 mm TCT (Premium)', '4270 mm (14 ft)', '1090 mm', '1000 mm', '15 degrees', 1, '2023-11-28 00:00:00'),
(12, '0.50 mm TCT (Premium)', '4880 mm (16ft)', '1090 mm', '1000 mm', '15 degrees', 1, '2023-11-28 00:00:00');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `configdetails`
--
ALTER TABLE `configdetails`
  ADD CONSTRAINT `configdetails_ibfk_1` FOREIGN KEY (`CategoryId`) REFERENCES `categorydetails` (`CategoryId`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `configdetails_ibfk_2` FOREIGN KEY (`Size_Id`) REFERENCES `sizedetails` (`Size_Id`) ON DELETE CASCADE,
  ADD CONSTRAINT `configdetails_ibfk_3` FOREIGN KEY (`UserId`) REFERENCES `dataownerdetails` (`UserId`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `orderdetails`
--
ALTER TABLE `orderdetails`
  ADD CONSTRAINT `orderdetails_ibfk_1` FOREIGN KEY (`PersonId`) REFERENCES `personaldetails` (`PersonId`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `orderdetails_ibfk_2` FOREIGN KEY (`Product_Id`) REFERENCES `productdetails` (`Product_Id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `orderdetails_ibfk_3` FOREIGN KEY (`UserId`) REFERENCES `dataownerdetails` (`UserId`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `productdetails`
--
ALTER TABLE `productdetails`
  ADD CONSTRAINT `productdetails_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `dataownerdetails` (`UserId`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
