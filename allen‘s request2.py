import pandas as pd
from bs4 import BeautifulSoup
import hashlib
import requests
from datetime import datetime
import os

# 查找可能包含更新时间的标签
def find_potential_update_time(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 查找<meta>标签中可能包含更新时间的信息
    meta_time = soup.find('meta', {'name': 'last-modified'})
    if meta_time:
        print(f"Meta last-modified: {meta_time.get('content')}")

    # 查找<time>标签中可能包含更新时间的信息
    time_tags = soup.find_all('time')
    for time_tag in time_tags:
        print(f"Time tag: {time_tag.get_text(strip=True)}")

    # 查找<div>和<span>标签中可能包含更新时间的信息
    div_tags = soup.find_all('div')
    for div in div_tags:
        if 'update' in div.get_text().lower():
            print(f"Div with update text: {div.get_text(strip=True)}")

    span_tags = soup.find_all('span')
    for span in span_tags:
        if 'update' in span.get_text().lower():
            print(f"Span with update text: {span.get_text(strip=True)}")

# 获取网页内容哈希值
def get_content_hash(url):
    """获取网页内容的哈希值"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content = response.content
            return hashlib.md5(content).hexdigest()  # 返回内容的MD5哈希值
        else:
            print(f"Failed to access {url}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error accessing {url}: {e}")
        return None

# 读取之前的哈希值
def read_previous_hashes(filename):
    """Reads previous hashes from a file and returns a dictionary."""
    try:
        with open(filename, "r") as file:
            return {line.split()[0]: line.split()[1] for line in file}
    except FileNotFoundError:
        return {}

# 写入当前哈希值到文件
def write_hashes(filename, hashes):
    """Writes the current hash dictionary to a file."""
    with open(filename, "w") as file:
        for url, hash_value in hashes.items():
            file.write(f"{url} {hash_value}\n")

# 主函数
def main():
    """Main function to check updates on websites and handle file operations."""
    urls = [
        'https://afghanistan.un.org/en/stories',
        'https://albania.un.org/en/stories',
        'https://algeria.un.org/fr/stories',
        'https://angola.un.org/pt/stories',
        'https://argentina.un.org/es/stories',
        'https://armenia.un.org/en/stories',
        'https://azerbaijan.un.org/en/stories',
        'https://bahrain.un.org/en/stories',
        'https://bangladesh.un.org/en/stories',
        'https://belarus.un.org/en/stories',
        'https://belize.un.org/en/stories',
        'https://benin.un.org/fr/stories',
        'https://bhutan.un.org/en/stories',
        'https://bolivia.un.org/es/stories',
        'https://bosniaherzegovina.un.org/en/stories',
        'https://botswana.un.org/en/stories',
        'https://brasil.un.org/pt-br/stories',
        'https://burkinafaso.un.org/fr/stories',
        'https://burundi.un.org/fr/stories',
        'https://caboverde.un.org/pt/stories',
        'https://cambodia.un.org/en/stories',
        'https://cameroon.un.org/fr/stories',
        'https://caribbean.un.org/en/stories',
        'https://republiquecentrafricaine.un.org/fr/stories',
        'https://chad.un.org/fr/stories',
        'https://chile.un.org/es/stories',
        'https://china.un.org/en/stories',
        'https://colombia.un.org/es/stories',
        'https://comoros.un.org/fr/stories',
        'https://congo.un.org/fr/stories',
        'https://costarica.un.org/es/stories',
        'https://cotedivoire.un.org/fr/stories',
        'https://cuba.un.org/es/stories',
        'https://djibouti.un.org/fr/stories',
        'https://dominicanrepublic.un.org/es/stories',
        'https://dprk.un.org/en/stories',
        'https://drcongo.un.org/fr/stories',
        'https://easterncaribbean.un.org/en/stories',
        'https://ecuador.un.org/es/stories',
        'https://egypt.un.org/en/stories',
        'https://elsalvador.un.org/es/stories',
        'https://eritrea.un.org/en/stories',
        'https://eswatini.un.org/en/stories',
        'https://ethiopia.un.org/en/stories',
        'https://gabon.un.org/fr/stories',
        'https://gambia.un.org/en/stories',
        'https://georgia.un.org/en/stories',
        'https://ghana.un.org/en/stories',
        'https://guatemala.un.org/es/stories',
        'https://guinee.un.org/fr/stories',
        'https://guineabissau.un.org/pt/stories',
        'https://guineaecuatorial.un.org/es/stories',
        'https://guyana.un.org/en/stories',
        'https://haiti.un.org/fr/stories',
        'https://honduras.un.org/es/stories',
        'https://india.un.org/en/stories',
        'https://indonesia.un.org/en/stories',
        'https://iran.un.org/en/stories',
        'https://iraq.un.org/en/stories',
        'https://jamaica.un.org/en/stories',
        'https://jordan.un.org/en/stories',
        'https://kazakhstan.un.org/en/stories',
        'https://kenya.un.org/en/stories',
        'https://kosovoteam.un.org/en/stories',
        'https://kuwait.un.org/en/stories',
        'https://kyrgyzstan.un.org/en/stories',
        'https://laopdr.un.org/en/stories',
        'https://lebanon.un.org/en/stories',
        'https://lesotho.un.org/en/stories',
        'https://liberia.un.org/en/stories',
        'https://libya.un.org/en/stories',
        'https://madagascar.un.org/fr/stories',
        'https://malawi.un.org/en/stories',
        'https://malaysia.un.org/en/stories',
        'https://maldives.un.org/en/stories',
        'https://mali.un.org/fr/stories',
        'https://mauritania.un.org/fr/stories',
        'https://mauritius.un.org/en/stories',
        'https://mexico.un.org/es/stories',
        'https://micronesia.un.org/en/stories',
        'https://moldova.un.org/en/stories',
        'https://mongolia.un.org/en/stories',
        'https://montenegro.un.org/en/stories',
        'https://morocco.un.org/fr/stories',
        'https://mozambique.un.org/pt/stories',
        'https://myanmar.un.org/en/stories',
        'https://namibia.un.org/en/stories',
        'https://nepal.un.org/en/stories',
        'https://niger.un.org/fr/stories',
        'https://nigeria.un.org/en/stories',
        'https://northmacedonia.un.org/en/stories',
        'https://pacific.un.org/en/stories',
        'https://pakistan.un.org/en/stories',
        'https://palestine.un.org/en/stories',
        'https://panama.un.org/es/stories',
        'https://papuanewguinea.un.org/en/stories',
        'https://paraguay.un.org/es/stories',
        'https://peru.un.org/es/stories',
        'https://philippines.un.org/en/stories',
        'https://rwanda.un.org/en/stories',
        'https://samoa.un.org/en/stories',
        'https://unsdg.un.org/latest?f%5B0%5D=content_type_latest_page%3Astory&f%5B1%5D=content_type_latest_page%3Ablog_post',
        'https://saudiarabia.un.org/en/stories',
        'https://senegal.un.org/fr/stories',
        'https://serbia.un.org/en/stories',
        'https://seychelles.un.org/en/stories',
        'https://sierraleone.un.org/en/stories',
        'https://somalia.un.org/en/stories',
        'https://southafrica.un.org/en/stories',
        'https://southsudan.un.org/en/stories',
        'https://srilanka.un.org/en/stories',
        'https://sudan.un.org/en/stories',
        'https://suriname.un.org/en/stories',
        'https://syria.un.org/en/stories',
        'https://tajikistan.un.org/en/stories',
        'https://tanzania.un.org/en/stories',
        'https://thailand.un.org/en/stories',
        'https://timorleste.un.org/en/stories',
        'https://togo.un.org/fr/stories',
        'https://trinidadandtobago.un.org/en/stories',
        'https://tunisia.un.org/fr/stories',
        'https://turkiye.un.org/en/stories',
        'https://turkmenistan.un.org/en/stories',
        'https://uganda.un.org/en/stories',
        'https://ukraine.un.org/en/stories',
        'https://unitedarabemirates.un.org/en/stories',
        'https://uruguay.un.org/es/stories',
        'https://uzbekistan.un.org/en/stories',
        'https://venezuela.un.org/es/stories',
        'https://vietnam.un.org/en/stories',
        'https://yemen.un.org/en/stories',
        'https://zambia.un.org/en/stories',
        'https://zimbabwe.un.org/en/stories'
    ]


    filename = "hashes.txt"
    previous_hash = read_previous_hashes(filename)
    update_records = []
    first_run = not os.path.exists(filename)  # 判断是否是第一次运行
    current_hashes = {}

    for url in urls:
        current_hash = get_content_hash(url)
        if current_hash:
            if url in previous_hash and previous_hash[url] != current_hash:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                actual_update_time = find_potential_update_time(url)  # 获取实际更新时间
                if actual_update_time:
                    print(f"Web page {url} has been updated at {actual_update_time}.")
                    update_records.append({'URL': url, 'Update Time': actual_update_time})
                else:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"Web page {url} has been updated. Last update time: {current_time}")
                    update_records.append({'URL': url, 'Update Time': current_time})
            elif url not in previous_hash:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"First-time check or new page {url}, storing hash.")
                current_hashes[url] = current_hash

    write_hashes(filename, current_hashes)

    # 将更新记录导出到 Excel 文件
    if update_records:
        df = pd.DataFrame(update_records)
        df.to_excel('website_updates.xlsx', index=False)  # 保存到 Excel 文件
        print("Updates exported to Excel.")
    else:
        print("No updates found.")

if __name__ == "__main__":
    main()