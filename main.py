from playwright.sync_api import sync_playwright
import pickle

def load_cookies_from_file(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def get_instagram_session_id(cookies):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Set cookies
        page.context.add_cookies(cookies)

        page.goto('https://www.instagram.com/')
        page.wait_for_load_state("networkidle")

        # Extract session ID
        session_id = None
        cookies = page.context.cookies()
        for cookie in cookies:
            if cookie['name'] == 'sessionid':
                session_id = cookie['value']
                break

        print(f"Session ID: {session_id}" if session_id else "Session ID not found")
        browser.close()

# Load cookies from a file
cookies = load_cookies_from_file('instagram_cookies.pkl')
get_instagram_session_id(cookies)
