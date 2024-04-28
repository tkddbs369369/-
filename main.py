from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()


gallery_url = 'https://gall.dcinside.com/mgallery/board/lists/?id=hypergryph&page='
target_id = input("타겟 ID를 입력하세요: ")



for i in range(1,int(input('몇 페이지까지?'))): #찾을 페이지수

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
                print('ㅇㅇ')
                title_selector = f"#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr:nth-child({i}) > td.gall_tit.ub-word"
                title_a = table.find_element(By.CSS_SELECTOR, title_selector)
                title = title_a.text
                print(title)
    except:
        pass

driver.quit()