import os
import boto3
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_VERSION = os.getenv("LINODE_API_VERSION")
LINODE_API_KEY = os.getenv("LINODE_API_KEY")
REGION = os.getenv("REGION")
BUCKET_NAME = os.getenv("BUCKET_NAME")

# Initialize Linode S3 client
session = boto3.session.Session()
s3_client = session.client(
    "s3",
    region_name=REGION,
    endpoint_url=f"https://{REGION}.linodeobjects.com",
    aws_access_key_id=LINODE_API_KEY,
    aws_secret_access_key="")

# Function to list bucket contents
def list_bucket_contents():
    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        file_list.delete(0, tk.END)
        
        if 'Contents' in response:
            for obj in response['Contents']:
                file_list.insert(tk.END, obj['Key'])
        else:
            messagebox.showinfo("Info", "Bucket is empty.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Tkinter UI Setup
root = tk.Tk()
root.title("Linode Object Storage UI")

frame = tk.Frame(root)
frame.pack(pady=10)

list_button = tk.Button(frame, text="List Bucket Contents", command=list_bucket_contents)
list_button.pack()

file_list = tk.Listbox(root, width=50, height=20)
file_list.pack(pady=10)

root.mainloop()
