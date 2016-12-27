RTM Special Conditions for MME
================================

This is a collection of RTM mornitering modules for MME special conditions(usually for issue).

- [Duplicated IMSI issue(dupimsi)](dupimsi/Readme.md)

  This module can find the duplicated IMSI info from the MMDU of MME and send the 
  duplicated IMSI number to Zabbix. if the number reach the threshold, then will 
  execute the commands (usually delete user commands) defined in configuration 
  file `baseconfig.py`

  See the [deployment guide](dupimsi/doc/deployment_guide.md) for more detail.
