from selenium import webdriver
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':

    #URL = 'https://confluence.globallogic.com/pages/viewpage.action?spaceKey=AC&title=Accelerators+Home'
    #URL = 'https://www.olx.ua/d/uk/nedvizhimost/zemlya/sofievskaya-borschagovka/'
    URL = 'https://time.is/'
    driver = webdriver.Chrome()
    driver.get(URL)
    with open("yyy.html", "w", encoding='utf-8') as f:
        f.write(driver.page_source)

    driver.close()
    i=0