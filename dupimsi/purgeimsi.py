#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
#HELP: purgeimsi.py
Check the log file ends with ne name, find the duplicated IMSI number and send
to Zabbix server, then generate the delimsi_hostname.cmd file. if option 'go'
is used execute the command file.

Usage:
    purgeimsi.py <ne_name> [go]

请使用前修改basicconfig.py配置文件以适应你的系统环境

"""
import re, sys
import logging
from collections import defaultdict
from baseconfig import PurgeIMSIConfig as conf
from baseconfig import MyBase, ZabbixBinBase, HostList
from rtm.zbxsender import ZabbixSender
from rtm.utils import execute_external_command

DEFAULT_FILENAME = {'logfile': 'mme%s.log', 'dupimsi': 'dup%s.txt'}
DEFAULT_PATHS = {'logfile': 'tmp/', 'dupimsi': 'tmp/'}

DELETE_IMSI_COMMAND = MyBase("delete_imsi").fullpath

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(filename)s[%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',)

rootlog = logging.getLogger()
log = logging.getLogger('purgeimsi')


def counter(datalist):
    """A Counter used for python version below 2.7
    """
    _counter = defaultdict(int)
    for data in datalist:
        _counter[data] += 1

    return _counter


def find_dupimsi_from_log(imsi_pat, logfile):
    """return the duplicated imsi list.
    """
    _allimsi = []
    with open(logfile) as logfp:
        for line in logfp:
            _matched = imsi_pat.match(line)
            if _matched:
                _allimsi.append(_matched.group())
    log.debug("found IMSI in log: %s", len(_allimsi))

    imsi_counter = counter(_allimsi)
    dupimsi = [imsi for imsi, n in imsi_counter.items() if n > 1]
    log.debug("found duplicated IMSI: %s", len(dupimsi))

    return dupimsi


def get_imsi(line):
    """get the correct 15 digits IMSI from the raw IMSI string:
    example:
      input 'line':
        64009778311904f1
      return:
        460079871391401
    """
    couple_chars = re.findall(r'.{2}', line)
    return ''.join([c[::-1] for c in couple_chars])[:-1]


def save_delete_imsi_cmds(imsilist, filename, template):
    """Save the commands list to command file.
    """
    cmds = [template % dict(imsi=get_imsi(s)) for s in imsilist]
    with open(filename, 'w') as fp:
        fp.write(''.join(cmds))

    return cmds


def execute_delimsi_script(host):
    """execute the delete IMSI script. the command file will be determinated by hostname
    """
    cmdstr = "%s %s" % (DELETE_IMSI_COMMAND, host.hostname)

    log.info("Running: %s", cmdstr)
    status, output = execute_external_command(cmdstr)
    log.info("Delete IMSI execution status:%s", status)


if __name__ == "__main__":
    #start the program
    go_delete = False

    if len(sys.argv) < 2:
        print("Usage: python purgeimsi.py <hostname> [go]")
        exit(1)

    if len(sys.argv) == 3 and sys.argv[2] == 'go':
        go_delete = True

    host = HostList.account(sys.argv[1], by_hostname=True)
    if not host:
        log.error("Can't find the host named:%s", sys.argv[1])
        exit(1)

    if conf.logging_level:
        rootlog.setLevel(conf.logging_level)
        log.debug("set log level to:%s", conf.logging_level)

    log.debug(conf.__dict__)

    logfile = conf.logfile_pattern % host.hostname
    output_file = conf.delimsi_cmdfile_pattern % host.hostname
    log.debug("logfile:%s, output file:%s", logfile, output_file)

    # parse the log and find the duplicated IMSI
    dupimsi = find_dupimsi_from_log(re.compile(conf.imsi_regex), logfile)
    dupimsi_num = len(dupimsi)

    zbxsender = ZabbixSender(
        sender_location=ZabbixBinBase('zabbix_sender').fullpath)
    zbxsender.send(host.hostname, conf.zbx_dupimsi_item_key, dupimsi_num)

    if dupimsi_num > conf.delimsi_freshold:
        cmdlist = save_delete_imsi_cmds(
            dupimsi, output_file, conf.delimsi_template)
        if go_delete:
            execute_delimsi_script(host)

### End ###
