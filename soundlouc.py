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
        tk.Label(self.root, text="Click count:").grid(row=0, column=0, padx=10, pady=10)
        self.click_count_entry = tk.Entry(self.root)
        self.click_count_entry.grid(row=0, column=1, padx=10, pady=10)
        ok_button = tk.Button(self.root, text="OK", command=self.create_second_screen)
        ok_button.grid(row=1, column=0, padx=10, pady=10)

    def create_second_screen(self):
        click_count = int(self.click_count_entry.get())

        second_screen = tk.Toplevel(self.root)
        second_screen.title("Clicker App - Second Screen")

        tk.Label(second_screen, text="URL:").grid(row=0, column=0, padx=10, pady=10)
        self.url_entry = tk.Entry(second_screen)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(second_screen, text="Number of Threads:").grid(row=1, column=0, padx=10, pady=10)
        self.thread_entry = tk.Entry(second_screen)
        self.thread_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(second_screen, text="Number of Repeats:").grid(row=2, column=0, padx=10, pady=10)
        self.repeat_entry = tk.Entry(second_screen)
        self.repeat_entry.grid(row=2, column=1, padx=10, pady=10)

        for i in range(click_count):
            tk.Label(second_screen, text=f"Click {i+1}:").grid(row=i+3, column=0, padx=10, pady=10)
            xpath_entry = tk.Entry(second_screen)
            xpath_entry.grid(row=i+3, column=1, padx=10, pady=10)
            self.xpath_entries.append(xpath_entry)

        start_button = tk.Button(second_screen, text="Start", command=self.start_clicking)
        start_button.grid(row=click_count+4, column=0, padx=10, pady=10)


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
                for entry in self.xpath_entries:
                    try:
                        xpath = entry.get()
                        print("beklenmeye başlandı")
                        time.sleep(2)
                        element = driver.find_element(By.XPATH, xpath)
                        element.click()
                        print("tıklandı")

                    except Exception as e:
                        print(f"Error while clicking: {e}")
                        print("tıklanmadı")
                time.sleep(9)

                print("kapoandı")
                driver.quit()
                time.sleep(1)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ClickerApp()
    app.run()