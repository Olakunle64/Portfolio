#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# https://www.indeed.com/jobs?q=software+engineer+email&l=&vjk=d79c45952da2585c
# https://www.indeed.com/jobs?q=software+engineer+email&start=10&vjk=3c42553a23033564
driver = webdriver.Chrome()
for t in range(10, 20, 10):
    #driver.get(f'https://www.indeed.com/jobs?q=crop+production+email&l=United+States&start={t}&vjk=3a47f30d7740f3a7')
    driver.get(f'https://www.indeed.com/jobs?q=software+engineer+email&start={t}&vjk=3c42553a23033564')
    a =[1,2,3,4,5,7,8,9,10,11,13,14,15,16,17]
    # a = [i for i in range(1, 50)]
    for x in a:
        try:
            driver.find_element(By.XPATH, f"//li[@class='css-5lfssm eu4oa1w0'][{x}]/div/div/div/div/div/table/tbody/tr/td/div/h2/a").click()
            time.sleep(1)
            b = driver.find_element(By.XPATH, '//*[@id="jobDescriptionText"]').text
            with open ('links.txt', 'a') as c:
                c.write(f'{b}\n')
                # //*[@id="jobDescriptionText"]ss
            # //*[@id="jobDescriptionText"]/divjnununub

        except:
            pass
            
    print(f'page {t} done')
