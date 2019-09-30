from selenium import webdriver
from selenium.common.exceptions import *
import platform
from bs4 import BeautifulSoup
import math
import time

class KobisCrawler():
    def __init__(self):
        # self.agrs = ['load', 'save', 'maxpages']
        self.user_operating_system = str(platform.system())
        print('user_operating_system: ', self.user_operating_system)
        self.wd_path = './webdriver/' + self.user_operating_system + '/chromedriver'
        self.data_path = './kobis/'
        self.browser = webdriver.Chrome(self.wd_path)
        self.defaultURL = "http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieList.do"

    def get_total(self):
        tmp = self.browser.find_element_by_xpath('//*[@class="total"]/em').text.replace(',','')
        return (tmp, math.ceil(int(tmp)/10))

    def get_movie_codes(self):
        return [i.text for i in self.browser.find_elements_by_xpath('//*[@class="tac"]/span')]
    def save(self, fileName, data):
        with open(self.data_path + str(fileName) + ".json", 'a', encoding="utf-8") as f:
            f.write('\n'.join(str(d) for d in data))
    def get(self, Year):
        sYear, eYear = Year
        self.browser.get(self.defaultURL)

        e1 = self.browser.find_element_by_id("sPrdtYearS")
        e2 = self.browser.find_element_by_id("sPrdtYearE")
        e2.send_keys(eYear)
        e1.send_keys(sYear)
        self.browser.find_element_by_xpath('//*[@class="wrap_btn"]/button[1]').click()
        time.sleep(2)#5)

        #총 몇 건이 있고, 몇 페이지인지 확인
        total, num_pages = self.get_total()
        print('총', total, '건', num_pages, '페이지')

        movies_gen, movies_art, movies_ind, movies_art_ind = [], [], [], []
        for p in range(1, num_pages+1):
            print(p, '페이지 시작')
            #페이지 번호 클릭
            self.browser.execute_script("goPage('" +str(p)+"')")
            time.sleep(1)#3)

            #해당 페이지에 있는 영화 코드 리스트
            code_list = self.get_movie_codes()
            print(code_list)

            #해당 코드 상세 페이지
            for code in code_list:
                self.browser.execute_script("mstView('movie','"+str(code)+"');return false;")
                time.sleep(1)#3)
                soup = BeautifulSoup(self.browser.page_source, 'html.parser')
                html_1 = str(soup.find_all(class_='ovf cont')[0]).split('요약정보')[1].split('</dd>')[0]
                if '일반영화' in html_1: movies_gen.append(code)
                if '예술' in html_1: movies_art.append(code)
                if '독립' in html_1: movies_ind.append(code)
                if '예술' in html_1 and '독립' in html_1: movies_art_ind.append(code)
                time.sleep(0.5)#1)
                self.browser.find_element_by_xpath('//*[@class="close back"]').click()
                time.sleep(1)#3)

            # if p == 2:
            #     break
            #
            # if p%10 == 2:
            #     self.save('gen/' + str(sYear), movies_gen)
            #     self.save('art/' + str(sYear), movies_art)
            #     self.save('ind/' + str(sYear), movies_ind)
            #     self.save('art_ind/' + str(sYear), movies_art_ind)
            #     movies_gen, movies_art, movies_ind, movies_art_ind = [], [], [], []

        self.save('gen_' + str(sYear), movies_gen)
        self.save('art_' + str(sYear), movies_art)
        self.save('ind_' + str(sYear), movies_ind)
        self.save('art_ind_' + str(sYear), movies_art_ind)

crawler = KobisCrawler()
for yyyy in range(2000, 2019):
    y = (yyyy, yyyy) # 제작년도 2000년~2000년
    crawler.get(y)