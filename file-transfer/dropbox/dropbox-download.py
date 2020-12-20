import dropbox
import os
import subprocess

# shut down offload
INTERFACE = 'enp0s20f0u1'
subprocess.check_output(["sudo", "ethtool", "-K", INTERFACE, "tx", "off", "sg", "off", "tso", "off", "gso", "off", "gro", "off","lro", "off" ])
subprocess.check_output(["sudo", "ifconfig",  INTERFACE, "-multicast" ])
access_token = 'Z-XhybPdTJwAAAAAAAAAAZL94Qi9V2qGg38WpJHJPEzUbQMJe0i69TJ6sqXwemxL'
dbx = dropbox.Dropbox(access_token)
response = dbx.files_list_folder("/inputs/")
# print("Number of files is : ".format(len(list(response.entries))))
for file in response.entries:
    print(file.name)
    x = file.name
    PCAP_PATH = '/home/solana/5g/data/5G_data_September_2020/file_transfer/dropbox/download/pcaps/' \
                + x.replace("_db.pcap", "") \
                + '_db_downlink.pcap'
    p = subprocess.Popen(['sudo', 'tcpdump', 'ip and  not ether multicast',
                          '-i', INTERFACE, '-vvv', '-s 0',
                          '-w', PCAP_PATH],
                         stdout=subprocess.PIPE)
    with open('download/' + x, "wb") as f:
        metadata, res = dbx.files_download(path="/inputs/" + x)
        f.write(res.content)
    print('============= downloaded :', x)
    cmd = "sudo killall  tcpdump"
    os.system(cmd)

