# LiveBOS
一款用友 LiveBOS漏洞检测工具
![图片](https://github.com/user-attachments/assets/9adc72f6-f4c3-4e81-8620-75b7cb1c60e6)

```
简介
LiveBOS，由顶点软件股份有限公司开发的对象型业务架构中间件及其集成开发工具，是一种创新的软件开发模式，以业务模型建立为核心，直接完成软件
开发。它适用于各类基于WEB的专业应用软件和行业大型应用的开发。LiveBOS由三个相对独立的产品组成：运行支持支撑平台 LiveBOS Server，开发集
成环境LiveBOSStudio以及运维管理工具LiveBOS Manager。然而，其接口UploadFile.do;.js.jsp存在任意文件上传漏洞，攻击者可以利用该漏洞获取
系统服务器权限，从而控制该系统。

使用方法
[+] LiveBOS.py --url http://www.xxx.com 进行单个漏洞检测
[+] LiveBOS.py --file targeturl.txt 进行批量漏洞检测
[+] LiveBOS.py --help 查看详细帮助信息

fofa
body="Power by LiveBOS"

```
