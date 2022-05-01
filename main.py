from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import codecs
import csv
from unidecode import unidecode

driver = webdriver.Chrome(ChromeDriverManager().install())
def signin():
    url = "https://www.linkedin.com/login"
    driver.get(url)
    email = driver.find_element(By.ID, ("username"))
    password = driver.find_element(By.ID, ("password"))
    login = driver.find_element(By.CLASS_NAME, ("login__form_action_container"))
    email.clear()
    password.clear()
    authenticate = open("Authentication.txt")
    credential = authenticate.readlines()
    myemail = credential[0]
    mypassword = credential[1]
    email.send_keys(myemail)
    password.send_keys(mypassword)
    login.submit()
signin()
sleep(1)
input("Please Hit ENTER...")
sleep(1)

name = []
position = []
location = []
getlinklist = []
filteredname = []
filteredposition = []
filteredlocation = []
filteredgetlinklist = []
jobtitlesen = []
searchmore = []
pgs = 6
num_of_people = 10

class home():

    def searchmorelink(self, t):
        self.t = t
        search_ = driver.find_element(By.XPATH, '//*[@id="global-nav-typeahead"]/input')
        openfile = open("Resized_data.txt", encoding="utf-8")
        tkeyword = openfile.readlines()
        self.keyword = tkeyword[self.t].lower().strip()
        self.unikeyword = unidecode(self.keyword.strip())
        search_.send_keys(self.keyword)
        driver.maximize_window()
        search_.send_keys(Keys.RETURN)
        sleep(3)
        try:
           driver.execute_script("document.getElementsByClassName('artdeco-pill artdeco-pill--slate artdeco-pill--choice artdeco-pill--2 search-reusables__filter-pill-button search-reusables__filter-pill-button')[0].click();")
        except Exception:
            driver.execute_script("document.getElementsByClassName('artdeco-pill artdeco-pill--slate artdeco-pill--choice artdeco-pill--2 search-reusables__filter-pill-button search-reusables__filter-pill-button')[1].click();")
        sleep(2)
    def page(self):
        sleep(1)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        # Collect profile data
        body = soup.find("body")
        main = body.find("main", {"id": "main"})
        for divclass in main.find_all("span", {"class": "entity-result__title-text t-16"}):
            try:
                y = divclass.find_all("span", {"dir": "ltr"})[0].text.strip()
                for xx in divclass.find_all("span", {"dir": "ltr"}):
                    try:
                        getnames = xx.find_all("span")[0].text.strip()
                        name.append(getnames)
                    except Exception:
                        pass
            except Exception:
                name.append("Linkedin member")
            try:
                a = divclass.find("a", href=True)
                if a.text:
                    getlinklist.append(a['href'])
            except Exception:
                pass

        for main in body.find_all("main", {"id": "main"}):
            for i in range(0, num_of_people):
                try:
                    getposition = main.find_all("div", {"class": "entity-result__primary-subtitle t-14 t-black t-normal"})[i].text.strip()
                    position.append(getposition)
                except AttributeError:
                    pass
                try:
                    getlocation = main.find_all("div", {"class": "entity-result__secondary-subtitle t-14 t-normal"})[i].text.strip()
                    location.append(getlocation)
                except AttributeError:
                    pass
        sleep(3)

    def printdata(self, w, x, y, z):
        sleep(1)
        for t in range(0, len(w)):
            try:
                print(w[t], x[t], y[t], z[t])
                lowered = x[t].lower()
                unilowered_ = unidecode(lowered)
                if ((unilowered_.find(self.unikeyword) != -1) and (w[t] != "Linkedin member")):
                    with codecs.open("Job_titles.txt", 'r', encoding='utf-8') as job:
                        readl = job.readlines()
                        for kk in range(len(readl)):
                            jobtfr = readl[kk].lower().strip()
                            jobten = unidecode(jobtfr).lower().strip()
                            _unilowered_ = unidecode(lowered)
                            if ((_unilowered_.find(jobten) != -1)):
                                filteredname.append(w[t]), filteredposition.append(x[t]), filteredlocation.append(y[t]), filteredgetlinklist.append(z[t])
                            else:
                                pass
                else:
                    pass
            except IndexError:
                pass
x = home()
def scrolldown():
    for pagesx in range(0, 10):
        driver.find_element(By.XPATH, '//*[@id="global-nav-typeahead"]/input').clear()
        x.searchmorelink(pagesx)
        sleep(1)
        for pagesy in range(1, pgs):
            try:
                x.page()
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                next_button = driver.find_element(By.CLASS_NAME, "artdeco-pagination__button--next")
                next_button.click()
            except Exception:
                pass
        x.printdata(name, position, location, getlinklist)



scrolldown()
print("#______________________________________________________________..._____________________________________________________________________#")
with codecs.open(r"C:\Users\adema\Downloads\LinkedIn_list.csv", 'w', encoding='utf-8') as f:
    for p in range(0, len(filteredname)):
        try:
            print(p + 1, filteredname[p], filteredposition[p], filteredlocation[p], filteredgetlinklist[p])
            wr = csv.writer(f)
            wr.writerow([filteredname[p], filteredposition[p], filteredlocation[p], filteredgetlinklist[p]])
        except Exception:
            pass
print("#______________________________________________________________..._____________________________________________________________________#")

name.clear()
position.clear()
location.clear()
getlinklist.clear()
filteredname.clear()
filteredposition.clear()
filteredlocation.clear()
filteredgetlinklist.clear()
jobtitlesen.clear()
sleep(100)

