# -*- coding: utf-8 -*-
from rtm.netaccount import AccountFile
from rtm.utils import BasePath
import logging

####################### Paths Definition ##########################
#RTM installation base directory
RtmBase = BasePath("/opt/RTM")
MyBase = RtmBase("specialconditions/mme/dupimsi")

#Network Element host account file
HostsFile = MyBase('hosts.yml')

#Zabbix Config file diectory
ZabbixConfigBase = BasePath("/etc/zabbix")

#Zabbix bin files diectory
ZabbixBinBase = BasePath("/usr/bin")

#Zabbix ExternalScripts directory
ZabbixExtBase = BasePath("/etc/zabbix/externalscripts")

#cache for log
CacheBase = BasePath("/tmp/cache")

############### config for purgeimsi.py #####################
class PurgeIMSIConfig():
    logging_level = logging.INFO
    logging_file = "/tmp/cache/purgeimsi.log"
    logfile_pattern = CacheBase('log/flexins_dupimsi_%s.log').fullpath
    delimsi_cmdfile_pattern = CacheBase('cmdfile/delimsi_%s.cmd').fullpath
    imsi_regex = "^\d+f\d"
    zbx_dupimsi_item_key = "dupimsi.counter"
    delimsi_freshold = 3
    delimsi_template = """\
ZMMD:IMSI=%(imsi)s:;
ZMMD:IMSI=%(imsi)s:;
"""
###################################################################
HostList = AccountFile(HostsFile.fullpath)
PathList = dict(
    RtmBase=RtmBase,
    MyBase=MyBase,
    HostsFile=HostsFile,
    ZabbixConfigBase=ZabbixConfigBase,
    ZabbixBinBase=ZabbixBinBase,
    ZabbixExtBase=ZabbixExtBase,
    CacheBase=CacheBase,
    )

def print_host_info(hostname):
    host = HostList.account(hostname, by_hostname=True)
    if host:
        print(host.ipaddr, host.username, host.decrypt_password(), host.hostname)
    else:
        print('None')

def print_path_info(name):
    print(PathList[name]())

if __name__ == "__main__":
    import sys

    print_info = {'host': print_host_info, 'path': print_path_info }
    infotype, name = sys.argv[1:]

    if infotype in ['host', 'path']:
        print_info[infotype](name)
