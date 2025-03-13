def log_activity(username, action):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO logs (username, action, timestamp) VALUES (?, ?, ?)", (username, action, timestamp))
    conn.commit()

def register():
    username = input("İstifadəçi adı: ")
    password = getpass.getpass("Şifrə: ")
    passkey = input("Şifrəni sıfırlamaq üçün passkey: ")
    role = "user"
    try:
        cursor.execute("INSERT INTO users (username, password, role, passkey) VALUES (?, ?, ?, ?)", (username, password, role, passkey))
        conn.commit()
        print("Qeydiyyat uğurla tamamlandı!")
        log_activity(username, "Qeydiyyat edildi")
    except sqlite3.IntegrityError:
        print("Bu istifadəçi adı artıq mövcuddur!")

def login():
    username = input("İstifadəçi adı: ")
    password = getpass.getpass("Şifrə: ")
    cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    if user:
        print(f"Xoş gəldiniz, {username}! Rolunuz: {user[0]}")
        log_activity(username, "Sistemdə daxil oldu")
        if user[0] == "admin":
            admin_panel()
        else:
            user_panel(username)
    else:
        print("Yanlış istifadəçi adı və ya şifrə!")

def reset_password():
    username = input("İstifadəçi adı: ")
    passkey = input("Passkey: ")
    cursor.execute("SELECT * FROM users WHERE username = ? AND passkey = ?", (username, passkey))
    if cursor.fetchone():
        new_password = getpass.getpass("Yeni şifrə: ")
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
        conn.commit()
        print("Şifrə uğurla yeniləndi!")
        log_activity(username, "Şifrə sıfırlandı")
    else:
        print("Yanlış passkey!")

def delete_account(username):
    confirm = input("Hesabınızı silmək istədiyinizə əminsinizmi? (bəli/xeyr): ")
    if confirm.lower() == "bəli":
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        print("Hesab uğurla silindi!")
        log_activity(username, "Hesab silindi")

def admin_panel():
    while True:
        print("\nAdmin paneli:")
        print("1. İstifadəçiləri siyahıya bax")
        print("2. İstifadəçi sil")
        print("3. Çıxış")
        choice = input("Seçim edin: ")
        if choice == "1":
            cursor.execute("SELECT username, role FROM users")
            users = cursor.fetchall()
            for user in users:
                print(f"İstifadəçi: {user[0]}, Rol: {user[1]}")
        elif choice == "2":
            user_to_delete = input("Silinəcək istifadəçi adı: ")
            cursor.execute("DELETE FROM users WHERE username = ?", (user_to_delete,))
            conn.commit()
            print("İstifadəçi silindi!")
            log_activity("admin", f"{user_to_delete} silindi")
        elif choice == "3":
            break
        else:
            print("Yanlış seçim!")

def user_panel(username):
    while True:
        print("\n1. Şifrəni sıfırla")
        print("2. Hesabı sil")
        print("3. Çıxış")
        choice = input("Seçim edin: ")
        if choice == "1":
            reset_password()
        elif choice == "2":
            delete_account(username)
        elif choice == "3":
            log_activity(username, "Sistemdən çıxış etdi")
            break
        else:
            print("Yanlış seçim!")

while True:
    print("\n1. Qeydiyyat")
    print("2. Giriş")
    print("3. Şifrəni unutdum")
    print("4. Çıxış")
    choice = input("Seçim edin: ")
    if choice == "1":
        register()
    elif choice == "2":
        login()
    elif choice == "3":
        reset_password()
    elif choice == "4":
        print("Sistemdən çıxış edildi!")
        break
    else:
        print("Yanlış seçim!")

conn.close()
