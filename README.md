# DNSapi
使用上游DNS进行解析A记录，返回api的结果


# 代码使用 Flask 框架创建了一个 /dns_query 的路由，接受 GET 请求并从查询参数中获取 domain 参数。添加了错误处理和返回 JSON 格式的响应，然后，使用 dns.resolver 模块执行 DNS 查询操作，并返回查询结果。如果查询成功，将返回域名和对应的 IP 地址列表。如果查询失败，将返回相应的错误信息。



# 接口地址

https://api.3dweb.ltd/dns_query?domain=github.com

# 返回格式

{"domain":"github.com","ip_addresses":["20.205.243.166"]}
