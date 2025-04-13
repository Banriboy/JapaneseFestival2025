import os
import time
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from hx711v0_5_1 import HX711
import requests
from datetime import datetime

# Google Sheets認証設定
SPREADSHEET_ID = '1U9EQ-MyJoNE4MNQpgrImWAmd0_4mUTUboey09Sirwe8'  # Google SheetsのIDを指定
RANGE_NAME = 'Sheet1'  # データを挿入する範囲

# StreamlitサーバーURL
STREAMLIT_SERVER_URL = "https://japanesefestival2025.streamlit.app"

# HX711の設定
hx1 = HX711(5, 6)
hx2 = HX711(20, 21)
hx3 = HX711(23, 24)
hx4 = HX711(17, 27)

def authenticate_google_sheets():
    """ Google Sheetsの認証を行う """
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("/home/pi/iot-python/hx711py/credentials.json", scope)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        worksheet = spreadsheet.sheet1
        print("Connected to Google Sheets successfully.")
        return worksheet
    except gspread.exceptions.SpreadsheetNotFound:
        print("Spreadsheet not found. Please check the spreadsheet name and permissions.")
        sys.exit()
    except Exception as e:
        print(f"Failed to connect to Google Sheets: {e}")
        sys.exit()

def send_weight_data_to_sheets(weight, station, category, co2_emission=0, chopsticks_count=0, worksheet=None):
    """ 測定データをGoogle Sheetsに送信 """
    timeStamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    row_data = [timeStamp,  station, category, round(weight, 2), round(co2_emission, 2), chopsticks_count]
    worksheet.append_row(row_data)
    print(f"[INFO] Data appended to Google Sheets: {row_data}")

def categorize_and_add_weight(weight, worksheet=None):
    if category:
        print(f"[INFO] {category} Total Weight: {weight:.2f} kg")

        co2_emission = 0
        chopsticks_count = 0

        if category == "Chopsticks":
            chopsticks_count = int(weight / 0.003)  # 1本の重量を0.01kgと仮定
            co2_emission = chopsticks_count * 50 / 1000

            print(f"CO2 Emission: {co2_emission:.1f} kg, Count: {chopsticks_count}")

        # Google Sheetsにデータ送信
        send_weight_data_to_sheets(weight, station, category, co2_emission, chopsticks_count, worksheet)
    else:
        print("[ERROR] Invalid selection. Data not recorded.")

def get_raw_weight_data():
    """ HX711から重量データを取得 """
    raw_data1 = hx1.getRawBytes()
    raw_data2 = hx2.getRawBytes()
    raw_data3 = hx3.getRawBytes()
    raw_data4 = hx4.getRawBytes()

    weight1 = hx1.rawBytesToWeight(raw_data1) / 1000
    weight2 = hx2.rawBytesToWeight(raw_data2) / 1000
    weight3 = hx3.rawBytesToWeight(raw_data3) / 1000
    weight4 = hx4.rawBytesToWeight(raw_data4) / 1000

    total_weight = weight1 + weight2 + weight3 + weight4
    #raw_data = hx.getRawBytes()
    #weight = hx.rawBytesToWeight(raw_data) / 1000  # 単位はkgに変換
    return total_weight


def add_data_to_named_range(worksheet, row_data):
    try:
        # 名前付き範囲を参照
        range_names = {
            "Time Stamp": "TimeStamp",
            "Station": "Station",
            "Category": "Category",
            "Weight (kg)": "Weight",
            "CO2 Emission (kg)": "CO2_Emission",
            "Chopsticks Count (pair)": "Chopsticks_Count"
        }

        # 名前付き範囲にデータを挿入
        for header, value in row_data.items():
            # 名前付き範囲に値を設定
            cell_range = range_names.get(header, None)
            if cell_range:
                # 名前付き範囲を取得し、値を設定
                worksheet.update_acell(cell_range, value)

    except Exception as e:
        print(f"Error inserting data into named range: {e}")

if __name__ == "__main__":
    # Google Sheetsの認証
    worksheet = authenticate_google_sheets()

    # HX711設定
    hx1.setReadingFormat("MSB", "MSB")
    hx1.autosetOffset()
    hx1.setReferenceUnit(-102.28)

    hx2.setReadingFormat("MSB", "MSB")
    hx2.autosetOffset()
    hx2.setReferenceUnit(-100.9)

    hx3.setReadingFormat("MSB", "MSB")
    hx3.autosetOffset()
    hx3.setReferenceUnit(-106.1)

    hx4.setReadingFormat("MSB", "MSB")
    hx4.autosetOffset()
    hx4.setReferenceUnit(95.53)

    while True:
        try:
            print("Select station:\n1) Station 1\n2) Station 2\n3) Station 3")
            station_choice = input("Enter station number: ")

            if station_choice not in ["1", "2", "3"]:
                print("[ERROR] Invalid station selection. Please select a valid station.")
                continue

            station_map = {"1": "Station 1", "2": "Station 2", "3": "Station 3"}
            station = station_map[station_choice]

            print("Select category:\n1) Chopsticks\n2) Recycle")
            category_choice = input("Enter category number: ")

            if category_choice not in ["1", "2"]:
                print("[ERROR] Invalid selection. Please select a valid category.")
                continue

            category_map = {"1": "Chopstciks", "2": "Recycle"}
            category = category_map[category_choice]

            weight = get_raw_weight_data()
            print(f"[INFO] Measured weight: {weight:.3f} kg")
            categorize_and_add_weight(weight, worksheet)


        except KeyboardInterrupt:
            print("Process interrupted by user.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
