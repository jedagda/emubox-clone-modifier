import os
import xml.etree.ElementTree as ET
import virtualbox
from virtualbox.library import NetworkAttachmentType

"""
### Script by Joshua Dagda
### Commissioned by Dr. Jaime Acosta
### Last modification: 02/20/19
### Description: Script modifies the network adapter settings of VirtualBox vm clones created by Emubox using pyvbox 
### which is a complete implementation of the VirtualBox Main API for python.
### External Library used: pyvbox 1.1.0 by Michael Dorman
"""

# Emubox's filepath for Debian-based Linux ditros
workshop_configs_path = "/root/emubox/workshop-creator/bin/workshop_creator_gui_resources/workshop_configs/"
print "These are the workshops that are available: \n\n"

# Lists the workshop names and appends a file_num key
dirs = os.listdir(workshop_configs_path)
file_list = {}
file_num = 0
for file_name in dirs:
    if file_name.endswith(".xml"):
        file_num += 1
        file_list[file_num] = file_name
if file_num < 1:
    print "There are no workshops created yet"
    exit()
for x in file_list:
    print x, file_list[x]

# Requests the user to select an existing workshop and parse the selected xml file
try:
    num = int(raw_input("Select the number associated to the workshop that you wish to modify\n\n"))
except ValueError:
    print "Err... integers only"
else:
    full_file = os.path.abspath(os.path.join(workshop_configs_path, file_list[num]))

# Parses through workshop xml file and stores it in dom
dom = ET.parse(full_file)

# Finds the name of the workshop
base_group_name = dom.find('testbed-setup/vm-set/base-groupname').text
print "Base Group Name: " + base_group_name

# Finds all the virtual machines available in the workshop xml file and stores a key and a value in a dictionary
vms = dom.findall('testbed-setup/vm-set/vm')
vm_list = {}
vm_num = 0
for x in vms:
    vm_num += 1
    vm_name = x.find('name').text
    vm_list[vm_num] = vm_name
    print vm_num, vm_list[vm_num]

# Prompts the user to select a virtual machine
vm_num_select = int(raw_input("Select the number associated to the virtual machine that you wish to modify\n\n"))
vm_select = vm_list[vm_num_select]

# Number of clones created of the workshop
num_clones = dom.find('testbed-setup/vm-set/num-clones').text
print "Number of Clones: " + num_clones

# IP address related to the workshop
ip_address = dom.find('testbed-setup/network-config/ip-address').text
print "Ip-Address: " + ip_address

# Base output name of the workshop which is then turned into the starting host id
base_output_name = dom.find('testbed-setup/vm-set/base-outname').text
print "Base output name: " + base_output_name
host_id = int(base_output_name) - 1

# VRDP Baseport -- nothing is done with this, yet
vrdp_base_port = dom.find('testbed-setup/vm-set/vrdp-baseport').text
print "VRDP Base Port: " + vrdp_base_port

# Opens an instance of virtual box, finds the machine that is to be modified, creates a session of the virtual machine.
# Loops through the group of virtual machine clones that is selected by the user.
# The script prompts the user which network adapter they wish to modify.
# Script then gets the network adapter selected by the user, changes the network attachment to Generic Driver.
# Changes the name of the Generic Driver to UDPTunnel.
# Sets the appropriate properties of the virtual machine
# Saves the settings, and unlocks the machine.
vbox = virtualbox.VirtualBox()
adapter_num = -1
x = 0
while x < int(num_clones):
    x += 1
    last_digit = str(x)
    vm = vbox.find_machine(vm_select+base_output_name+last_digit)
    session = vm.create_session()
    if adapter_num < 0:
        adapter_num = int(raw_input("Select the adapter number you wish to modify, enter a number between 1 - 8\n\n"))
        adapter_num -= 1
    net_adapter = session.machine.get_network_adapter(adapter_num)
    net_adapter.attachment_type = NetworkAttachmentType.generic
    net_adapter.generic_driver = 'UDPTunnel'
    net_adapter.set_property('sport', str(host_id+x))
    net_adapter.set_property('dport', str(host_id + x))
    net_adapter.set_property('dest', '192.168.1.'+str(host_id + x))
    session.machine.save_settings()
    session.unlock_machine()

exit()









