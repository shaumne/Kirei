import threading
import tkinter as tk
from emre import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random
import os
import pyautogui, time
from pynput import mouse 

class Recorder:
    def __init__(self, master):
        self.master = master
        master.title("Mouse Recorder")
        master.geometry("400x500")

        self.url_label = tk.Label(master, text="URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(master)
        self.url_entry.pack()

        self.threads_label = tk.Label(master, text="Number of Threads:")
        self.threads_label.pack()

        self.threads_entry = tk.Entry(master)
        self.threads_entry.pack()

        self.repeats_label = tk.Label(master, text="Number of Repeats:")
        self.repeats_label.pack()

        self.repeats_entry = tk.Entry(master)
        self.repeats_entry.pack()

        self.start_button = tk.Button(master, text="Start", command=self.start)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stop", state=tk.DISABLED, command=self.stop)
        self.stop_button.pack()

        self.play_button = tk.Button(master, text="Play", state=tk.DISABLED, command=self.play_once)
        self.play_button.pack()

        self.recording = False
        self.stopped = False

        self.is_m_lc_down = False
        self.is_m_lc_up = False
        self.m_lc_down_x = 0
        self.m_lc_down_y = 0
        self.m_lc_up_x = 0
        self.m_lc_up_y = 0
        self.mbutton = ''
        self.this_time_ms = self.prev_time_ms = self.wait_time_ms = self.event_id = 0
        self.mch = {}
        self.button_type = ""
        self.action_string = ""
        self.x = -1
        self.y = -1
        self.sleep_time = 0 # recorded time between events

        self.is_down = 'm_lc_down_xy'
        self.is_up = 'm_lc_up_xy'
        self.btn_left_action_text = "Button.left"
        self.btn_right_action_text = "Button.right"

    def start_listener(self):
        self.listener = mouse.Listener(on_click=self.on_click)
        print(self.repeats_label)
        self.listener.start()

    def stop_listener(self):
        self.listener.stop()
        self.listener.join()
        print("RESULT:")
        print(self.mch)

    def on_click(self, x, y, button, pressed):
        self.this_time_ms = self.time_now_mls()
        self.mbutton = str(button)
        self.wait_time_ms = self.this_time_ms - self.prev_time_ms

        if pressed:
            self.is_m_lc_down = True
            self.m_lc_down_x = x
            self.m_lc_down_y = y
        else:
            self.is_m_lc_up = True
            self.m_lc_up_x = x
            self.m_lc_up_y = y

        self.prev_time_ms = self.this_time_ms
        self.record_event()

    def time_now_mls(self):
        return round(time.time() * 1000)

    def record_event(self):
        if self.is_m_lc_down:
            self.event_id += 1
            print('\nIn Loop: m_lc_down:', self.m_lc_down_x, self.m_lc_down_y, " event_id: ", self.event_id)
            self.mch[self.event_id] = self.wait_time_ms, self.mbutton, 'm_lc_down_xy', self.m_lc_down_x, self.m_lc_down_y
            self.is_m_lc_down = False

        if self.is_m_lc_up:
            self.event_id += 1
            print('\nIn Loop: m_lc_up:', self.m_lc_up_x, self.m_lc_up_y, " event_id: ", self.event_id)
            self.mch[self.event_id] = self.wait_time_ms, self.mbutton, 'm_lc_up_xy', self.m_lc_up_x, self.m_lc_up_y
            self.is_m_lc_up = False

    def start(self):
        url = self.url_entry.get()
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(url)
        self.recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.play_button.config(state=tk.DISABLED)

        self.start_listener()
        # self.mouse_actions = []
        # actions = ActionChains(self.driver)

        # while self.recording:
        #     # Get mouse position
        #     x, y = self.driver.execute_script("return [window.screenX + window.outerWidth/2, window.screenY + window.outerHeight/2];")

        #     # Add mouse position to actions list
        #     self.mouse_actions.append((x, y))

        #     # Perform mouse actions
        #     print(x)
        #     print(y)
        #     actions = ActionChains(self.driver)
        #     actions.move_by_offset(x, y).click().perform()

        #     time.sleep(0.1)  # wait for 0.1 seconds between actions



    def stop(self):
        self.recording = False
        self.stopped = True
        self.driver.quit()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.play_button.config(state=tk.NORMAL)
        self.stop_listener()

    def play(self):
        url = self.url_entry.get()
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(url)
        self.play_button.config(state=tk.DISABLED)

        # Load list of proxies from file
        with open('proxies.txt', 'r') as f:
            proxies = [line.strip() for line in f]

        # Shuffle proxies
        random.shuffle(proxies)

        # Validate input for num_threads
        try:
            num_threads = int(self.threads_entry.get())
            if num_threads <= 0:
                raise ValueError
        except ValueError:
            print( "Number of threads must be a positive integer")
            return

        # Validate input for num_repeats
        try:
            num_repeats = int(self.repeats_entry.get())
            if num_repeats <= 0:
                raise ValueError
        except ValueError:
            print("Number of repeats must be a positive integer")
            return

        threads = []
        for i in range(num_threads):
            # Assign each thread a different proxy
            proxy = proxies[i % len(proxies)]
            t = threading.Thread(target=self.play_once, args=(proxy, num_repeats))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        self.driver.quit()
        self.play_button.config(state=tk.NORMAL)

    def play_once(self):
        # options = webdriver.ChromeOptions()
        # options.add_argument('--proxy-server=%s' % proxy)
        # driver = webdriver.Chrome(options=options)
        # actions = ActionChains(driver)
        url = self.url_entry.get()
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(url)
        self.play_button.config(state=tk.DISABLED)

        num_repeats = int(self.repeats_entry.get())
        for r in range(num_repeats):
            for key, item in self.mch.items():
                #print(item)
                sleep_time,button_type,action_string, x, y = item
                #print(button_type,action_string, x, y)

                sleep_time = sleep_time/1000

                if button_type == self.btn_left_action_text:
                    if action_string == self.is_down:
                        print("left_down",x,y)
                        pyautogui.mouseDown(x=x,y=y)
                    elif action_string == self.is_up:
                        print("LEFT_UP",x,y)
                        pyautogui.mouseUp(x=x,y=y)
                        
                elif button_type == self.btn_right_action_text:
                    if action_string == self.is_down:
                        print("right_down",x,y)
                        pyautogui.mouseDown(button='right',x=x,y=y)
                    elif action_string == self.is_up:
                        print("RIGHT_UP",x,y)
                        pyautogui.mouseUp(button='right',x=x,y=y)
                        
                time.sleep(1) # give some time to respond
                print("Sleep {0}".format(sleep_time))
            self.driver.refresh()

        self.driver.quit()




root = tk.Tk()
recorder = Recorder(root)
root.mainloop()

        