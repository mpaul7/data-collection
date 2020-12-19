from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import random
import subprocess
import os
import datetime
import time

sys_config = {'interface': 'enp0s20f0u1',
              'driver_path': '/usr/local/bin/chromedriver',
              'pcap_path': '/home/solana/5g/data/5G_data_September_2020/text_chat/messenger/pcaps/'
              }

msg_config = {'num_pcaps': 11,  # number of pcaps to collect
              'num_texts': 1000,  # number of text messages per pcap
              'inter_text_gap': 3,
              'sender_username': 'mnir@solananetworks.com',
              'sender_pwd': 'Paul7377',
              'receiver_account': 'https://www.facebook.com/messages/t/100685868602912'
              }


# Apply Filters
def applyfilters():
    subprocess.check_output(["sudo", "ethtool", "-K", sys_config['interface'], "tx", "off", "sg", "off", "tso", "off",
                         "gso", "off", "gro", "off", "lro", "off"])
    subprocess.check_output(["sudo", "ifconfig", sys_config['interface'], "-multicast"])


def getChromeDriver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.geolocation": 1,
        "profile.default_content_setting_values.notifications": 1
    })
    driver = webdriver.Chrome(sys_config['driver_path'], options=chrome_options)
    return driver


def getTextMessage():
    names = ["Ryan", "Alex", "Callum", "Ethan", "Sarah", "Chloe", "Lauren", "Richard", "Britney", "Sophia", "Ava", "Josh"]
    verbs = ["runs", "hits", "jumps", "barks", "drinks", "sleeps", "sits", "stands", "reads", "writes", "talks", "throws"]
    message = random.choice(names) + " " + random.choice(verbs)
    return message


def loginFacebookAccount():
    driver = getChromeDriver()
    driver.get(msg_config['receiver_account'])
    # Login to FB page
    driver.find_element_by_css_selector("#email").send_keys(msg_config['sender_username'])
    driver.find_element_by_css_selector("#pass").send_keys(msg_config['sender_pwd'])
    driver.find_element_by_id('loginbutton').click()
    driver.implicitly_wait(10)
    return driver


def startDataCapture(nth_pcap):
    now = datetime.datetime.now()
    pcap_name = 'facebook' + str(nth_pcap) + "_" + str(now.day) + "_" + str(now.month) + "_" + str(now.year) + '.pcap'
    pcap = os.path.join(sys_config['pcap_path'], pcap_name)
    subprocess.Popen(['sudo', 'tcpdump', 'ip and  not ether multicast and not ether broadcast',
                      '-i', sys_config['interface'],
                      '-vvv', '-s 0',
                      '-w', pcap],
                     stdout=subprocess.PIPE)


def sendText(nth_pcap=None, num_texts=None, sleep=None):
    startDataCapture(nth_pcap)
    facebook_page = loginFacebookAccount()
    for nth_text in range(num_texts):
        message = getTextMessage()
        element = facebook_page.switch_to.active_element
        try:
            element.send_keys(message)
        except:
            pass
        facebook_page.switch_to.active_element.send_keys(Keys.ENTER)
        print('Message Sent {}-{}'.format(nth_pcap, nth_text))
        time.sleep(sleep)
    os.system("sudo killall tcpdump")
    facebook_page.quit()


def main():
    for nth_pcap in range(10, msg_config['num_pcaps']):
        startime = time.time()
        sendText(nth_pcap=nth_pcap, num_texts=msg_config['num_texts'], sleep=msg_config['inter_text_gap'])
        print("Elapsed pcap time: {} - {}".format(nth_pcap, time.time() - startime))


if __name__ == "__main__":
    applyfilters()
    main()

