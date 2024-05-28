import requests
from xml.etree import ElementTree
import re
import json
import subprocess

def parse_rss(latest, source):
    r = requests.get(source)

    tree = ElementTree.fromstring(r.content)
    title = ""
    item = []
    updated_latest = latest
    for child in tree[0]:
        if child.tag == "title":
            title = child.text.replace("Mikan Project - ", "")
            print("title = " + title)

        if child.tag == "item":
            for info in child:
                if info.tag == "title":
                    #Change here to sort only requested output
                    mytitle = info.text
                    for filt in filter_string:
                        mytitle = mytitle.replace(filt, "")
                    numbers = re.findall(r'\d+', mytitle)
                    episode = -1
                    for number in numbers:
                        if int(number) < 50 and int(number) > 0:
                            episode = int(number)
                            #print(episode)
                    if episode <= latest:
                        break
                    updated_latest = max(updated_latest, episode)
                if info.tag == "enclosure":
                    #print(info.attrib['url'])
                    item.append(info.attrib['url'])
    return updated_latest, title, item

accepted_subgroup = [
    203, #桜都字幕组
#   615, #Kirara Fantasia
    382, #喵萌奶茶屋
    552, #Lilith-Raws
    583, #ANi

    ]
filter_string = [
    "MP4",
    "21°C",
    "mp4"
]

subscription_file = "~/scripts/subscribed.json"
email_addr=""
subFile = open(subscription_file, 'r')
subscribed = json.load(fp=subFile)
subFile.close()

auto_generated_magnet_set = ""
auto_generated_notify = "echo 'Subject: 你订阅的番剧有更新. \n\n以下番剧已更新: \n"

for bangumi_info in subscribed:
    for subgroupid in accepted_subgroup:
        result_latest,  result_title, result_item = parse_rss(bangumi_info[0], 'https://mikanani.me/RSS/Bangumi?bangumiId=' + str(bangumi_info[1]) + '&subgroupid='+str(subgroupid))
        bangumi_info[0] = result_latest
        if (len(result_item) > 0):
            for url in result_item:
                auto_generated_magnet_set += (url + "%" + result_title + "\n")
            auto_generated_notify += ("    - " + result_title + " 已更新至第 " + str(result_latest) + " 话 \n")
            break

if len(auto_generated_magnet_set) > 3:

    start_download_file = open("/home/laixuan/scripts/bangumi/auto_magnet_set", "w")
    start_download_file.write(auto_generated_magnet_set)
    start_download_file.close()

    subFile = open(subscription_file, 'w')
    json.dump(subscribed, fp=subFile, indent=4)
    subFile.close()
    if len(email_addr) > 0:
        subprocess.run(auto_generated_notify + "' | sendmail -v "+email_addr, shell=True)

