# PACKAGE - LINKEDIN-BOT

### **But**
Ce packages permet d'automatiser les tâches de like, partage et commentaire sur linkedIn.

### **Pour importer**
    from bot_linkedin import automate_linkedin

### **Fonctions**

- **linkedin_test_driver_manager_chrome(self)**: 

    Allow to install chromedriver and out in PATH

- **linkedin_get_ip(self)**: 

    Allow to return proxy

- **linkedin_create_session_crawl(self)**: 

    Allow to add options of my driver

- **linkedin_launch_page(self, link: str)**: 

    Allow to create my driver

- **linkedin_connect_account(self, url:str)**: 

    Allow to connect on LinkedIn account with driver

- **linkedin_get_last_publication(self)**: 

    Allow to get a last publication. Here this function return a first 

- **linkedin_get_publications(self)**: 

    Allow to get a publication in list contains element de type object_selenium

- **linkedin_like_post(self, post)**: 

    Allow to like a post

- **linkedin_share_post(self, post, text_share="Merci pour ce post")**: 

    Allow to share a post
                    
- **linkedin_comment_post(self, post, text_comment="Très intéressant :)")**: 

    Allow to comment a post 

- **linkedin_close_session(self)**: 

     Allow to close session create for the driver
