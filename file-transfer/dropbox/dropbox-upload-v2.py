import datetime
import dropbox
import os
import subprocess

sys_config = {'interface': 'enp0s20f0u1',
              'driver_path': '/usr/local/bin/chromedriver',
              'pcap_path': '/home/solana/5g/data/5G_data_September_2020/file_transfer/dropbox/upload/pcaps/'
              }

dropbox_config = {'access_token': 'Z-XhybPdTJwAAAAAAAAAAZL94Qi9V2qGg38WpJHJPEzUbQMJe0i69TJ6sqXwemxL',
                  'input_files_path': r"C:\Users\Owner\mltat\data\mltat\Dataset\Solana-5G\web\chrome\features",
                  'upload_path': '/inputs/'
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
    files = listFiles(path=dropbox_config['input_files_path'])
    ignore_files = []
    file_num = 1
    for file in files:
        # startDataCapture(file)
        try:
            upload_path = dropbox_config['upload_path'] + os.path.basename(file)
            with open(file, 'rb') as f:
                dbx.files_upload(f.read(), upload_path, mute=True)
        except:
            ignore_files.append(file)
            pass
        print(' ==== uploaded {}-{}: {}'.format(len(files), file_num, os.path.basename(file)))
        file_num += 1
        # os.system("sudo killall  tcpdump")
    print('========= ignored_files =========== :')
    for f in ignore_files:
        print(f)


if __name__ == "__main__":
    # applyfilters()
    main()