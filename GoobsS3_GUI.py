#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
from dotenv import load_dotenv
import requests
import os

# Load environment variables from .env.prod
load_dotenv(dotenv_path=".env.prod")

# Linode Object Storage settings https://techdocs.akamai.com/linode-api/reference/get-object-storage-bucket-content
API_VERSION = "v4"
LINODE_API_KEY = os.getenv("LINODE_API_KEY")
REGION = os.getenv("REGION")
BUCKET_NAME = os.getenv("BUCKET_NAME")
ENDPOINT_URL = f"https://api.linode.com/{API_VERSION}/object-storage/buckets/{REGION}/{BUCKET_NAME}/object-list?page_size=100"

headers = {
    "accept": "application/json",
    "authorization": f"Bearer {LINODE_API_KEY}"
}

# Get and display the contents of the bucket.
def list_files():
    try: # API Documentation here https://www.ipify.org/
        url = f"https://api.linode.com/{API_VERSION}/object-storage/buckets/{REGION}/{BUCKET_NAME}/object-list?page_size=100"
        response = requests.get(url, headers=headers) # Requests doc https://requests.readthedocs.io/en/latest/

        if response.status_code == 200:
            file_listbox.delete(0, tk.END)  # Clear the listbox
            data = response.json()
            if "data" in data and data["data"]:
                for obj in data["data"]:
                    file_listbox.insert(tk.END, obj["name"])
            else:
                file_listbox.insert(tk.END, "There are no objects to list inside this bucket.")
        else:
            file_listbox.delete(0, tk.END)
            file_listbox.insert(tk.END, f"Error: {response.status_code} - {response.text}")
    except Exception as e: # Basic error catching. I want to add specific messages for HTTP failures outlined here. https://techdocs.akamai.com/linode-api/reference/get-object-storage-bucket
        file_listbox.delete(0, tk.END)  # Clear the listbox on error
        file_listbox.insert(tk.END, f"Error: {e}")

# Upload a file to the bucket from the specified path.
def upload_file():
    filepath = file_entry.get()
    if filepath:
        try:
            filename = filepath.split("/")[-1]  # Extract filename from path
            with open(filepath, "rb") as file_data:
                url = f"{ENDPOINT_URL}/{BUCKET_NAME}/{filename}"
                response = requests.put(
                    url, 
                    data=file_data,
                    headers={"authorization": f"Bearer {LINODE_API_KEY}"} # code directly ripped from the Linode docs.
                )

            if response.status_code == 200 or response.status_code == 201:
                print(f"Uploaded {filename} to {BUCKET_NAME}")
                file_entry.delete(0, tk.END)
                list_files()  # Refresh the list of files
            else:
                print(f"Upload failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Upload failed: {e}")

# Create the main window
root = tk.Tk()
root.title("Goob's Object Storage GUI")
root.geometry("1280x720")

# Create a frame for the file listing
list_frame = ttk.Frame(root)
list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Add a button to refresh the file list
refresh_button = ttk.Button(list_frame, text="Get Bucket Content", command=list_files)
refresh_button.pack(side=tk.BOTTOM, pady=5)

# Add a listbox to display files
file_listbox = tk.Listbox(list_frame, font=("Helvetica", 12), bg="black", fg="green")
file_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

# Add a scrollbar for the listbox
scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=file_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
file_listbox.config(yscrollcommand=scrollbar.set)

# Create a frame for the input and button
input_frame = ttk.Frame(root)
input_frame.pack(fill=tk.X, padx=10, pady=10)

# Add an entry box for the file path
file_entry = ttk.Entry(input_frame, font=("Helvetica", 12))
file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

# Add an upload button
upload_button = ttk.Button(input_frame, text="Upload", command=upload_file)
upload_button.pack(side=tk.RIGHT)

# Start the GUI event loop
root.mainloop()
