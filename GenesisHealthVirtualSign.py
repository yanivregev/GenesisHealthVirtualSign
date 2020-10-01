from selenium import webdriver
from selenium.webdriver.support.ui import Select
from configparser import ConfigParser


## override w/o ini file
user = ""
passw = ""
driver = "";

### values to fill:
configur = ConfigParser()
configur.read('GenesisHealthVirtualSign.ini')
if (user == ""):
    user = configur.get('config','user')
if (passw==""):
    passw = configur.get('config','password')
if (driver==""):
    driver = configur.get('config','driver')


## Edge
browser = webdriver.Edge(executable_path=driver)
## Chrome
#browser = webdriver.Chrome(executable_path=driver)






#### don't touch from here ## configure number of children and type of form at the end this file

loggedIn= False
browser.get("https://parents.genesisedu.com/hoboken/parents?gohome=true")


def automate_form(name,formName):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Name: {name} Form: {formName}')  # Press Ctrl+F8 to toggle the breakpoint.
    global loggedIn
    global tables
    global table
    global browser

    if (not loggedIn):



        input1 = browser.find_element_by_id('j_username')
        input2 = browser.find_element_by_id("j_password")
        input3 = browser.find_element_by_class_name("saveButton")

        input1.send_keys(user)
        input2.send_keys(passw)
        input3.click()

        browser.implicitly_wait(10)

        forms = browser.find_elements_by_tag_name("span")[10] # the 10th element is "Forms"
        forms.click()

        loggedIn=True


    tables = browser.find_elements_by_tag_name("table")[2]
    table = tables.find_elements_by_tag_name("td")

    found = False
    i=0 # start with 1st student

    while ((found==False) and (i<len(table))):
        getname = table[i]
        if (getname.text==name):
            inner_found = False
            j=i+1
            while ((inner_found == False) and (j < len(table))):
                getform=table[j]
                if ((getform.text[:len(formName)])==formName):  ## return left part of TD
                    form=getform
                    inner_found=True
                j=j+1
            found=True
        i=i+1

    if (form):
        form.click()


    button = browser.find_element_by_class_name("saveButton")
    select = Select(browser.find_elements_by_tag_name("select")[1])

    select.select_by_visible_text('Yes')
    button.click()
    #forms = browser.find_elements_by_tag_name("span")[10]  # the 10th element is "Forms"
    #forms.click()


    browser.maximize_window()
    browser.save_screenshot('result.png')


if __name__ == '__main__':

    logged_in = False

    #options are: "Covid Daily Parent Form" or "Remote Student Attendance AM"


    ## copy below line for each kid, as they appear "Lastname, Firstnanme" - please note space after comma
    automate_form('Last, First',"Covid Daily Parent Form")
    automate_form('Last, First2',"Covid Daily Parent Form")
    automate_form('Last, First',"Remote Student Attendance AM")
    automate_form('Last, First2',"Remote Student Attendance AM")


    browser.close()

    print(f'Done!')
