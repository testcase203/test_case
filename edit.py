import json
import os
import subprocess
import tkinter as tk
from tkinter import messagebox

# Đọc dữ liệu từ file movies1.json
def read_movies(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return []

# Lưu dữ liệu vào file movies1.json và thực hiện lệnh git
def save_movies(file_path, movies):
    # Lưu vào file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)
    
    # Thực hiện các lệnh git
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', '"Update movies"'], check=True)
        subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)
        messagebox.showinfo("Thành công", "Dữ liệu đã được lưu và đẩy lên Git.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Lỗi Git", f"Đã xảy ra lỗi khi thực hiện Git: {e}")

# Thêm một bộ phim mới
def add_movie(movies, title, description, url, thumbnail):
    movie_id = max([movie['id'] for movie in movies], default=0) + 1
    new_movie = {
        "id": movie_id,
        "title": title,
        "description": description,
        "url": url,
        "thumbnail": thumbnail
    }
    movies.append(new_movie)

# Xoá một bộ phim theo id
def delete_movie(movies, movie_id):
    movies = [movie for movie in movies if movie['id'] != movie_id]
    return movies

# Cập nhật giao diện khi thêm hoặc xoá phim
def update_movie_list():
    movies = read_movies('movies1.json')
    listbox.delete(0, tk.END)
    for movie in movies:
        listbox.insert(tk.END, f"{movie['id']}: {movie['title']}")

# Thêm phim
def on_add_movie():
    title = title_entry.get()
    description = description_entry.get()
    url = url_entry.get()
    thumbnail = thumbnail_entry.get()
    
    if title and description and url and thumbnail:
        movies = read_movies('movies1.json')
        add_movie(movies, title, description, url, thumbnail)
        save_movies('movies1.json', movies)
        update_movie_list()
    else:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin.")

# Xoá phim
def on_delete_movie():
    selected_movie = listbox.curselection()
    if selected_movie:
        movie_id = int(listbox.get(selected_movie[0]).split(':')[0])
        movies = read_movies('movies1.json')
        updated_movies = delete_movie(movies, movie_id)
        save_movies('movies1.json', updated_movies)
        update_movie_list()
    else:
        messagebox.showwarning("Chọn phim", "Vui lòng chọn bộ phim để xoá.")

# Tạo giao diện người dùng
root = tk.Tk()
root.title("Quản lý Phim")

# Nhập thông tin phim
title_label = tk.Label(root, text="Tiêu đề:")
title_label.grid(row=0, column=0)
title_entry = tk.Entry(root)
title_entry.grid(row=0, column=1)

description_label = tk.Label(root, text="Mô tả:")
description_label.grid(row=1, column=0)
description_entry = tk.Entry(root)
description_entry.grid(row=1, column=1)

url_label = tk.Label(root, text="URL:")
url_label.grid(row=2, column=0)
url_entry = tk.Entry(root)
url_entry.grid(row=2, column=1)

thumbnail_label = tk.Label(root, text="Thumbnail:")
thumbnail_label.grid(row=3, column=0)
thumbnail_entry = tk.Entry(root)
thumbnail_entry.grid(row=3, column=1)

# Các nút
add_button = tk.Button(root, text="Thêm Phim", command=on_add_movie)
add_button.grid(row=4, column=0)

delete_button = tk.Button(root, text="Xoá Phim", command=on_delete_movie)
delete_button.grid(row=4, column=1)

save_button = tk.Button(root, text="Lưu và Đẩy lên Git", command=lambda: save_movies('movies1.json', read_movies('movies1.json')))
save_button.grid(row=5, column=0, columnspan=2)

# Danh sách phim
listbox = tk.Listbox(root, width=50, height=10)
listbox.grid(row=6, column=0, columnspan=2)

# Cập nhật danh sách phim
update_movie_list()

# Chạy ứng dụng
root.mainloop()
