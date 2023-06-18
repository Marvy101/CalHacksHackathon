import openai
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui
import random
import pygetwindow as gw
from love import openai



def browser_emulator(input_url, user_prompt, num_pages):
    options = Options()
    driver = webdriver.Chrome(options=options)

    driver.maximize_window()
    driver.get(input_url)

    for _ in range(num_pages):

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )

        links = driver.find_elements(By.CSS_SELECTOR, "a")
        height = driver.get_window_size()["height"]
        links = [link for link in links if link.is_enabled() and link.is_displayed() and link.location["y"] <= height]

        link_data = []  # list to store link info

        for link in links:
            link_info = {
                "href": link.get_attribute("href"),
                "text": link.text,
                "size": link.size,
                "location": link.location,
            }
            link_data.append(link_info)

        # Use GPT-4 to decide which link to click
        link_texts = [link["text"] for link in link_data]
        print("List of texts to make decision from: ", link_texts)
        link_prompt = f"{user_prompt}\n All these texts are buttons on a webpage, output the most relevant one to the User Prompt. Do not output anything else/ \n \nOptions:\n" + "\n".join(link_texts)
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": "You are a brilliant comedian"},
                {"role": "user", "content": link_prompt},
            ],
        )

        chosen_link_text = response["choices"][0]["message"]["content"]
        chosen_link_info = next((link for link in link_data if link["text"] == chosen_link_text), None)

        if not chosen_link_info:
            print("GPT-4 did not select a valid link. Please try again.")
            return

        browser_info = gw.getWindowsWithTitle(driver.title)
        print("\n Choice:", chosen_link_text)

        browser_window = gw.getWindowsWithTitle(driver.title)[0]
        window_position = browser_window.topleft
        window_position_x = window_position[0]
        window_position_y = window_position[1]

        # Assuming an offset of 100 pixels for the URL bar
        offset_y = 116

        link_size = chosen_link_info['size']
        link_location = chosen_link_info['location']

        center_x = link_location['x'] + link_size['width'] / 2
        center_y = link_location['y'] + link_size['height'] / 2

        screen_x = window_position_x + center_x
        screen_y = window_position_y + center_y + offset_y

        pyautogui.moveTo(screen_x, screen_y, duration=0.5)
        pyautogui.click(x=screen_x, y=screen_y)



    time.sleep(5)
    driver.quit()

# Example user_prompt
user_prompt = "Buy iphone"
url = "https://www.apple.com/"

# Define the GPT-4 interaction to obtain number of pages to navigate
prompt = f'''You are an AI that visits websites how many pages will it take you to accomplish: user_prompt = {user_prompt} from this url:{url}. Output only a number without saying any other thing.'''
response = openai.ChatCompletion.create(
    model="gpt-4-0613",
    messages=[
        {"role": "system", "content": "You are only output numbers"},
        {"role": "user", "content": prompt},
    ],
)

# Extract the number of pages from the response
num_pages = int(response["choices"][0]["message"]["content"])

print(num_pages)

# Call the function with url, user_prompt, and the obtained num_pages
browser_emulator(url, user_prompt, num_pages)
