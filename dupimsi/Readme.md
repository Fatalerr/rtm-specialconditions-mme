Readme
======================

This is a mornitering module of RTM for the issue which MME having duplicated IMSI. 
this module can find the duplicated IMSI info from the MMDU of MME and send the 
duplicated IMSI number to Zabbix. if the number reach the threshold, then will execute
the commands (usually delete user commands) defined in configuration file `baseconfig.py`  

See the [deployment guide](doc/deployment_guide.md) for more detail.