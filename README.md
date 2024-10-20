# pyUDPtool
send udp packet and receive in host, for dev. other project, utility 
It consists of two project, </br>
1. pyUDPhost : host a udp server and listen to a designated port
2. pyUDPsend : send a stream from csv file row by row, according to designated castType for each colum. 

# pyUDPhost
open a server listening UDP socket </br>
usage : </br>
```
python pyUDPhost.py --ip 127.0.0.1 --port 5500
```

# pyUDPsend
  ## pyUDPSend
It sends arbirary data stream (csv form) according to designated cast type for each column.</br>
To send a data stream, you need a csvfile formated data table

``` csv
34.7915,128.6954,62.44,63.28,60.5,225,160,61
34.7328,128.63,69.41,61.54,65.63,233,209,151
34.9676,128.3873,64.54,65.12,68.69,4,177,221
34.1309,128.1063,62.14,65.54,61.33,172,67,236
```

each column will be packed according to cast type in castType.json 
``` castType.json
{
    "column1": "double",
    "column2": "double",
    "column3": "float",
    "column4": "float",
    "column5": "float",
    "column7": "byte",
    "column8": "byte",
    "column9": "byte"
}
```

To run this code, process next line in terminal 
```
python pyUDPSend.py castType.json test.csv 127.0.0.1 5500 
```


  ## pyUDPm2 
  
It sends arbirary data stream (csv form) according to designated cast type for each column.</br>
in mode2, it can have predefined header bytes in front and checksum byte in tail. </br>
for the setting, you need to edit a settings.json file. see ex_setting.json </br>
            
syntax : follow json format </br>
component : castType, csv_file, ip, port, header, checksumFlag</br>
ex <ex_setting.json></br>
```
{
    "castType": "castType.json",
    "csv_file": "csv_file.csv",
    "ip": "192.168.0.1",
    "port": 5500,
    "header" : "0x000003F264"
    "checksumNote" : 1 #or 0 
}
```
how to run the code, use following syntax </br>
```
python pyUDPm2.py ex_setting.json 
```
note ! </br>
header should be described in hex value. and fill zeros for digits preserves

## Any support is welcome

1.[buy me a coffe](https://buymeacoffee.com/ghmoon90) </br>
2.Kaspa coin wallet </br>
   (Don't send other currency to this, it will make unintentional loss)</br>
<p align="center">
   <a href="/ref/kaspa_public.jpg" >kaspa:qqtjrkyrten8uzvf9ffrn68nj3jw83q8yaaxdcl695nctr803mf9z9r8v0k7x</a>  </br>
</p>
3. bitcoin wallet </br> 
<p align="center">
  <a href="/ref/bitcoin_public.jpg" >bc1q0rxl49ygktx0n66umevy6vzqk02eshyxq5ppzc</a>  </br>
</p>

