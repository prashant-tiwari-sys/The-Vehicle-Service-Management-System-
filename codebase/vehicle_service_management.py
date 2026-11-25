
import json
import os

FILE = "services.txt"

PRICES = {
    "Oil Change": 1500,
    "Wheel Alignment": 800,
    "Full Service": 4500,
    "Brake Repair": 2200
}


class VehicleService:

    def __init__(self):
        self.records = {}
        self.load_records()

    # Load saved records
    def load_records(self):
        if os.path.exists(FILE):
            try:
                with open(FILE, "r") as f:
                    self.records = json.load(f)
            except (json.JSONDecodeError, TypeError):
                self.records = {}

    # Save records
    def save_records(self):
        with open(FILE, "w") as f:
            json.dump(self.records, f, indent=4)

    # Calculate service cost
    def calculate_cost(self, service):
        return PRICES[service] * 1.18

    # Add a new record
    def add_record(self):
        reg = input("Registration Number: ").strip().upper()
        owner = input("Owner Name: ").strip()
        vehicle = input("Vehicle Type: ").strip()
        print("\nAvailable Services:")
        for name, price in PRICES.items():
         print(name, "- Rs.", price)

        service = input("Enter Service Name: ").strip().title()

        if not reg or not owner or not vehicle:
            print("All fields are required!")
            return

        if service not in PRICES:
            print("Invalid service!")
            return

        if reg in self.records:
            print("Record already exists!")
            return

        self.records[reg] = {
            "owner": owner,
            "vehicle": vehicle,
            "service": service,
            "status": "Pending"
        }

        self.save_records()
        print("Record added successfully!")
        print("Total Cost including GST: Rs.", self.calculate_cost(service))

    # View records
    def view_records(self):
        if not self.records:
            print("No records found!")
            return

        for reg, data in self.records.items():
            print("\nRegistration:", reg)
            print("Owner:", data["owner"])
            print("Vehicle:", data["vehicle"])
            print("Service:", data["service"])
            print("Cost: Rs.", self.calculate_cost(data["service"]))
            print("Status:", data["status"])

    # Update service status
    def update_record(self):
        reg = input("Enter Registration Number: ").strip().upper()

        if reg in self.records:
            status = input("Enter Status (Pending/In Progress/Completed): ").strip().title()

            if status in ["Pending", "In Progress", "Completed"]:
                self.records[reg]["status"] = status
                self.save_records()
                print("Status updated!")
            else:
                print("Invalid status!")
        else:
            print("Record not found!")

    # Delete a record
    def delete_record(self):
        reg = input("Enter Registration Number: ").strip().upper()

        if reg in self.records:
            del self.records[reg]
            self.save_records()
            print("Record deleted!")
        else:
            print("Record not found!")

    # Main menu
    def run(self):
        while True:
            print("\n===== VEHICLE SERVICE MANAGEMENT =====")
            print("1. Add Record")
            print("2. View Records")
            print("3. Update Status")
            print("4. Delete Record")
            print("5. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_record()
            elif choice == "2":
                self.view_records()
            elif choice == "3":
                self.update_record()
            elif choice == "4":
                self.delete_record()
            elif choice == "5":
                print("Thank you!")
                break
            else:
                print("Invalid choice!")


if __name__ == "__main__":
    system = VehicleService()
    system.run()
