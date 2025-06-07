import requests

BASE = 'http://localhost:5001'

# 1️⃣ 本地註冊
def test_register():
    print("\n🔐 測試本地註冊")
    data = {
        'email': 'testuser1@example.com',
        'passwd': 'test123',
        'name': '測試使用者1',
        'role': 'user',
        'addr': '台灣某地'
    }
    r = requests.post(BASE + '/register', json=data)
    print("Status:", r.status_code, "Result:", r.json())

# 2️⃣ 本地登入
def test_login():
    print("\n🔑 測試本地登入")
    data = {
        'email': 'testuser1@example.com',
        'passwd': 'test123'
    }
    r = requests.post(BASE + '/login', json=data)
    print("Status:", r.status_code, "Result:", r.json())
    return r.json().get('user_id')

# 3️⃣ 查詢使用者
def test_get_user(user_id):
    print("\n🔍 查詢使用者資訊")
    r = requests.get(f"{BASE}/user/{user_id}")
    print("Status:", r.status_code, "Result:", r.json())

# 4️⃣ 測試 Firebase 登入（請貼上從瀏覽器取得的 idToken）
def test_firebase_login(id_token):
    print("\n🎯 測試 Firebase 登入")
    headers = {'Authorization': f'Bearer {id_token}'}
    r = requests.get(BASE + '/secure', headers=headers)
    print("Status:", r.status_code, "Result:", r.json())


if __name__ == '__main__':
    test_register()
    user_id = test_login()
    if user_id:
        test_get_user(user_id)

    # 貼上你剛剛登入成功畫面顯示的 ID Token
    FIREBASE_ID_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjZlODk1YzQ3YTA0YzVmNmRlMzExMmFmZjE2ODFhMzUwNzdkMWNjZDQiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoi5p6X57W56ZyWIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xfTVpQTndDblZkenJLTWpLS3g4Yk1pcVk3SDUtdDlGSlpaMkJ4WEhtNENLcHVXaGs9czk2LWMiLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ2RnLWZvb2RzaGFyZSIsImF1ZCI6ImdkZy1mb29kc2hhcmUiLCJhdXRoX3RpbWUiOjE3NDkyODUyNjksInVzZXJfaWQiOiJYRWxOd0dCb3ZWZW40R2hzV1pBMDRyWnV5VG0yIiwic3ViIjoiWEVsTndHQm92VmVuNEdoc1daQTA0clp1eVRtMiIsImlhdCI6MTc0OTI4NTI2OSwiZXhwIjoxNzQ5Mjg4ODY5LCJlbWFpbCI6Im1pcmFjbGUueWx1bDEwMjBAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZ29vZ2xlLmNvbSI6WyIxMTgyMTc4MzIxMDU1NzI0NTI4NTUiXSwiZW1haWwiOlsibWlyYWNsZS55bHVsMTAyMEBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.SinQhEksv3Zocmoy2sVHTlJUwbqhNTryl1HqJf2NiKqhFD3apsx4WsBFRc0_D_w9buFD0a2hPzrzfEPVBDL8WN_54pR_rdQxjqCU4lyoshKLL-YnY31FDLupPeRxR1mhv2GCK9Hse2CfmmyQLPoePqi6cB2q5oVoMhjIp0ShTGZz5htPQiP6OfzBWX6OiggNZPbSuuZpVvJIwl1yieQ0hFtzFJZ9UqLRPzuhK0Lp9qT8_htO0OCs9YRSuqPCyinFCs7ERuVGxPKgZAmbHMk8AJDABwPC7eInaMA7_QmvoKTGJxGyUahP9iEW0pvj3knbJE8mpbLplJ90SFJBTOENtg"
    #if FIREBASE_ID_TOKEN != "eyJhbGciOiJSUzI1NiIsImtpZCI6IjZlODk1YzQ3YTA0YzVmNmRlMzExMmFmZjE2ODFhMzUwNzdkMWNjZDQiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoi5p6X57W56ZyWIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xfTVpQTndDblZkenJLTWpLS3g4Yk1pcVk3SDUtdDlGSlpaMkJ4WEhtNENLcHVXaGs9czk2LWMiLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZ2RnLWZvb2RzaGFyZSIsImF1ZCI6ImdkZy1mb29kc2hhcmUiLCJhdXRoX3RpbWUiOjE3NDkyODUyNjksInVzZXJfaWQiOiJYRWxOd0dCb3ZWZW40R2hzV1pBMDRyWnV5VG0yIiwic3ViIjoiWEVsTndHQm92VmVuNEdoc1daQTA0clp1eVRtMiIsImlhdCI6MTc0OTI4NTI2OSwiZXhwIjoxNzQ5Mjg4ODY5LCJlbWFpbCI6Im1pcmFjbGUueWx1bDEwMjBAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZ29vZ2xlLmNvbSI6WyIxMTgyMTc4MzIxMDU1NzI0NTI4NTUiXSwiZW1haWwiOlsibWlyYWNsZS55bHVsMTAyMEBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.SinQhEksv3Zocmoy2sVHTlJUwbqhNTryl1HqJf2NiKqhFD3apsx4WsBFRc0_D_w9buFD0a2hPzrzfEPVBDL8WN_54pR_rdQxjqCU4lyoshKLL-YnY31FDLupPeRxR1mhv2GCK9Hse2CfmmyQLPoePqi6cB2q5oVoMhjIp0ShTGZz5htPQiP6OfzBWX6OiggNZPbSuuZpVvJIwl1yieQ0hFtzFJZ9UqLRPzuhK0Lp9qT8_htO0OCs9YRSuqPCyinFCs7ERuVGxPKgZAmbHMk8AJDABwPC7eInaMA7_QmvoKTGJxGyUahP9iEW0pvj3knbJE8mpbLplJ90SFJBTOENtg":
    test_firebase_login(FIREBASE_ID_TOKEN)
