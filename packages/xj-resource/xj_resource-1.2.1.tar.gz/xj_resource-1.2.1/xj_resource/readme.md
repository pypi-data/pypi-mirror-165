# 模块介绍

## 1.资源上传

1.文件上传

2.图片上传

# SQL

```mysql
CREATE TABLE `resource_file` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL DEFAULT '0' COMMENT '用户ID',
  `title` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `url` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '保存路径',
  `filename` varchar(80) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '文件名称',
  `format` varchar(10) COLLATE utf8_unicode_ci NOT NULL COMMENT '文件后缀',
  `thumb` varchar(255) COLLATE utf8_unicode_ci DEFAULT '' COMMENT '缩略图位置',
  `md5` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `snapshot` json DEFAULT NULL COMMENT '文件快照',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='文件上传表';


CREATE TABLE `resource_file_map` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_id` int(11) NOT NULL COMMENT '图片ID',
  `source_id` int(11) NOT NULL COMMENT '来源表 关联ID',
  `source_table` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT '来源表表明',
  `price` int(10) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `image_id` (`file_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


CREATE TABLE `resource_image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL DEFAULT '0' COMMENT '用户ID',
  `title` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `url` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '保存路径',
  `filename` varchar(80) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '文件名称',
  `format` varchar(10) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '文件后缀',
  `thumb` varchar(255) COLLATE utf8_unicode_ci DEFAULT '' COMMENT '缩略图位置',
  `md5` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `snapshot` json DEFAULT NULL COMMENT '文件快照',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='文件上传表';

CREATE TABLE `resource_image_map` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `image_id` int(11) NOT NULL COMMENT '图片ID',
  `source_id` int(11) NOT NULL COMMENT '来源表 关联ID',
  `source_table` varchar(255) COLLATE utf8_unicode_ci NOT NULL COMMENT '来源表表明',
  `price` int(10) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `image_id` (`image_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
```



# 配置

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
```

