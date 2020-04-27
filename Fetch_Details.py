from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
from lxml import html


class LicenseDetails:

    def get_captcha(self):
        captcha = input("\nEnter Captcha: ")
        return captcha

    def run_sim(self):
        verification_error_id = "form_rcdl:j_idt13"
        alert_class = "ui-dialog-message ui-messages-warn-icon"

        driver = webdriver.Chrome(executable_path="chromedriver.exe")
        driver.maximize_window()
        wait = WebDriverWait(driver, 10)
        driver.get("https://parivahan.gov.in/rcdlstatus/?pur_cd=101")
        dl_no = input("Enter Driving License NUmber: ")
        dob = input("Enter DOB in DD-MM-YYYY format: ")
        # dl_no = "DL-0420110149646"
        # dob = "09-02-1976"
        dl_field = wait.until(ec.presence_of_element_located((By .ID, "form_rcdl:tf_dlNO")))
        dl_field.send_keys(dl_no)

        dob_field = driver.find_element_by_id("form_rcdl:tf_dob_input")
        dob_field.send_keys(dob)
        dob_field.send_keys(Keys.TAB)

        while 1:
            try:
                captcha_field = driver.find_element_by_id("form_rcdl:j_idt34:CaptchaID")
                captcha_field.click()
                captch = self.get_captcha()
                print("Got Captcha")
                captcha_field.clear()
                captcha_field.send_keys(captch)
                driver.find_element_by_id("form_rcdl:j_idt46").click()
                WebDriverWait(driver, 4).until(ec.presence_of_element_located((By .ID, "form_rcdl:j_idt118")))
                print("Correct Captcha")
                break

            except:
                print(sys.exc_info())
                if len(driver.find_elements_by_id(verification_error_id)):
                    print("Incorrect Captcha")

        print("Login Success")
        try:
            p = {}
            src = driver.page_source
            info_tree = html.fromstring(src)
            table_1 = info_tree.xpath(
                "//table[@class='table table-responsive table-striped table-condensed table-bordered']/tbody")[0]
            p["Status"] = table_1.xpath(".//tr[1]/td[2]/span/text()")[0]
            name = lambda x: x[0] + " " + x[-1]
            p["Holder's Name"] = name(table_1.xpath(".//tr[2]/td[2]/text()")[0].split(" "))
            p["Date Of Issue"] = table_1.xpath(".//tr[3]/td[2]/text()")[0]
            p["Last Transaction"] = table_1.xpath(".//tr[4]/td[2]/text()")[0]
            p["Old/New DL"] = table_1.xpath(".//tr[5]/td[2]/text()")[0]

            table_2 = info_tree.xpath("//table[@class='table table-responsive table-striped table-condensed table-bordered data-table']/tbody")[0]
            p["Non Transport Validity From"] = table_2.xpath(".//tr[1]/td[2]/text()")[0]
            p["Non Transport Validity To"] = table_2.xpath(".//tr[1]/td[3]/text()")[0]
            p["Transport Validity From"] = table_2.xpath(".//tr[2]/td[2]/text()")[0]
            p["Transport Validity To"] = table_2.xpath(".//tr[2]/td[3]/text()")[0]

            table_3 = info_tree.xpath(
                "(//table[@class='table table-responsive table-striped table-condensed table-bordered data-table']/tbody/tr)[3]")[0]
            p[table_3.xpath(".//td[1]/span/text()")[0]] = table_3.xpath(".//td[2]/text()")[0]
            p[table_3.xpath(".//td[3]/span/text()")[0]] = table_3.xpath(".//td[4]/text()")[0]


            p[info_tree.xpath("//span[@class='ui-column-title']/text()")[0]] = info_tree.xpath("//td[@role='gridcell']/text()")[0]
            p[info_tree.xpath("//span[@class='ui-column-title']/text()")[1]] = info_tree.xpath("//td[@role='gridcell']/text()")[1]
            p[info_tree.xpath("//span[@class='ui-column-title']/text()")[2]] = info_tree.xpath("//td[@role='gridcell']/text()")[2]
            return p

        except:
            print(sys.exc_info())
            print("Enter Correct Details")
        driver.quit()


if __name__ == '__main__':
    obj = LicenseDetails()
    params = obj.run_sim()
    print(params)
