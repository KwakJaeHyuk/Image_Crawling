from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
from PIL import Image

#! 검색어 입력
search = "military texture image"

options1 = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options1)

driver.get('https://www.google.co.kr/')

driver.maximize_window()

elem = driver.find_element(By.NAME, "q") # 검색창 찾기
elem.send_keys(search)

# enter
elem.send_keys(Keys.RETURN)

try:
    img_ = driver.find_element(By.XPATH, '//*[@id="hdtb-msb"]/div[1]/div/div[2]/a')
except:
    img_ = driver.find_element(By.XPATH, '//*[@id="cnt"]/div[5]/div/div/div/div[1]/div/a[1]')
# time.sleep(60)
# //*[@id="cnt"]/div[5]/div/div/div/div[1]/div/a[1]
# print(img_)
# if ((driver.find_element(By.XPATH, '//*[@id="hdtb-msb"]/div[1]/div/div[2]/a')) == False):
#     img_ = driver.find_element(By.XPATH, '//*[@id="cnt"]/div[5]/div/div/div/div[1]/div/a[1]')
# else:
#     img_ = driver.find_element(By.XPATH, '//*[@id="hdtb-msb"]/div[1]/div/div[2]/a')

driver.execute_script("arguments[0].click();", img_)
SCROLL_PAUSE_TIME = 1

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        try:
            driver.find_element(By.CSS_SELECTOR, ".mye4qd").click()
        except:
            break
    last_height = new_height

imgs = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd") #작게 뜬 이미지들 모두 선택(elements)

count = 0
for img in imgs:

    driver.execute_script("arguments[0].click();", img)
    time.sleep(2)
    try:
        imgUrl = driver.find_element(By.XPATH,
            '/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]').get_attribute(
            "src")
    except: 
        continue
    
    driver.execute_script("window.open('" + imgUrl + "');")
    time.sleep(2)
    print(len(driver.window_handles))
    if len(driver.window_handles) == 1:
        continue
    
    driver.switch_to.window(driver.window_handles[1])
    
    try:
        new_imgUrl = driver.find_element(By.XPATH, '/html/body/img').get_attribute("src")
    except:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        continue
    path = 'C:\\Users\\MSI\\Desktop\\crawling\\data\\'
    
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    
    urllib.request.urlretrieve(new_imgUrl, path + str(count) + ".jpg")
    image = Image.open('data/' + str(count) + '.jpg')
    image = image.resize((800, 800))
    
    image = image.convert("RGB")
    
    #! 저장 위치
    final_path = 'final_dataset/'
    image.save(final_path + 'resize_800x800_' + str(count) + '.jpg')
    count = count + 1
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    
    #! 다운 받을 이미지 갯수 조정
    if count > 200: 
        break
    
    print('saved_' + str(count) + '_img')

time.sleep(30)

