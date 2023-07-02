from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import re
import threading
import json

name = ""

id = ""
password = ""

driver = ""
element = ""
elements2 = ""
elements3 = ""

#아래 코드수정으로 명령어 추가, 제거
def question():
    global name
    if element.text == name + "안녕":
        makeComments(driver, "안녕하세요!")
    if element.text == name + "닉네임":
        makeComments(driver, elements2[0].text.split('\n')[0] + "님 안녕하세요!")
    if element.text == name + "프사":
        makeComments(driver, elements2[0].text.split('\n')[0] + "님의 프사는 https://playentry.org/" + extract_first_url(elements3[1].get_attribute("style")) + " 입니다!")
    if element.text == name + "인사":
        makeComments(driver, "반갑습니다! 무슨 도움이 필요하세요?")
    if element.text.startswith(name + "계산 "):
        expression = element.text[len(name + "계산:"):].strip()
        if "**" in expression:
            makeComments(driver, "과부하 방지를 위해제곱 연산(**)은 사용할 수 없습니다.")
        else:
            try:
                result = safe_eval(expression)
                makeComments(driver, f"계산 결과: {expression} = {result}")
            except:
                makeComments(driver, "계산식을 올바르게 입력해주세요. 예) 2 + 3 * 4")
    if element.text.startswith(name + " 타이머 "):
        timer_duration = element.text[len(name + " 타이머 "):].strip()
        try:
            timer_duration = int(timer_duration)
            makeComments(driver, f"{timer_duration}초 타이머를 시작할게요!")
            time.sleep(timer_duration)
            makeComments(driver, f"{timer_duration}초가 지났습니다!")
        except:
            makeComments(driver, "올바른 시간 값을 입력해 주세요. 예) 뤼튼 타이머 5")
    if element.text == name + "좋아요 눌러줘":
        makeLike(driver)
        makeComments(driver, "댓글에 좋아요를 눌렀습니다!")

    # 봇 호출 반응
    #if "봇" in element.text:
    #    makeComments(0, driver, "누구인가 누가 내이름을 불렀는가👂")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_first_url(text: str) -> str:
    pattern = r'url\("([^"]+)"\)'
    urls = re.findall(pattern, text)

    if len(urls) > 0:

        return urls[0]

    return ""

def safe_eval(expression):

    allowed_chars = re.compile(r'^[-+*/\d\s()]*$')
    
    if allowed_chars.match(expression):
        try:
            result = eval(expression)
            return result
        except:
            return "계산식을 올바르게 입력해주세요. 예) 2 + 3 * 4"
    else:
        return "알 수 없는 문자가 포함되어 있습니다. 숫자와 허용된 연산자만 사용해 주세요."

#만약 글을 쓰고 싶으면 아래 함수를 쓰세요.
def makeCommunity(driver, content):
    textarea_element = driver.find_element(By.ID, "Write")
    textarea_element[0].clear()
    textarea_element[0].send_keys(content)
    a_elements = driver.find_elements(By.CSS_SELECTOR, ".css-10xvtsb.e1h77j9v8")
    a_elements[0].click()

def makeComments(driver, content):
    reply_elements = driver.find_elements(By.CSS_SELECTOR, "a.reply")
    reply_elements[0].click()

    textarea_element = driver.find_elements(By.ID, "Write")
    textarea_element[1].clear()
    textarea_element[1].send_keys(content)
    a_elements = driver.find_elements(By.CSS_SELECTOR, ".css-10xvtsb.e1h77j9v8")
    a_elements[1].click()
    print("ㄴ " + content)
    reply_elements = driver.find_elements(By.CSS_SELECTOR, "a.reply")
    reply_elements[0].click()

def makeLike(driver):
    like_elements = driver.find_elements(By.CSS_SELECTOR, "a.like")
    like_elements[0].click()

running = False

@app.get("/")
def main():
    global running

    if not running:
        running = True
        thread = threading.Thread(target=main_func)
        thread.start()
        return "봇 동작중..."

    else:
        return "이미 봇이 동작중입니다."

def main_func():
    global id
    global password
    global driver
    global element
    global elements2
    global elements3

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    
    print("로그인중...")
    driver.get("https://playentry.org/signin")
    
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys(id)
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)

    login_button = driver.find_element(By.CSS_SELECTOR, ".css-1cooiky.e13821ld0")
    login_button.click()
    
    time.sleep(2)
    
    print("로그인 완료!")
    
    driver.get("https://playentry.org/community/entrystory/list?sort=created&term=all")

    last = "3asef!@#"

    while True:
        try:
            driver.refresh()
    
            elements = driver.find_elements(By.CSS_SELECTOR, ".css-sy8ihv")
            elements2 = driver.find_elements(By.CSS_SELECTOR, ".css-1t19ptn")
            elements3 = driver.find_elements(By.CSS_SELECTOR, ".css-18bdrlk")

            if True:
                element = elements[0]
                if not last == elements2[0].text + " + " + elements[0].text + " + " + elements3[0].text:
                    print("")
                    print(element.text + "\n" + elements2[0].text)
                    question()
                last = elements2[0].text + " + " + elements[0].text + " + " + elements3[0].text
            time.sleep(0.2)
        except Exception as e:
            print(f"에러가 발생했습니다: {str(e)}")
    driver.quit()
    pass

def BOT_RUN(name2, id2, password2, question2):
    global name
    global id
    global password
    global question

    question = question2

    name = name2
    id = id2
    password = password2

    uvicorn.run(app, host="0.0.0.0", port=8000)#, host="0.0.0.0"