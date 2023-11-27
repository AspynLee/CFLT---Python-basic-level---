import os
import pandas as pd # pandas 에는 read_html이 있어서, 현재 페이지 데이터 넣어주면 데이터 식별해서 데이터 가져오는 작업을 쉽게 할 수 있다.
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.maximize_window() # 창 최대화

# 1. 페이지 이동
url = 'https://finance.naver.com/sise/sise_market_sum.naver?&page='
browser.get(url)

# 2. 조회 항목 초기화(체크되어 있는 항목 체크 해제)
checkboxes = browser.find_elements(By.NAME, 'fieldIds')
for checkbox in checkboxes:
    if checkbox.is_selected(): #체크된 상태라면?
        checkbox.click() #클릭 (체크 해제)

# 3. 조회 항목 설정 (원하는 항목)
# items_to_select = ['영업이익', '자산총계', '매출액'] # [items_to_select] 으로 정의된 리스트를, 원하는걸로 바꿀 수 있음
items_to_select = ['시가', '고가', '저가']
for checkbox in checkboxes: # 체크박스를 돌면서, 체크박스 기준으로 -> 부모 tag로 갔다가, 다시 부모 밑에 있는 label을 찾아서 -> 그 label의 해당하는 이름을 찾아서, 그 이름이 [items_to_select] 리스트 안에 내용에 포함된다고 하면은,   
    parent = checkbox.find_element(By.XPATH, '..') # 부모 elemnet
    label = parent.find_element(By.TAG_NAME, 'label') # parent = td, 즉 td라는 elemnet 속에 있는, label이라는 tag 이름을 가진 element를 찾아서, label에 반환함
    # print(label.text) # 목록 이름 확인용
    if label.text in items_to_select: # 드롭박스 선택 항목과 일치한다면
        checkbox.click() # 체크, 그때 체크 박스 클릭 해줌. 

# 4. 적용하기 버튼 클릭
btn_apply = browser.find_element(By.XPATH, '//a[@href="javascript:fieldSubmit()"]') # // 슬래시 2개는 전체 html문서에서 찾겠다가 라는 의미.a tag
btn_apply.click()

for idx in range(1, 40): #1이상 40미만 페이지 반복
    # 사전 작업: 페이지 이동
    browser.get(url + str(idx)) #http://naver.com....&page=2

    # 5. 데이터 추출
    df = pd.read_html(browser.page_source)[1] # data frame 구성됨, NaN = Not A Number, 결측치
    df.dropna(axis='index', how='all', inplace=True) # row 기준, 줄 기준으로 삭제, all - 줄 전체가 비어 있을경우 삭제해라. any = 하나라도 결측치가 있으면 지워라
    df.dropna(axis='columns', how='all', inplace=True)
    if len(df) == 0: # 더 이상 가져올 데이터가 없으면? 반복문 탈출한다. 데이터 프레임에 검색되는 데이터가 없음.
        break

    # 6. 파일 저장 (1page만 header 있고, 나머지는 헤더 미포함.)
    f_name = 'sise.csv'
    if os.path.exists(f_name):#파일이 있다면? 헤더부분은 제외, os모듈
        df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=False) #csv 메소드 호출, 인코딩 호출, 한글 깨짐, mode='a' 는 append, 앞에 헤더 데이터에 뒤에 데이터 추가로 붙임.
    else: #파일이 없다면? 헤더 포함
        df.to_csv(f_name, encoding='utf-8-sig', index=False)
    print(f'{idx} 페이지 완료')

browser.quit() #브라우저 종료



# # 5. 데이터 추출
# df = pd.read_html(browser.page_source)[1] # data frame 구성됨, NaN = Not A Number, 결측치
# df.dropna(axis='index', how='all', inplace=True) # row 기준, 줄 기준으로 삭제, all - 줄 전체가 비어 있을경우 삭제해라. any = 하나라도 결측치가 있으면 지워라
# df.dropna(axis='columns', how='all', inplace=True)

# # 6. 파일 저장 (1page만 header 있고, 나머지는 헤더 미포함.)
# f_name = 'sise.csv'
# if os.path.exists(f_name):#파일이 있다면? 헤더부분은 제외, os모듈
#     df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=False) #csv 메소드 호출, 인코딩 호출, 한글 깨짐, mode='a' 는 append, 앞에 헤더 데이터에 뒤에 데이터 추가로 붙임.
# else: #파일이 없다면? 헤더 포함
#     df.to_csv(f_name, encoding='utf-8-sig', index=False)


# print(f'{idx} 페이지 완료')