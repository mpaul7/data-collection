import datetime
import dropbox
import os
import subprocess

sys_config = {'interface': 'enp0s20f0u1',
              'driver_path': '/usr/local/bin/chromedriver',
              'pcap_path': '/home/solana/5g/data/5G_data_September_2020/file_transfer/dropbox/upload/pcaps/'
              }

dropbox_config = {'access_token': 'Z-XhybPdTJwAAAAAAAAAAZL94Qi9V2qGg38WpJHJPEzUbQMJe0i69TJ6sqXwemxL',
                  'download_files_path': r"C:\Users\Owner\Desktop\downloads\_",
                  'dropbox_download_path': '/inputs/'
                  }


# Apply Filters
def applyfilters():
    subprocess.check_output(["sudo", "ethtool", "-K", sys_config['interface'], "tx", "off", "sg", "off", "tso", "off",
                         "gso", "off", "gro", "off", "lro", "off"])
    subprocess.check_output(["sudo", "ifconfig", sys_config['interface'], "-multicast"])


def listFiles(path=None):
    files = []
    for p, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(p, file))
    return files


def startDataCapture(file):
    now = datetime.datetime.now()
    pcap_name = file.replace(".pcap", "") + '_db_uplink.pcap'
    pcap = os.path.join(sys_config['pcap_path'], pcap_name)
    subprocess.Popen(['sudo', 'tcpdump', 'ip and  not ether multicast and not ether broadcast',
                      '-i', sys_config['interface'],
                      '-vvv', '-s 0',
                      '-w', pcap],
                     stdout=subprocess.PIPE)


def main():
    dbx = dropbox.Dropbox(dropbox_config['access_token'])
    response = dbx.files_list_folder(dropbox_config['dropbox_download_path'])
    # print(list(response.entries))
    total_files = len(list(response.entries))
    ignore_files = []
    file_num = 1
    print("Total {} files, starting download...".format(total_files))
    for file in response.entries:
	    # startDataCapture(file)
        file_name = file.name
        with open(dropbox_config['download_files_path'] + file_name, "wb") as f:
            metadata, res = dbx.files_download(path=dropbox_config['dropbox_download_path'] + file_name)
            f.write(res.content)
        print('==== downloaded: {}-{}: {}'.format(total_files, file_num, file_name))
        file_num += 1
        # os.system("sudo killall  tcpdump")


if __name__ == "__main__":
    # applyfilters()
    main()