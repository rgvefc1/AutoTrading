import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.maximize_window() # 창 최대화

#1. 페이지 이동
url = 'https://finance.naver.com/sise/sise_market_sum.naver?&page='
browser.get(url)

# 2. 조회 항목 초기화 (체크되어있는 항목 초기화)
checkboxes = browser.find_elements(By.NAME,'fieldIds')
for checkbox in checkboxes:
    if checkbox.is_selected(): #체크된 상태라면?
        checkbox.click()    #클릭(체크 해제)

# 3. 조회 항목 설정 (원하는 항목)
# 최대 6개까지 설정 가능
items_to_select = ['시가','고가','저가','PER','ROE']
for checkbox in checkboxes:
    parent = checkbox.find_element(By.XPATH, '..') # 부모 ELEMENT 찾기
    label = parent.find_element(By.TAG_NAME,'label')
    
    if label.text in items_to_select:   #선택항목과 일치 한다면
        checkbox.click()    #선택

#4. 적용하기 버튼 클릭
btn_apply = browser.find_element(By.XPATH,'//a[@href="javascript:fieldSubmit()"]')
btn_apply.click()

for idx in range(1,40):  #1~40 미만 페이지 반복
    #사전작업 :페이지 이동
    browser.get(url + str(idx))

    #5. 데이터 추출
    df = pd.read_html(browser.page_source)[1] 
    df.dropna(axis='index' ,how='all', inplace=True)
    df.dropna(axis='columns' ,how='all', inplace=True)
    if len(df) == 0: #더이상 가져올 데이터가 없으면면
        break
    #6. 파일저장
    f_name = 'sise.csv'
    if os.path.exists(f_name):  # 파일이 있다면? 헤더 제외
        df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=False)
    else: # 파일이 없으면 헤더 포함
        df.to_csv(f_name, encoding='utf-8-sig')
    print(f'{idx} 페이지 완료')
browser.quit() # 브라우저 종료