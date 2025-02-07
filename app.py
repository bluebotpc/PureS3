#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
from dotenv import load_dotenv
import requests
import os
import boto3

# Load in script variables from a DOTENV file for flexibility.
load_dotenv(dotenv_path=".env")
API_VERSION = os.getenv("LINODE_API_VERSION")
LINODE_API_KEY = os.getenv("LINODE_API_KEY")
REGION = os.getenv("REGION")
BUCKET_NAME = os.getenv("BUCKET_NAME")
ENDPOINT_URL = f"https://api.linode.com/{API_VERSION}/object-storage/buckets/{REGION}/{BUCKET_NAME}/"
# Linode Object Storage settings https://techdocs.akamai.com/linode-api/reference/get-object-storage-bucket-content
headers = {
    "accept": "application/json",
    "authorization": f"Bearer {LINODE_API_KEY}"
}

# Using the boto3 module because it is mature, stable, and well documented.
s3session = boto3.session.Session()
s3_client = s3session.client(
    "s3",
    region_name=REGION,
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=LINODE_API_KEY,
    aws_secret_access_key="")

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

# Upload a file to the bucket using boto3
def upload_file():
    filepath = file_entry.get()
    if filepath:
        try:
            filename = os.path.basename(filepath)  # Extract filename from path
            s3_client.upload_file(filepath, BUCKET_NAME, filename)
            print(f"Uploaded {filename} to {BUCKET_NAME}")
            file_entry.delete(0, tk.END)
            list_files()  # Refresh file list
        except Exception as e:
            print(f"Upload failed: {e}")
#ABOVE THIS LINE IS FOR FUNCTIONS - BELOW THIS LINE IS FOR GUI COMPONENTS.
# Create the main window.
root = tk.Tk()
root.title("BlueBotPC GoobyS3 Interface")
root.geometry("1280x720")

# Frame to contain the Object Storage content.
list_frame = ttk.Frame(root)
list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Button to get/refresh the Object Storage content list.
refresh_button = ttk.Button(list_frame, text="Get Bucket Content", command=list_files)
refresh_button.pack(side=tk.BOTTOM, pady=5)

# Add a listbox to display files.
file_listbox = tk.Listbox(list_frame, font=("Helvetica", 12), bg="black", fg="green")
file_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

# Add a scrollbar for the Object Storage content listbox.
scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=file_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
file_listbox.config(yscrollcommand=scrollbar.set)

# Create a frame for the input and button
input_frame = ttk.Frame(root)
input_frame.pack(fill=tk.X, padx=10, pady=10)

# Add an entry box for the file path
file_entry = ttk.Entry(input_frame, font=("Helvetica", 12))
file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

# Upload Button
upload_button = ttk.Button(input_frame, text="Upload", command=upload_file)
upload_button.pack(side=tk.RIGHT)

# Start the GUI event loop
root.mainloop()
