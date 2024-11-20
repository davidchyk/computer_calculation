import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Ініціалізація Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("path/to/your/credentials.json", scope)
client = gspread.authorize(creds)

# Відкриття таблиці Google Sheets
sheet = client.open("License Database").sheet1  # Замініть на назву вашої таблиці

def verify_and_activate_license(entered_key):
    unused_keys = sheet.col_values(1)  # Отримуємо всі невикористані ключі (1-й стовпець)
    used_keys = sheet.col_values(2)    # Отримуємо всі використані ключі (2-й стовпець)

    if entered_key in unused_keys:
        # Переміщуємо ключ до стовпця "Used Keys"
        row = unused_keys.index(entered_key) + 1  # Індекс рядка для невикористаного ключа
        sheet.update_cell(row, 1, "")  # Очищаємо клітинку в "Unused Keys"
        
        # Знаходимо перший порожній рядок у стовпці "Used Keys"
        empty_row = len(used_keys) + 1
        sheet.update_cell(empty_row, 2, entered_key)  # Додаємо ключ до "Used Keys"
        
        print("Ключ активовано успішно!")
    elif entered_key in used_keys:
        print("Цей ключ уже використано.")
    else:
        print("Недійсний ключ.")

# Приклад використання функції перевірки
user_key = input("Введіть ліцензійний ключ: ")
verify_and_activate_license(user_key)
