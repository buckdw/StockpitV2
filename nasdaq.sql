SET NAMES latin1;
SET FOREIGN_KEY_CHECKS = 0;

CREATE TABLE `nasdaq` (
`long_name` varchar(255) NOT NULL DEFAULT '',
`symbol` varchar(8) NOT NULL DEFAULT '',
`open` float NOT NULL DEFAULT '0',
`close` float NOT NULL DEFAULT '0',
`eps` float NOT NULL DEFAULT '0',
PRIMARY KEY (`symbol`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

insert into `nasdaq` values('Apple Inc.','AAPL','0','0','0');

SET FOREIGN_KEY_CHECKS = 1;

