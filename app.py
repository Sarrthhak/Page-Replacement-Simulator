import streamlit as st
import os
import hashlib
import shutil

# ----- Helper Functions -----
# Get file hash to detect duplicates
def get_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

# Scan directory and list all files
def scan_directory(directory):
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)
    return file_list

# Detect duplicates by comparing hashes
def detect_duplicates(file_list):
    hash_map = {}
    duplicates = []
    for file in file_list:
        file_hash = get_file_hash(file)
        if file_hash in hash_map:
            duplicates.append(file)
        else:
            hash_map[file_hash] = file
    return duplicates

# Identify large files (over 50 MB)
def identify_large_files(file_list, size_limit=50):
    large_files = [file for file in file_list if os.path.getsize(file) > size_limit * 1024 * 1024]
    return large_files

# Restore deleted files (placeholder)
def recover_files(directory):
    # Add actual recovery logic (if needed)
    st.info("File recovery is not fully implemented yet. This is a placeholder.")
    return []

# ----- Streamlit UI -----
st.title("🗂️ File Recovery and Optimization System")

# Select Directory
directory = st.text_input("📁 Enter the directory path:", "")

# Scan and analyze files
if st.button("🔍 Scan Directory"):
    if os.path.isdir(directory):
        st.success(f"Scanning directory: {directory}...")
        
        file_list = scan_directory(directory)
        st.write(f"✅ Total Files Found: {len(file_list)}")

        # Detect Duplicates
        duplicates = detect_duplicates(file_list)
        st.write(f"🗃️ Duplicates Found: {len(duplicates)}")
        if duplicates:
            st.write(duplicates)

        # Identify Large Files
        large_files = identify_large_files(file_list)
        st.write(f"📦 Large Files Found: {len(large_files)}")
        if large_files:
            st.write(large_files)

        # Recover Deleted Files (Placeholder)
        recovered_files = recover_files(directory)
        st.write(f"🔄 Recovered Files: {len(recovered_files)}")
        if recovered_files:
            st.write(recovered_files)

    else:
        st.error("❗ Please enter a valid directory path.")

# Optimization Options
st.sidebar.title("⚙️ File Optimization Options")
delete_duplicates = st.sidebar.button("🗑️ Delete Duplicates")
delete_large_files = st.sidebar.button("📉 Delete Large Files")

# Handle actions
if delete_duplicates and duplicates:
    for file in duplicates:
        os.remove(file)
    st.sidebar.success(f"✅ {len(duplicates)} duplicate files deleted.")

if delete_large_files and large_files:
    for file in large_files:
        os.remove(file)
    st.sidebar.success(f"✅ {len(large_files)} large files deleted.")
