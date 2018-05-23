#!/usr/bin/env python
# encoding:utf8
import os
try:
    from termcolor import colored
except:
    print "[-] pip install termcolor"
    exit(1)

__author__ = 'whois'
__date__   = '2016/6/2'
__update__ = '2018/01/08'

"""
    根据域名来生成字典
        1.后台地址   name_admin
        2.备份文件   name.rar
        3.后台账号   name1997
    拼音模式，beijingnihao.com  --> bei-jing-ni-hao
    普通模式，example.com  --> example

"""


def banner():
    print colored('\t$'+'-'*50+'$\n', 'red')
    print colored('\t\t\t\tGenerate Web Path', 'green')
    print colored('\t\t\t\t\t\tv0.5', 'green')
    print colored('\t$'+'-'*50+'$', 'red')
    print colored('\t'+'='*52, 'red')
    print '\n'
    print colored('\t==> ','magenta') + colored('1. Pinyin Mode', 'green')
    print colored('\t==> ','magenta') + colored('2. Normal Mode', 'green')
    print colored('\t==> ','magenta') + colored('3. Help', 'green')
    print colored('\t==> ','magenta') + colored('4. Exit\n', 'red')

class Mydic():

    # 常用后台列表及弱口令
    login_list = [
        '','admin','admin1','admin123','admin111','admin888','ad','guanli','houtai',
        'login','login1','admin_login','webadmin','logon','manager','manage','user',
        '123','1234','12345','123456','1234567','12345678','abc','888888','111',
    ]

    asp_list = [
        'admin.asp', 'login.asp', 'manage.asp'
    ]

    php_list = [
        'admin.php', 'login.php', 'manage.php'
    ]

    aspx_list = [
        'admin.aspx', 'login.aspx', 'manage.aspx'
    ]

    jsp_list = [
        'admin.jsp', 'login.jsp', 'manage.jsp'
    ]


    # 备份文件后缀名
    bak_list = ['', '.zip', '.rar', '.bak', '.tar.gz', '.7z', '.old']

    # 年份列表
    date_list = [ str(d) for d in xrange(1980, 2018) ]

    # 数字列表
    num_list = [ str(n) for n in xrange(0, 15) ]

    # 分隔符  zj_admin
    spe_list = [ '', '_', '-' ]


def pass_return_list():

        pass_list = []

        pass_file = "E:\\Tools\\PassList\\Passwords\\top300pass.txt"

        if not os.path.exists(pass_file):
            print "[x] File does not exist"
            exit(1)
        with open(pass_file, 'r') as f:
            for line in f.readlines():
                pass_list.append(line.rstrip())

        return pass_list



def ext_return_list():
    ext = raw_input(colored("[x] Choose website extend [asp, aspx, php, jsp]\n>>> ", 'yellow'))

    if ext == 'asp':
        return Mydic.asp_list
    elif ext == 'aspx':
        return Mydic.aspx_list
    elif ext == 'php':
        return Mydic.php_list
    elif ext == 'jsp':
        return Mydic.jsp_list
    else:
        print colored("[x] Please choose [asp, aspx, php, jsp]", 'red')
        exit(1)


def genpass():

    dic_list = []
    dic_list2 = []

    global dict_file  # use scan

    ext_list = ext_return_list()
    pass_list = pass_return_list()

    path_list = Mydic.login_list + ext_list

    number = int(raw_input(colored("[=] Choose your number >>> ", 'yellow')))

    if number == 1:
        print colored("[!] Domain format is xx-yy-zz !", 'green')
        domain = raw_input(colored('[*] Input Domain >>> ', 'yellow'))

        # 全组合 shang-hai-xin-xi => shanghaixinxi
        domain1 = domain.replace('-', '')

        #首字母组合
        domain2 = ''.join([ x[0] for x in domain.split('-') ])

        #首字母取前两位 => 具体情况具体调整
        domain3 = domain2[:2]

        # 通过分隔符进行遍历
        for sp in Mydic.spe_list:
            for path in path_list:
                if path != '':
                    dic_list.append(domain1+sp+path)
                    dic_list.append(domain2+sp+path)

        dic_list.append(domain.split('-')[0])
        dic_list.append(domain.split('-')[1])

        [ dic_list.append(domain1+bak) for bak in Mydic.bak_list ]
        [ dic_list.append(domain2+bak) for bak in Mydic.bak_list ]
        [ dic_list.append(domain1+num+bak) for num in Mydic.num_list for bak in Mydic.bak_list ]
        [ dic_list.append(domain2+num+bak) for num in Mydic.num_list for bak in Mydic.bak_list ]
        [ dic_list.append(domain1+date+bak) for date in Mydic.date_list for bak in Mydic.bak_list ]
        [ dic_list.append(domain2+date+bak) for date in Mydic.date_list for bak in Mydic.bak_list ]

        [ dic_list2.append(domain1+psd) for psd in pass_list ]
        [ dic_list2.append(domain2+psd) for psd in pass_list]

    elif number == 2:
        print colored("[*] Domain format is xyz !",'green')
        domain = raw_input(colored('[*] Input Domain >>> ','yellow'))

        [ dic_list.append(domain+sp+path) for sp in Mydic.spe_list for path in path_list if path != '']
        [ dic_list.append(domain+bak) for bak in Mydic.bak_list ]
        [ dic_list.append(domain+num+bak) for num in Mydic.num_list for bak in Mydic.bak_list ]
        [ dic_list.append(domain+date+bak) for date in Mydic.date_list for bak in Mydic.bak_list ]

        [ dic_list2.append(domain+psd) for psd in pass_list ]

    else:
        print colored("[x] Please input number !!!",'red')
        exit(1)

    if not os.path.isdir('output'):
        os.mkdir('output')
    dict_file = 'output/'+domain+'.txt'       #  用于路径字典
    dict_file2 = 'output/'+domain+'2.txt'     #  用于爆破后台用户名或密码


    dict_ok = []
    [ dict_ok.append(d) for d in dic_list if d not in dict_ok ]

    with open(dict_file,'a') as f:
        [ f.writelines(dic+'\n') for dic in dict_ok ]

    with open(dict_file2,'a') as f:
        [ f.writelines(dic+'\n') for dic in dict_ok if '.' not in dic ]
        [ f.writelines(dic+'\n') for dic in dic_list2 ]

    print "[+] Generate is ok :)"


""" 调用dirsearch 进行扫描"""
def scan():

    import os

    choose = raw_input("[*] Scan target? (y/n)")

    if choose == 'y':

        target = raw_input(colored("[*] Input target (www.xx.com)>>> ",'yellow'))
        try:
            command = "python3 E:\\Tools\\Information-Gather\\Dir-Scan\\dirsearch\\dirsearch.py -u http://{0} -w {1} -e php --random-agents ".format(target, dict_file)

            os.system(command)

        except Exception as e:
            print colored("[x] Please install dirsearch!",'red')
            exit(1)

    else:
        print colored('By','green')
        exit(1)



if __name__ == '__main__':
    banner()
    genpass()
    scan()
