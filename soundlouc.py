import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import threading
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class ClickerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.click_count_entry = None
        self.xpath_entries = []
        self.url_entry = None
        self.thread_entry = None
        self.repeat_entry = None
        self.clicker_threads = []
        self.stop_event = threading.Event()

        self.create_first_screen()

    def create_first_screen(self):
        self.root.title("Clicker App")
        tk.Label(self.root, text="URL:").grid(row=0, column=0, padx=10, pady=10)
        self.url_entry = tk.Entry(self.root)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Number of Threads:").grid(row=1, column=0, padx=10, pady=10)
        self.thread_entry = tk.Entry(self.root)
        self.thread_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Number of Repeats:").grid(row=2, column=0, padx=10, pady=10)
        self.repeat_entry = tk.Entry(self.root)
        self.repeat_entry.grid(row=2, column=1, padx=10, pady=10)

        self.soundcloud_var = tk.BooleanVar()
        self.soundcloud_checkbutton = tk.Checkbutton(self.root, text="Soundcloud", variable=self.soundcloud_var)
        self.soundcloud_checkbutton.grid(row=3, column=0, padx=10, pady=10)

        self.beatstars_var = tk.BooleanVar()
        self.beatstars_checkbutton = tk.Checkbutton(self.root, text="Beatstars", variable=self.beatstars_var)
        self.beatstars_checkbutton.grid(row=3, column=1, padx=10, pady=10)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_clicking)
        self.start_button.grid(row=4, column=0, padx=10, pady=10)

    


    def start_clicking(self):
        url = self.url_entry.get()
        repeat_count = int(self.repeat_entry.get())
        thread_count = int(self.thread_entry.get())
        self.stop_event.clear()

        for _ in range(thread_count):
            t = threading.Thread(target=self.click_elements, args=(repeat_count, url))
            t.start()
            self.clicker_threads.append(t)

    def click_elements(self, repeat_count, url):
            for _ in range(repeat_count):
                if self.stop_event.is_set():
                    break
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                driver = webdriver.Chrome()
                driver.get(url)
                print(self.soundcloud_var.get())
                print(self.beatstars_var.get())
               
                if self.soundcloud_var.get():
                    try:
                        time.sleep(6)
                        soundcloud_button = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div[2]/div/button[1]")
                        soundcloud_button.click()
                        time.sleep(6)
                        soundcloud_play_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div[1]/a")
                        soundcloud_play_button.click()
                    except Exception as e:
                        print(f"Error while clicking: {e}")
                        print("tıklanmadı")
                elif self.beatstars_var.get():
                    try:
                        time.sleep(6)
                        beatstars_button = driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div/div[1]/div/div[2]/div/button[3]")
                        beatstars_button.click()
                        time.sleep(3)
                        beatstars_play_button = driver.find_element(By.XPATH, "/html/body/mp-root/div/div/ng-component/mp-wrapper-member-track-content/mp-member-content-item-template/bs-container-grid/div[2]/div[2]/mp-button-play-track-visual-eq-related/div/div[1]/bs-vb-button-play-item/button/i")
                        beatstars_play_button.click()
                    except Exception as e:
                        print(f"Error while clicking: {e}")
                        print("tıklanmadı")
                print("kapoandı")
                time.sleep(6)

                driver.quit()
                time.sleep(1)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ClickerApp()
    app.run()