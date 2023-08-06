net module 0.3.0 documentation

Author: JoStudio, Date: 2022/8/1

net Module
======================

This net package provides tools to perform net ping, scan port, send email, http, web spider,
access web API.




Submodules
======================

* net.http
* net.mail
* net.scan
* net.spider
* net.test
* net.util
* net.webapi



Functions in the module
================================


net.spider.get_requests()
      import requests package

net.spider.html2text(html, convert=True)
      Convert html to text.
  
  :Chinese: 将HTML转化为纯文本
  
  :param html:   HTML string
  :param convert: (optinal) whether convert to pure text
  :return: str

net.util.rprint(\*args, \*\*kwargs)
      replacement of builtins.print() function, compatible in python 2 and python 3.
  
  :Chinese: 打印（兼容Python2, Python3)
  
  :param args:  arguments to be printed
  
  :param kwargs:  Optional keyword arguments: 

      sep:   string inserted between values, default a space.

      end:   string appended after the last value, default a newline.

      flush: whether to forcibly flush the stream.


  :return: None

net.webapi.headers_get(headers, name, sub_name=None)
      取得headers中的名为name的字段的值, sub_name是子字段




Classes in the module
================================


class net.http.Http
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

+ **properties**

    - content :
      get the bytes of response

    - content_type :
      

    - status_code :
      

    - text :
      get the text of response



+ **methods**


__init__(self)
      Initialize self.  See help(type(self)) for accurate signature.

header(self, name, sub_name=None)
      

json(self, \*\*kwargs)
      get the json data of response

request(self, url, data=None, headers=None, method='GET')
      Sends a request.
  
  :param url: URL for the new `Request` object.
  :param data: (optional) Dictionary, list of tuples or bytes to send
      in the query string for the `Request`.
  :param headers: Optional headers of the request.
  :param method: Optional method of the request, 'GET', 'POST', 'PUT', 'DELETE', 'HEAD'.
  :return: return self

save_to_file(self, filename)
      save response to file

delete(url, params=None, headers=None)
      send a DELETE request

get(url, params=None, headers=None)
      send a GET request

head(url, params=None, headers=None)
      send a HEAD request

post(url, data=None, headers=None)
      send a POST request

put(url, data=None, headers=None)
      send a get request




+ **attributes**

  - req

  - response




class net.http.UserAgent
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>






+ **attributes**

  - chrome = 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 ...ML, like ...

  - default = 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 ...ML, like...




class net.mail.Mail
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



+ **methods**


__init__(self, user, passwd, sender=None, host=None)
      create instance of Mail
  
  :param user:   username to login SMTP server
  :param passwd: password to login SMTP server
  :param host:   (optional) SMTP server. if empty, detect host by the user parameter.
  :param sender: (optional) sender of the mail. if empty, use the user parameter

send(self, receivers: list, subject: str, body: str, attach_filenames: list = None)
      send a mail
  
  :param receivers:  list of the e-mail addresses of receivers
  :param subject:    title of the mail
  :param body:    content of the mail
  :param attach_filenames:      (optional) attachment file name list
  
  :return: return True if success, return SMTPException object if failed.




+ **attributes**

  - user

  - passwd

  - host

  - sender




class net.scan.Net
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



+ **methods**


get_connection_ip(host, port)
      Get the local IP address that connects to the specified host.
  
  :Chinese: 取得可连接到指定服务器的本地IP地址.
  
  :param host:  host domain or ip
  :param port:  the port
  :return: return the local IP address that connects to the specified host.
  :Chinese: 返回连接指定服务器的本地IP地址.

get_mac(ip)
      Get the MAC address of specified IP address.
  
  :Chinese: 取得 IP地址 对应的 MAC地址。
  
  :param ip:  IP address string.
  :return: return MAC address string, like: 78:44:fd:6d:1c:91". return empty string if fail.
  :Chinese: 返回MAC地址字符串。如："78:44:fd:6d:1c:91"

has_internet()
      Whether internet is available

ip_get(ip, index)
      Get ip address number at specified index.
  
  :Chinese: 获取 IP地址中 指定位置的数值
  
  :param ip:   IPv4 address string
  :param index:  the index of the number, first is 0, valid indexes are 0, 1, 2, 3
  :Chinese: 第几位， 0表示第一位，取值范围是 0, 1, 2, 3
  :return: return ip address number at specified index. return None if error occurs.
  :Chinese: 返回IP地址中第 index 位的数值(整数)。如果出错，返回None

ip_range(ip, start=None, end=None, index=3)
      Define an IP address range, return  a list of IP address string.
  
  :Chinese: 定义一个IP地址范围, 返回一个IP地址列表.
  
  :param ip:    IPv4 address string
  :param start:  start number
  :param end:    end number
  :param index:  (optional)the index of the number, first is 0, valid indexes are 0, 1, 2, 3
  :Chinese: 第几位， 0表示第一位，取值范围是 0, 1, 2, 3
  :return: return  a list of IP address string.
  :Chinese: 返回一个IP地址列表

ip_scan(ip_list, mac=False, exists=True, threads=0)
      Scan IP address list, return a list of ip address or MAC address which is pingable.
  
  :Chinese: 扫描 IP地址列表，取得 可PING通的 IP地址列表 (或MAC地址列表).
  
  :param ip_list:   the IP address list
  :param mac: (optional) whether get MAC address, default is False.

          if mac == True, the item of result list is MAC address list.

          if mac == 2, the item of result list is a 2-elements tuple of (ip, mac)

          if mac == 3, the item of result list is a 3-elements tuple of (ip, mac, factory)

  
  :Chinese:
          （可选）是否取得MAC地址，默认值是False.

          如果mac=True,则结果列表每一项是MAC地址。

          如果mac=2, 则结果列表每一项是一个tuple, 形如：(IP地址, MAC地址)。

          如果mac=3, 则结果列表每一项是一个tuple, 形如：(IP地址, MAC地址, 厂商)。

  
  :param exists:  (optional) Whether get pingable IPs. if exists is False, return list is not pingable IPs.
  :Chinese:（可选）是否取得Ping通的地址，默认值是True.

          如果exists=False,则结果列表是PING不通的IP地址。

  :param threads:   (optional) how many threads that uses. default is 0 for auto detect.
  :Chinese:（可选）并发线程数量，默认值是0(自动选择线程数量）
  :return:  return a list. the item of list depends on the mac parameter.

ip_set(ip, index, number)
      Change ip address number at specified index to specified number.
  
  :Chinese: 更改 IP地址 指定位置的数值
  
  :param ip: IPv4 address string
  :param index:  the index of the number, first is 0, valid indexes are 0, 1, 2, 3
  :Chinese: 第几位， 0表示第一位，取值范围是 0, 1, 2, 3
  :param number:   the number , the value range is [0-255]
  :Chinese: 数值(整数)，取值范围是 0 - 255
  :return: return IP address string. return None if error occurs.
  :Chinese: 返回更改后的IP地址。如果出错，返回None

is_ip(text)
      Whether the string is an IPV4 string.
  
  :Chinese: 判断指定文字是否是一个 IP 地址
  
  :param text: the string
  :return: True or False

is_lan_ip(ip)
      Whether specified IP address is LAN IP address

is_port_open(ip, port, udp=False)
      Whether specified port is opened on specified IP address.
  
  :Chinese: 判断服务器的指定端口是否开放.
  
  :param ip:    the IP address or host name
  :param port:  port number, int
  :param udp:   (optional) whether use UDP. default is False
  :return: return True if the port is opened. return False if not opened.

local_ip()
      Get local IP address.
  
  :Chinese: 取得局域网IP地址.
  
  :return: return IP address string

mac_factory(mac)
      Get manufacture factory name by specified MAC address.
  
  :Chinese: 根据mac码，获取制造工厂名称.
  
  :param mac:  the MAC address string
  :return: return a string of manufacture factory name. return empty string if fail.
  :Chinese: 返回字符串（制造工厂名称)

ping(ip, times=1, timeout=1000)
      Pint specified IP address
  
  :param ip:  IP address string or host name
  :param times:  (optional) times of ping
  :param timeout:  (optional) waiting timeout in milliseconds，defalut is 1000.
  :return: return time usage of ping in millisecond.  return -1 when ping fails.
  :Chinese: 返回Ping通时间（单位为毫秒)。 返回-1表示Ping不通。

port_range(port_start, port_end=None)
      Define a port range, return  a list of port int.
  
  :Chinese: 定义一个端口范围, 返回一个端口列表.
  
  :param port_start:  starting port number, int, value range is [1-65535]
  :Chinese: 起始端口(整数), 取值范围是 1-65535
  :param port_end:  ending port number, int, value range is [1-65535]
  :Chinese:结束端口(整数), 取值范围是 1-65535
  :return: return  a list of port int.

port_scan(ip, port_list=None, exists=True, threads=0, name=False)
      Scan ports of specified IP address.
  
  :Chinese: 对于指定IP地址，扫描端口列表， 取得 可连接的 端口列表
  
  :param ip:         the IP address.
  :param port_list:  (optional) a list of port. If port_list is None, scan common used ports.
  :Chinese: (可选)端口列表, 如果port_list为None，则扫描常见端口
  :param exists:   (optional) Whether return opened ports. If exists is False, return not-opened ports.
  :Chinese:（可选）是否取得可连接的端口，默认值是True.

          如果exists=False,则结果列表是不可连接的端口。

  :param threads:  (optional) how many threads that uses. default is 0 for auto detect.
  :Chinese:（可选）并发线程数量，默认值是0(自动选择线程数量）
  :param name:    (optional) whether return the protocol name.
                  If name is True, each item of result list is a tuple of (port, protocol).
  :Chinese:（可选）是否返回协议名，默认值是False.
          如果name=True,则结果列表每一项是一个tuple, 形如：(端口号, 协议名称)。

  :return:  return a list.

run_command(cmd_line)
      run a command in current OS
  
  :param cmd_line:  command line
  :return: return a tuple (ret, text), the first element is return value，the second is result text.







class net.scan.Port
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



+ **methods**


common_ports()
      return a list of common used ports

name_of(port_number)
      get the name of protocol of specified port number




+ **attributes**

  - BGP = 179

  - BackOrifice = 18006

  - BackupExec = 10000

  - BitTorrent = 6881

  - BitTorrent2 = 6999

  - DNS = 53

  - Echo = 7

  - FTP = 21

  - FTPS = 989

  - FTPS2 = 990

  - FTP_Data = 20

  - GoogleDesktop = 4664

  - HPJetDirect = 9100

  - HP_Openview = 381

  - HP_Openview2 = 383

  - HTTP = 80

  - HTTP2 = 8080

  - HTTPS = 443

  - IMAP = 143

  - IMAPS = 993

  - IMAPS2 = 585

  - IRC = 6665

  - IRC2 = 6669

  - KasperskyAV = 8086

  - KasperskyAV2 = 8087

  - Kerberos = 88

  - Kerberos2 = 464

  - LDAP = 389

  - LDAPS = 636

  - MPLS = 646

  - MSDOM = 593

  - MSExchange = 102

  - MSExchange2 = 691

  - MSRPC = 135

  - MySQL = 3306

  - NFS = 2049

  - NNTP = 119

  - NNTPS = 563

  - NetBIOS = 137

  - NetBIOS_SMB = 139

  - NetBus = 12345

  - OpenVPN = 1194

  - Oracle = 2483

  - Oracle2 = 2484

  - POP3 = 110

  - POP3S = 995

  - PPTP = 1723

  - PostgreSQL = 5432

  - Quicktime = 6970

  - RADIUS = 1812

  - RADIUS2 = 1813

  - RDC = 3389

  - RPC = 1025

  - RTSP = 554

  - SCP = 9999

  - SIP = 5060

  - SMB = 445

  - SMTP = 25

  - SMTPS = 465

  - SMTPS2 = 587

  - SNMP = 161

  - SSH = 22

  - SqlServer = 1433

  - Steam = 1725

  - Sub7 = 27374

  - SymantecAV = 2967

  - SynologyNAS = 5000

  - TFTP = 69

  - Telnet = 23

  - UPnP = 5000

  - VMwareServer = 8222

  - VNC = 5900

  - VQP = 1589

  - Vmware = 902

  - WASTE = 1337

  - WHOIS = 43

  - WINS = 42

  - Warcraft = 3724

  - XBOX = 3074

  - cPanel = 2082

  - eMule = 4672

  - radsec = 2083




class net.spider.BaiKe
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

+ **properties**

    - catalog :
      目录列表

    - explain :
      解释文字



+ **methods**


__contains__(self, item)
      

__getitem__(self, item)
      

__init__(self, word=None, finding=None)
      Initialize self.  See help(type(self)) for accurate signature.

count(self)
      返回同义词的数量

find_others(self, finding)
      寻找同义词,  如找到则返回对象本身, 如找不到返回None

load(self, word, finding=None)
      读取一个词的百科
  
  :param word:  一个词
  :param finding: （可选)限定语，用于寻找同义词
  :return: 返回对象本身

others(self, index)
      跳转到指定序号index的同义词。
  
  :param index:  序号index
  :return: 返回一个BaiKe对象，指向序号index的同义词

find(self, before, after=None, begin=None)
      find words
  
  :param before: before condition, could be a string or a list of string
  :param after: (optional) after condition, could be a string or a list of string
  :param begin: (optional) begin condition, could be a string or a list of string or an offset int
  :return:  return string

find_list(self, before, after=None, begin=None)
      find a list
  
  :param before: before condition, could be a string or a list of string
  :param after:  (optional) after condition, could be a string or a list of string
  :param begin:  (optional) begin condition, could be a string or a list of string or an offset int
  ::return:  return string

search(self, word)
      search a word




+ **attributes**

  - base_url

  - BAIDU = 'https://www.baidu.com/s?wd={0}'

  - BING = 'https://cn.bing.com/search?q={0}'




class net.spider.DeHTMLParser
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



+ **methods**


__init__(self)
      Initialize and reset this instance.
  
  If convert_charrefs is True (the default), all character references
  are automatically converted to the corresponding Unicode characters.

handle_data(self, data)
      

handle_startendtag(self, tag, attrs)
      

handle_starttag(self, tag, attrs)
      

text(self)
      

check_for_whole_start_tag(self, i)
      # Internal -- check to see if we have a complete starttag; return end
  # or -1 if incomplete.

clear_cdata_mode(self)
      

close(self)
      Handle any buffered data.

feed(self, data)
      Feed data to the parser.
  
  Call this as often as you want, with as little or as much text
  as you want (may include '\n').

get_starttag_text(self)
      Return full source of start tag: '<...>'.

goahead(self, end)
      # Internal -- handle data as far as reasonable.  May leave state
  # and data to be processed by a subsequent call.  If 'end' is
  # true, force handling all data as if followed by EOF marker.

handle_charref(self, name)
      # Overridable -- handle character reference

handle_comment(self, data)
      # Overridable -- handle comment

handle_decl(self, decl)
      # Overridable -- handle declaration

handle_endtag(self, tag)
      # Overridable -- handle end tag

handle_entityref(self, name)
      # Overridable -- handle entity reference

handle_pi(self, data)
      # Overridable -- handle processing instruction

parse_bogus_comment(self, i, report=1)
      # Internal -- parse bogus comment, return length or -1 if not terminated
  # see http://www.w3.org/TR/html5/tokenization.html#bogus-comment-state

parse_endtag(self, i)
      # Internal -- parse endtag, return end or -1 if incomplete

parse_html_declaration(self, i)
      # Internal -- parse html declarations, return length or -1 if not terminated
  # See w3.org/TR/html5/tokenization.html#markup-declaration-open-state
  # See also parse_declaration in _markupbase

parse_pi(self, i)
      # Internal -- parse processing instr, return end or -1 if not terminated

parse_starttag(self, i)
      # Internal -- handle starttag, return end or -1 if not terminated

reset(self)
      Reset this instance.  Loses all unprocessed data.

set_cdata_mode(self, elem)
      

unescape(self, s)
      # Internal -- helper to remove special character quoting

unknown_decl(self, data)
      

error(self, message)
      

getpos(self)
      Return current line number and offset.

parse_comment(self, i, report=1)
      # Internal -- parse comment, return length or -1 if not terminated

parse_declaration(self, i)
      # Internal -- parse declaration (for use by subclasses).

parse_marked_section(self, i, report=1)
      # Internal -- parse a marked section
  # Override this to handle MS-word extension syntax <![if word]>content<![endif]>

updatepos(self, i, j)
      # Internal -- update line number and offset.  This should be
  # called for each piece of data exactly once, in order -- in other
  # words the concatenation of all the input strings to this
  # function should be exactly the entire input.




+ **attributes**

  - CDATA_CONTENT_ELEMENTS = ('script', 'style')




class net.spider.ImageData
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



+ **methods**


__init__(self, data)
      Initialize self.  See help(type(self)) for accurate signature.

download(self, filename=None)
      下载图片, 保存到文件.
  
  :param filename: (可选)存盘文件名.
          文件名可以不带扩展名， 如: file1,
          本函数将根据图片类型自动添加扩展名， 并返回实际存盘的文件名， 如: file1.jpg。
  
  :return: 如果失败，则返回None。

          如果成功存盘，返回存盘文件名。

          如果参数filename缺省，则不存盘，返回图片数据(bytes)。

valid(self)
      图片是否有效

valid_format(self, fmt)
      fmt 是否是有效的图片格式

get_file_ext(url)
      取得 url 中的文件扩展名

get_file_name(url)
      取得 url 中的文件名




+ **attributes**

  - url

  - thumb_url

  - filename

  - file_ext

  - ref_url

  - title




class net.spider.Spider
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



+ **methods**


__init__(self, url=None)
      Initialize self.  See help(type(self)) for accurate signature.

find(self, before, after=None, begin=None)
      find words
  
  :param before: before condition, could be a string or a list of string
  :param after: (optional) after condition, could be a string or a list of string
  :param begin: (optional) begin condition, could be a string or a list of string or an offset int
  :return:  return string

find_list(self, before, after=None, begin=None)
      find a list
  
  :param before: before condition, could be a string or a list of string
  :param after:  (optional) after condition, could be a string or a list of string
  :param begin:  (optional) begin condition, could be a string or a list of string or an offset int
  ::return:  return string

search(self, word)
      search a word




+ **attributes**

  - BAIDU = 'https://www.baidu.com/s?wd={0}'

  - BING = 'https://cn.bing.com/search?q={0}'




class net.spider.WebImage
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



+ **methods**


__init__(self, word, file_ext=None, size=None, count=20, first=0)
      Initialize self.  See help(type(self)) for accurate signature.

count(self)
      return count of images

download_all(self, path=None)
      download all image, save file to specified path
  
  :param path:  save path
  :return: return count of downloaded files

load(self, word, file_ext=None, size=None, count=20, first=0)
      search keyword
  
  :param word:    keyword
  :param file_ext: (optional) file extension of image, such as 'jpg' 'png'  'gif'
  :param count:    (optional) count of image
  :param first:   (optional) skip first some images
  :return: self

find(self, before, after=None, begin=None)
      find words
  
  :param before: before condition, could be a string or a list of string
  :param after: (optional) after condition, could be a string or a list of string
  :param begin: (optional) begin condition, could be a string or a list of string or an offset int
  :return:  return string

find_list(self, before, after=None, begin=None)
      find a list
  
  :param before: before condition, could be a string or a list of string
  :param after:  (optional) after condition, could be a string or a list of string
  :param begin:  (optional) begin condition, could be a string or a list of string or an offset int
  ::return:  return string

search(self, word)
      search a word




+ **attributes**

  - word

  - images

  - MAX_IMAGES = 50

  - BAIDU = 'https://www.baidu.com/s?wd={0}'

  - BING = 'https://cn.bing.com/search?q={0}'




class net.spider.ZhiDao
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



+ **methods**


__init__(self, word)
      Initialize self.  See help(type(self)) for accurate signature.

answer(self, index=0)
      返回答案文字
  
  :param index (可选)第几条答案

count(self)
      返回答案的数量

search(self, word)
      提出一个问题

find(self, before, after=None, begin=None)
      find words
  
  :param before: before condition, could be a string or a list of string
  :param after: (optional) after condition, could be a string or a list of string
  :param begin: (optional) begin condition, could be a string or a list of string or an offset int
  :return:  return string

find_list(self, before, after=None, begin=None)
      find a list
  
  :param before: before condition, could be a string or a list of string
  :param after:  (optional) after condition, could be a string or a list of string
  :param begin:  (optional) begin condition, could be a string or a list of string or an offset int
  ::return:  return string




+ **attributes**

  - BAIDU = 'https://www.baidu.com/s?wd={0}'

  - BING = 'https://cn.bing.com/search?q={0}'




class net.test.A
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

+ **properties**

    - prop1 :
      



+ **methods**


__init__(self)
      Initialize self.  See help(type(self)) for accurate signature.

func1(self)
      

func2(abb)
      




+ **attributes**

  - ok

  - area

  - Constant = 'abb'




class net.test.Base
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



+ **methods**


__init__(self)
      Initialize self.  See help(type(self)) for accurate signature.




+ **attributes**

  - name




class net.util.StrUtil
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



+ **methods**


find_sep(text, sep, start_offset=0)
      find separator char
  
  :Chinese: 查找分割符
  
  :param text:  the string
  :param sep:   the separator char
  :param start_offset: 
  :return: return a tuple of (offset, length_of_sep)

find_word(text, finding, index=0, sep=None)
      Find a word ing a line.
  
  :Chinese: 在一行文字中查找符合条件的词.
  
  :param text:   the string
  :param index:  the index of occurrence , the first is 0, second is 1 ...
  :Chinese: 第几个. 0表示第一个， 1表示第二个
  :param finding: (optional) finding condition, could be a sub string or a list of string.

  :Chinese:(可选)查找条件，可以是一个子字符串，或一个字符串列表
  :param sep:   separate char, default is blank char.

  :Chinese:(可选)词分割符，默认为空格
  :return: return str if found, return None if not found.
  :Chinese: 如果找到，返回字符串。如果找不到，返回None

get_word(text, before, after, start_offset=0, return_offset=False)
      Get a word from text, the word is between before condition, and after condition.
  
  :Chinese: 从文本中提取一个词，该词在查找条件before后, 查找条件after前
  
  :param text:    the string
  :param before:  the before condition, could be a sub string or a list of string.

  :Chinese: 查找条件before
  :param after:   the end condition, could be a sub string or a list of string.

  :Chinese: 查找条件end
  :param start_offset:    offset to start finding.
  :Chinese:（可选）开始查找的位置
  :param return_offset:  whether return offset, boolean.
  :Chinese:（可选）是否返回查找后的位置
  :return: return str if found, return None if not found.
  :Chinese: 返回一个词。 如果找不到，返回None

get_word_list(text, begin, betweens, start_offset=0, end=None)
      get a list of keywords from the text.
  
  :Chinese: 从文本中, 查找出一串单词列表。
  
  :param text:   the text to process
  :param begin:  begin condition, could be a sub string or a list of string.

  :param betweens:  words definition list
          each item is a keyword definition tuple, which contains a before and after condition.
          Example:
          <code>
              [
                (['<li', '<a', '>'], '</a'),
                (['author', '>'], '</a')
              ]
          </code>
          define two keywords.
  
  :Chinese: betweens 是一个单词定义列表。
                   每一个元素单词定义, 一个 2个元素tuple, 第0个元素是before条件，
                   第1个元素是after条件.
  
  :param start_offset: (optional) offset to start finding
  :param end:  (optional) end condition, could be a sub string or a list of string.

  :return:  return a list of words

get_words(text, line_findings, word_findings, index=0, multiple=False, number_unit=False)
      

grep(text, finding)
      Split the text into lines, return the lines matched the finding condition.
  
  :Chinese: 将文本切分为多行, 返回符合查找条件的行
  
  :param text:  the string
  :param finding: the finding condition, could be a sub string, or a list of string.
  :Chinese: 查找条件，可以是一个子字符串，或一个字符串列表
  :return: return a list of str， each element is a line matched the finding condition.
  :Chinese: 返回一个字符串列表， 每个元素是一个符合查找条件的行

is_blank_char(c)
      Whether the c is blank char

is_ip_number(text)
      Whethe the string is a valid IP number, which range is [0-255]
  
  :Chinese: 判断文字是否是有效的IP数字范围 [0-255]
  
  :param text: the string
  :return:  True of False

is_json_string(s)
      Whether the string is a JSON string.
  
  :Chinese: 判断 字符串s 是否是一个json字符串
  
  :param s: the string
  :return: True or False

is_xml_string(s)
      Whether the string is a XML string.
  
  :Chinese: 判断 字符串s 是否是一个 xml 字符串
  
  :param s: the string
  :return: True or False

match(text, findings, start_offset=0)
      Whether the string match the finding condition.
  
  :Chinese: 判断字符串是否符合条件, 返回True, False
  
  :param text:  the string
  :param findings: Find condition, could be a sub string, or a list of str for continuous finding,
          or a tuple of str for finding one of them.

  :Chinese: 查找条件，可以是一个子字符串，或一个字符串list(表示连续查找、and关系),
          或一个字符串tuple(表示查找其中一个、or关系)
  :param start_offset:    (optional) the offset to start finding.

  :Chinese: (可选)起始查找位置, 默认值为0.
  :return: return True if matched, else return False.

match_offset_length(text: str, findings: [<class 'str'>, <class 'list'>, <class 'tuple'>], start_offset=0)
      Match the finding condition in the string, return matched offset, length.
  
  :Chinese: 查找字符串, 返回匹配的offset和长度length。
  
  :param text:     The string
  :param findings:  Find condition, could be a sub string, or a list of str for continuous finding,
          or a tuple of str for finding one of them.

  :Chinese: 查找条件，可以是一个子字符串，或一个字符串list(表示连续查找、and关系),
          或一个字符串tuple(表示查找其中一个、or关系)
  :param start_offset:    (optional) the offset to start finding.

  :Chinese: (可选)起始查找位置, 默认值为0.
  :return: return a tuple of (offset, length).  If not found, offset is -1.
  :Chinese: 返回一个tuple(offset, length)。如果找不到，tuple 中的 offset = -1

split(text, sep=None)
      split the text into word list by specified separator
  
  :param text:  the text
  :param sep:  separator string
  :return: return a list of str

split2(text, sep, first=True)
      Split the text into two-word list.
  
  :Chinese: 将一个字符串切分为两个词
  
  :param text:  the text
  :param sep:   separator string
  :param first: (optional) If True, when separator is missing, set the first word with text and
          leave the second word empty. If False, vise versa.
  :return: return a 2-word list

split_number_unit(s)
      Split the string, such as '2ms', into number and unit.
  
  :Chinese: 将一个形如: 2ms 的字符串切分为 数字,单位
  
  :param s: the string
  :return: return a tuple of (number, unit)

sys_encoding()
      return system encoding.
  
  :Chinese: 取得系统编码
  
  :return: str

trim_quote(s)
      Trim quote marks at the beginning and ending of the string.
  
  :Chinese: 删除字符串两端的引号 (包括单引号、双引号)
  
  :param s: the string
  :return: str







class net.webapi.WebAPI
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



+ **methods**


__init__(self)
      Initialize self.  See help(type(self)) for accurate signature.

add_func(self, method, url, func_name, \*\*kwargs)
      Add a API function
  
  :param method:  HTTP method, such as 'GET', 'POST', 'DELETE', 'PUT'
  :param url:     url
  :param func_name:  function name
  :param kwargs:     key-value arguments of the function
  :return:  None

call(self, func_name, \*\*kwargs)
      Call a function
  
  :param func_name:  function name
  :param kwargs:  key-value arguments of the function
  :return:  return the result of the function. raise exception if error occurs

find_func(self, func_name)
      Find a function
  :param func_name: function name
  :return: return WebAPI.API object if success. raise Exception if not found

help(self, func_name=None)
      get help of API function




+ **attributes**

  - API = <class 'net.webapi.WebAPI.API'>










net module 0.3.0 documentation
Author: JoStudio, Date: 2022/8/1