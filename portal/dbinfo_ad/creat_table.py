# -*- coding: utf-8 -*-
# @Time    : 2018/8/8 14:21
# @Author  :
from dbinfo_ad.newdbtest import dbinfo
# 9
dfs_table = '''
CREATE TABLE `folder_api_log` (
  `id` int(255) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `username` varchar(255) DEFAULT NULL COMMENT '对应传入IP',
  `isSuccess` varchar(255) DEFAULT NULL COMMENT '是否成功',
  `optype` varchar(255) DEFAULT NULL COMMENT '接口名称',
  `message` varchar(2550) DEFAULT NULL COMMENT '结果',
  `parameter` varchar(2550) DEFAULT NULL COMMENT '传入的值',
  `times` datetime DEFAULT NULL COMMENT '传入时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=180 DEFAULT CHARSET=utf8mb4 COMMENT='文件夹权限接口日志';

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
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COMMENT='文件夹权限申请流程表';

CREATE TABLE `folder_first_choice` (
  `id` int(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `folder_path` varchar(255) NOT NULL COMMENT '文件夹路径',
  `folder_level` int(50) NOT NULL COMMENT '文件夹层级，只能填写0，1',
  `server` varchar(255) DEFAULT NULL COMMENT '服务器IP',
  `server_manager` varchar(255) DEFAULT NULL COMMENT '服务器管理员',
  `watchdog` int(255) DEFAULT NULL COMMENT '是否允许自动监测文件变化（1:自动监测 or 不自动监测）',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COMMENT='文件夹权限的初始设置';

CREATE TABLE `folder_level1` (
  `id` int(50) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `level1_id` int(50) NOT NULL COMMENT '第一层目录ID',
  `name` varchar(255) NOT NULL COMMENT '第一层目录名称',
  `level1_manager` varchar(255) DEFAULT NULL COMMENT '第一层文件夹管理员',
  `level1_path` varchar(255) NOT NULL COMMENT '第一层目录路径',
  PRIMARY KEY (`id`),
  KEY `level1_id` (`level1_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8mb4 COMMENT='第一层文件夹目录';

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
) ENGINE=InnoDB AUTO_INCREMENT=797 DEFAULT CHARSET=utf8mb4 COMMENT='第二层文件夹目录';

CREATE TABLE `folder_level3` (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `level3_id` int(50) NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `level3_path` varchar(255) CHARACTER SET utf8mb4 NOT NULL COMMENT '第三层目录路径',
  PRIMARY KEY (`id`),
  KEY `level3_id` (`level3_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4229 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_slovenian_ci COMMENT='第三层文件夹目录';

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
) ENGINE=InnoDB AUTO_INCREMENT=4183 DEFAULT CHARSET=utf8 COMMENT='文件目录关系表';

CREATE TABLE `manager_dfs_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `folder_level3_id` int(11) NOT NULL,
  `perm_value` varchar(255) NOT NULL,
  `group_name` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `level3_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `manager_dfs_group_group_name` (`group_name`(191)) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=8444 DEFAULT CHARSET=utf8 COMMENT='文件夹权限表';
CREATE TABLE `watchdog_log` (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `isSuccess` varchar(255) DEFAULT NULL,
  `optype` varchar(255) DEFAULT NULL,
  `src_path` varchar(255) DEFAULT NULL,
  `dest_path` varchar(255) DEFAULT NULL,
  `message` varchar(255) DEFAULT NULL,
  `times` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=108 DEFAULT CHARSET=utf8mb4;
'''

interface_c_log ='''
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
) ENGINE=InnoDB AUTO_INCREMENT=12567 DEFAULT CHARSET=utf8mb4 COMMENT='C#接口类日志';

'''

global_configuration = '''
CREATE TABLE `global_configuration` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `iis_ip` varchar(255) DEFAULT NULL COMMENT 'iisi接口地址',
  `iis_port` varchar(255) DEFAULT NULL COMMENT 'iis接口端口',
  `ad_ip` varchar(255) DEFAULT NULL COMMENT 'ip',
  `ad_ips` varchar(255) DEFAULT NULL COMMENT '(IP_string)',
  `ad_account` varchar(255) DEFAULT NULL COMMENT '账号',
  `ad_password` varchar(255) DEFAULT NULL COMMENT '密码',
  `ad_domain` varchar(255) DEFAULT NULL COMMENT '域名',
  `ad_path` varchar(255) DEFAULT NULL COMMENT '原始路径',
  `ex_ip` varchar(255) DEFAULT NULL COMMENT 'ip',
  `ex_account` varchar(255) DEFAULT NULL COMMENT '账号',
  `ex_password` varchar(255) DEFAULT NULL COMMENT '密码',
  `ex_domain` varchar(255) DEFAULT NULL COMMENT '域名',
  `skey` varchar(255) DEFAULT NULL COMMENT '秘钥',
  `it_group` varchar(255) DEFAULT NULL COMMENT 'IT隶属组',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COMMENT='全局配置数据库';
CREATE TABLE `management_configuration` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(255) NOT NULL,
  `ADdepartMent` varchar(255) DEFAULT NULL,
  `internet_group` varchar(255) DEFAULT NULL COMMENT '网络权限',
  `vpn_group` varchar(255) DEFAULT NULL COMMENT 'VPN权限组',
  `it_authority_group` varchar(255) DEFAULT NULL COMMENT 'IT权限组（可使用IT工具）',
  `part_time_group` varchar(255) DEFAULT NULL COMMENT '可以申请兼职账号的权限组',
  `dfs_group` varchar(255) DEFAULT NULL,
  `mail_group` varchar(255) DEFAULT NULL COMMENT '邮箱群组路径',
  `NoLockGroup` varchar(255) DEFAULT NULL COMMENT '防锁定组',
  `jz_account_dn` varchar(255) DEFAULT NULL,
  `times` datetime DEFAULT NULL,
  `Basic_authority` varchar(255) DEFAULT NULL COMMENT 'dfs的默认权限初始权限；（建议 Authenticated Users）',
  `dfs_manager` varchar(255) DEFAULT NULL COMMENT '文件夹权限管理账号',
  `AD_time` int(11) unsigned zerofill NOT NULL COMMENT 'AD组新建完成后的缓冲时间，（文件夹无法实时获取到新建组）',
  `dfs_relation_name` varchar(255) DEFAULT NULL,
  `dfs_relation` varchar(255) DEFAULT NULL,
  `dfs_relation_mail` varchar(255) DEFAULT NULL,
  `dfs_api` varchar(255) DEFAULT NULL,
  `mailgroupdefaultOU` varchar(255) DEFAULT NULL COMMENT '创建邮箱群组时默认OU',
  `pubmailfence` varchar(255) NOT NULL COMMENT '公共邮箱管理者栏位信息',
  `pubmailou` varchar(255) DEFAULT NULL COMMENT '公共邮箱OU',
  `pubmailDB` varchar(255) DEFAULT NULL COMMENT '公共邮箱DB',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='默认权限组设置';
'''
api='''
CREATE TABLE `api` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mess` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
CREATE TABLE `remind` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tip` varchar(255) DEFAULT NULL,
  `top` varchar(255) DEFAULT NULL,
  `length` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
CREATE TABLE `sendmailsite` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mailcount` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `mailserver` varchar(255) DEFAULT NULL,
  `mailaddress` varchar(255) DEFAULT NULL,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
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
  `types` varchar(255) DEFAULT NULL COMMENT 'dfs，exchange，ad等类型',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4;
'''

mail_ex='''
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
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COMMENT='只有一层（主管审批）flow';
CREATE TABLE `mailsetting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `OU` varchar(255) DEFAULT NULL,
  `DB` varchar(255) DEFAULT NULL,
  `datetime` datetime DEFAULT NULL,
  `mailgroupdefaultOU` varchar(255) DEFAULT NULL COMMENT '创建邮箱群组时默认OU',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
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
'''

dxw_jz='''
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
) ENGINE=InnoDB AUTO_INCREMENT=201 DEFAULT CHARSET=utf8mb4;

'''
# def creatdb(create_interface_c_log):
#     conn = dbinfo()
#     try:
#         conncur = conn.cursor()
#         conncur.execute(create_interface_c_log)
#         conn.commit()
#         conn.close()
#         return True
#     except Exception as e:
#         print(e)
#         return False
