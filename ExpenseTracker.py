
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import date


class ExpenseTracker:

    def __init__(self, root):
        self.root = root
        self.root.title("Personal Expense Tracker")
        self.root.geometry("900x700")
        self.root.minsize(600, 450)
        self.root.resizable(True, True)

        self.expenses = []
        self.budget = 0.0

        self.create_scrollable_window()
        self.load_data()
        self.create_interface()
        self.update_table()
        self.update_summary()

    def create_scrollable_window(self):

        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            container,
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.content_frame = tk.Frame(self.canvas)

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.content_frame,
            anchor="nw"
        )

        self.content_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_content
        )

        self.root.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )

        self.root.bind_all(
            "<Button-4>",
            self.on_mousewheel
        )

        self.root.bind_all(
            "<Button-5>",
            self.on_mousewheel
        )

    def update_scroll_region(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def resize_content(self, event):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )

    def on_mousewheel(self, event):

        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")

        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

        else:
            if event.delta:
                if abs(event.delta) >= 120:
                    movement = int(-event.delta / 120)
                else:
                    movement = -1 if event.delta > 0 else 1

                self.canvas.yview_scroll(
                    movement,
                    "units"
                )

        return "break"

    def load_data(self):

        if os.path.exists("expenses.json"):
            try:
                with open("expenses.json", "r") as file:
                    data = json.load(file)

                self.expenses = data.get("expenses", [])
                self.budget = float(data.get("budget", 0))

            except (json.JSONDecodeError, ValueError, TypeError):
                messagebox.showerror(
                    "Error",
                    "Could not load saved data."
                )

    def save_data(self):

        data = {
            "expenses": self.expenses,
            "budget": self.budget
        }

        with open("expenses.json", "w") as file:
            json.dump(data, file, indent=4)

    def create_interface(self):

        title = tk.Label(
            self.content_frame,
            text="PERSONAL EXPENSE TRACKER",
            font=("Arial", 22, "bold")
        )

        title.pack(pady=15)

        budget_frame = tk.Frame(self.content_frame)
        budget_frame.pack(pady=5)

        tk.Label(
            budget_frame,
            text="Set Budget: ₱"
        ).pack(side="left")

        self.budget_entry = tk.Entry(
            budget_frame,
            width=15
        )

        self.budget_entry.pack(
            side="left",
            padx=5
        )

        self.budget_entry.insert(
            0,
            str(self.budget)
        )

        tk.Button(
            budget_frame,
            text="Update Budget",
            command=self.set_budget
        ).pack(side="left")

        form = tk.LabelFrame(
            self.content_frame,
            text="Add New Expense",
            padx=10,
            pady=10
        )

        form.pack(
            fill="x",
            padx=20,
            pady=10
        )

        tk.Label(
            form,
            text="Date (YYYY-MM-DD)"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.date_entry = tk.Entry(
            form,
            width=18
        )

        self.date_entry.grid(
            row=0,
            column=1
        )

        self.date_entry.insert(
            0,
            date.today().isoformat()
        )

        tk.Label(
            form,
            text="Category"
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        self.category_entry = ttk.Combobox(
            form,
            values=[
                "Food",
                "Transportation",
                "Education",
                "Entertainment",
                "Shopping",
                "Bills",
                "Others"
            ],
            state="readonly",
            width=17
        )

        self.category_entry.grid(
            row=0,
            column=3
        )

        self.category_entry.set("Food")

        tk.Label(
            form,
            text="Description"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        self.description_entry = tk.Entry(
            form,
            width=20
        )

        self.description_entry.grid(
            row=1,
            column=1
        )

        tk.Label(
            form,
            text="Amount (₱)"
        ).grid(
            row=1,
            column=2,
            padx=5
        )

        self.amount_entry = tk.Entry(
            form,
            width=20
        )

        self.amount_entry.grid(
            row=1,
            column=3
        )

        tk.Button(
            form,
            text="Add Expense",
            command=self.add_expense
        ).grid(
            row=2,
            column=0,
            columnspan=4,
            pady=10
        )

        search_frame = tk.Frame(self.content_frame)
        search_frame.pack(pady=5)

        tk.Label(
            search_frame,
            text="Search:"
        ).pack(side="left")

        self.search_entry = tk.Entry(
            search_frame,
            width=30
        )

        self.search_entry.pack(
            side="left",
            padx=5
        )

        tk.Button(
            search_frame,
            text="Search",
            command=self.search_expense
        ).pack(
            side="left",
            padx=3
        )

        tk.Button(
            search_frame,
            text="Show All",
            command=self.update_table
        ).pack(
            side="left",
            padx=3
        )

        table_frame = tk.Frame(self.content_frame)

        table_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        columns = (
            "Date",
            "Category",
            "Description",
            "Amount"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=5
        )

        for col in columns:
            self.table.heading(
                col,
                text=col
            )

            self.table.column(
                col,
                width=200,
                anchor="center"
            )

        self.table.pack(fill="x")

        tk.Button(
            self.content_frame,
            text="Delete Selected Expense",
            command=self.delete_expense
        ).pack(pady=5)

        overview = tk.LabelFrame(
            self.content_frame,
            text="Budget Overview",
            padx=15,
            pady=10
        )

        overview.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        tk.Label(
            overview,
            text="Starting Budget",
            font=("Arial", 11, "bold")
        ).pack(anchor="w")

        self.starting_budget_label = tk.Label(
            overview,
            text="₱0.00",
            font=("Arial", 18, "bold"),
            fg="green"
        )

        self.starting_budget_label.pack(
            anchor="w",
            pady=5
        )

        ttk.Separator(
            overview,
            orient="horizontal"
        ).pack(
            fill="x",
            pady=8
        )

        tk.Label(
            overview,
            text="Add Expense",
            font=("Arial", 11, "bold")
        ).pack(
            anchor="w",
            pady=5
        )

        expense_list_frame = tk.Frame(overview)

        expense_list_frame.pack(
            fill="both",
            expand=True
        )

        self.overview_table = ttk.Treeview(
            expense_list_frame,
            columns=("Category", "Amount"),
            show="",
            height=5
        )

        self.overview_table.column(
            "Category",
            width=700,
            anchor="w"
        )

        self.overview_table.column(
            "Amount",
            width=180,
            anchor="e"
        )

        self.overview_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            expense_list_frame,
            orient="vertical",
            command=self.overview_table.yview
        )

        self.overview_table.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        ttk.Separator(
            overview,
            orient="horizontal"
        ).pack(
            fill="x",
            pady=8
        )

        self.total_label = tk.Label(
            overview,
            text="Total Expenses: ₱0.00",
            font=("Arial", 11, "bold")
        )

        self.total_label.pack(
            anchor="e",
            pady=3
        )

        self.remaining_label = tk.Label(
            overview,
            text="Remaining Budget: ₱0.00",
            font=("Arial", 12, "bold"),
            fg="green"
        )

        self.remaining_label.pack(
            anchor="e",
            pady=3
        )

    def add_expense(self):

        expense_date = self.date_entry.get().strip()
        category = self.category_entry.get()
        description = self.description_entry.get().strip()
        amount_text = self.amount_entry.get().strip()

        if not expense_date or not category or not description or not amount_text:
            messagebox.showwarning(
                "Missing Information",
                "Please complete all fields."
            )
            return

        try:
            date.fromisoformat(expense_date)
            amount = float(amount_text)

            if amount <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter a valid date and a positive amount."
            )
            return

        expense = {
            "date": expense_date,
            "category": category,
            "description": description,
            "amount": amount
        }

        self.expenses.append(expense)

        self.save_data()
        self.update_table()
        self.update_summary()

        self.description_entry.delete(
            0,
            tk.END
        )

        self.amount_entry.delete(
            0,
            tk.END
        )

        messagebox.showinfo(
            "Success",
            "Expense added successfully!"
        )

    def update_table(self, records=None):

        for item in self.table.get_children():
            self.table.delete(item)

        if records is None:
            records = list(enumerate(self.expenses))

        for index, expense in records:

            self.table.insert(
                "",
                tk.END,
                iid=str(index),
                values=(
                    expense["date"],
                    expense["category"],
                    expense["description"],
                    f"₱{expense['amount']:,.2f}"
                )
            )

    def search_expense(self):

        keyword = self.search_entry.get().strip().lower()

        if not keyword:
            self.update_table()
            return

        results = []

        for index, expense in enumerate(self.expenses):

            if (
                keyword in expense["category"].lower()
                or keyword in expense["description"].lower()
                or keyword in expense["date"].lower()
            ):
                results.append((index, expense))

        self.update_table(results)

        if not results:
            messagebox.showinfo(
                "Search",
                "No matching expenses found."
            )

    def delete_expense(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select an expense to delete."
            )
            return

        index = int(selected[0])

        if messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this expense?"
        ):

            del self.expenses[index]

            self.save_data()
            self.update_table()
            self.update_summary()

    def set_budget(self):

        try:
            new_budget = float(
                self.budget_entry.get()
            )

            if new_budget < 0:
                raise ValueError

            self.budget = new_budget

            self.save_data()
            self.update_summary()

            messagebox.showinfo(
                "Success",
                "Budget updated successfully!"
            )

        except ValueError:
            messagebox.showerror(
                "Invalid Budget",
                "Please enter a valid non-negative amount."
            )

    def update_summary(self):

        total = sum(
            expense["amount"]
            for expense in self.expenses
        )

        remaining = self.budget - total

        self.starting_budget_label.config(
            text=f"₱{self.budget:,.2f}"
        )

        for item in self.overview_table.get_children():
            self.overview_table.delete(item)

        for index, expense in enumerate(self.expenses):

            self.overview_table.insert(
                "",
                tk.END,
                iid=str(index),
                values=(
                    expense["category"],
                    f"- ₱{expense['amount']:,.2f}"
                )
            )

        self.total_label.config(
            text=f"Total Expenses: ₱{total:,.2f}"
        )

        self.remaining_label.config(
            text=f"Remaining Budget: ₱{remaining:,.2f}"
        )

        if remaining < 0:
            self.remaining_label.config(fg="red")
        else:
            self.remaining_label.config(fg="green")


if __name__ == "__main__":

    root = tk.Tk()

    app = ExpenseTracker(root)

    root.mainloop()
