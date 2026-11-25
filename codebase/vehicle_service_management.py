"""
Vehicle Service Management System
Python 3 | OOP | Dictionary | File Handling | CRUD

Run: python vehicle_service_management.py
Data is stored in services.txt in the same folder.
"""

import json
import os

DATA_FILE = "services.txt"
GST_RATE = 0.18

SERVICE_PRICES = {
    "Oil Change": 1500,
    "Wheel Alignment": 800,
    "Full Service": 4500,
    "Brake Repair": 2200
}

VALID_STATUSES = ["Pending", "In Progress", "Completed"]


class ServiceRecord:
    """Stores and displays one vehicle service record."""

    def __init__(self, registration_number, owner, vehicle, service,
                 status="Pending"):
        self.registration_number = registration_number.strip().upper()
        self.owner = owner.strip()
        self.vehicle = vehicle.strip()
        self.service = service.strip()
        self.status = status

    def calculate_cost(self):
        """Return service price including 18% GST."""
        base_price = SERVICE_PRICES[self.service]
        return base_price * (1 + GST_RATE)

    def display(self):
        """Display all details of this service record."""
        print("-" * 45)
        print("Registration Number :", self.registration_number)
        print("Owner               :", self.owner)
        print("Vehicle             :", self.vehicle)
        print("Service             :", self.service)
        print("Cost including 18% GST: Rs. {:.2f}".format(
            self.calculate_cost()))
        print("Status              :", self.status)
        print("-" * 45)

    def to_dictionary(self):
        """Convert the object into a dictionary for file storage."""
        return {
            "registration_number": self.registration_number,
            "owner": self.owner,
            "vehicle": self.vehicle,
            "service": self.service,
            "status": self.status
        }


class VehicleServiceManagementSystem:
    """Manages service records using a dictionary and a text file."""

    def __init__(self):
        # Dictionary key = vehicle registration number
        self.records = {}
        self.load_records()

    def load_records(self):
        """Load saved records. A missing/empty file is treated as empty."""
        if not os.path.exists(DATA_FILE):
            self.save_records()
            return

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if content:
                    saved_records = json.loads(content)
                    for item in saved_records:
                        record = ServiceRecord(
                            item["registration_number"],
                            item["owner"],
                            item["vehicle"],
                            item["service"],
                            item.get("status", "Pending")
                        )
                        self.records[record.registration_number] = record
        except (json.JSONDecodeError, KeyError, TypeError):
            print("Warning: Data file is invalid. Starting with empty records.")
            self.records = {}

    def save_records(self):
        """Save all records to services.txt."""
        data = [record.to_dictionary()
                for record in self.records.values()]
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def add_record(self, registration_number, owner, vehicle, service):
        """Create and save a new service record."""
        registration_number = registration_number.strip().upper()
        service = service.strip().title()

        if not registration_number or not owner.strip() or not vehicle.strip():
            print("Invalid input. All fields are required.")
            return

        if service not in SERVICE_PRICES:
            print("Invalid service type. Choose from: "
                  "Oil Change, Wheel Alignment, Full Service, Brake Repair.")
            return

        if registration_number in self.records:
            print("A record already exists for {}.".format(
                registration_number))
            return

        record = ServiceRecord(registration_number, owner, vehicle, service)
        self.records[registration_number] = record
        self.save_records()

        print("Record added. {} | {} | Cost incl. 18% GST: Rs. {:.2f} "
              "| Status: {}".format(
                  record.registration_number,
                  record.service,
                  record.calculate_cost(),
                  record.status
              ))

    def view_record(self, registration_number):
        """Find and display one record."""
        registration_number = registration_number.strip().upper()
        record = self.records.get(registration_number)

        if record is None:
            print("No record found for {}.".format(registration_number))
        else:
            record.display()

    def view_all_records(self):
        """Display every saved record."""
        if not self.records:
            print("No service records available.")
            return

        for record in self.records.values():
            record.display()

    def update_status(self, registration_number, new_status):
        """Update the status of an existing record."""
        registration_number = registration_number.strip().upper()
        new_status = new_status.strip().title()

        record = self.records.get(registration_number)
        if record is None:
            print("No record found for {}.".format(registration_number))

            return

        if new_status not in VALID_STATUSES:
            print("Invalid status. Choose from: Pending, In Progress, Completed.")
            return

        old_status = record.status
        record.status = new_status
        self.save_records()
        print("Status updated: {} -> {}".format(old_status, new_status))

    def delete_record(self, registration_number):
        registration_number = registration_number.strip().upper()

        if registration_number not in self.records:
            print("No record found for {}.".format(registration_number))
            return

        del self.records[registration_number]
        self.save_records()
        print("Record for {} deleted.".format(registration_number))

    def show_menu(self):
        print("\n========== VEHICLE SERVICE MANAGEMENT SYSTEM ==========")
        print("1. Add service record")
        print("2. View one service record")
        print("3. View all service records")
        print("4. Update service status")
        print("5. Delete service record")
        print("6. Exit")

    def run(self):
        while True:
            self.show_menu()
            choice = input("Enter your choice (1-6): ").strip()

            if choice == "1":
                print("\n--- Add Service Record ---")
                reg_no = input("Registration number: ")
                owner = input("Owner name: ")
                vehicle = input("Vehicle type: ")
                print("Available services:", ", ".join(SERVICE_PRICES))
                service = input("Service: ")
                self.add_record(reg_no, owner, vehicle, service)

            elif choice == "2":
                reg_no = input("Enter registration number: ")
                self.view_record(reg_no)

            elif choice == "3":
                self.view_all_records()

            elif choice == "4":
                reg_no = input("Enter registration number: ")
                print("Available statuses:", ", ".join(VALID_STATUSES))
                status = input("Enter new status: ")
                self.update_status(reg_no, status)

            elif choice == "5":
                reg_no = input("Enter registration number: ")
                self.delete_record(reg_no)

            elif choice == "6":
                print("Thank you for using Vehicle Service Management System.")
                break

            else:
                print("Invalid menu choice. Please enter a number from 1 to 6.")


# Main program
if __name__ == "__main__":
    system = VehicleServiceManagementSystem()
    system.run()
