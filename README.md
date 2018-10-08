# aox_proxy_pool | Ip代理池项目
本项目是为了解决在抓取代理ip后, 代理ip失效快, 不稳定的问题 以及代理ip使用不方便等问题。

1. 可以自己去增加抓取的代理ip网站, 项目会自动去重, 并且之前抓取过的ip会保存在数据库中, 不会删除, 所以放心不会出现重复抓取的问题
2. 通过校验服务器开放的端口、访问的速度、校验多个网址访问的情况来对代理ip设置权重排序, 达到过滤垃圾ip的目的, 运行一段时间后剩下的ip, 则可以进入使用, 而且实测比较稳定
3. 通过脚本自动更新squid配置文件, 这样使用的客户端只需要指定squid服务器的地址即可。
4. 自动网络监测, 断网等情况下不会进行ip监测, 防止意外数据出错。

![avatar](https://raw.githubusercontent.com/aox-lei/aox_proxy_pool/master/readme/1.png)

## 功能特色

1. 可自行增加代理抓取渠道
2. ip校验模块
3. squid配置自动更新
4. 客户端使用简单

## 运行环境
1. python 3.6
2. pipenv
3. scrapy模块
3. mysql5.6

## 运行部署
1. 克隆代码
```
git clone "https://github.com/aox-lei/aox_proxy_pool"
```

2. 本机安装python3.6、pip、pipenv、mysql
3. 安装虚拟环境以及python模块
```
> pipenv --three
> pipenv shell
> pipenv install 
```
4. 复制配置文件
```
> cp proxy_pool/config.ini.default proxy_pool/config.ini
```
5. 修改配置信息和创建数据表
```sql
CREATE TABLE `ip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` char(15) NOT NULL DEFAULT '',
  `port` int(6) NOT NULL DEFAULT '0',
  `score` tinyint(5) NOT NULL DEFAULT '5' COMMENT '得分, 默认5分, 抓取成功一次, 分数+1, 失败一次-1, 到0则不抓取',
  `weight` int(3) NOT NULL DEFAULT '0' COMMENT '权重',
  `speed` int(11) NOT NULL DEFAULT '0' COMMENT '平均速度',
  `http_type` tinyint(1) NOT NULL DEFAULT '1' COMMENT '支持的http类型: 1:http 2:https 3:all',
  `country` char(5) NOT NULL DEFAULT '' COMMENT '所属国家',
  `open_port` varchar(255) NOT NULL DEFAULT '' COMMENT '开放端口， 逗号分隔',
  `create_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `update_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_ip_port` (`ip`,`port`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4538 DEFAULT CHARSET=utf8
```
6. 运行抓取项目
```
> scrapy crawl xici
> scrapy crawl kuaidaili
> scrapy crawl ip66
```
7. 运行ip检测
```
> python manager.py check_proxy
```
8. 运行squid同步
```
> python manager.py sync_squid -d 默认配置文件地址 -c squid的配置文件地址
```

## squid同步配置文件说明
1. 安装完squid后修改配置文件, 之后复制一份squid.conf为squid.conf.default
2. 执行squid同步的命令, python会读取有效的代理ip和squid.conf.default, 拼合成新的配置文件squid.conf。

## 运行效果检测
1. 抓取了4537个免费代理ip, 但是在运行一段时间检测后, 长期比较稳定的基本只有60多个, 所以如果需要大量的代理ip, 那么必须得增加抓取量
2. 代理ip的速度以及稳定性还是比较不错的, 偶尔会发生无法访问的情况, 但是总体来说, 还是比较ok的, 可以在生产环境中使用。

## 目前支持的抓取网站
1. 西祠代理
2. 快代理
3. ip66

如果有什么新的好一些的免费代理网站, 可以提ISSUE或者qq:2387813033, 微信: 18500402623
