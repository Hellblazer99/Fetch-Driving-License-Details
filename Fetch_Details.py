from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys


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
            values = {
                'Current_Status': '//*[@id="form_rcdl:j_idt118"]/table[1]/tbody/tr[1]/td[2]/span',
                'Holder Name': '//*[@id="form_rcdl:j_idt118"]/table[1]/tbody/tr[2]/td[2]',
                "Date of Issue": '//*[@id="form_rcdl:j_idt118"]/table[1]/tbody/tr[3]/td[2]',
                "Last Transaction at ": '//*[@id="form_rcdl:j_idt118"]/table[1]/tbody/tr[4]/td[2]',
                "DL No.": '//*[@id="form_rcdl:j_idt118"]/table[1]/tbody/tr[5]/td[2]',
                "Non Transport": '//*[@id="form_rcdl:j_idt118"]/table[2]/tbody/tr[1]/td[1]',
                "Valid From": '//*[@id="form_rcdl:j_idt118"]/table[2]/tbody/tr[1]/td[2]',
                "Valid To": '//*[@id="form_rcdl:j_idt118"]/table[2]/tbody/tr[1]/td[3]',
                "COV Category": '//*[@id="form_rcdl:j_idt167_data"]/tr/td[1]',
                "Class Of Vehicle": '//*[@id="form_rcdl:j_idt167_data"]/tr/td[2]',
                "COV Issue Date": '//*[@id="form_rcdl:j_idt167_data"]/tr/td[3]'}

            for key in values:
                values[key] = driver.find_element_by_xpath(values[key]).text

            values["Valid From"] = values["Valid From"].split(":")[1]
            values["Valid To"] = values["Valid To"].split(":")[1]
            return values

        except:
            print(sys.exc_info())
            print("Enter Correct Details")
        driver.quit()


if __name__ == '__main__':
    obj = LicenseDetails()
    params = obj.run_sim()
    print(params)
