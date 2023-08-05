import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager


def click_after_delay(css):
    element = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, css)))
    sleep(1)
    element.click()


def enter_after_delay(text, css):
    element = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, css)))
    sleep(1)
    element.clear()
    element.send_keys(text)


def get_browser():
    os.environ['WDM_LOG_LEVEL'] = '0'
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-blink-features')
    options.add_argument('--disable-blink-features=AutomationControlled')
    s = Service(executable_path=ChromeDriverManager().install())
    _driver = webdriver.Chrome(service=s, options=options)
    _driver.maximize_window()
    _wait = WebDriverWait(_driver, 60)
    return _driver, _wait


def set_ssh():
    email = input('\n Enter email:\n [<username>@<server>.<domain>] ')

    global wait
    driver, wait = get_browser()

    driver.get('https://github.com/settings/ssh/new')
    enter_after_delay('mysshkey', '[name="ssh_key[title]"]')

    os.system("ssh-keygen -t ed25519 -C \"{}\" -f /tmp/sshkey -N \"\"".format(email))
    os.system("ssh-add /tmp/sshkey")
    with open("/tmp/sshkey.pub","r") as f:
        ssh_key = f.read()
    print(ssh_key.strip())
    enter_after_delay(ssh_key, '[name="ssh_key[key]"]')
    click_after_delay('.btn-primary')
    driver.close()

def create_repo():
    username = input('\n Enter username:\n ')
    repo_name = 'cosmo540'

    global wait
    driver, wait = get_browser()

    driver.get('https://github.com/new')
    enter_after_delay(repo_name, '#repository_name')
    enter_after_delay('My first repo!', '#repository_description')
    click_after_delay('.btn-primary')
    click_after_delay('[data-ga-click="Empty repo, click, Clicked SSH protocol"]')
    sleep(1)
    ssh_link = f'git@github.com:{username}/{repo_name}.git'
    driver.close()

    os.system('git clone {}'.format(ssh_link))
    os.chdir('cosmo540/')
    os.system('touch hello_world.py')

    with open('hello_world.py', 'a') as the_file:
        the_file.write("print('Hello, World!')")

    os.system('git add hello_world.py')
    os.system('git commit -m "add hello world"')
    os.system('git push')
   

def main():
    email = input('\n Enter email:\n [<username>@<server>.<domain>] ')
    password = input('\n Enter password:\n [>7 chars+upper/lowercase+numbers+special chars] ')
    username = input('\n Enter username:\n ')
    repo_name = 'cosmo540'
   
    global wait
    driver, wait = get_browser()
    driver.get('https://github.com/signup?ref_cta=Sign+up&ref_loc=header+logged+out&ref_page=%2F&source=header-home')
    enter_after_delay(email, '#email')
    click_after_delay('.js-continue-button')
    enter_after_delay(password, '#password')
    click_after_delay('[data-continue-to="username-container"]')
    enter_after_delay(username, '#login')
    click_after_delay('[data-continue-to="opt-in-container"]')
    enter_after_delay('n', '#opt_in')
    click_after_delay('[data-continue-to="captcha-and-submit-container"]')
    
    click_after_delay('.js-octocaptcha-form-submit')
    
    click_after_delay('.js-form-radio-button-item')
    click_after_delay('.btn')
    click_after_delay('.btn')
    click_after_delay('.btn')
    sleep(5)
    
    driver.get('https://github.com/settings/ssh/new')
    enter_after_delay('mysshkey', '[name="ssh_key[title]"]')
    
    os.system("ssh-keygen -t ed25519 -C \"{}\" -f /tmp/sshkey -N \"\"".format(email))
    os.system("ssh-add /tmp/sshkey")
    with open("/tmp/sshkey.pub","r") as f:
        ssh_key = f.read()
    print(ssh_key.strip())
    enter_after_delay(ssh_key, '[name="ssh_key[key]"]')
    click_after_delay('.btn-primary')
    #click_after_delay('.btn')
    
    driver.get('https://github.com/new')
    enter_after_delay(repo_name, '#repository_name')
    enter_after_delay('My first repo!', '#repository_description')
    click_after_delay('.btn-primary')
    click_after_delay('[data-ga-click="Empty repo, click, Clicked SSH protocol"]')
    sleep(1)
    ssh_link = f'git@github.com:{username}/{repo_name}.git'
    driver.close()
    
    os.system('git clone {}'.format(ssh_link))
    os.chdir('cosmo540/')
    os.system('touch hello_world.py')
    
    with open('hello_world.py', 'a') as the_file:
        the_file.write("print('Hello, World!')")
    
    os.system('git add hello_world.py')
    os.system('git commit -m "add hello world"')
    os.system('git push')


if __name__=='__main__':
    main()
