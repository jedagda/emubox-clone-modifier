import os
import xml.etree.ElementTree as ET
import virtualbox

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

dom = ET.parse(full_file)

base_group_name = dom.find('testbed-setup/vm-set/base-groupname').text
print "Base Group Name: " + base_group_name

vms = dom.findall('testbed-setup/vm-set/vm')

vm_list = {}
vm_num = 0

for x in vms:
    vm_num += 1
    vm_name = x.find('name').text
    vm_list[vm_num] = vm_name
    print vm_num, vm_list[vm_num]

vm_num_select = int(raw_input("Select the number associated to the virtual machine that you wish to modify\n\n"))
vm_select = vm_list[vm_num_select]

num_clones = dom.find('testbed-setup/vm-set/num-clones').text
print "Number of Clones: " + num_clones

ip_address = dom.find('testbed-setup/network-config/ip-address').text
print "Ip-Address: " + ip_address

base_output_name = dom.find('testbed-setup/vm-set/base-outname').text
print "Base output name: " + base_output_name

vrdp_base_port = dom.find('testbed-setup/vm-set/vrdp-baseport').text
print "VRDP Base Port: " + vrdp_base_port

vbox = virtualbox.VirtualBox()
x = 0
while x < int(num_clones):
    x += 1
    last_digit = str(x)
    vm = vbox.find_machine(vm_select+base_output_name+last_digit)
    print vm.name







