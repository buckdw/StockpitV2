SET NAMES latin1;
SET FOREIGN_KEY_CHECKS = 0;

CREATE TABLE `nasdaq` (
`symbol` varchar(8) NOT NULL DEFAULT '',
`long_name` varchar(255) NOT NULL DEFAULT '',
`regular_market_open` float NOT NULL DEFAULT '0',
`close` float NOT NULL DEFAULT '0',
`market_cap` float NOT NULL DEFAULT '0',
`eps` float NOT NULL DEFAULT '0',
`forward_eps` float NOT NULL DEFAULT '0',
`regular_market_price` float NOT NULL DEFAULT '0',
PRIMARY KEY (`symbol`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

SET FOREIGN_KEY_CHECKS = 1;

