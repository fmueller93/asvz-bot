#!/usr/bin/python3
# coding=UTF-8

"""
Test script to check if "Freie Plätze" counter is visible without logging in
"""

import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

def test_public_visibility(lesson_id):
    """
    Test if the free places counter is visible without authentication

    Args:
        lesson_id: The ASVZ lesson ID to check
    """
    lesson_url = f"https://schalter.asvz.ch/tn/lessons/{lesson_id}"

    print(f"Testing lesson: {lesson_url}")
    print("=" * 60)

    # Set up headless Chrome
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = None
    try:
        # Get ChromeDriver
        chromedriver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
        if not chromedriver_path:
            chromedriver_path = ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()

        driver = webdriver.Chrome(
            service=Service(chromedriver_path),
            options=options,
        )

        # Load the page WITHOUT logging in
        print("\n1. Loading lesson page (no login)...")
        driver.get(lesson_url)
        driver.implicitly_wait(3)

        # Check if we can see the free places counter
        print("2. Looking for 'Freie Plätze' counter...")

        try:
            # Try to find the free places element
            num_free_spots_element = driver.find_element(
                By.XPATH, "//dl[contains(., 'Freie Plätze')]/dd/span"
            )
            num_free_spots = int(num_free_spots_element.get_attribute("innerHTML"))

            print(f"\n✅ SUCCESS! Counter is publicly visible!")
            print(f"   Free places: {num_free_spots}")
            print("\n" + "=" * 60)
            print("RESULT: You CAN check availability without logging in!")
            print("=" * 60)
            print("\nThis means you can:")
            print("  • Monitor for free spots without authentication")
            print("  • Only log in when spots become available")
            print("  • Significantly reduce detectability")
            return True

        except NoSuchElementException:
            print("\n❌ Counter NOT found without login")
            print("\n   Checking if login is required...")

            # Check if there's a login button/requirement
            try:
                login_button = driver.find_element(
                    By.XPATH, "//button[@title='Login'] | //a[@title='Login & Anmelden']"
                )
                print("   Found login button - authentication likely required")
            except NoSuchElementException:
                pass

            # Save page source for debugging
            print("\n   Saving page source to debug.html for inspection...")
            with open("debug.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)

            print("\n" + "=" * 60)
            print("RESULT: Counter may require login to view")
            print("=" * 60)
            print("\nYou may need to:")
            print("  • Check debug.html to see what's on the page")
            print("  • Verify the lesson ID is correct")
            print("  • Stay logged in to monitor availability")
            return False

    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        return False

    finally:
        if driver:
            driver.quit()
            print("\nBrowser closed.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_public_visibility.py LESSON_ID")
        print("Example: python test_public_visibility.py 196346")
        sys.exit(1)

    lesson_id = sys.argv[1]
    test_public_visibility(lesson_id)
