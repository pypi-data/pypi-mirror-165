#!/usr/bin/python
# coding:utf-8
#
# network ping and scan
#

import socket
import platform
import subprocess
import threading
import signal
import time

from .util import rprint, StrUtil
from .http import Http


# A task for scan
class _ScanTask:
    """
    A task for scan
    :Chinese: 用于批量扫描的任务类
    """
    BLOCK = ''

    cancel = False

    # noinspection PyMethodMayBeStatic
    def block_char(self):
        if not _ScanTask.BLOCK:
            _ScanTask.BLOCK = "▋" if platform.system().lower() == 'windows' else '#'
        return _ScanTask.BLOCK

    def __init__(self, data_list, tag, exists):
        self.data_list = data_list
        self.tag = tag
        self.exists = exists
        self.result = []  # 结果列表
        self.locker = threading.RLock()  # 线程锁
        self.finished = 0   # 完成扫描的IP个数
        self.total = len(self.data_list)  # 需要扫描的IP总数
        self.progress_delta = 5
        _ScanTask.cancel = False
        signal.signal(signal.SIGINT, _ScanTask.handler)
        signal.signal(signal.SIGTERM, _ScanTask.handler)

    @staticmethod
    def handler(signal_num, handler):
        _ScanTask.cancel = True
        rprint("User canceled", end='')
        if signal_num or handler:
            pass

    def append_result(self, s):
        # 添加到结果列表
        self.locker.acquire()
        try:
            self.result.append(s)
        finally:
            self.locker.release()

    def finish_one(self):
        # 完成一个IP的扫描
        self.locker.acquire()
        try:
            self.finished += 1
            self.print_progress()
        finally:
            self.locker.release()

    def print_progress(self):
        # 显示进度
        if (self.finished % self.progress_delta == 0) or self.finished >= self.total:
            percent = self.finished * 1.0 / self.total * 100
            blocks = self.block_char() * int(round(percent / 5))
            msg = "\rScanning %s/%s :  %s %s" % (self.finished, self.total, blocks, int(percent))
            rprint(msg + '%', end='', flush=True)

    # noinspection PyMethodMayBeStatic
    def clear_progress(self):
        # 清除进度显示
        space = " " * 70
        msg = "\r" + space
        rprint(msg, end='', flush=True)
        rprint("\r", end='', flush=True)

    # noinspection PyMethodMayBeStatic
    def get_threads(self, total):
        """ 判断线程数量 """
        max_threads = 20
        threads = int(round(total / 5))
        if threads <= 0:
            threads = 1
        if threads > max_threads:
            threads = max_threads
        return threads


# Internal use：Thread function: scan a range of ip
def _ip_scan_thread(task, start, end):
    for i in range(start, end):
        time.sleep(0.05)
        if _ScanTask.cancel:
            return

        if i >= len(task.data_list):
            continue

        ip = task.data_list[i]  # get an ip
        timeout = 50 if Net.is_lan_ip(ip) else 500  # long timeout for LAN

        # ping twice
        can_ping = Net.ping(ip, 1, timeout) >= 0
        if not can_ping:
            can_ping = Net.ping(ip, 1, timeout * 2) >= 0  # try again

        if can_ping and task.exists:
            # if ping failed, and need result, put it in list
            if task.tag:
                mac_address = Net.get_mac(ip)
                if task.tag == 'list' or task.tag >= 2:
                    if task.tag == 3:
                        t = (ip, mac_address, Net.mac_factory(mac_address))
                    else:
                        t = (ip, mac_address)
                    task.append_result(t)
                else:
                    if mac_address is not None:
                        task.append_result(mac_address)
            else:
                task.append_result(ip)
        elif not can_ping and not task.exists:
            # if ping failed, and need result, put it in list
            task.append_result(ip)

        task.finish_one()  # Notify parent: one ip is finished


# Internal use：Thread function: scan a range of port
def _port_scan_thread(task, start, end):
    """ 内部使用的：线程函数，用于扫描一批IP端口 """
    for i in range(start, end):
        if _ScanTask.cancel:
            return

        if i >= len(task.data_list):
            continue

        ip = task.tag  # 取得IP地址
        port = task.data_list[i]  # 取得一个端口
        port = int(port)
        # timeout = 50 if is_lan_ip(ip) else 500  # 如果是本地IP，则超时设短一些

        # 测试端口是否能连通
        opened = Net.is_port_open(ip, port)
        # rprint('ip', ip, 'port', port, ' open=', opened)

        if opened and task.exists:
            # 如果端口能连通，且需要连通结果，则加入结果列表中
            task.append_result(port)
        elif not opened and not task.exists:
            # 如果端口不能连通，且需要连不通的结果，则加入结果列表中
            task.append_result(port)

        task.finish_one()  # 完成一个


# Network ping and scan
class Net:
    """
    Network ping and scan

    """

    @staticmethod
    def is_ip(text):
        """
        Whether the string is an IPV4 string.

        :Chinese: 判断指定文字是否是一个 IP 地址

        :param text: the string
        :return: True or False
        """
        if text is None:
            text = ''
        arr = text.split('.')
        if len(arr) != 4:
            return False
        for item in arr:
            if not StrUtil.is_ip_number(item):
                return False
        return True

    @staticmethod
    def ip_set(ip, index, number):
        """
        Change ip address number at specified index to specified number.

        :Chinese: 更改 IP地址 指定位置的数值

        :param ip: IPv4 address string
        :param index:  the index of the number, first is 0, valid indexes are 0, 1, 2, 3
                :Chinese: 第几位， 0表示第一位，取值范围是 0, 1, 2, 3
        :param number:   the number , the value range is [0-255]
                :Chinese: 数值(整数)，取值范围是 0 - 255
        :return: return IP address string. return None if error occurs.
                :Chinese: 返回更改后的IP地址。如果出错，返回None
        """
        if ip is None:
            raise TypeError('ip is None')

        arr = ip.split('.')
        if 0 <= index < len(arr):
            if StrUtil.is_ip_number(number) or number == '*':
                arr[index] = str(number)
                return '.'.join(arr)
            else:
                raise ValueError('number must in the range of [0 - 255]')
        else:
            raise ValueError('index must be 0 or 1 or 2 or 3')

    @staticmethod
    def ip_get(ip, index):
        """
        Get ip address number at specified index.

        :Chinese: 获取 IP地址中 指定位置的数值

        :param ip:   IPv4 address string
        :param index:  the index of the number, first is 0, valid indexes are 0, 1, 2, 3
                :Chinese: 第几位， 0表示第一位，取值范围是 0, 1, 2, 3
        :return: return ip address number at specified index. return None if error occurs.
                :Chinese: 返回IP地址中第 index 位的数值(整数)。如果出错，返回None
        """
        if ip is None:
            raise TypeError('ip is None')

        arr = ip.split('.')
        if 0 <= index < len(arr):
            return int(arr[index])
        else:
            raise ValueError('index invalid')

    @staticmethod
    def ip_range(ip, start=None, end=None, index=3):
        """
        Define an IP address range, return  a list of IP address string.

        :Chinese: 定义一个IP地址范围, 返回一个IP地址列表.

        :param ip:    IPv4 address string
        :param start:  start number
        :param end:    end number
        :param index:  (optional)the index of the number, first is 0, valid indexes are 0, 1, 2, 3
                :Chinese: 第几位， 0表示第一位，取值范围是 0, 1, 2, 3
        :return: return  a list of IP address string.
                :Chinese: 返回一个IP地址列表
        """
        if start is None and end is None:
            arr = ip.split('.')
            if len(arr) != 4:
                raise TypeError('%s is not a IP address' % ip)
            if arr[3] == '*':
                ip2 = Net.ip_set(ip, 3, 1)
                return Net.ip_range(ip2, 1, 255)
            elif arr[3].find('-') > 0:
                s1, s2 = StrUtil.split2(arr[3], '-')
                ip2 = Net.ip_set(ip, 3, 1)
                return Net.ip_range(ip2, int(s1), int(s2))
            elif Net.is_ip(ip):
                return [ip]
            else:
                raise ValueError('%s invalid ip' % ip)
        else:
            if Net.is_ip(ip):
                if not (0 <= start <= 255):
                    raise ValueError('start number %s is not in range 0-255')
                if not (0 <= end <= 255):
                    raise ValueError('end number %s is not in range 0-255')
                if not (2 <= index <= 3):
                    raise ValueError('index %s is not in range 2-3')
                arr = ip.split('.')
                result = []
                for i in range(start, end+1):
                    if index == 3:
                        arr[index] = str(i)
                        result.append('.'.join(arr))
                    elif index == 2:
                        arr[index] = str(i)
                        for n in range(1, 255):
                            arr[index + 1] = str(n)
                            result.append('.'.join(arr))
                return result
            raise TypeError('%s is not a IP address' % ip)

    @staticmethod
    def port_range(port_start, port_end=None):
        """
        Define a port range, return  a list of port int.

        :Chinese: 定义一个端口范围, 返回一个端口列表.

        :param port_start:  starting port number, int, value range is [1-65535]
                    :Chinese: 起始端口(整数), 取值范围是 1-65535
        :param port_end:  ending port number, int, value range is [1-65535]
                    :Chinese:结束端口(整数), 取值范围是 1-65535
        :return: return  a list of port int.
        """
        if isinstance(port_start, str) and port_end is None:
            if port_start == 'commons' or port_start == "common":
                return Port.common_ports()

            if port_start.find('-') >= 0:
                s1, s2 = StrUtil.split(port_start, '-')
                port_start = int(s1)
                port_end = int(s2)
            elif port_start.find(',') >= 0:
                arr = port_start.split(',')
                ret = []
                for item in arr:
                    item = item.strip()
                    ret.append(int(item))
                return ret
            else:
                port_start = int(port_start)
                port_end = port_start

        if not isinstance(port_start, int) or not (0 <= port_start < 65536):
            raise ValueError('port %s is out of range [1, 65535]' % port_start)
        if not isinstance(port_end, int) or not (0 <= port_end < 65536):
            raise ValueError('port %s is out of range [1, 65535]' % port_end)
        if port_end < port_start:
            port_start, port_end = port_end, port_start

        result = []
        for i in range(port_start, port_end + 1):
            result.append(i)
        return result

    @staticmethod
    def get_connection_ip(host, port):
        """
        Get the local IP address that connects to the specified host.
        
        :Chinese: 取得可连接到指定服务器的本地IP地址.

        :param host:  host domain or ip
        :param port:  the port
        :return: return the local IP address that connects to the specified host.
                :Chinese: 返回连接指定服务器的本地IP地址.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # noinspection PyBroadException
        try:
            sock.connect((host, port))
            host = sock.getsockname()
            sock.close()
            return host[0]
        except Exception:
            if sock:
                sock.close()
            return None

    @staticmethod
    def local_ip():
        """
        Get local IP address.

        :Chinese: 取得局域网IP地址.

        :return: return IP address string
        """
        my_ip = Net.get_connection_ip("qq.com", 80)  # try internet
        if my_ip is None:
            my_ip = Net.get_connection_ip("10.0.0.1", 80)
            if my_ip is None:
                my_ip = Net.get_connection_ip("192.168.1.1", 80)
        return my_ip

    @staticmethod
    def has_internet():
        """ Whether internet is available """
        my_ip = Net.get_connection_ip("qq.com", 80)  # try internet
        return my_ip is not None

    @staticmethod
    def is_lan_ip(ip):
        """ Whether specified IP address is LAN IP address """
        arr = ip.split('.')
        if arr[0] == '192':
            if len(arr) >= 1 and arr[1] == '168':
                return True
        elif arr[0] == '172':
            if len(arr) >= 1 and ('16' <= arr[1] <= '31'):
                return True
        elif arr[0] == '10':
            return True
        elif ip == '127.0.0.1':
            return True
        return False

    @staticmethod
    def run_command(cmd_line):
        """
        run a command in current OS

        :param cmd_line:  command line
        :return: return a tuple (ret, text), the first element is return value，the second is result text.
        """

        # 创建一个进程，运行命令
        p = subprocess.Popen(cmd_line,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True
                             )
        p.wait()

        # 取得返回值
        ret_code = p.returncode
        out = ''

        # noinspection PyBroadException
        try:
            # 取得返回文字
            out = p.stdout.read()
            p.stdout.close()
            p.stderr.close()
        except Exception:
            pass

        # 转换文字编码
        encode = StrUtil.sys_encoding() if platform.system().lower() == 'windows' else 'utf-8'
        # encode = "gbk" if platform.system().lower() == 'windows' else 'utf-8'

        # noinspection PyBroadException
        try:
            text = out.decode(encode)
            if not isinstance(text, str):
                text = str(text)
        except Exception:
            # noinspection PyBroadException
            try:
                text = out.decode('ascii')
                if not isinstance(text, str):
                    text = str(text)
            except Exception:
                text = out

        return ret_code, text

    @staticmethod
    def ping(ip, times=1, timeout=1000):
        """
        Pint specified IP address

        :param ip:  IP address string or host name
        :param times:  (optional) times of ping
        :param timeout:  (optional) waiting timeout in milliseconds，defalut is 1000.
        :return: return time usage of ping in millisecond.  return -1 when ping fails.
            :Chinese: 返回Ping通时间（单位为毫秒)。 返回-1表示Ping不通。
        """

        # compose a command line : "ping -c 1 bing.com"
        if platform.system().lower() == 'windows':
            command = 'ping -w %s -n %s %s' % (timeout, times, ip)
        else:
            timeout = round(timeout / 10) / 100
            command = 'ping -W %s -c %s %s' % (timeout, times, ip)

        code, text = Net.run_command(command)

        # find lines which has 'time' word
        lines = StrUtil.grep(text, ('时间', 'time'))

        # get time from response text
        time_usages = []
        for line in lines:
            word = StrUtil.find_word(line, ('时间', 'time'))  # find word with time
            _, s_time = StrUtil.split2(word, ('=', '<'))  # find word  after '=' or '<'
            number, unit = StrUtil.split_number_unit(s_time)  # split into number, unit
            if isinstance(number, int) or isinstance(number, float):
                if times == 1:
                    return number
                elif number >= 0:
                    time_usages.append(number)

        if len(time_usages) == 0:
            return -1
        else:
            # for multi time value, calculate the average time
            total = 0
            for number in time_usages:
                total += number
            return round(total / len(time_usages), 2)

    @staticmethod
    def get_mac(ip):
        """
        Get the MAC address of specified IP address.

        :Chinese: 取得 IP地址 对应的 MAC地址。

        :param ip:  IP address string.
        :return: return MAC address string, like: 78:44:fd:6d:1c:91". return empty string if fail.
                :Chinese: 返回MAC地址字符串。如："78:44:fd:6d:1c:91"
        """
        # command line: "arp -a 192.168.1.1"
        if platform.system().lower() == 'windows':
            command = 'arp -a %s' % ip
            delimiter = '-'
        else:
            # cmd = 'arp -a %s' % ip
            command = 'arping -c 1 %s' % ip
            delimiter = ':'

        code, text = Net.run_command(command)

        # get MAC from response text
        lines = StrUtil.grep(text, ip)  # find lines with ip
        for line in lines:
            # rprint(delimiter, type(line), line)
            word = StrUtil.find_word(line, [delimiter, delimiter])
            if word:
                if word.find('--') >= 0:
                    continue
                if delimiter == '-':
                    word = word.replace(delimiter, ':')
                if word.startswith('[') and word.endswith(']'):
                    word = word[1: len(word) - 1]
                return word

        return ''

    @staticmethod
    def mac_factory(mac):
        """
        Get manufacture factory name by specified MAC address.

        :Chinese: 根据mac码，获取制造工厂名称.

        :param mac:  the MAC address string
        :return: return a string of manufacture factory name. return empty string if fail.
            :Chinese: 返回字符串（制造工厂名称)
        """
        url = 'https://mac.bmcx.com/{0}__mac/'
        mac = mac.replace(':', '-')
        page = Http.get(url, mac)
        name = StrUtil.get_word(page, ['组织名称', '<td', '>'], ['</td'])
        if name is not None:
            return name
        else:
            url = 'http://www.coffer.com/mac_find/?string={0}'
            page = Http.get(url, mac)
            name = StrUtil.get_word(page, ['Vendor</th', '<tr', '<td', '<td', '<a', '>'], ['</a'])
            return name if name is not None else ''

    @staticmethod
    def ip_scan(ip_list, mac=False, exists=True, threads=0):
        """
        Scan IP address list, return a list of ip address or MAC address which is pingable.

        :Chinese: 扫描 IP地址列表，取得 可PING通的 IP地址列表 (或MAC地址列表).

        :param ip_list:   the IP address list
        :param mac: (optional) whether get MAC address, default is False.<br>
                if mac == True, the item of result list is MAC address list.<br>
                if mac == 2, the item of result list is a 2-elements tuple of (ip, mac)<br>
                if mac == 3, the item of result list is a 3-elements tuple of (ip, mac, factory)<br>

                :Chinese:
                （可选）是否取得MAC地址，默认值是False.<br>
                如果mac=True,则结果列表每一项是MAC地址。<br>
                如果mac=2, 则结果列表每一项是一个tuple, 形如：(IP地址, MAC地址)。<br>
                如果mac=3, 则结果列表每一项是一个tuple, 形如：(IP地址, MAC地址, 厂商)。<br>

        :param exists:  (optional) Whether get pingable IPs. if exists is False, return list is not pingable IPs.
                :Chinese:（可选）是否取得Ping通的地址，默认值是True.<br>
                如果exists=False,则结果列表是PING不通的IP地址。<br>
        :param threads:   (optional) how many threads that uses. default is 0 for auto detect.
                :Chinese:（可选）并发线程数量，默认值是0(自动选择线程数量）
        :return:  return a list. the item of list depends on the mac parameter.
        """
        # 创建一个扫描任务
        task = _ScanTask(ip_list, mac, exists)
        total = len(ip_list)
        if total == 0:
            return []

        # detect thread count
        if threads <= 0:
            threads = task.get_threads(total)

        # create each thread
        start = 0    # the start index of the ip_list for the thread
        thread_pool = []
        rprint('\rScanning...', end='')
        for i in range(0, threads):
            end = start + int(round(total / threads))  # the end index of the ip_list for the thread
            if i == threads - 1:
                end = total
            # create thread
            t = threading.Thread(target=_ip_scan_thread, args=(task, start, end))
            thread_pool.append(t)  # add to pool
            t.start()
            start = end  # next start point

        # wait for all threads end.
        while True:
            alive = False
            for i in range(len(thread_pool)):
                alive = alive or thread_pool[i].is_alive()
            if not alive:
                break

        task.clear_progress()  # clear progress bar

        return task.result

    @staticmethod
    def is_port_open(ip, port, udp=False):
        """
        Whether specified port is opened on specified IP address.

        :Chinese: 判断服务器的指定端口是否开放.

        :param ip:    the IP address or host name
        :param port:  port number, int
        :param udp:   (optional) whether use UDP. default is False
        :return: return True if the port is opened. return False if not opened.
        """
        family = socket.SOCK_DGRAM if udp else socket.SOCK_STREAM
        sock = socket.socket(socket.AF_INET, family)
        sock.settimeout(2000)

        if not isinstance(port, int):
            port = int(port)

        # noinspection PyBroadException
        try:
            state = sock.connect_ex((ip, port))
            sock.close()
            return state == 0
        except Exception:
            return False

    @staticmethod
    def port_scan(ip, port_list=None, exists=True, threads=0, name=False):
        """
        Scan ports of specified IP address.

        :Chinese: 对于指定IP地址，扫描端口列表， 取得 可连接的 端口列表

        :param ip:         the IP address.
        :param port_list:  (optional) a list of port. If port_list is None, scan common used ports.
                :Chinese: (可选)端口列表, 如果port_list为None，则扫描常见端口
        :param exists:   (optional) Whether return opened ports. If exists is False, return not-opened ports.
                :Chinese:（可选）是否取得可连接的端口，默认值是True.<br>
                如果exists=False,则结果列表是不可连接的端口。<br>
        :param threads:  (optional) how many threads that uses. default is 0 for auto detect.
                    :Chinese:（可选）并发线程数量，默认值是0(自动选择线程数量）
        :param name:    (optional) whether return the protocol name.
                        If name is True, each item of result list is a tuple of (port, protocol).
                :Chinese:（可选）是否返回协议名，默认值是False.
                如果name=True,则结果列表每一项是一个tuple, 形如：(端口号, 协议名称)。<br>
        :return:  return a list.
        """
        if not Net.is_ip(ip):
            raise TypeError("%s is not a ip" % repr(ip))

        if port_list is None:
            port_list = Port.common_ports()

        if isinstance(port_list, int):
            port_list = [port_list]

        # create a scan task
        task = _ScanTask(port_list, ip, exists)
        total = len(port_list)
        if total == 0:
            return []

        # detect thread count
        if threads <= 0:
            threads = task.get_threads(total)

        # create each thread
        start = 0  # the start index of the port_list for the thread
        thread_pool = []  # 线程池
        rprint('Scanning...\r', end='')
        for i in range(0, threads):
            end = start + int(round(total / threads))  # the end index of the port_list for the thread
            if i == threads - 1:
                end = total
            # 创建线程
            t = threading.Thread(target=_port_scan_thread, args=(task, start, end))
            thread_pool.append(t)
            t.start()
            start = end  # next start point

        # wait all threads end
        while True:
            alive = False
            for i in range(len(thread_pool)):
                alive = alive or thread_pool[i].is_alive()
            if not alive:
                break

        task.clear_progress()  # clear progress bar

        if name:
            # if name is true, get protocol by port
            ret = []
            for port in task.result:
                protocol = Port.name_of(port)
                ret.append((port, protocol))
            return ret
        else:
            return task.result


# noinspection PyPep8Naming
# noinspection SpellCheckingInspection
class Port:
    """ common used port """

    Echo = 7  # Echo service
    FTP_Data = 20  # File Transfer Protocol data transfer
    FTP = 21  # File Transfer Protocol (FTP) control connection
    SSH = 22  # Secure Shell, secure logins, file transfers (scp, sftp), and port forwarding
    Telnet = 23  # Telnet protocol—unencrypted text communications
    SMTP = 25  # Simple Mail Transfer Protocol, used for email routing between mail servers
    WINS = 42  # WINS Replication
    WHOIS = 43  # WHOIS
    DNS = 53  # Domain Name System name resolver
    TFTP = 69  # Trivial File Transfer Protocol
    HTTP = 80  # HTTP v1, v2 uses TCP.  HTTP v3 uses QUIC/UDP
    Kerberos = 88  # Network authentication system
    MSExchange = 102  # MS Exchange
    POP3 = 110  # Post Office Protocol, version 3 (POP3)
    NNTP = 119  # NNTP (Usenet)
    MSRPC = 135  # Microsoft End Point Mapper, manage services including DHCP server, DNS server, and WINS, DCOM
    NetBIOS = 137  # NetBIOS Name Service, used for name registration and resolution
    NetBIOS_SMB = 139  # NetBIOS Session Service
    IMAP = 143  # Internet Message Access Protocol (IMAP)
    SNMP = 161  # SNMP
    BGP = 179  # BGP
    HP_Openview = 381  # HP data alarm manager
    HP_Openview2 = 383  # HP data alarm manager
    LDAP = 389  # LDAP
    HTTPS = 443  # HTTPS v1, v2 uses TCP. HTTP v33 uses QUIC/UDP.
    SMB = 445  # Microsoft File sharing:Server Message Blocks name
    Kerberos2 = 464  # Kerberos Change/Set password
    SMTPS = 465  # Authenticated SMTP over TLS/SSL (SMTPS)
    RTSP = 554  # RTSP
    NNTPS = 563  # NNTP over SSL
    IMAPS2 = 585  # Secure IMAP
    SMTPS2 = 587  # Email message submission
    MSDOM = 593  # Microsoft DCOM, HTTP RPC Ep Map
    LDAPS = 636  # Lightweight Directory Access Protocol over TLS/SSL
    MPLS = 646  # LDP (MPLS)
    MSExchange2 = 691  # MS Exchange Routing
    Vmware = 902  # VMware ESXi
    FTPS = 989  # FTPS Protocol (data), FTP over TLS/SSL
    FTPS2 = 990  # FTPS Protocol (control), FTP over TLS/SSL
    IMAPS = 993  # Internet Message Access Protocol over TLS/SSL (IMAPS)
    POP3S = 995  # Post Office Protocol 3 over TLS/SSL
    RPC = 1025  # Microsoft Remote Procedure Call
    OpenVPN = 1194  # OpenVPN
    WASTE = 1337  # WASTE Encrypted File Sharing Program
    SqlServer = 1433  # Microsoft SqlServer DB
    VQP = 1589  # Cisco VLAN Query Protocol (VQP)
    PPTP = 1723  # MS PPTP
    Steam = 1725  # Valve Steam Client uses port 1725
    RADIUS = 1812  # RADIUS authentication
    RADIUS2 = 1813  # RADIUS authentication
    NFS = 2049  # Network File System
    cPanel = 2082  # cPanel default
    radsec = 2083  # Secure RADIUS Service (radsec), cPanel default SSL
    Oracle = 2483  # Oracle database listening for insecure client connections to the listener, replaces port 1521
    Oracle2 = 2484  # Oracle database listening for SSL client connections to the listener
    SymantecAV = 2967  # Symantec System Center agent (SSC-AGENT)
    XBOX = 3074  # Xbox LIVE and Games for Windows – Live
    MySQL = 3306  # MySQL database system
    RDC = 3389  # default Remote Desktop
    Warcraft = 3724  # Some Blizzard games, Unofficial Club Penguin Disney online game for kids
    GoogleDesktop = 4664  # Google Desktop Search
    eMule = 4672  # eMule
    SynologyNAS = 5000  # Synology NAS
    UPnP = 5000  # UPnP
    SIP = 5060  # Telephone Session initiation protocol
    PostgreSQL = 5432  # PostgreSQL database system
    VNC = 5900  # virtual Network Computing (VNC) Remote Frame Buffer RFB protocol
    IRC = 6665  # Internet Relay Chat
    IRC2 = 6669  # Internet Relay Chat
    BitTorrent = 6881  # BitTorrent is part of the full range of ports used most often
    BitTorrent2 = 6999  # BitTorrent is part of the full range of ports used most often
    Quicktime = 6970  # QuickTime Streaming Server
    HTTP2 = 8080  # alternate HTTP port (also a Tomcat port)
    KasperskyAV = 8086  # Kaspersky AV Control Center
    KasperskyAV2 = 8087  # Kaspersky AV Control Center
    VMwareServer = 8222  # VMware Server Management User Interface (insecure Web interface).
    HPJetDirect = 9100  # HP JetDirect
    SCP = 9999  # SCP
    BackupExec = 10000  # Webmin, Web-based Unix/Linux system administration tool (default port)
    NetBus = 12345  # NetBus remote administration tool (often Trojan horse).
    Sub7 = 27374  # Sub7 default
    BackOrifice = 18006  # Back Orifice 2000 remote administration tools

    @staticmethod
    def common_ports():
        """ return a list of common used ports """
        result = []
        for name in Port.__dict__:
            if isinstance(Port.__dict__[name], int):
                result.append(Port.__dict__[name])
        return result

    @staticmethod
    def name_of(port_number):
        """ get the name of protocol of specified port number """
        for name in Port.__dict__:
            if Port.__dict__[name] == port_number:
                return name
        return ''

