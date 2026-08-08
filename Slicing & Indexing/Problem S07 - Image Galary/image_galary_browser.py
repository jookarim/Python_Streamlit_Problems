import streamlit as st

class ImageGalaryBrowser:
    def __init__(self):
        self.__images = []
        self.__page = 1
        self.__generate_images()
        
    def __generate_images(self):
        for i in range(20):
            self.__images.append(f"Image: {i + 1}")
            
    def next_page(self):
        if self.__page < (len(self.__images) // 4):
            self.__page += 1
        
    def prev_page(self):
        if self.__page > 1:
            self.__page -= 1
    
    def first_page(self):
        self.__page = 1

    def last_page(self):
        self.__page = len(self.__images) // 4
        
    def get_images_page(self):
        page = self.__page - 1
        
        start = page * 4
        end = page * 4 + 4
        
        return self.__images[start : end]
    

class ImageGalaryDisplayer:
    def __init__(self, image_galary_browser):
        self.image_galary_browser = image_galary_browser
    
    def display_images(self):
        for image in self.image_galary_browser.get_images_page():
            st.write(f"Image: {image}")
            
    def display_next_page_button(self):
        next_page_button = st.button("Next Page")
        if next_page_button:
            self.image_galary_browser.next_page()
            st.rerun()
    
    def display_prev_page_button(self):
        prev_page_button = st.button("Prev Page")
        if prev_page_button:
            self.image_galary_browser.prev_page()
            st.rerun()
    
    def display_first_page_button(self):
        first_page_button = st.button("First Page")
        if first_page_button:
            self.image_galary_browser.first_page()
            st.rerun()
            
    def display_last_page_button(self):
        last_page_button = st.button("Last Page")
        if last_page_button:
            self.image_galary_browser.last_page()
            st.rerun()

class Application:
    def __init__(self, image_galary_displayer, image_galary_browser):
        self.image_galary_displayer = image_galary_displayer
    
    def display(self):
        self.image_galary_displayer.display_next_page_button()
        self.image_galary_displayer.display_prev_page_button()
        self.image_galary_displayer.display_first_page_button()
        self.image_galary_displayer.display_last_page_button()
        self.image_galary_displayer.display_images()

if "browser_instance" not in st.session_state:
    st.session_state.browser_instance = ImageGalaryBrowser()

image_galary_browser = st.session_state.browser_instance            
image_galary_displayer = ImageGalaryDisplayer(image_galary_browser)

application = Application(image_galary_displayer, image_galary_browser)

application.display()
