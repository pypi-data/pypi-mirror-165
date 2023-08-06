import base64
import getpass
import json
import logging
import os
import random
import shlex
import subprocess
# import pwd
import tempfile
import threading
import time
import traceback
from pathlib import Path

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from stem.control import Controller
from stem.util import term

from mtlibs import mtutils
from mtlibs.mtutils import ranstr
from mtlibs.process_helper import exec, is_tool

logger = logging.getLogger(__name__)

# 全局设置，忽略ssl证书校验警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 外网IP检查间隔（秒）
TOR_CHECK_IP_INTERVAL = 10


def ensureIntor():
    """确保网络在tor里面"""
    tor_socks_port = os.environ.get("TOR_SOCKS_PORT", "0.0.0.0:9050")
    controll_port = os.environ.get("TOR_CONTROLL_PORT", "127.0.0.1:9051")
    controll_password = os.environ.get("TORCONTROLL_PASSWORD", "my_password")
    b64_hs_ed25519_secret_key = os.environ.get("ONIONKEY", None)
    if mtutils.is_tcp_listen(controll_port):
        logger.info("####tor controll %s 运行中" % controll_port)
        return True
    else:

        set_iptables()
        tor_proc = TorProc()
        print("开始启动tor进程", flush=True)
        is_tor_connected = tor_proc.start(
            socks_port=tor_socks_port,
            hiddenservice_ports=["80 80"],
            controll_port=controll_port,
            controll_password=controll_password,
            b64_hs_ed25519_secret_key=b64_hs_ed25519_secret_key,
            wait=True)
        print("tor进程启动完毕", flush=True)
        if is_tor_connected:
            print(term.format("TOR 已经连接上", term.Color.GREEN), flush=True)
            print(term.format("TOR hidden dir: %s" % tor_proc.hidden_dir,
                              term.Color.GREEN),
                  flush=True)

            if tor_proc.onion_name:
                os.environ["MAIN_ONION"] = tor_proc.onion_name
            print(term.format("onion:  %s" % tor_proc.onion_name,
                              term.Color.GREEN),
                  flush=True)
            print(term.format("private key:  %s" % tor_proc.private_key,
                              term.Color.GREEN),
                  flush=True)

            threading.Thread(target=ip_protect, daemon=True).start()
            return True
        else:
            return False


def ip_protect():
    """
        后台线程，不断检测IP是否处于安全状态
    """
    current_user = getpass.getuser()
    # curl --insecure https://116.202.120.181/api/ip
    urllist = [
        "https://116.202.120.181/api/ip", "https://check.torproject.org/api/ip"
    ]
    count = 1
    total_seconds = 0
    while True:
        url = urllist[count % len(urllist)]
        # logger.info("准备检测：{}".format(url))
        try:
            t1 = time.time()
            response = requests.get(url, verify=False)
            resultObj = json.loads(response.content.decode())
            if resultObj['IsTor'] == 'False':
                logger.error("错误，外网IP泄露")
                exit(-128)
            else:
                current_seconds = time.time() - t1
                total_seconds += current_seconds
                ava_seconds = total_seconds / count
                logger.info("u:%s %.2f/%.2f ip:%s %s" %
                            (current_user, current_seconds, ava_seconds,
                             resultObj['IP'], url))
        except requests.exceptions.ConnectionError as e:
            print(e)
            logger.info("ip_protect -> user:{}, 连接失败 {}".format(
                current_user, url))
        time.sleep(TOR_CHECK_IP_INTERVAL)
        count += 1


class TorProc():
    """表示一个可控的Tor进程"""

    def __init__(self):
        self.connected = False
        self._hidden_dir = 'hidden_service'

    def getHostname(self):
        """获取隐藏服务的域名"""
        with open(self.hidden_dir + "/hostname") as f:
            return f.read().strip()

    def getSocksPort(self):
        """获取当前tor进程的socks5代理端口"""
        return self.socks_port

    def checkIpSafe(self):
        proxies = {
            "http": "socks5://{}:{}".format("127.0.0.1", self.socks_port),
            "https": "socks5://{}:{}".format("127.0.0.1", self.socks_port),
        }
        res = requests.get("https://check.torproject.org/api/ip",
                           proxies=proxies)
        return res.content.decode().index("\"IsTor\":true") > 0

    async def stop(self):
        """停止tor进程"""
        # TODO: 停止tor进程
        pass

    def start(self,
              socks_port=0,
              b64_hs_ed25519_secret_key=None,
              hiddenservice_ports=["80 80"],
              controll_password='my_password',
              controll_port='9051',
              user='debian-tor',
              wait=True):
        """
            socks_port :0 为随机端口
            返回值:
            [是否成功,实际实用的socks端口号]
        """
        if socks_port == 0:
            socks_port = random.randrange(40001, 49999)
        self.socks_port = socks_port
        self.hiddenservice_ports = hiddenservice_ports
        toruser = pwd.getpwnam(user)
        if not is_tool("tor"):
            exec("sudo apt install -y tor")

        self.tmpdirname = tempfile.gettempdir() + "/tor_" + ranstr(20)
        self.hidden_dir = self.tmpdirname + "/" + self._hidden_dir
        Path(self.tmpdirname).mkdir(mode=0o700, exist_ok=True)
        os.chown(self.tmpdirname, toruser.pw_uid, toruser.pw_gid)

        torargs = ["SocksPort {}".format(socks_port)]
        torargs.append("DataDirectory \"{}\"".format(self.tmpdirname))
        torargs.append("ControlPort {}".format(controll_port))
        torargs.append("CookieAuthentication 1")
        torargs.append("VirtualAddrNetworkIPv4 10.192.0.0/10")
        torargs.append("AutomapHostsOnResolve 1")
        torargs.append('TransPort 0.0.0.0:9040')
        torargs.append('DNSPort 0.0.0.0:5353')
        # torargs.append('ExitNodes ru')

        if self.hiddenservice_ports:
            # tor 会使用现成的hs_ed25519_secret_key文件生成公钥和域名. 这样就相当于预先指定了onion域名
            # 否则,会重新生成新的私钥和新的域名
            Path(self.hidden_dir).mkdir(mode=0o700, exist_ok=True)

            os.chown(self.hidden_dir, toruser.pw_uid, toruser.pw_gid)
            torargs.append("HiddenServiceDir \"{}\"".format(self.hidden_dir))

            for port in self.hiddenservice_ports:
                torargs.append("HiddenServicePort \"{}\"".format(port))

            # 必须配置了端口，才能配置私钥，要不然tor不能正常启动。
            if b64_hs_ed25519_secret_key:
                filepath = self.hidden_dir + "/hs_ed25519_secret_key"
                Path(filepath).touch(mode=0o700)
                with open(filepath, 'wb') as f:
                    f.write(base64.b64decode(b64_hs_ed25519_secret_key))
                os.chown(filepath, toruser.pw_uid, toruser.pw_gid)

        # 明文参数
        # torargs.append("--hash-password 'my_password'")
        # 密码使用hash
        # 这个hash 对应的密码："my_password"
        torargs.append(
            "HashedControlPassword 16:E600ADC1B52C80BB6022A0E999A7734571A451EB6AE50FED489B72E3DF"
        )

        cmdline = "sudo -u debian-tor tor " + " ".join(torargs)
        logger.info("[exec]{}".format(cmdline))

        self.process = subprocess.Popen(shlex.split(cmdline),
                                        stdout=subprocess.PIPE)

        # if wait:
        connect_result = self.waite_tor_connect()
        if connect_result == False:
            logger.info("TOR 启动失败")
            return False
        else:
            self.onion_name = self.getHostname()
            self.private_key = self.getPrivateKey_b64()
            self.dataDirectory = self.tmpdirname
            return True

        # else:
        #     threading.Thread(target=self.waite_tor_connect).start()

    def getHostname(self):
        """获取隐藏服务的实际域名"""
        hostnameFile = self.hidden_dir + "/hostname"
        if Path(hostnameFile).exists():
            with open(hostnameFile) as f:
                return f.read().strip()
        else:
            return None

    def getPrivateKey_b64(self):
        """获取隐藏服务对应的私钥的base64编码的字符"""
        keyfile = self.hidden_dir + "/hs_ed25519_secret_key"
        if Path(keyfile).exists():
            with open(keyfile, 'rb') as f:
                return base64.b64encode(f.read()).decode()
        else:
            return None

    def wait(self):
        """等待直到连接上"""
        while not self.connected:
            time.sleep(1)
        return

    def waite_tor_connect(self):
        """处理tor进程的输出，当成功连接，或者失败时返回"""
        try:
            while True:
                if self.process.stdout:
                    line = self.process.stdout.readline().decode().strip()
                    logger.debug("tor->{}".format(line))
                    if line.strip().find('Bootstrapped 100%') > 0:
                        self.connected = True
                        return True
                    elif line.strip().find(
                            'Catching signal TERM, exiting cleanly.') > 0:
                        logger.info("[tor exited]")
                        return False
                    elif line.strip().find('[err]') > 0:
                        logger.error('tor 连接出错 {}'.format(line.strip()))
                        return False

                if self.process.stderr:
                    line = self.process.stderr.readline().decode()
                    logger.error("tor->[error]{}".format(line))
                    return False

                if self.process.poll() is not None:
                    break

        except Exception as e:
            logger.error(traceback.format_exc(e))
            return False


def set_iptables():
    """
        设置IPtables
        1: 本地自动透明代理
        2：vpn自动透明代理（跟openvpn搭配使用）
        3: 特定用户进程能真实IP连接外网
        4: 只允许特定端口入站。
    """
    print("set_iptables called", flush=True)

    _tor_uid = pwd.getpwnam('debian-tor').pw_uid
    # 另外一个高权限的非tor用户
    _nottor_uid = '567'
    # Tor's TransPort
    _trans_port = "9040"
    # Tor's DNSPort
    _dns_port = "5353"
    # Tor's VirtualAddrNetworkIPv4
    _virt_addr = "10.192.0.0/10"
    # Your outgoing interface
    _out_if = "eth0"
    # LAN destinations that shouldn't be routed through Tor
    # _non_tor="127.0.0.0/8 10.0.0.0/8 172.16.0.0/12 192.168.0.0/16 10.12.12.0/24 172.17.0.0/16 10.18.0.0/16"
    _non_tor = "127.0.0.0/8 10.0.0.0/8 172.16.0.0/12 192.168.0.0/16 172.17.0.0/16"
    # Other IANA reserved blocks (These are not processed by tor and dropped by default)
    _resv_iana = "0.0.0.0/8 100.64.0.0/10 169.254.0.0/16 192.0.0.0/24 192.0.2.0/24 192.88.99.0/24 198.18.0.0/15 198.51.100.0/24 203.0.113.0/24 224.0.0.0/4 240.0.0.0/4 255.255.255.255/32"
    # 允许入站端口
    _input_ports = "80 8080 49090 41890 41080 48811"
    os.system("iptables -F && iptables -t nat -F")
    os.system(
        """iptables -t nat -A OUTPUT -d {_virt_addr} -p tcp -m tcp --tcp-flags FIN,SYN,RST,ACK SYN -j REDIRECT --to-ports {_trans_port}"""
        .format(_virt_addr=_virt_addr, _trans_port=_trans_port))

    # nat dns requests to Tor
    exec(
        "iptables -t nat -A OUTPUT -d 127.0.0.1/32 -p udp -m udp --dport 53 -j REDIRECT --to-ports {_dns_port}"
        .format(_dns_port=_dns_port))

    # Don't nat the Tor process, the loopback, or the local network
    exec("iptables -t nat -A OUTPUT -m owner --uid-owner {_tor_uid} -j RETURN".
         format(_tor_uid=_tor_uid))
    exec(
        "iptables -t nat -A OUTPUT -m owner --uid-owner {_nottor_uid} -j RETURN"
        .format(_nottor_uid=_nottor_uid))
    exec("iptables -t nat -A OUTPUT -o lo -j RETURN")

    # 内网网段
    for _lan in _non_tor.split(' '):
        exec("iptables -t nat -A OUTPUT -d {_lan} -j RETURN".format(_lan=_lan))
    for _iana in _resv_iana.split(' '):
        exec("iptables -t nat -A OUTPUT -d {_iana} -j RETURN".format(
            _iana=_iana))
    # Redirect all other pre-routing and output to Tor's TransPort
    exec(
        "iptables -t nat -A OUTPUT -p tcp -m tcp --tcp-flags FIN,SYN,RST,ACK SYN -j REDIRECT --to-ports {_trans_port}"
        .format(_trans_port=_trans_port))

    # 允许入站的端口
    for _input_port in _input_ports.split(' '):
        exec(
            "iptables -A INPUT -i {_out_if} -p tcp --dport {_input_port} -m state --state NEW -j ACCEPT"
            .format(_out_if=_out_if, _input_port=_input_port))

    # 关闭其他入站端口
    exec("iptables -A INPUT -m state --state ESTABLISHED -j ACCEPT")
    exec("iptables -A INPUT -i lo -j ACCEPT")

    # Allow INPUT from lan hosts in $_non_tor
    # 允许内网入站连接
    for _lan in _non_tor.split(' '):
        exec("iptables -A INPUT -s {_lan} -j ACCEPT".format(_lan=_lan))

    # iptables -A INPUT -j DROP
    # 暂时接受所有入站请求，毕竟是在容器内，本身就有端口的限制。
    # exec("iptables -A INPUT -j DROP")
    exec("iptables -A INPUT -j ACCEPT")
    # *filter FORWARD
    exec("iptables -A FORWARD -j DROP")

    # *filter OUTPUT
    exec("iptables -A OUTPUT -m state --state INVALID -j DROP")
    exec("iptables -A OUTPUT -m state --state ESTABLISHED -j ACCEPT")

    # Allow Tor process output
    # 允许特定用户直连外网。
    exec(
        "iptables -A OUTPUT -o {_out_if} -m owner --uid-owner {_tor_uid} -p tcp -m tcp --tcp-flags FIN,SYN,RST,ACK SYN -m state --state NEW -j ACCEPT"
        .format(_tor_uid=_tor_uid, _out_if=_out_if))
    exec(
        "iptables -A OUTPUT -o {_out_if} -m owner --uid-owner {_nottor_uid} -p tcp -m tcp --tcp-flags FIN,SYN,RST,ACK SYN -m state --state NEW -j ACCEPT"
        .format(_nottor_uid=_nottor_uid, _out_if=_out_if))

    # Allow loopback output
    exec("iptables -A OUTPUT -d 127.0.0.1/32 -o lo -j ACCEPT")
    # Tor transproxy magic
    exec(
        "iptables -A OUTPUT -d 127.0.0.1/32 -p tcp -m tcp --dport {_trans_port} --tcp-flags FIN,SYN,RST,ACK SYN -j ACCEPT"
        .format(_trans_port=_trans_port))

    # Allow OUTPUT to lan hosts in $_non_tor
    for _lan in _non_tor.split(' '):
        exec("iptables -A OUTPUT -d {_lan} -j ACCEPT".format(_lan=_lan))

    exec("iptables -A OUTPUT -j DROP")
    # -P 参数表示默认策略
    # ### Set default policies to DROP
    exec("iptables -P INPUT DROP")
    exec("iptables -P FORWARD DROP")
    exec("iptables -P OUTPUT DROP")

    # # Set default policies to DROP for IPv6
    # exec("ip6tables -P INPUT DROP")
    # exec("ip6tables -P FORWARD DROP")
    # exec("ip6tables -P OUTPUT DROP")

    # ##
    # # vpn 内网透明代理
    # ##
    # exec("iptables -t nat -A PREROUTING -s 10.12.12.0/24 -p udp --dport 53 -j REDIRECT --to-ports 5353")
    # # exec("iptables -t nat -A PREROUTING -s 10.12.12.0/24 -p udp --dport 5353 -j REDIRECT --to-ports 5353")

    # exec("iptables -t nat -A PREROUTING -s 10.12.12.0/24 -p tcp --syn -j REDIRECT --to-ports {_trans_port}".format(
    #     _trans_port=_trans_port
    # ))

    # #
    # # 下面这三行是根据tun0接口来做透明代理转发，有效的。
    # #
    exec(
        "iptables -t nat -A PREROUTING -i tun0 -p udp --dport 53 -j REDIRECT --to-ports 5353"
    )
    exec(
        "iptables -t nat -A PREROUTING -i tun0 -p udp --dport 5353 -j REDIRECT --to-ports 5353"
    )
    exec(
        "iptables -t nat -A PREROUTING -i tun0 -p tcp --syn -j REDIRECT --to-ports 9040"
    )

    # ##
    # ## vpn 内网访问web 被拦截了。现在试试看能不能解决。
    # ##
    # exec("iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE")
    # exec("iptables -t nat -A POSTROUTING -o tun0 -j MASQUERADE")
    # exec("iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE")


# def start_tor(controll_port=9051, process_user='debian-tor'):
#     """
#         启动tor进程。
#         注意：  由于容器内部需要做透明代理，同时确保只有debian-tor用户启动的进程才能无障碍的连接外网。
#                 然而 stem 库，没有考虑到透明代理和需要以debian-tor身份启动tor。
#                 所以，用一个独立的py脚本文件来启动tor（以debian-tor身份）

#     """

#     if mtutils.is_tcp_listen(controll_port):
#         logger.info("tor controll 端口已经打开，不必重新启动tor")
#     else:
#         # 由于 start_tor.py 运行权限比较低，所以创建文件夹的工作，在这里做。
#         Path("/tmp/tor").mkdir(mode=777, exist_ok=True)
#         hidden_service_dir = '/tmp/tor/hidden_service'
#         b64_hs_ed25519_secret_key = os.environ.get('ONIONKEY', None)
#         keyfile = hidden_service_dir + "/hs_ed25519_secret_key"
#         if b64_hs_ed25519_secret_key:
#             if b64_hs_ed25519_secret_key == 'auto':
#                 pass
#             else:
#                 Path(hidden_service_dir).mkdir(mode=0o700, exist_ok=True)
#                 Path(keyfile).touch(mode=0o700)
#                 with open(keyfile, 'wb') as f:
#                     f.write(base64.b64decode(b64_hs_ed25519_secret_key))
#                 uid = pwd.getpwnam(process_user).pw_uid

#         exec("sudo chmod 700 -R /tmp/tor")
#         exec("sudo chown debian-tor -R /tmp/tor")

#         torargs = ["SocksPort {}".format('0.0.0.0:9050')]
#         torargs.append()

#         exec("chmod 777 ./start_tor.py")
#         process = subprocess.run(shlex.split(
#             'bash -c "./start_tor.py"'), user=process_user)
#         logger.info("tor connected, onion hostname: %s " %
#                     open(hidden_service_dir+'/hostname').read())

#
# 读取相关信息回显
#
# tor_helper.create_hidden_service(controll_password=TORCONTROLL_PASSWORD)
# tor_helper.create_ephemeral_hidden_service(controll_password=TORCONTROLL_PASSWORD)
# tor_helper.create_hidden_service(
#     port=80,
#     targetport=80,
#     b64_hs_ed25519_secret_key=os.environ.get('ONIONKEY',None),
#     controll_password=TORCONTROLL_PASSWORD
#     )

# 添加隐藏域名
# with Controller.from_port() as controller:
#     controller.authenticate(TORCONTROLL_PASSWORD)
#     hidden_service_dir = os.path.join(
#         controller.get_conf('DataDirectory', '/tmp'), 'hiddenservice1')
#     result = controller.create_hidden_service(
#         hidden_service_dir, 80, target_port=HTTP_PORT)
#     if result.hostname:
#         print(" * Creating our hidden service in %s" %
#               hidden_service_dir)
#         print(" * onion domain: %s" % result.hostname, flush=True)
#     else:
#         print("添加隐藏域名失败", flush=True)
# tor_helper.set_hiddenservice()

# def create_hidden_service(port=80,
#                           targetport=80,
#                           b64_hs_ed25519_secret_key=None,
#                           controll_password=None):
#     """添加隐藏服务域名"""
#     # with Controller.from_port() as controller:
#     #     controller.authenticate(controll_password)
#     #     hidden_service_dir = os.path.join(
#     #         controller.get_conf('DataDirectory', '/tmp'), 'myhiddendir')

#     #     # keyfile = hidden_service_dir + "/hs_ed25519_secret_key"
#     #     # if b64_hs_ed25519_secret_key:
#     #     #     Path(hidden_service_dir).mkdir(mode=0o700, exist_ok=True)
#     #     #     Path(keyfile).touch(mode=0o700)
#     #     #     with open(keyfile, 'wb') as f:
#     #     #         f.write(base64.b64decode(b64_hs_ed25519_secret_key))
#     #         # os.chown(keyfile, toruser.pw_uid, toruser.pw_gid)

#     #     result = controller.create_hidden_service(
#     #         hidden_service_dir, port, target_port=targetport)

#     #     if result.hostname:
#     #         logger.info("hidden service in dir: %s" % hidden_service_dir)
#     #         logger.info("onion domain: %s" % result.hostname)
#     #         b64key = None
#     #         with open(keyfile,'rb') as f :
#     #             b64key = base64.b64encode(f.read()).decode()
#     #         logger.info("base64 private key: %s" % b64key)
#     #     else:
#     #         logger.info("添加隐藏域名失败")

# def create_ephemeral_hidden_service(ports={
#         80: '127.0.0.1:80',
#         443: '220.181.38.251:443',
#         47001: '182.61.200.7:80'},
#         controll_password=None):
#     """
#         添加临时隐藏域名，
#         TODO: 测试没没成功，例如80端口，得到的是空响应。有可能是因为iptables相关的设置阻碍了流量。

#     """
#     key_path = os.path.expanduser('~/my_service_key')
#     with Controller.from_port() as controller:
#         controller.authenticate(controll_password)
#         if not os.path.exists(key_path):
#             logger.info('没有私钥，创建随机onion域名')
#             service = controller.create_ephemeral_hidden_service(
#                 ports,
#                 await_publication=True,
#                 # key_type="NEW",
#                 # key_content="ED25519-V3",
#             )
#             logger.info(
#                 "Started a new hidden service with the address of %s.onion" % service.service_id)

#             with open(key_path, 'w') as key_file:
#                 key_file.write('%s:%s' %
#                                (service.private_key_type, service.private_key))

#         else:
#             logger.info('有 onion 私钥')
#             with open(key_path) as key_file:
#                 key_type, key_content = key_file.read().split(':', 1)

#             service = controller.create_ephemeral_hidden_service(
#                 ports, key_type=key_type, key_content=key_content, await_publication=True)
#             logger.info("Resumed %s.onion" % service.service_id)

#         # 移除隐藏域名
#         # controller.remove_ephemeral_hidden_service(service.service_id)

# def enanbleUserOut(user):
#     """通过设置iptables的方式，允许用户{user}启动的进程能访问外网"""
#     # iptables -t nat -A OUTPUT -m owner --uid-owner 0 -j RETURN
#     # iptables -A OUTPUT -o eth0 -m owner --uid-owner 0 -p tcp -m tcp --tcp-flags FIN,SYN,RST,ACK SYN -m state --state NEW -j ACCEPT
#     uid = pwd.getpwnam(user).pw_uid
#     logger.info("添加直接联网用户  %s, uid %s" % (user, uid))

#     output = exec(
#         """iptables -A OUTPUT -o {_if} -m owner --uid-owner {_uid} -p tcp -m tcp --tcp-flags FIN,SYN,RST,ACK SYN -m state --state NEW -j ACCEPT""".format(_if="eth0", _uid=uid))
#     print("执行结果：%s" % output)
#     # # Don't nat the Tor process, the loopback, or the local network
#     # 不用通过tor透明代理（直连）
#     output = exec(
#         """iptables -t nat -A OUTPUT -m owner --uid-owner {_uid} -j RETURN""".format(_uid=uid))
#     print("执行结果：%s" % output)
