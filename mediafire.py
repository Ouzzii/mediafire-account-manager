from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import selenium
from requests import post, get
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs
import os
import sys
from time import sleep
from os import get_terminal_size
from sys import platform
from json import load, dump
from requests import get
ua = UserAgent()


for _os in ["linux", "windows", "macos"]:
    sys.path.append(os.path.join("/".join(__file__.split("/")[:-1]), f"driver-s/{_os}/"))
    
try:
    from tools import tools as t
    from Exceptions import *
except:
    from .tools import tools as t
    from .Exceptions import *



global accountsFilePath
global driverPath


if platform == "Win32":
    accountsFilePath = os.environ["HOMEDRIVE"] + os.environ["HOMEPATH"] + "\\accounts.json"
    driverPath = "./driver-s/windows/chromedriver"
elif platform == "linux":
    accountsFilePath = os.environ["HOME"] + "/accounts.json"
    driverPath = "./driver-s/linux/chromedriver"

class Mediafire:
    def __init__(self, headless=False):
        self.options = Options()
        self.options.add_argument("--headless" if headless else "pass")
        self.options.add_argument('log-level=3')
        self.options.add_argument('--disable-dev-shm-usage')
        self.chrome = webdriver.Chrome(options=self.options, service=Service(driverPath))
        self.headless = True if "--headless" in self.options.arguments else False
        self.chrome.set_window_position(0, 0)
        tools = t(self.chrome)

        if os.path.exists(accountsFilePath):
            with open(accountsFilePath, encoding="utf-8")as f:
                self.accountsFile = load(f)
        else:
            with open(accountsFilePath, "w")as f:
                f.write("{}")
                self.accountsFile = {}
        
        
        self.css_selector = tools.css_selector
        self.css_selector_all = tools.css_selector_all
        self.xpath = tools.xpath

        self.waitfor = tools.waitfor
        self.file_links = []

    def login(self, email, password):
        self.email = email
        self.password = password
        self.chrome.get("https://www.mediafire.com/login/")
        try:
            self.waitfor(self.css_selector, "input[type='email']", timeout=10).send_keys(email)
            self.waitfor(self.css_selector, "input[type='password']", timeout=10).send_keys(password)
            self.waitfor(self.css_selector, "button[type='submit']", timeout=10).click()
        except:
            TimeoutError

        while True:
            if self.chrome.current_url == "https://app.mediafire.com/myfiles":
                break
            else:
                self.chrome.get("https://app.mediafire.com/myfiles")
        print("Login to", self.email)
        
        self.accountsFile[self.email] = {
            "password": self.password
        }
        self.write_to_local(self.accountsFile)
        
        self.closepopup()
    def upload(self, directory, file):
        path = os.path.join(directory, file)
        target = ""
        
        while True:
            try:
                self.waitfor(self.css_selector, "button[aria-label='Upload files']", timeout=3).click()
                self.waitfor(self.css_selector, "div[data-text-as-pseudo-element='Select Files to Upload']", timeout=3)
                break
            except:
                self.relogin()
        self.waitfor(self.css_selector, "input[type='file']").send_keys(path)
        

        if self.headless:
            xpath = '/html/body/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div/div/div/div/div[4]/div/div'
            
        else:
            xpath = '/html/body/div[1]/div/div[1]/div[3]/div/div/div/div[2]/div/div[1]/div/div/div/div/div[4]/div/div'
        while True:
            try:

                status = self.waitfor(self.xpath, xpath, timeout=3, silent=True).get_attribute("data-text-as-pseudo-element")
                print(path, status, end=f"{(get_terminal_size()[0]-(len(path)+len(status)+2))*' '}\r")
                if status == "Queued":
                    try:
                        self.waitfor(self.css_selector, "button[title='Begin upload']", timeout=1, silent=True).click()
                    except TimeoutError:
                        pass
                elif status == "Conflict":
                    raise Conflict
                elif status == "Completed":
                    return "Completed"
                    raise Completed
                elif status == "Not enough storage":
                    raise NotEnoughStorage
                elif status == "Upload worker failed":
                    raise Failed
            except TimeoutError:
                pass
    def relogin(self):
        self.login(self.email, self.password)
    
    def get_content(self, passlist=[]):

        folder_dict = {
            "": "",
            "myfiles": "myfiles"
        }


        pathes_as_key = ["/myfiles/"]
        pathes = ["/myfiles/"]
        scanable = ["myfiles"]
        scanned = []


        while True:
            try: #scan folders
                base_folder = scanable[0]
                
                del scanable[0]
                scanned.append(base_folder)
                
                folders = self.get_session_file_info(base_folder, "folders")
                
                for _ in folders:
                    if not _ == []:
                        folder_dict[_['folderkey']] = _['name']
                        
                        pathes.append(f"/{folder_dict[base_folder]}/{_['name']}/")
                        pathes_as_key.append(f"/{base_folder}/{_['folderkey']}/")
                        
                        if not _['folderkey'] in scanned and not _['folderkey'] in scanable:
                            scanable.append(_['folderkey'])
                    else:
                        raise IndexError
            except IndexError: #merge when all folders scanned
                break

        n_pathes = []
        n_pathes_as_key = []
        n_files = []
        n_files_as_key = []
        for i in pathes_as_key:
            for z in pathes_as_key:
                if i.split("/")[-2] == z.split("/")[1]:
                    n_pak = "/".join(i.split("/")[:-2] + z.split("/")[1:])
                    n_p = "/".join([folder_dict[a] for a in i.split("/")[:-2] + z.split("/")[1:]])
                    n_pathes_as_key.append(n_pak)
                    n_pathes.append(n_p)

        ret = []

        #get file infos
        for _ in n_pathes_as_key:

            for file in self.get_session_file_info(_.split("/")[-2], "files"):
                
                print(file)
                n_files.append(n_pathes[n_pathes_as_key.index(_)]+file["filename"])
                
                
                ret.append({
                    "filename": file["filename"],
                    "filekey": file["quickkey"],
                    "filehash": file["hash"],
                    "path": n_pathes[n_pathes_as_key.index(_)],
                    "path_as_key": _,
                    "filetype": file["filetype"],
                    "mimetype": file["mimetype"],
                    "size_as_byte": int(file["size"]),
                    "size_as_mb": int(file["size"])/1024/1024,
                    "link": file["links"]["normal_download"],
                    "downloads": file["downloads"],
                    "views": file["views"],
                    "privacy": file["privacy"],
                    "created_at": file["created"]
                })
                
        self.accountsFile[self.email]["files"] = []
        self.accountsFile[self.email]["files"].extend(ret)
        self.accountsFile[self.email]["folders"] = n_pathes
        self.write_to_local(self.accountsFile)
        return ret


    def get_account_storage(self):
        response = post("https://www.mediafire.com/api/1.5/user/get_info.php",
                        headers={"User-Agent": ua.random},
                        cookies={c['name']:c['value'] for c in self.chrome.get_cookies()},
                        data={"session_token": self.get_session_token(),
                              "response_format": "json"}).json()["response"]["user_info"]
        self.accountsFile[self.email]["storage"] = {}
        self.accountsFile[self.email]["storage"]["total"] = int(response["storage_limit"])
        self.accountsFile[self.email]["storage"]["used"] = int(response["used_storage_size"])
        self.accountsFile[self.email]["storage"]["space"] = int(response["storage_limit"])-int(response["used_storage_size"])
        self.write_to_local(self.accountsFile)
        return {"total": int(response["storage_limit"]), "used": int(response["used_storage_size"]), "empty": int(response["storage_limit"])-int(response["used_storage_size"])}
    

    def closepopup(self):
        self.chrome.execute_script("""
            setInterval(function(){
                var fpopup = document.querySelector("body > div > div > div:nth-child(2) > div > div > button")
                var spopup = document.querySelector("body > div > div > div:nth-child(2) > div > div > div > div > div:nth-child(3) > button:nth-child(3)")
                var upgrade_storage_reminder = document.querySelector('div#storage_upsell_remind button.storage_upsell_close')
                var welcome_to = document.querySelector('button[title="Close welcome dialog"]')
                var special_one_time = document.querySelector("button[title='Close dialog']")

                if (fpopup != null){
                    fpopup.click()
                }
                if (spopup != null){
                    spopup.click()
                }
                if (upgrade_storage_reminder != null){
                    upgrade_storage_reminder.click()
                }
                if (welcome_to != null){
                    welcome_to.click()
                }
                if (special_one_time != null){
                    special_one_time.click()
                }
                console.log("Merhaba")
            }, 250)
        """)


    def close(self):
        self.chrome.close()

    def get_session_token(self):
        while True:
            r = post("https://www.mediafire.com/application/get_session_token.php", cookies={c['name']:c['value'] for c in self.chrome.get_cookies()}, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Whale/3.24.223.18 Safari/537.36"})
            if "error" in list(r.json()["response"].keys()):
                self.relogin()
                sleep(3)
            else:
                self.session_token = r.json()["response"]["session_token"]
                return self.session_token

    def get_source_url(self, url):
        try:
            return bs(get(url, cookies={c['name']:c['value'] for c in self.chrome.get_cookies()}, headers={"User-Agent": ua.random}).text, "html.parser").find("a", {"aria-label": "Download file"})["href"]
        except:
            return None
        
        
    def get_session_file_info(self, folderkey, content_type):
        data = {"session_token": self.get_session_token(),
                "response_format": "json",
                "content_type": content_type,
                "folder_key": folderkey
                }



        response = post("https://www.mediafire.com/api/1.5/folder/get_content.php",
                        data=data,
                        cookies={c['name']:c['value'] for c in self.chrome.get_cookies()},)
        return response.json()["response"]["folder_content"][content_type]
    
    def download(self, file, target_directory = None, save_as = None, silent=False):
            
        
        
        if "/" in file:
            url = file
        elif "." in file:
            allfiles = [eleman for alt_liste in [[b for b in self.accountsFile[a]["files"]] for a in self.accountsFile] for eleman in alt_liste]
            if file not in [a["filename"] for a in allfiles]:
                raise FileNotFound
            else:
                url = [a for a in allfiles if a["filename"] == file][0]["link"]
        else:
            url = f"https://www.mediafire.com/file/{file}/"

        download_url = self.get_source_url(url)
        
        target_directory = "./" if target_directory == None else target_directory
        filename = save_as if save_as != None else bs(get(url).text, "html.parser").find("div", {"class": "filename"}).text
        
        response = get(self.get_source_url(url), stream=True)
        filesize = 0
        totalfilzesize = int(response.headers.get('Content-Length'))
        
        with open(os.path.join(target_directory, filename), "wb")as f:
            for chunk in response.iter_content(chunk_size=128):
                if chunk:
                    f.write(chunk)
                    if not silent:
                        filesize+=len(chunk)
                        percent = self.percentof(totalfilzesize, filesize, 100, None)
                        note = f"{filename} {percent}% "
                        terminalsize = os.get_terminal_size()[0] - len(note)
                        downloaded_size = self.percentof(terminalsize, None, 100, percent)
                        not_downlaoded_size = terminalsize - downloaded_size
                        print(f"{note}{downloaded_size*'█'}{not_downlaoded_size*'▞'}", end="\r")
    
    def write_to_local(self, dict):
        with open(accountsFilePath, "w", encoding="utf-8")as f:
            dump(dict, f, indent=2, ensure_ascii=False)


    def percentof(self, totalsize, size):
        print(int(size*100/totalsize))
        
    def percentof(self, total_length=None, length=None, max_ratio=None, ratio=None):
        if total_length == None:
            return int(max_ratio*length/ratio)
        elif length == None:
            return int(total_length*ratio/max_ratio)
        elif max_ratio == None:
            return int(total_length*ratio/length)
        elif ratio == None:
            return int(max_ratio*length/total_length)
    
        
#100
#321312
#256
#x