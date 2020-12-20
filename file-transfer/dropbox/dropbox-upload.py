import dropbox
import os
import subprocess

# shut down offload
dbx = dropbox.Dropbox('Z-XhybPdTJwAAAAAAAAAAZL94Qi9V2qGg38WpJHJPEzUbQMJe0i69TJ6sqXwemxL')
INTERFACE = 'enp0s20f0u1'
subprocess.check_output(
    ["sudo", "ethtool", "-K", INTERFACE, "tx", "off", "sg", "off", "tso", "off", "gso", "off", "gro", "off", "lro",
     "off"])
subprocess.check_output(["sudo", "ifconfig", INTERFACE, "-multicast"])

PCAP_PATH = '/home/solana/5g/data/5G_data_September_2020/file_transfer/dropbox/upload/pcaps/'

dbx.users_get_current_account()
files = [f for f in os.listdir(os.path.join('inputs/')) if os.path.isfile(os.path.join('inputs/', f))]
print(files)
ignore_files = []
for x in files:
    try:
        with open('inputs/' + x, "rb") as f:
            file_size = os.path.getsize('inputs/' + x)
            print(file_size)
            print(f)
            CHUNK_SIZE = 4 * 1024 * 1024
            PCAP_NAME = x.replace("_db.pcap", "") + '_db_uplink.pcap'
            p = subprocess.Popen(['sudo', 'tcpdump', 'ip and  not ether multicast',
                                  '-i', INTERFACE, '-vvv', '-s 0',
                                  '-w', PCAP_PATH + PCAP_NAME],
                                 stdout=subprocess.PIPE)
            if file_size <= CHUNK_SIZE:
                print(dbx.files_upload(f.read(), '/' + 'inputs/' + x, mute=True))
            else:
                upload_session_start_result = dbx.files_upload_session_start(f.read(CHUNK_SIZE))
                cursor = dropbox.files.UploadSessionCursor(session_id=upload_session_start_result.session_id,
                                                           offset=f.tell())
                commit = dropbox.files.CommitInfo(path='/' + 'inputs/' + x)
                while f.tell() < file_size:
                    if (file_size - f.tell()) <= CHUNK_SIZE:
                        print(dbx.files_upload_session_finish(f.read(CHUNK_SIZE), cursor, commit))
                    else:
                        dbx.files_upload_session_append(f.read(CHUNK_SIZE), cursor.session_id, cursor.offset)
                        cursor.offset = f.tell()
    except:
        ignore_files.append(x)
        pass
    print(' =============== uploaded', 'inputs/' + x)
    cmd = "sudo killall  tcpdump"
    print('================= ignore_files ================= :')
    for f in ignore_files:
        print(f)
    os.system(cmd)
