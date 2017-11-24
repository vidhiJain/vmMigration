#Assumptions
#Password less login has been already setup with the hosts

from __future__ import print_function
import sys
import libvirt

#uri - qemu+ssh://uname@ipaddr/system

user_name = "user_name"
ip_address = "ip_addr"
name = "name"
protocol = "qemu+ssh://"

#========================Setup Connection=============================

host_list = [{user_name : "FDUSER", ip_address : "172.18.16.69", name : "node2"}
,{user_name : "FDUSER", ip_address : "172.18.16.13", name : "node3"}]

conn_dict = {}
active_hosts = []

for host in host_list:
	uri = protocol+host[user_name]+"@"+host[ip_address]+"/system"
	conn = libvirt.open(uri)
	if conn == None:
		print("Failed to open for %s "%(host))
	else:
		conn_dict[host[name]] = conn
		active_hosts.append(host[name])

for name in active_hosts:
	print(conn_dict[name])


#==================Get Stats for all domains at a host=================

def printHostInfo(host_name):
	memoryStats = conn_dict[host_name].getMemoryStats(libvirt.VIR_NODE_MEMORY_STATS_ALL_CELLS)
	cpuStats = conn_dict[host_name].getCPUStats(libvirt.VIR_NODE_CPU_STATS_ALL_CPUS)
	print("For %s : memoryStats = %s, cpuStats=%s"%(host_name,memoryStats,cpuStats))

def getStats(host_name):
	conn = conn_dict.get(host_name)
	if conn == None:
		print("unable to get stats for %s"%(node_name))
		return
	domainIds = conn.listDomainsID()
	printHostInfo(host_name)
	print("Domains : %s"%(domainIds))




#===========================Main=======================================
#Run a separate for getting getStats for each host

for host_name in active_hosts:
	print(getStats(host_name))


#=========================Close the program============================


for name in active_hosts:
	conn_dict[name].close()
