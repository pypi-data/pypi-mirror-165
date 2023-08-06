# KAI_AUTOMATE_LINKEDIN -- APPLICATION

# Library to crawl LINKEDIN
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#  Library native of python
from time import sleep
from random import randint

# Other library python
from fp.fp import FreeProxy

class AutomateLinkedIn:
    """
        This class is used to automate tasks on
        LINKEDIN social networks.
        This class will allow
            - LIKE
            - SHARE
            - COMMENT
    """
    credentials = {}
    my_bot_linkedin = None
    
    def __init__(self, email: str, password: str):
        """ Description
                This function is a constructor of my class.
            Params:
                email:str: email to connect on your linkedIn account
            
                password:str: password to connect on your linkedIn account
        """
        self.credentials['email'] =  email  
        self.credentials['password'] =  password
        
        print('Object create')
    
    def linkedin_test_driver_manager_chrome(self):
        """ Description
                Allow to install chromedriver and out in PATH
        """
        service = ChromeService(executable_path=ChromeDriverManager().install())
        return service
    
    def linkedin_get_ip(self):
        """ Description
                Allow to return proxy
            
            Return:
                ip:str
        """
        ip = FreeProxy(country_id=['FR'], rand=True).get().split('//')[-1]
        print(ip)
        return ip

    def linkedin_create_session_crawl(self):        
        """ Description
                Allow to add options of my driver
        """
        userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36' 
    
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={userAgent}')
        options.add_argument("no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--incognito")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--single-process')
        options.add_argument("--start-maximized")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("disable-infobars")
        
        return options
    
    def linkedin_launch_page(self, link: str):
        """ Description
                Allow to create my driver
            
            Params:
                link:str: url of page you want to visit             
        """
        try:
            options = self.linkedin_create_session_crawl()
            
            driver = None
            chrome_driver = 'http://localhost:4431'    
            while True:
                try:
                    driver = webdriver.Remote(
                        command_executor=chrome_driver,
                        desired_capabilities=DesiredCapabilities.CHROME,
                        options=options)
                    print('remote ready')
                    driver.save_screenshot("launch_page.png")
                    break
                except:
                    print('remote not ready, sleeping for ten seconds.')
                    sleep(5)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            print(driver.execute_script("return navigator.userAgent;"))
            
            driver.get(link)
            sleep(randint(3,5))
            self.my_bot_linkedin = driver
        except Exception as e:
            print("I can not open navigator. See error : ", e)
            if(self.my_bot_linkedin !=None):
                print("yes with capture")
                self.my_bot_linkedin.save_screenshot("launch_page.png")
                self.my_bot_linkedin.quit()
            else:
                print("yes with capture, launch page")
                driver.save_screenshot("launch_pageError.png")
                driver.quit()
            raise
        
    def linkedin_connect_account(self, url:str):
        """ Description
                Allow to connect on LinkedIn account with driver
                
            Params:
                link:str: url of page you want to visit
        """
        try:
            self.linkedin_launch_page(url)
            
            id_email = 'username'
            id_password = 'password'
            class_button = 'btn__primary--large'
            linkedin_detected = False
            if(self.my_bot_linkedin.execute_script('return document.getElementsByClassName("authwall-join-form__form-toggle--bottom form-toggle").length') > 0):
                self.my_bot_linkedin.execute_script('document.getElementsByClassName("authwall-join-form__form-toggle--bottom form-toggle")[0].click()')
                sleep(randint(2,3))
                
                id_email = 'session_key'
                id_password = 'session_password'
                class_button = 'sign-in-form__submit-button'
                
                linkedin_detected = True

            email = self.my_bot_linkedin.find_element(By.ID, id_email)
            email.send_keys(self.credentials['email'])
            sleep(randint(2,3))
            
            password = self.my_bot_linkedin.find_element(By.ID, id_password)
            password.send_keys(self.credentials['password'])
            sleep(randint(2,3))
        
            self.my_bot_linkedin.save_screenshot("connect.png")
            
            self.my_bot_linkedin.find_element(By.CLASS_NAME, class_button).click()
            sleep(randint(5,10))
            
            if linkedin_detected == True:
                self.my_bot_linkedin.get(url)
        except Exception as e:
            print("I can not connect with this credentials. See error : ", e)
            if(self.my_bot_linkedin !=None):
                self.my_bot_linkedin.save_screenshot("connect.png")
                self.my_bot_linkedin.quit()
            else:
                print("connect_accountError")
                self.my_bot_linkedin.quit()
            raise
        
    def linkedin_get_last_publication(self):
        """ Description
                Allow to get a last publication. Here this function return a first 
                element in list of publication
            
            Return:
                last_publications : object_seleniulm
        """
        try:
            script_get_publications = '''return document.getElementsByClassName("ember-view  occludable-update")'''
            last_publications = self.my_bot_linkedin.execute_script(script_get_publications)
            return last_publications[0]
        except Exception as e:
            print("I can not get last publication. See error : ", e)
            if(self.my_bot_linkedin !=None):
                self.my_bot_linkedin.save_screenshot("get_last_publicationError.png")
                self.my_bot_linkedin.quit()
            raise
    
    def linkedin_get_publications(self):
        """ Description
                Allow to get a publication in list contains element de type object_selenium
            
            Return:
                last_publications : list
        """
        try:
            script_get_publications = '''return document.getElementsByClassName("ember-view  occludable-update")'''
            last_publications = self.my_bot_linkedin.execute_script(script_get_publications)
            scrollSize = 10000
            scrollStart = 0
            while(scrollSize < 50000):
                self.my_bot_linkedin.execute_script('window.scrollTo(arguments[0],arguments[1])', scrollStart, scrollSize)
                scrollStart = scrollSize
                scrollSize += 10000
                sleep(randint(1,2))
            return last_publications          
        except Exception as e:
            print("I can not get many publications. See error : ", e)
            if(self.my_bot_linkedin !=None):
                self.my_bot_linkedin.save_screenshot("get_publicationsError.png")
                self.my_bot_linkedin.quit()
            raise
        
    def linkedin_like_post(self, post):        
        """ Description
                Allow to like a post
            
            Params:
                post:object_selenium: represent a post 
                
            Return:
                boolean : True if like is success
        """
        try:            
            counter_like = 0
            script_for_is_pressed = '''
                                        return arguments[0].getElementsByClassName("artdeco-button artdeco-button--muted artdeco-button--4 \
                                                                                    artdeco-button--tertiary ember-view social-actions-button \
                                                                                    react-button__trigger")[0] \
                                                            .getAttribute("aria-pressed")
                                    '''
            script_do_like ='''
                                arguments[0].getElementsByClassName("artdeco-button artdeco-button--muted artdeco-button--4 \
                                                                            artdeco-button--tertiary ember-view social-actions-button \
                                                                            react-button__trigger")[0].click()          
                            '''
            self.my_bot_linkedin.execute_script('window.scrollTo(arguments[0],arguments[1])', 0, 0)
            
            is_pressed = self.my_bot_linkedin.execute_script(script_for_is_pressed, post)
            
            while is_pressed == 'false':
                self.my_bot_linkedin.execute_script(script_do_like, post)
                                
                is_pressed = self.my_bot_linkedin.execute_script(script_for_is_pressed, post)
                print('regarde', is_pressed)
                if is_pressed == "true":
                    print("is_pressed button like")
                    counter_like += 1
                    self.my_bot_linkedin.save_screenshot("like_"+str(counter_like)+".png")
                else:
                    print("is not pressed button")
            return True
        except Exception as e:
            print("I can not like this publication. See error : ", e)
            if(self.my_bot_linkedin !=None):
                self.my_bot_linkedin.save_screenshot("likeErrror.png")
                self.my_bot_linkedin.quit()
            raise
                  
    def linkedin_share_post(self, post, text_share="Merci pour ce post"):                   
        """ 
            Description
                Allow to share a post
            
            Params:
                post:object_selenium: represent a post 
                
                text_share:str: text to attach to the post to share
            
            Return:
                boolean : True if share is success
        """
        try:
            script_button_share='''
                                    arguments[0].getElementsByClassName("artdeco-dropdown__trigger artdeco-dropdown__trigger--placement-bottom \
                                                                                ember-view artdeco-button social-actions-button social-reshare-button \
                                                                                flex-wrap artdeco-button--muted artdeco-button--4 artdeco-button--tertiary")[0].click()  
                                '''
            script_click_button_share = '''
                                            document.getElementsByClassName("share-actions__primary-action artdeco-button artdeco-button--2 \
                                                                            artdeco-button--primary ember-view")[0] \
                                                    .click()
                                        '''
            script_number_items_dropdowns = '''
                                                return document.getElementsByClassName("artdeco-dropdown__item artdeco-dropdown__item--is-dropdown \
                                                                                        ember-view social-reshare-button__sharing-as-is-dropdown-item") \
                                                                .length
                                            '''
            script_click_items ='''
                                    document.getElementsByClassName("artdeco-dropdown__item artdeco-dropdown__item--is-dropdown\
                                                                    ember-view social-reshare-button__sharing-as-is-dropdown-item")[arguments[0]].click()
                                '''
                                
            script_insert_text_share ='''
                                    document.getElementsByClassName('editor-content ql-container')[0].innerHTML=arguments[0]
                                '''
                                
            script_close_popup_share = '''
                                    document.getElementsByClassName('artdeco-modal__dismiss artdeco-button artdeco-button--circle \
                                                                    artdeco-button--muted artdeco-button--2 \
                                                                    artdeco-button--tertiary ember-view')[0].click()       
                                '''
            script_confirm_close_popup_share = '''
                                    document.getElementsByClassName('artdeco-modal__confirm-dialog-btn artdeco-button \
                                                                    artdeco-button--2 artdeco-button--primary ember-view')[0].click() 
            '''

            self.my_bot_linkedin.execute_script('window.scrollTo(arguments[0],arguments[1])', 0, 0)
            
            self.my_bot_linkedin.execute_script(script_button_share, post)
            sleep(5)
            
            nb_select = self.my_bot_linkedin.execute_script(script_number_items_dropdowns)
            if nb_select > 1:
                self.my_bot_linkedin.execute_script(script_click_items, 1)
            else:
                self.my_bot_linkedin.execute_script(script_click_items, 0)
            sleep(5)
            
            self.my_bot_linkedin.execute_script(script_insert_text_share, text_share)
            sleep(5)
            
            self.my_bot_linkedin.save_screenshot("share.png")
            
            self.my_bot_linkedin.execute_script(script_click_button_share)
            sleep(10)
            if(self.my_bot_linkedin.find_element(By.CLASS_NAME, 'artdeco-toast-item__message').find_element(By.TAG_NAME, 'span').text == "Ce post a déjà été partagé." or
               len(self.my_bot_linkedin.find_element(By.CLASS_NAME, 'artdeco-toast-item__message').find_elements(By.TAG_NAME, 'a')) == 0):
                self.my_bot_linkedin.execute_script(script_close_popup_share)
                sleep(2)
                self.my_bot_linkedin.execute_script(script_confirm_close_popup_share)
            return True
        except Exception as e:
            print("I can not share this publication. See error : ", e)
            if(self.my_bot_linkedin !=None):
                self.my_bot_linkedin.save_screenshot("shareError.png")
                self.my_bot_linkedin.quit()
            raise
             
    def linkedin_comment_post(self, post, text_comment="Très intéressant :)"):
        """ 
            Description
                Allow to comment a post
            
            Params:
                post:object_selenium: represent a post 
                
                text_comment:str: comment to add on post
            
            Return:
                boolean : True if comment add is success 
        """
        try:
            script_click_button_comment='''
                                            return arguments[0].getElementsByClassName("artdeco-button artdeco-button--muted artdeco-button--4 \
                                                                                        artdeco-button--tertiary ember-view social-actions-button \
                                                                                        comment-button flex-wrap")[0].click()
                                        '''
            script_click_button_publish_comment='''
                                                    arguments[0].getElementsByClassName("comments-comment-box__submit-button mt3 \
                                                                                        artdeco-button artdeco-button--1 \
                                                                                        artdeco-button--primary ember-view")[0].click()
                                                '''
            
            self.my_bot_linkedin.execute_script('window.scrollTo(arguments[0],arguments[1])', 0, 0)
            
            self.my_bot_linkedin.execute_script(script_click_button_comment, post)
            sleep(5)
            
            script_insert_comment = '''arguments[0].getElementsByClassName("ql-editor ql-blank")[0].innerHTML = arguments[1]'''
            self.my_bot_linkedin.execute_script(script_insert_comment, post, text_comment)
            sleep(5)
            
            self.my_bot_linkedin.save_screenshot("post.png")
            self.my_bot_linkedin.execute_script(script_click_button_publish_comment, post)
            sleep(10)
            return True
        except Exception as e:
            print("I can not comment this publication. See error : ", e)
            if(self.my_bot_linkedin !=None):
                self.my_bot_linkedin.save_screenshot("postError.png")
                self.my_bot_linkedin.quit()
            raise
        
    def linkedin_close_session(self):
        """ 
            Description
                Allow to close session create for the driver
        """
        if(self.my_bot_linkedin !=None):
            self.my_bot_linkedin.quit()
            return True
        else:
            return False
        
        
            
    
    
    
    
    
    
    
    
    
    