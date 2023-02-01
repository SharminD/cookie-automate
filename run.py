import os 
os.system('pip install selenium')
os.system('pip install webdriver_manager')
os.system('pip install time')
os.system('pip install beautifulsoup4')
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager as CM
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
with open('inputs.txt','r') as f :
    inputs=[item for item in f]
username = inputs[0]
password = inputs[1]
abilities = inputs[2].split(',')
prices = inputs[3]
ad_num_limit = int(inputs[4])
options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(executable_path=CM().install(),options=options)
driver.get('https://parscoders.com/login')
username_input = driver.find_element(By.NAME,'username')
username_input.send_keys(username)
password_input = driver.find_element(By.NAME,'password')
password_input.send_keys(password)
enter = driver.find_element(By.NAME,'_submit').click()
sleep(2)
projects = driver.find_element(By.LINK_TEXT,'مشاهده پروژه ها').click()
sleep(2)
abilities_find = driver.find_element(By.ID,'s2id_autogen3')
for ability in abilities:    
    abilities_find.send_keys(ability)
    sleep(0.5)
    abilities_find.send_keys(Keys.RETURN)
    sleep(0.5)
sleep(2)
ad_num = 0
page_link = 0
while ad_num!=ad_num_limit:
    page_link+=1
    if page_link!=1:
        driver.get(driver.current_url + f'/?page={page_link}')
    sleep(2)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    if page_link == 1:
        PriceList = soup.find('select',{'id':'project_filter_budget'}).find_all('option')
        money_search_bar = driver.find_element(By.ID,'s2id_autogen1')
        for option in PriceList:
            if str(option['value']) in prices:
                money_search_bar.send_keys(option.text.strip(' '))
                sleep(0.5)
                money_search_bar.send_keys(Keys.RETURN)
                sleep(0.5)
        sleep(2)
        SearchForJob = driver.find_element(By.CLASS_NAME,'col-sm-12').find_element(By.TAG_NAME,'button').click()
        sleep(2)
        soup = BeautifulSoup(driver.page_source,'html.parser')
    ads_list = soup.find('div',{'class','col-md-10 col-sm-12 col-xs-12'}).find_all('div')
    ads = []
    for div in ads_list:
        try:
            div['id']
            ads.append(div)
        except:
            None 
    for ad in ads:
        try :    
            title = ad.find('a',{'class','font-blue'}).text.strip()
        except:
            continue
        bio = ad.find('div',{'class','todo-tasklist-item-text'}).text.strip() 
        for span in ad.find_all('span'):
            try:
                if '0' in span.text.strip():
                    num = span.text.strip()
            except:
                None
        price = num
        link = 'https://parscoders.com' + ad.find('a',{'class','font-blue'})['href'] 
        ad_num+=1
        with open('reports.txt','a',encoding='utf-8') as f2:
            f2.write(f'({str(ad_num)})')
            f2.write(f'title : {title}\n')
            f2.write(f'bio : {bio}\n')
            f2.write(f'price : {price}\n')
            f2.write(f'link : {link}\n')
            f2.write('________________________________\n')
        if ad_num == ad_num_limit:
            break
driver.quit()