
CREATE TABLE `rules`
(
    `id` int NOT NULL auto_increment,
    `path` varchar(255) NOT NULL,
    `request` text NOT NULL,
    `response` text NOT NULL,
    PRIMARY KEY(`id`),
    KEY(`path`)
) ENGINE=InnoDB DEFAULT CHARSET utf8;
