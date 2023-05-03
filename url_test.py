import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import threading
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import *
import random
from tkinter import filedialog




def read_proxy_list(file_path, encoding='utf-8'):
    with open(file_path, encoding=encoding) as file:
        proxy_list = [line.strip() for line in file if line.strip()]
    return proxy_list

def read_url_list(file_path, encoding='utf-8'):
    with open(file_path, encoding=encoding) as file:
        url_list = [line.strip() for line in file if line.strip()]
    return url_list



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

    def select_proxy(self):
        self.proxy_file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        print(self.proxy_file_path)

    def select_url_file(self):
        self.url_file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        print(self.url_file_path)



    def create_first_screen(self):
        self.root.title("Kirei")
        self.select_url_button = tk.Button(
            self.root, text="Select URLs", command=self.select_url_file)
        self.select_url_button.grid(row=0, column=0, padx=10, pady=10)

        tk.Label(self.root, text="Number of Threads:").grid(
            row=1, column=0, padx=10, pady=10)
        self.thread_entry = tk.Entry(self.root)
        self.thread_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Number of Repeats:").grid(
            row=2, column=0, padx=10, pady=10)
        self.repeat_entry = tk.Entry(self.root)
        self.repeat_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.root, text="How many seconds would you like to listen?:").grid(
            row=3, column=0, padx=10, pady=10)
        self.listen = tk.Entry(self.root)
        self.listen.insert(0, "10")
        self.listen.grid(row=3, column=1, padx=10, pady=10)

        self.soundcloud_var = tk.BooleanVar()
        self.soundcloud_checkbutton = tk.Checkbutton(
            self.root, text="Soundcloud", variable=self.soundcloud_var,  command=lambda: self.disable_other_checkbuttons(self.soundcloud_var))
        self.soundcloud_checkbutton.grid(row=4, column=0, padx=10, pady=10)

        self.beatstars_var = tk.BooleanVar()
        self.beatstars_checkbutton = tk.Checkbutton(
            self.root, text="Beatstars", variable=self.beatstars_var, command=lambda: self.disable_other_checkbuttons(self.beatstars_var))
        self.beatstars_checkbutton.grid(row=4, column=1, padx=10, pady=10)

        self.soundclick_var = tk.BooleanVar()
        self.soundclick_checkbutton = tk.Checkbutton(
            self.root, text="Soundclick", variable=self.soundclick_var, command=lambda: self.disable_other_checkbuttons(self.soundclick_var))
        self.soundclick_checkbutton.grid(row=5, column=0, padx=10, pady=10)

        self.audiomack_var = tk.BooleanVar()
        self.audiomack_checkbutton = tk.Checkbutton(
            self.root, text="audiomack", variable=self.audiomack_var, command=lambda: self.disable_other_checkbuttons(self.audiomack_var))
        self.audiomack_checkbutton.grid(row=5, column=1, padx=10, pady=10)

        self.select_proxy_button = tk.Button(
            self.root, text="Select Your Proxy", command=self.select_proxy)
        self.select_proxy_button.grid(row=7, column=0, padx=10, pady=10)

        self.start_button = tk.Button(
            self.root, text="Start", command=self.start_clicking)
        self.start_button.grid(row=7, column=1, padx=10, pady=10)

        self.process_label = tk.Label(self.root, text="")
        self.process_label.grid(row=8, column=0, padx=10, pady=10)

        self.listen_label = tk.Label(self.root, text="")

    def disable_other_checkbuttons(self, selected_checkbutton_var):
        checkbutton_vars = [self.soundcloud_var, self.beatstars_var, self.soundclick_var, self.audiomack_var]
        for checkbutton_var in checkbutton_vars:
            if checkbutton_var != selected_checkbutton_var:
                if selected_checkbutton_var.get():
                    if checkbutton_var.trace_info():
                        checkbutton_var.trace_remove("write", checkbutton_var.trace_info()[0][1])
                    checkbutton_var.set(False)
                else:
                    checkbutton_var.trace_add("write", lambda *args, cb_var=checkbutton_var: self.disable_other_checkbuttons(cb_var))


        
    def start_clicking(self):
        self.process_label.config(text="Process started")
        urls = read_url_list(self.url_file_path)
        repeat_count = int(self.repeat_entry.get())
        thread_count = int(self.thread_entry.get())
        self.stop_event.clear()

        for i in range(thread_count):
            t = threading.Thread(target=self.click_elements,
                                args=(repeat_count, urls, i))
            t.start()
            self.clicker_threads.append(t)

        def wait_for_threads():
            for t in self.clicker_threads:
                t.join()
            self.process_label.config(text="Process finished")
            self.root.quit()

        threading.Thread(target=wait_for_threads).start()

    def click_elements(self, repeat_count, urls, thread_index):


      
        proxy_list = read_proxy_list(self.proxy_file_path)

        current_url_index = thread_index
        for _ in range(repeat_count):
            if self.stop_event.is_set():
                break

            while True:
                try:
                    current_proxy = random.choice(proxy_list)
                    print(current_proxy)
                except IndexError:
                    print("Proxy list is empty.")
                    break

                url = urls[current_url_index % len(urls)]
                current_url_index += len(self.clicker_threads)
                chrome_options = Options()
                # chrome_options.add_argument('--proxy-server=http://%s' % current_proxy)
                # chrome_options.add_argument("--headless")
                # chrome_options.add_argument("--mute-audio")
                driver = webdriver.Chrome(options=chrome_options)

                driver.set_page_load_timeout(60)

                try:
                    driver.get(url)
                    print(self.soundcloud_var.get())
                    print(self.beatstars_var.get())
                    print(self.soundclick_var.get())
                    print(self.audiomack_var.get())

                    if self.soundcloud_var.get():
                        try:
                            time.sleep(10)
                
                            try:
                                soundcloud_button = driver.find_element(
                                    By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div/div[2]/div/button[1]")
                                soundcloud_button.click()
                            except:
                                print("Cannot click the cookie")
                            time.sleep(3)
                            try:
                                play_button = driver.find_element(By.CSS_SELECTOR, ".sc-button-play.playButton.sc-button.m-stretch")

                                if play_button.get_attribute("title") == "Play":
                                    play_button.click()
                                    print("Play button clicked.")
                                    listen = int(self.listen.get())
                                    print(listen + 2 )
                                    time.sleep(listen + 2) 
                            except Exception as e:
                                print("Cannot find or click the play button:", e)
                                driver.quit()


                        except Exception as e:
                            print(f"Error while clicking: {e}")
                            print("nope")
                    elif self.beatstars_var.get():
                        try:
                            time.sleep(6)
                            try:
                                beatstars_button = driver.find_element(
                                    By.XPATH, "/html/body/div[4]/div[2]/div/div[1]/div/div[2]/div/button[2]")
                                beatstars_button.click()
                            except:
                                print("Cannot clicked cookie")
                            time.sleep(3)
                            try:
                                beatstars_play_button = driver.find_element(
                                    By.XPATH, "/html/body/mp-root/div/div/ng-component/mp-wrapper-member-track-content/mp-member-content-item-template/bs-container-grid/div[2]/div[2]/mp-button-play-track-visual-eq-related/div/div[1]/bs-vb-button-play-item/button/i")
                                beatstars_play_button.click()
                                print("yesss")
                                listen = int(self.listen.get())
                                print(listen + 5)

                                time.sleep(listen + 5) 
                            except:
                                print("cannot click the play button")
                                driver.quit()
                            
                        except Exception as e:
                            print(f"Error while clicking: {e}")
                            print("nope")

                    elif self.soundclick_var.get():
                        try:
                            time.sleep(6)
                            try:
                                soundclick_play_button = driver.find_element(
                                    By.XPATH, "/html/body/div[5]/div/div[2]/div/div[2]/div[3]/div[1]/i")
                                soundclick_play_button.click()
                                print("yesss")
                                listen = int(self.listen.get())
                                print(listen + 4)

                                time.sleep(listen + 4) 
                            except:
                                print("cannot clicked play button")
                                driver.quit()
                            
                        except Exception as e:
                            print(f"Error while clicking: {e}")
                            print("nope")

                    elif self.audiomack_var.get():
                        try:
                            time.sleep(6)
                            try:
                                audiomack_button = driver.find_element(
                                    By.XPATH, "/html/body/div[1]/div[5]/button")
                                audiomack_button.click()
                            except:
                                print("Cannot clicked cookie")
                            time.sleep(3)

                            try:
                                audiomack_play_button = driver.find_element(
                                    By.XPATH, "/html/body/div[1]/div[3]/div/div/div[1]/div/div/div/div[2]/div/span[1]/button")
                                audiomack_play_button.click()
                                print("yesss")
                                listen = int(self.listen.get())
                                print(listen + 2)

                                time.sleep(listen + 2) 
                            except:
                                print("cannot clicked play button")
                                driver.quit()
                            
                        except Exception as e:
                            print(f"Error while clicking: {e}")
                            print("nope")



                    print("Process finished")

                    driver.quit()
                    time.sleep(4)
                    break
                except Exception as e:
                    print(f"Proxy error: {e}")
                    driver.quit()
                    continue



    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ClickerApp()
    app.run()
