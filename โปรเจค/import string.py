import string
import random

# Getting password length
while True:
    try:
        length = int(input("Enter password length: ").strip())
        if length <= 0:
            print("Please enter a positive number!")
        else:
            break
    except ValueError:
        print("Invalid input! Please enter a valid number.")

print('''Choose character set for password from these:
    1. Digits
    2. Letters
    3. Special characters
    4. Exit''')

characterList = ""

# Getting character set for password
while True:
    try:
        choice = int(input("Pick a number: ").strip())
        if choice == 1:
            characterList += string.digits  # แก้ให้ถูกต้อง
        elif choice == 2:
            characterList += string.ascii_letters
        elif choice == 3:
            characterList += string.punctuation
        elif choice == 4:
            if characterList:  # เช็คว่ามีตัวเลือกอย่างน้อย 1 อย่าง
                break
            else:
                print("You must select at least one character type!")
        else:
            print("Please pick a valid option (1-4)!")
    except ValueError:
        print("Invalid input! Please enter a number.")

# Generate password
password = "".join(random.choice(characterList) for _ in range(length))
print("The random password is:", password) 