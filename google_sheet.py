import gspread
from oauth2client.service_account import ServiceAccountCredentials

WORDS_DICTIONARY = {}
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Italian Words').sheet1
for row in range(1, sheet.row_count + 1):
    WORDS_DICTIONARY[sheet.row_values(row)[0]] = sheet.row_values(row)[1]
print(WORDS_DICTIONARY)
