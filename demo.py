import requests

BASE_URL = "http://127.0.0.1:8000"


def upload_data():
    heading = input("Enter heading: ")
    description = input("Enter description: ")
    response = requests.post(
        f"{BASE_URL}/upload",
        json={"heading": heading, "description": description},
    )
    if response.status_code == 200:
        print(response.json()["message"])
    else:
        print(f"Error: {response.json()}")


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


def update_data():
    heading = input("Enter the heading you want to update: ")
    new_heading = input("Enter the new heading (leave blank to keep the same): ")
    new_description = input("Enter the new description: ")

    if not new_heading.strip():
        new_heading = heading

    response = requests.post(
        f"{BASE_URL}/update",
        json={
            "heading": heading,
            "new_heading": new_heading,
            "new_description": new_description,
        },
    )
    if response.status_code == 200:
        print(response.json()["message"])
    else:
        print(f"Error: {response.json().get('detail', response.json())}")


def delete_data():
    heading = input("Enter the heading you want to delete: ")
    response = requests.post(
        f"{BASE_URL}/delete",
        json={"heading": heading},
    )
    if response.status_code == 200:
        print(response.json()["message"])
    else:
        print(f"Error: {response.json().get('detail', response.json())}")


while True:
    print("\n[VERY EPIC DATA STORAGE APP 2.0 !!]")
    print("[1] Upload data")
    print("[2] View all data")
    print("[3] View data by heading")
    print("[4] Update data")
    print("[5] Delete data")
    print("[6] Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        upload_data()
    elif choice == "2":
        view_all()
    elif choice == "3":
        view_by_heading()
    elif choice == "4":
        update_data()
    elif choice == "5":
        delete_data()
    elif choice == "6":
        print("Bye.")
        break
    else:
        print("Invalid choice.")
