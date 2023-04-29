
# Kirei

Kirei is a bot project that can be used to increase the number of plays of songs on music platforms such as Soundcloud and Beatstars.

To operate, the project uses multiple threads that can click on a user-selected URL a desired number of times. The project can also hide the source of clicks by using a selected proxy list.

The user can control the program's usage through a simple interface. Through the interface, the user can set the duration and repeat count of clicks, enable special functions for Soundcloud and Beatstars websites, and select a proxy list.

This project was developed to help musicians gain more visibility for their music.

## Usage

Upon starting the application, the user is prompted for information such as URL, thread count, repeat count, and listen duration. The user can also select a proxy file. The application then opens a song on Soundcloud or Beatstars and listens for the specified duration. This process is repeated a number of times equal to the thread count.

## Libraries Used

* tkinter
* selenium
* threading
* time

## Installation

`pip install -r requirements.txt`

## Running

To run the application, use the following command:

`python main.py`

## Developer

The entire application has been developed by me, and you can use it as you wish. If you encounter any issues, you can contact me on Discord: `'Shaumne#9109`
