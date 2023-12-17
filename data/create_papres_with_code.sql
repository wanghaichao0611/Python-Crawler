# create pa
drop table if exists papers_with_code;
CREATE TABLE `papers_with_code`
(
    `id`          varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '主键Id',
    `title`       varchar(1000)                                           DEFAULT NULL COMMENT '标题',
    `content`     varchar(2000)                                           DEFAULT NULL COMMENT '简要',
    `star`        varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'star',
    `pdf_url`     varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT 'pdf_url',
    `github_url`  varchar(500)                                            DEFAULT NULL COMMENT 'github_url',
    `date`        varchar(100)                                            DEFAULT NULL COMMENT 'date',
    `create_time` datetime                                                DEFAULT NULL COMMENT 'create_time',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;