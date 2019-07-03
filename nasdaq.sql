SET NAMES latin1;
SET FOREIGN_KEY_CHECKS = 0;

CREATE TABLE `nasdaq` (
`symbol` varchar(8) NOT NULL DEFAULT '',
`long_name` varchar(255) NOT NULL DEFAULT '',
`regular_market_open` float NOT NULL DEFAULT '0',
`close` float NOT NULL DEFAULT '0',
`market_cap` float NOT NULL DEFAULT '0',
`eps` float NOT NULL DEFAULT '0',
PRIMARY KEY (`symbol`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

insert into `nasdaq` values('AAPL','Apple Inc.','203.28','0','936688000000','0'),
('SSYS','Stratasys Ltd.','27.36','0','1494160000','0'),
('DASTY','Dassault SystËmes SE','164.628','0','43373200000','0'),
('DDD','3D Systems Corporation','8.9','0','1051390000','0');

SET FOREIGN_KEY_CHECKS = 1;

