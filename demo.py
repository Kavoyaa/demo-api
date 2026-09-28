import requests

BASE_URL = "http://127.0.0.1:8000"


def upload_data():
    heading = input("Enter heading: ")
    description = input("Enter description: ")
    response = requests.post(
        f"{BASE_URL}/upload",
        json={"heading": heading, "description": description},
    )

    print(response.json()["message"])


def view_all():
    response = requests.get(f"{BASE_URL}/data")
    items = response.json()["data"]

    if not items:
        print("No data found.")
        return
    
    for item in items:
        for heading, description in item.items():
            print(f"{heading}: {description}")


def view_by_heading():
    wanted = input("Enter heading to look for: ").lower()
    response = requests.get(f"{BASE_URL}/data")
    found = False

    for item in response.json()["data"]:
        for heading, description in item.items():
            if heading.lower() == wanted:
                print(f"{heading}: {description}")
                found = True
                
    if not found:
        print("No data found with that heading.")


while True:
    print("\n[VERY EPIC DATA STORAGE APP!!]")
    print("[1] Upload data")
    print("[2] View all data")
    print("[3] View data by heading")
    print("[4] Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        upload_data()
    elif choice == "2":
        view_all()
    elif choice == "3":
        view_by_heading()
    elif choice == "4":
        print("Bye.")
        break
    else:
        print("Invalid choice.")
