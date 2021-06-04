#!/usr/bin/bash

target=$1
output=`basename $target`
bootstrap="/Users/tianxia/DeathNote/Coder/Python/PySec/Portscan/nmap-bootstrap.xsl"

if command -v xsltproc;then
    xsltproc -o "${output}.html" $bootstrap $target
    echo "[+] Success"

else
    echo "[x] Not found xsltproc"

fi
