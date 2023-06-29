# DNSapi
使用上游DNS进行解析A记录，返回api的结果


# 代码使用 Flask 框架创建了一个 /dns_query 的路由，接受 GET 请求并从查询参数中获取 domain 参数。添加了错误处理和返回 JSON 格式的响应，然后，使用 dns.resolver 模块执行 DNS 查询操作，并返回查询结果。如果查询成功，将返回域名和对应的 IP 地址列表。如果查询失败，将返回相应的错误信息。



# 接口地址

https://api.3dweb.ltd/dns_query?domain=github.com

# 返回格式

{"domain":"github.com","ip_addresses":["20.205.243.166"]}


# 宝塔面板python项目架设
在  /www/wwwroot/ 目录下 新建个文件夹，项目名称即可
如:/www/wwwroot/dnsapi

长传 app.py  
     requirements.txt  
     到 /www/wwwroot/dnsapi

进入宝塔面板-网站-Python项目-添加Python项目

项目路径:/www/wwwroot/dnsapi
项目名称:dnsapi
运行文件:/www/wwwroot/dnsapi/app.py
项目端口:5000
Python版本:随意，建议3.9.7
框架：flask
运行方式:gunicorn
网络协议:wsgi
安装依赖包:/www/wwwroot/dnsapi/requirements.txt

进程，线程默认即可

启动用户:www 即可

配置域名:127.0.0.1  端口不用写
外网映射：开

至此python项目架设完毕


# 新建站点

添加站点,域名就是你要的api域名
ssl，https访问正常添加证书操作步骤即可

# 设置反向代理

目标URL:http://127.0.0.1:5000
发送域名:$host

保存

# https://你的域名/dns_query?domain=要查询真实服务器IP带的网址
