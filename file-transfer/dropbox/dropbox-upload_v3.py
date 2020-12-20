import dropbox
import os
import subprocess

class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        dbx = dropbox.Dropbox(self.access_token)
        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to, mute=True)


def listFiles(path=None):
    files = []
    for p, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(p, file))
    return files


def applyfilters():
    subprocess.check_output(["sudo", "ethtool", "-K", sys_config['interface'], "tx", "off", "sg", "off", "tso", "off",
                         "gso", "off", "gro", "off", "lro", "off"])
    subprocess.check_output(["sudo", "ifconfig", sys_config['interface'], "-multicast"])


def main():
    applyfilters()
    access_token = 'Z-XhybPdTJwAAAAAAAAAAZL94Qi9V2qGg38WpJHJPEzUbQMJe0i69TJ6sqXwemxL'
    transderData = TransferData(access_token)
    input_files_path =r"C:\Users\Owner\mltat\data\mltat\Dataset\Solana-5G\p2p\bittorrent\features"
    files_to = '/inputs/p2p-1-29-09-2020_feature2.csv'
    files = listFiles(path=input_files_path)
    for file in files:
        file_to_dropbox = '/inputs/' + os.path.basename(file)
        dbx = dropbox.Dropbox(access_token)
        with open(file, 'rb') as f:
            dbx.files_upload(f.read(), file_to_dropbox, mute=True)



if __name__ == '__main__':
    main()
