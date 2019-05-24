/*
Navicat MySQL Data Transfer

Source Server         : 
Source Server Version : 50505
Source Host           : 
Source Database       : itdev-portal

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2018-08-24 17:31:51
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for account_configuration_del
-- ----------------------------
DROP TABLE IF EXISTS `account_configuration_del`;
CREATE TABLE `account_configuration_del` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(255) NOT NULL COMMENT '域名',
  `ADdepartMent` varchar(255) DEFAULT NULL COMMENT '公司名称',
  `ADuser` varchar(255) DEFAULT NULL,
  `ADpassword` varchar(255) DEFAULT NULL,
  `EXuser` varchar(255) DEFAULT NULL,
  `EXpassword` varchar(255) DEFAULT NULL,
  `DFSuser` varchar(255) DEFAULT NULL,
  `DFSpassword` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='账号密码管理';

-- ----------------------------
-- Table structure for ad_configuration_del
-- ----------------------------
DROP TABLE IF EXISTS `ad_configuration_del`;
CREATE TABLE `ad_configuration_del` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(255) NOT NULL COMMENT '域名',
  `ADdepartMent` varchar(255) DEFAULT NULL COMMENT '公司名称',
  `fulldomain` varchar(255) NOT NULL COMMENT '邮件后缀(例:@contoss.com)',
  `domainIp` varchar(255) NOT NULL COMMENT '域控ip(例:)',
  `domainIps` varchar(255) DEFAULT NULL COMMENT '(IP_string)',
  `_ldapIdentity` varchar(255) DEFAULT NULL COMMENT 'LDAP://(ldap连接)',
  `_suffixPath` varchar(255) DEFAULT NULL COMMENT 'DC=,DC=com(DC路径)\r\n            ',
  `userou` varchar(255) DEFAULT NULL COMMENT '默认userOU',
  `groupou` varchar(255) DEFAULT NULL COMMENT '默认group组ou',
  `organization` varchar(255) DEFAULT NULL COMMENT '默认组织单位OU',
  `lowuserou` varchar(255) DEFAULT NULL COMMENT '默认禁用OU',
  `endou` varchar(255) DEFAULT NULL,
  `_smtp` varchar(255) DEFAULT NULL COMMENT 'com(后缀)',
  `oulayer` varchar(255) DEFAULT NULL COMMENT 'ou层级(3)',
  `organizationlayer` varchar(255) DEFAULT NULL COMMENT '组织单位层级（3）',
  `times` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='AD,OU默认设置';

-- ----------------------------
-- Table structure for api
-- ----------------------------
DROP TABLE IF EXISTS `api`;
CREATE TABLE `api` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mess` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for apimessage
-- ----------------------------
DROP TABLE IF EXISTS `apimessage`;
CREATE TABLE `apimessage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titlename` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for Crontab
-- ----------------------------
DROP TABLE IF EXISTS `Crontab`;
CREATE TABLE `Crontab` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '定时任务',
  `inform_day_of_week` varchar(255) NOT NULL COMMENT '执行时间（0-6 每天，1-5周一至周五）',
  `inform_hour` varchar(2) NOT NULL COMMENT '时间双数24小时制如：01，22',
  `inform_minute` varchar(2) NOT NULL COMMENT '分钟，双数00-59',
  `delete_day_of_week` varchar(255) NOT NULL COMMENT '执行时间（0-6 每天，1-5周一至周五）',
  `delete_hour` varchar(2) NOT NULL COMMENT '时间双数24小时制如：01，22',
  `delete_minute` varchar(2) NOT NULL COMMENT '分钟，双数00-59',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for ex_configuration
-- ----------------------------
DROP TABLE IF EXISTS `ex_configuration`;
CREATE TABLE `ex_configuration` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(255) NOT NULL COMMENT '域名',
  `ADdepartMent` varchar(255) DEFAULT NULL COMMENT '公司',
  `mailip` varchar(255) DEFAULT NULL COMMENT '邮件服务器ip',
  `fullExchange` varchar(255) DEFAULT NULL,
  `defaultMsExchArchiveDatabase` varchar(255) DEFAULT NULL,
  `msExchArchiveDatabaseLink` varchar(255) DEFAULT NULL,
  `msExchArchiveName` varchar(255) DEFAULT NULL,
  `msExchArchiveQuota` varchar(255) DEFAULT NULL,
  `msExchArchiveWarnQuota` varchar(255) DEFAULT NULL,
  `msExchELCMailboxFlags` varchar(255) DEFAULT NULL,
  `msExchMailboxTemplateLink` varchar(255) DEFAULT NULL,
  `mailgroupdefaultOU` varchar(255) DEFAULT '' COMMENT '创建邮箱群组时默认OU',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='邮箱默认设置';

-- ----------------------------
-- Table structure for fixmanger
-- ----------------------------
DROP TABLE IF EXISTS `fixmanger`;
CREATE TABLE `fixmanger` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pubmailmanger` varchar(255) DEFAULT NULL,
  `mailgroumanger` varchar(255) DEFAULT NULL,
  `dfsmanger` varchar(255) DEFAULT NULL,
  `networkmanger` varchar(255) DEFAULT NULL,
  `vnpmanger` varchar(255) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for flow_director
-- ----------------------------
DROP TABLE IF EXISTS `flow_director`;
CREATE TABLE `flow_director` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(255) DEFAULT NULL COMMENT '访问IP',
  `adaccount` varchar(255) DEFAULT NULL COMMENT 'True:成功',
  `displayname` varchar(255) DEFAULT NULL COMMENT '认证tokenid（0:默认权限',
  `types` varchar(255) DEFAULT NULL COMMENT '类型，AD,EX，DFS',
  `applytype` varchar(255) DEFAULT NULL COMMENT '接口名字',
  `applydetail` varchar(255) DEFAULT NULL COMMENT '传入参数',
  `submittime` datetime DEFAULT NULL COMMENT '执行结果',
  `director` varchar(255) DEFAULT NULL,
  `directorstatus` int(11) DEFAULT NULL COMMENT '备注or其他',
  `flowstatus` int(11) NOT NULL COMMENT '0:等待审批；1:执行成功；2:执行失败；5:驳回',
  `endtime` datetime DEFAULT NULL,
  `message` varchar(255) CHARACTER SET utf8 DEFAULT NULL COMMENT '详情信息',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=utf8mb4 COMMENT='只有一层（主管审批）flow';

-- ----------------------------
-- Table structure for folder_api_log
-- ----------------------------
DROP TABLE IF EXISTS `folder_api_log`;
CREATE TABLE `folder_api_log` (
  `id` int(255) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `username` varchar(255) DEFAULT NULL COMMENT '对应传入IP',
  `isSuccess` varchar(255) DEFAULT NULL COMMENT '是否成功',
  `optype` varchar(255) DEFAULT NULL COMMENT '接口名称',
  `message` varchar(2550) DEFAULT NULL COMMENT '结果',
  `parameter` varchar(2550) DEFAULT NULL COMMENT '传入的值',
  `times` datetime DEFAULT NULL COMMENT '传入时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=233 DEFAULT CHARSET=utf8mb4 COMMENT='文件夹权限接口日志';

-- ----------------------------
-- Table structure for folder_dfs_flow
-- ----------------------------
DROP TABLE IF EXISTS `folder_dfs_flow`;
CREATE TABLE `folder_dfs_flow` (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL COMMENT '权限使用人账户',
  `displayName` varchar(255) DEFAULT NULL COMMENT '权限使用人',
  `tree_id` int(50) DEFAULT NULL COMMENT '3层目录关系ID,3层目录ID',
  `group_name` varchar(255) DEFAULT NULL COMMENT '权限组名称',
  `submit_time` datetime DEFAULT NULL COMMENT '申请时间',
  `director_name` varchar(255) DEFAULT NULL COMMENT '主管',
  `director_adaccount` varchar(255) DEFAULT NULL COMMENT '主管账户',
  `director_status` varchar(255) DEFAULT NULL COMMENT '主管审批状态',
  `director_time` datetime DEFAULT NULL COMMENT '主管审批时间',
  `relation_name` varchar(255) DEFAULT NULL COMMENT '文件夹管理员',
  `relation_adaccount` varchar(255) DEFAULT NULL COMMENT '文件夹管理员账户',
  `relation_status` varchar(255) DEFAULT NULL COMMENT '文件夹管理员审批状态',
  `relation_time` datetime DEFAULT NULL COMMENT '文件夹管理员审批时间',
  `flow_status` varchar(255) DEFAULT NULL COMMENT '最终审批状态',
  `end_time` datetime DEFAULT NULL COMMENT '最终审批时间',
  `authority_applicant` varchar(255) DEFAULT NULL COMMENT '权限申请人',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=111 DEFAULT CHARSET=utf8mb4 COMMENT='文件夹权限申请流程表';

-- ----------------------------
-- Table structure for folder_first_choice
-- ----------------------------
DROP TABLE IF EXISTS `folder_first_choice`;
CREATE TABLE `folder_first_choice` (
  `id` int(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `folder_path` varchar(255) NOT NULL COMMENT '文件夹路径',
  `folder_level` int(50) NOT NULL COMMENT '文件夹层级，只能填写0，1',
  `server` varchar(255) DEFAULT NULL COMMENT '服务器IP',
  `server_manager` varchar(255) DEFAULT NULL COMMENT '服务器管理员',
  `watchdog` int(255) DEFAULT NULL COMMENT '是否允许自动监测文件变化（1:自动监测 or 不自动监测）',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COMMENT='文件夹权限的初始设置';

-- ----------------------------
-- Table structure for folder_level1
-- ----------------------------
DROP TABLE IF EXISTS `folder_level1`;
CREATE TABLE `folder_level1` (
  `id` int(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `level1_id` int(50) NOT NULL COMMENT '第一层目录ID',
  `name` varchar(255) NOT NULL COMMENT '第一层目录名称',
  `level1_manager` varchar(255) DEFAULT NULL COMMENT '第一层文件夹管理员',
  `level1_path` varchar(255) NOT NULL COMMENT '第一层目录路径',
  PRIMARY KEY (`id`),
  KEY `level1_id` (`level1_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb4 COMMENT='第一层文件夹目录';

-- ----------------------------
-- Table structure for folder_level2
-- ----------------------------
DROP TABLE IF EXISTS `folder_level2`;
CREATE TABLE `folder_level2` (
  `id` int(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `level2_id` int(50) NOT NULL COMMENT '第二层目录ID',
  `name` varchar(255) NOT NULL COMMENT '第二层目录名称',
  `level2_manager` varchar(255) DEFAULT NULL COMMENT '第二层文件夹管理员账户',
  `level2_path` varchar(255) NOT NULL COMMENT '第二层目录路径',
  `level2_manager_name` varchar(255) DEFAULT NULL COMMENT '第二层目录文件夹管理员',
  `level2_manager_mail` varchar(255) DEFAULT NULL COMMENT '第二层目录文件夹管理员邮箱',
  PRIMARY KEY (`id`),
  KEY `level2_id` (`level2_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=802 DEFAULT CHARSET=utf8mb4 COMMENT='第二层文件夹目录';

-- ----------------------------
-- Table structure for folder_level3
-- ----------------------------
DROP TABLE IF EXISTS `folder_level3`;
CREATE TABLE `folder_level3` (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `level3_id` int(50) NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `level3_path` varchar(255) CHARACTER SET utf8mb4 NOT NULL COMMENT '第三层目录路径',
  PRIMARY KEY (`id`),
  KEY `level3_id` (`level3_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4239 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_slovenian_ci COMMENT='第三层文件夹目录';

-- ----------------------------
-- Table structure for folder_tree
-- ----------------------------
DROP TABLE IF EXISTS `folder_tree`;
CREATE TABLE `folder_tree` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tree_id` int(11) NOT NULL,
  `level1_id` int(11) NOT NULL,
  `level2_id` int(11) NOT NULL,
  `level3_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `folder_tree_level1_id_443c2a02_fk_folder_level1_id` (`level1_id`) USING BTREE,
  KEY `folder_tree_level2_id_87b6b092_fk_folder_level2_id` (`level2_id`) USING BTREE,
  KEY `folder_tree_level3_id_6e019842_fk_folder_level3_id` (`level3_id`) USING BTREE,
  KEY `treeid` (`tree_id`) USING BTREE,
  CONSTRAINT `folder_tree_ibfk_1` FOREIGN KEY (`level1_id`) REFERENCES `folder_level1` (`level1_id`),
  CONSTRAINT `folder_tree_ibfk_2` FOREIGN KEY (`level2_id`) REFERENCES `folder_level2` (`level2_id`),
  CONSTRAINT `folder_tree_ibfk_3` FOREIGN KEY (`level3_id`) REFERENCES `folder_level3` (`level3_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4193 DEFAULT CHARSET=utf8 COMMENT='文件目录关系表';

-- ----------------------------
-- Table structure for global_configuration
-- ----------------------------
DROP TABLE IF EXISTS `global_configuration`;
CREATE TABLE `global_configuration` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `iis_ip` varchar(255) DEFAULT 'None' COMMENT 'iisi接口地址',
  `iis_port` varchar(255) DEFAULT 'None' COMMENT 'iis接口端口',
  `ad_ip` varchar(255) DEFAULT 'None' COMMENT 'ip',
  `ad_ips` varchar(255) DEFAULT 'None' COMMENT '(IP_string)',
  `ad_account` varchar(255) DEFAULT 'None' COMMENT '账号',
  `ad_password` varchar(255) DEFAULT 'None' COMMENT '密码',
  `ad_domain` varchar(255) DEFAULT 'None' COMMENT '域名',
  `ad_path` varchar(255) DEFAULT 'None' COMMENT '原始路径',
  `ex_ip` varchar(255) DEFAULT 'None' COMMENT 'ip',
  `ex_account` varchar(255) DEFAULT 'None' COMMENT '账号',
  `ex_password` varchar(255) DEFAULT 'None' COMMENT '密码',
  `ex_domain` varchar(255) DEFAULT 'None' COMMENT '域名',
  `skey` varchar(255) DEFAULT NULL COMMENT '秘钥',
  `it_group` varchar(255) DEFAULT 'None' COMMENT 'IT隶属组',
  `adminpwd` varchar(255) DEFAULT 'None' COMMENT '管理员账号密码',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COMMENT='全局配置数据库';

-- ----------------------------
-- Table structure for interface_c_log
-- ----------------------------
DROP TABLE IF EXISTS `interface_c_log`;
CREATE TABLE `interface_c_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(255) DEFAULT NULL COMMENT '访问IP',
  `isSuccess` varchar(255) DEFAULT NULL COMMENT 'True:成功',
  `tokenid` varchar(255) DEFAULT NULL COMMENT '认证tokenid',
  `apiname` varchar(255) DEFAULT NULL COMMENT '接口名字',
  `parameter` mediumtext COMMENT '传入参数',
  `message` mediumtext COMMENT '执行结果',
  `times` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=88571 DEFAULT CHARSET=utf8mb4 COMMENT='C#接口类日志';

-- ----------------------------
-- Table structure for jztimecount
-- ----------------------------
DROP TABLE IF EXISTS `jztimecount`;
CREATE TABLE `jztimecount` (
  `id` int(111) NOT NULL AUTO_INCREMENT,
  `jzcount` varchar(255) DEFAULT NULL,
  `displayname` varchar(255) DEFAULT NULL,
  `deadtime` datetime DEFAULT NULL,
  `datetime` datetime DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `sqaccount` varchar(255) DEFAULT NULL,
  `sqname` varchar(255) DEFAULT NULL,
  `sqmail` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=358 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for mail_publicmail
-- ----------------------------
DROP TABLE IF EXISTS `mail_publicmail`;
CREATE TABLE `mail_publicmail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `displayname` varchar(255) DEFAULT NULL,
  `pubmail` varchar(255) DEFAULT NULL,
  `maildisname` varchar(255) DEFAULT NULL,
  `depment` varchar(255) DEFAULT NULL,
  `manger` varchar(255) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for mailsetting
-- ----------------------------
DROP TABLE IF EXISTS `mailsetting`;
CREATE TABLE `mailsetting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `OU` varchar(255) DEFAULT NULL,
  `DB` varchar(255) DEFAULT NULL,
  `datetime` datetime DEFAULT NULL,
  `mailgroupdefaultOU` varchar(255) DEFAULT NULL COMMENT '创建邮箱群组时默认OU',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for management_configuration
-- ----------------------------
DROP TABLE IF EXISTS `management_configuration`;
CREATE TABLE `management_configuration` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(255) NOT NULL,
  `internet_group` varchar(255) DEFAULT NULL COMMENT '网络权限',
  `wifi_group` varchar(255) DEFAULT NULL COMMENT '无线用户组',
  `vpn_group` varchar(255) DEFAULT NULL COMMENT 'VPN权限组',
  `part_time_group` varchar(255) DEFAULT NULL COMMENT '可以申请兼职账号的权限组',
  `dfs_group` varchar(255) DEFAULT NULL,
  `NoLockGroup` varchar(255) DEFAULT NULL COMMENT '防锁定组',
  `jz_account_dn` varchar(255) DEFAULT NULL COMMENT '创建兼职账号路径',
  `Basic_authority` varchar(255) DEFAULT NULL COMMENT 'dfs的默认权限初始权限；（建议 Authenticated Users）',
  `dfs_manager` varchar(255) DEFAULT NULL COMMENT '文件夹权限管理账号',
  `AD_time` int(11) unsigned zerofill DEFAULT NULL COMMENT 'AD组新建完成后的缓冲时间，（文件夹无法实时获取到新建组）',
  `dfs_relation_name` varchar(255) DEFAULT NULL,
  `dfs_relation` varchar(255) DEFAULT NULL,
  `dfs_relation_mail` varchar(255) DEFAULT NULL,
  `dfs_switch` varchar(255) DEFAULT NULL,
  `dfs_api` varchar(255) DEFAULT NULL,
  `mailgroupdefaultOU` varchar(255) DEFAULT NULL COMMENT '创建邮箱群组时默认OU',
  `pubmailfence` varchar(255) DEFAULT NULL COMMENT '公共邮箱管理者栏位信息',
  `pubmailou` varchar(255) DEFAULT NULL COMMENT '公共邮箱OU',
  `pubmailDB` varchar(255) DEFAULT NULL COMMENT '公共邮箱DB',
  `passwordlength` varchar(255) DEFAULT NULL,
  `pwdtips` varchar(255) DEFAULT NULL,
  `lengthpwd` varchar(255) DEFAULT NULL,
  `pwdremindertips` varchar(255) DEFAULT NULL COMMENT '是否开启密码过期提醒',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COMMENT='默认权限组设置';

-- ----------------------------
-- Table structure for management_configuration_copy
-- ----------------------------
DROP TABLE IF EXISTS `management_configuration_copy`;
CREATE TABLE `management_configuration_copy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(255) NOT NULL,
  `ADdepartMent` varchar(255) DEFAULT NULL,
  `internet_group` varchar(255) DEFAULT NULL COMMENT '网络权限',
  `wifi_group` varchar(255) DEFAULT NULL COMMENT '无线用户组',
  `vpn_group` varchar(255) DEFAULT NULL COMMENT 'VPN权限组',
  `part_time_group` varchar(255) DEFAULT NULL COMMENT '可以申请兼职账号的权限组',
  `dfs_group` varchar(255) DEFAULT NULL,
  `NoLockGroup` varchar(255) DEFAULT NULL COMMENT '防锁定组',
  `jz_account_dn` varchar(255) DEFAULT NULL COMMENT '创建兼职账号路径',
  `times` datetime DEFAULT NULL,
  `Basic_authority` varchar(255) DEFAULT NULL COMMENT 'dfs的默认权限初始权限；（建议 Authenticated Users）',
  `dfs_manager` varchar(255) DEFAULT NULL COMMENT '文件夹权限管理账号',
  `AD_time` int(11) unsigned zerofill DEFAULT NULL COMMENT 'AD组新建完成后的缓冲时间，（文件夹无法实时获取到新建组）',
  `dfs_relation_name` varchar(255) DEFAULT NULL,
  `dfs_relation` varchar(255) DEFAULT NULL,
  `dfs_relation_mail` varchar(255) DEFAULT NULL,
  `dfs_switch` varchar(255) DEFAULT NULL,
  `dfs_api` varchar(255) DEFAULT NULL,
  `mailgroupdefaultOU` varchar(255) DEFAULT NULL COMMENT '创建邮箱群组时默认OU',
  `pubmailfence` varchar(255) DEFAULT NULL COMMENT '公共邮箱管理者栏位信息',
  `pubmailou` varchar(255) DEFAULT NULL COMMENT '公共邮箱OU',
  `pubmailDB` varchar(255) DEFAULT NULL COMMENT '公共邮箱DB',
  `passwordlength` varchar(255) DEFAULT NULL,
  `pwdtips` varchar(255) DEFAULT NULL,
  `lengthpwd` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='默认权限组设置';

-- ----------------------------
-- Table structure for manager_dfs_group
-- ----------------------------
DROP TABLE IF EXISTS `manager_dfs_group`;
CREATE TABLE `manager_dfs_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `folder_level3_id` int(11) NOT NULL,
  `perm_value` varchar(255) NOT NULL,
  `group_name` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `level3_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `manager_dfs_group_group_name` (`group_name`(191)) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=8464 DEFAULT CHARSET=utf8 COMMENT='文件夹权限表';

-- ----------------------------
-- Table structure for sendmailsite
-- ----------------------------
DROP TABLE IF EXISTS `sendmailsite`;
CREATE TABLE `sendmailsite` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mailcount` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `mailserver` varchar(255) DEFAULT NULL,
  `mailaddress` varchar(255) DEFAULT NULL,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for systemlog
-- ----------------------------
DROP TABLE IF EXISTS `systemlog`;
CREATE TABLE `systemlog` (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL COMMENT '操作者用户名',
  `datetimevalue` datetime DEFAULT NULL COMMENT '时间',
  `ip` varchar(255) DEFAULT NULL COMMENT '操作者IP',
  `resultvalue` int(255) DEFAULT NULL COMMENT '日志状态。0：报错，1：正常，2：警告',
  `message` mediumtext COMMENT '执行结果详情',
  `issuccess` int(255) DEFAULT NULL COMMENT '执行结果状态。0：执行失败，1：执行成功',
  `inparameters` mediumtext COMMENT '传入参数',
  `methodname` varchar(255) DEFAULT NULL COMMENT '方法名',
  `returnparameters` mediumtext COMMENT '返回参数',
  `types` varchar(255) DEFAULT NULL COMMENT 'dfs，exchange，AD,other等类型',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4543 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for titleshow
-- ----------------------------
DROP TABLE IF EXISTS `titleshow`;
CREATE TABLE `titleshow` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `heard` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for watchdog_log
-- ----------------------------
DROP TABLE IF EXISTS `watchdog_log`;
CREATE TABLE `watchdog_log` (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `isSuccess` varchar(255) DEFAULT NULL,
  `optype` varchar(255) DEFAULT NULL,
  `src_path` varchar(255) DEFAULT NULL,
  `dest_path` varchar(255) DEFAULT NULL,
  `message` varchar(255) DEFAULT NULL,
  `times` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=116 DEFAULT CHARSET=utf8mb4;

INSERT  INTO global_configuration (id) VALUE (1);
