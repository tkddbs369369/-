from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


# 크롤링 옵션 생성
options = Options()
# 백그라운드 실행 옵션 추가
options.add_argument("headless")
driver = webdriver.Chrome(options= options)


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

driver.get(gallery_url)

target_id = input("2. 타겟 ID를 입력하세요: ")


#찾을 페이지수
pages_num = int(input("3. 몇 페이지까지 탐색할까요 : "))
print(" ")

for i in range(1,pages_num): 

    try:

        driver.get(gallery_url+str(i))


        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.gall_list")))


        table = driver.find_element(By.CSS_SELECTOR, "table.gall_list")


        for i in range(1, 53):
            writer_td_selector = f"#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr:nth-child({i}) > td.gall_writer.ub-writer"
            writer_td = table.find_element(By.CSS_SELECTOR, writer_td_selector)
            writer_id = writer_td.get_attribute("data-uid")
            if writer_id == target_id:
                title_selector = f"#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr:nth-child({i}) > td.gall_tit.ub-word"
                title_a = table.find_element(By.CSS_SELECTOR, title_selector)
                title = title_a.text
                print(title)
    except:
        pass

driver.quit()