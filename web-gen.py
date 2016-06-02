#!/usr/bin/env python
# encoding:utf-8
__author__ = 'whois'
__date__ = '2016/6/2'
"""
    根据域名来生成字典
        1.后台地址   name_admin
        2.备份文件   name.rar
        3.后台账号   name1997
    拼音模式，beijingnihao.com  --> bei-jing-ni-hao
    普通模式，example.com  --> example
"""

def banner():
    print """
        $--------------------------------------------------$
               
                            Generate Web Path                          
                                                v0.3                       
        $--------------------------------------------------$
        ====================================================
            ===> 1. Pinyin mode
            ===> 2. Normal mode
    """

class Mydic():
    login_list = [
        'admin','admin1','admin123','admin111','admin888','ad','adm','guanli',
        'houtai','admin.php','admin.asp','admin.jsp','login','login1','admin_login',
        'login.asp','login.php','login.jsp','logon','manager','manage','user'
                ]                                         # 常用后台名列表

    bak_list = ['.zip','.rar','.bak','.tar.gz','.7z']  # 后缀名列表

    date_list = [ str(d) for d in range(1990,2017) ]  # 成年份列表

    num_list = [ str(n) for n in range(0,15) ]          #  数字列表

    spe_list = ['','_','-']                               # 分隔符


def gen():

    dic_list = []
    global dict_file

    number = raw_input("[#] Choose your number >>> ")
    number = int(number)
    if number == 1:
        print "[*] Domain format is xx-yy-zz !"
        domain = raw_input('[#] Input Domain >>> ')

        domain1 = domain.replace('-','')  #全组合
        domain2 = ''.join([ x[0] for x in domain.split('-') ])  #首字母组合
        domain3 = domain2[:2]   #首字母取前两位

        for sp in Mydic.spe_list:
            for lo in Mydic.login_list:
                dic_list.append(domain1)
                dic_list.append(domain2)
                dic_list.append(domain1+sp+lo)
                dic_list.append(domain2+sp+lo)

        [ dic_list.append(domain1+date) for date in Mydic.date_list ]
        [ dic_list.append(domain2+date) for date in Mydic.date_list ]
        [ dic_list.append(domain1+num) for num in Mydic.num_list ]
        [ dic_list.append(domain2+num) for num in Mydic.num_list ]
        [ dic_list.append(domain1+bak) for bak in Mydic.bak_list ]
        [ dic_list.append(domain2+bak) for bak in Mydic.bak_list ]
        [ dic_list.append(domain1+num+bak) for num in Mydic.num_list for bak in Mydic.bak_list ]
        [ dic_list.append(domain2+num+bak) for num in Mydic.num_list for bak in Mydic.bak_list ]
        [ dic_list.append(domain1+date+bak) for date in Mydic.date_list for bak in Mydic.bak_list ]
        [ dic_list.append(domain2+date+bak) for date in Mydic.date_list for bak in Mydic.bak_list ]

    elif number == 2:
        print "[*] Domain format is xyz !"
        domain = raw_input('[#] Input Domain >>> ')

        [ dic_list.append(domain+sp+lo) for sp in Mydic.spe_list for lo in Mydic.login_list]
        [ dic_list.append(domain+date) for date in Mydic.date_list ]
        [ dic_list.append(domain+num) for num in Mydic.num_list ]
        [ dic_list.append(domain+bak) for bak in Mydic.bak_list ]
        [ dic_list.append(domain+num+bak) for num in Mydic.num_list for bak in Mydic.bak_list ]
        [ dic_list.append(domain+date+bak) for date in Mydic.date_list for bak in Mydic.bak_list ]

    else:
        print "[-] Please input number!!!"
        exit(1)

    dict_file = domain+'.txt'       #  用于路径字典
    dict_file2 = domain+'2.txt'     #  用于爆破用户名或密码
    

    with open(dict_file,'a') as f:
        [ f.writelines(dic+'\n') for dic in dic_list ]

    with open(dict_file2,'a') as f:
        [ f.writelines(dic+'\n') for dic in dic_list if '.' not in dic ]

    print "[+] Generate is ok\t Happy hacking :)"

    
""" 调用dirsearch 进行扫描"""
def scan():
    
    import os

    choose = raw_input("[*] Scan target? (y/n)")

    if choose == 'y':
        good_path = "E:\Tools\PassList\Webpath\good.txt"
        common_path = "E:\Tools\PassList\Webpath\common.txt"
        print "[*] Load other web_path {0}\n\t\t\t{1}".format(good_path, common_path)

        target = raw_input("[*] Input target (www.xx.com)>>> ")
        try:
            command = "python3 E:\Tools\Information-Gather\Dir-Scan\dirsearch\dirsearch.py -u http://{0} -w {1} -e php --random-agents ".format(target, dict_file)
            command2 = "python3 E:\Tools\Information-Gather\Dir-Scan\dirsearch\dirsearch.py -u http://{0} -w {1} -e php --random-agents".format(target, good_path)
            command3 = "python3 E:\Tools\Information-Gather\Dir-Scan\dirsearch\dirsearch.py -u http://{0} -w {1} -e php --random-agents".format(target, common_path)

            os.system(command)
            os.system(command2)
            os.system(command3)

        except Exception as e:
            print e 
            print "[-] Please install dirsearch!"
            exit(1)
    else:
        exit(1)
        
if __name__ == '__main__':
    banner()
    gen()
    scan()
