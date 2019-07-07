# 基于Socket的服务器和Web框架
## 简介
* 使用原生Socket创建了一个应用服务器，监听端口接收请求，使用多线程处理请求。
* 分解请求内容，根据路由，调用相应函数进行处理并返回。
## 运行环境
* python3.6
* mysql数据库
```
pip install pymysql jinja2
```
## 如何运行
```
git clone https://github.com/tjucch/webFrame.git
cd webFrame
python reset.py
python server.py
```
## 功能演示
### 登录
![](https://github.com/tjucch/webFrame/tree/master/images/login.gif)
### 添加weibo或评论
![](https://github.com/tjucch/webFrame/blob/master/images/add.gif)
### 删除weibo或评论
![](https://github.com/tjucch/webFrame/tree/master/images/delete.gif)
### 修改weibo
![](https://github.com/tjucch/webFrame/tree/master/images/update.gif)
