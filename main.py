from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import threading

# 크롤링 옵션 생성
options = Options()
# 백그라운드 실행 옵션 추가
#options.add_argument("headless")

import galleryIdChecker

# 갤러리 id 입력 및 체크
while True:
    gall_id = input("1. 갤러리 id를 입력해주세요 : ")

    (mg, gall_name) = galleryIdChecker.gall_check(True, gall_id)
    if gall_name != "망갤":
        print(f"{gall_name}에서 검색합니다.")
        break
    else:
        print("id를 잘못 입력한 것 같습니다.")

gallery_url = f"https://gall.dcinside.com/mgallery/board/lists/?id={gall_id}&page="

target_id = input("2. 타겟 ID를 입력하세요: ")

while True:
    # 찾을 페이지수
    pages_num = int(input("3. 몇 페이지까지 탐색할까요 : "))
    print(" ")

    num_threads = int(input("4. 병렬처리 설정 추천=1 : "))
    pages_per_thread = pages_num // num_threads

    if pages_num%num_threads ==0:
        break
    else:
        print('Error! 페이지수는 병렬처리수로 나누어져야 합니다. ')

global pages
pages = 0
import csv
csv_file = open(f'{gall_name}_{target_id}.csv', 'w', newline='', encoding='utf-8-sig')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['제목', '날짜', 'URL'])
def search_pages(start_page, end_page):
    driver = webdriver.Chrome(options=options)

    for page in range(start_page, end_page + 1):
        global pages
        try:
            driver.get(gallery_url + str(page))

            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.gall_list")))

            table = driver.find_element(By.CSS_SELECTOR, "table.gall_list")
            pages += 1
            for i in range(1, 53):
                writer_td_selector = f"#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr:nth-child({i}) > td.gall_writer.ub-writer"
                writer_td = table.find_element(By.CSS_SELECTOR, writer_td_selector)
                writer_id = writer_td.get_attribute("data-uid")
                if writer_id == target_id:
                    title_selector = f"#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr:nth-child({i}) > td.gall_tit.ub-word > a"
                    date_selector = f"#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr:nth-child({i}) > td.gall_date"
                    title_a = table.find_element(By.CSS_SELECTOR, title_selector)
                    title = title_a.text
                    url = title_a.get_attribute("href")
                    date = table.find_element(By.CSS_SELECTOR, date_selector).text
                    print(title, date, url)
                    csv_writer.writerow([title, date, url])
        except:
            pass

    driver.quit()

threads = []
for i in range(num_threads):
    start_page = i * pages_per_thread + 1
    end_page = (i + 1) * pages_per_thread
    if i == num_threads - 1:
        end_page = pages_num
    thread = threading.Thread(target=search_pages, args=(start_page, end_page))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print(f'{pages} 페이지를 탐색함')
csv_file.close()