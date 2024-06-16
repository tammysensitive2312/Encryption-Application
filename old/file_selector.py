import tkinter as tk
from tkinter import filedialog, ttk
from functools import partial
from rsa_cript import RSA_CRIPT
from file_encryption import EncryptorFactory
from utils import public, private


class FileSelector:
    def __init__(self, root_):
        self.file_path_key_public = None
        self.file_path_key_private = None
        self.key_key_public = None
        self.key_key_private = None
        self.locations_key = ["2048", "4096"]
        self.locations_key_public = []
        self.locations_key_private = []
        self.from_key = None
        self.ma_key_public = None
        self.ma_them_key_public = None
        self.ma_ban_ro = None
        self.ma_ban_ma = None
        self.giai_key_private = None
        self.giai_ban_ma = None
        self.giai_ban_giai = None
        self.giai_them_key_private = None
        self.file_type_var = tk.StringVar()  # Variable to hold file type
        self.root = root_
        self.file_path_open = tk.StringVar()
        self.file_path_save = tk.StringVar()
        self.file_name = tk.StringVar()
        self.rsa_public_key = None  # Thêm biến lưu trữ khóa công khai
        self.rsa_private_key = None  # Thêm biến lưu trữ khóa riêng tư
        self.main_ui()
        self.set_key()

    def set_key(self):
        try:
            for i in public:
                if len(i) > 1:
                    self.locations_key_public.append(i[1])
                else:
                    print(f"Warning: public key entry {i} does not have enough elements.")

            for i in private:
                if len(i) > 1:
                    self.locations_key_private.append(i[1])
                else:
                    print(f"Warning: private key entry {i} does not have enough elements.")
        except Exception as e:
            print(f"Error setting keys: {e}")

    def main_ui(self):
        self.root.geometry("600x700")
        self.root.title("Ứng dụng mã hóa dữ liệu")
        tk.Label(self.root, text="Ứng dụng mã hóa dữ liệu", font=("Arial Bold", 25)).pack(padx=5, pady=10)
        tk.Button(self.root, text="Create key", fg="red", font=("Arial", 20), command=self.create_key_window).pack(
            padx=5, pady=10)
        tk.Button(self.root, text="Mã hóa", fg="blue", font=("Arial", 20), command=self.ma_hoa_window).pack(padx=5,
                                                                                                            pady=10)
        tk.Button(self.root, text="Giải mã", fg="green", font=("Arial", 20), command=self.giai_ma_window).pack(padx=5,
                                                                                                               pady=10)
        tk.Label(self.root, text="Chọn loại tệp:").pack(padx=5, pady=5)
        ttk.Combobox(self.root, textvariable=self.file_type_var, values=["docx", "pdf", "wav", "csv", "png"],
                     width=37).pack(padx=5, pady=5)

    def create_key_window(self):
        key_window = tk.Toplevel(self.root)
        key_window.title("Create key")
        key_window.geometry("500x200")

        tk.Label(key_window, text="Chọn độ dài khóa:").grid(row=0, column=0, padx=5, pady=5)
        self.from_key = ttk.Combobox(key_window, values=self.locations_key, width=37)
        self.from_key.grid(row=0, column=1, pady=5)

        self.file_path_key_public = tk.StringVar()
        self.file_path_key_private = tk.StringVar()

        tk.Label(key_window, text="Xuất khóa công khai:").grid(row=2, column=0, padx=5, pady=5)
        self.key_key_public = tk.Entry(key_window, width=40)
        self.key_key_public.grid(row=2, column=1, pady=5)
        tk.Button(key_window, text="Chọn nơi lưu",
                  command=partial(self.save_file, self.key_key_public, 'Key file', 'pem')).grid(row=2, column=2, padx=5,
                                                                                                pady=5)

        tk.Label(key_window, text="Xuất khóa riêng tư:").grid(row=3, column=0, padx=5, pady=5)
        self.key_key_private = tk.Entry(key_window, width=40)
        self.key_key_private.grid(row=3, column=1, pady=5)
        tk.Button(key_window, text="Chọn nơi lưu",
                  command=partial(self.save_file, self.key_key_private, 'Key file', 'pem')).grid(row=3, column=2,
                                                                                                 padx=5, pady=5)

        tk.Button(key_window, text="Tạo khóa", command=self.create_key).grid(row=4, column=1, pady=5, padx=5)

    def create_key(self):
        rsa = RSA_CRIPT()
        rsa.eport_key(int(self.from_key.get()), self.key_key_public.get(), self.key_key_private.get())

        # Lưu khóa công khai và riêng tư vào biến của lớp
        with open(self.key_key_public.get(), 'r') as f:
            self.rsa_public_key = f.read()

        with open(self.key_key_private.get(), 'r') as f:
            self.rsa_private_key = f.read()

        self.done_window("Tạo khóa thành công!", 1)

    def ma_hoa_window(self):
        ma_window = tk.Toplevel(self.root)
        ma_window.title('Mã hóa')
        ma_window.geometry("500x250")

        tk.Label(ma_window, text="Chọn khóa công khai:").grid(row=0, column=0, padx=5, pady=5)
        self.ma_key_public = ttk.Combobox(ma_window, values=self.locations_key_public)
        self.ma_key_public.grid(row=0, column=1, pady=5)

        tk.Label(ma_window, text="Thêm khóa công khai:").grid(row=2, column=0, padx=5, pady=5)
        self.ma_them_key_public = tk.Entry(ma_window, width=40)
        self.ma_them_key_public.grid(row=2, column=1, pady=5)
        tk.Button(ma_window, text=" ...  ",
                  command=partial(self.open_file, self.ma_them_key_public, 'Key file', 'pem')).grid(row=2, column=2,
                                                                                                    padx=5, pady=5)

        tk.Label(ma_window, text="Thêm bản rõ").grid(row=3, column=0, padx=5, pady=5)
        self.ma_ban_ro = tk.Entry(ma_window, width=40)
        self.ma_ban_ro.grid(row=3, column=1, pady=5)
        tk.Button(ma_window, text=" ...  ", command=self.open_file_for_content).grid(row=3, column=2, padx=5, pady=5)

        tk.Label(ma_window, text="Xuất bản mã").grid(row=4, column=0, padx=5, pady=5)
        self.ma_ban_ma = tk.Entry(ma_window, width=40)
        self.ma_ban_ma.grid(row=4, column=1, pady=5)
        tk.Button(ma_window, text="Chọn nơi lưu", command=self.save_file_for_output).grid(row=4, column=2, padx=5,
                                                                                          pady=5)

        tk.Button(ma_window, text="Mã hóa", command=self.ma_hoa).grid(row=5, column=1, pady=5, padx=5)

    def save_file_for_output(self):
        file_type = self.file_type_var.get()
        if file_type == "pdf":
            file_path_ = filedialog.asksaveasfilename(filetypes=[("PDF files", "*.pdf")])
        elif file_type == "wav":
            file_path_ = filedialog.asksaveasfilename(filetypes=[("WAV files", "*.wav")])
        elif file_type == "csv":
            file_path_ = filedialog.asksaveasfilename(filetypes=[("CSV files", "*.csv")])
        elif file_type == "png":
            file_path_ = filedialog.asksaveasfilename(filetypes=[("Encrypted Image files", "*.dat")])
        else:
            file_path_ = filedialog.asksaveasfilename(filetypes=[("All files", "*.*")])

        if file_path_:
            self.ma_ban_ma.delete(0, tk.END)  # Clear the current content of the entry
            self.ma_ban_ma.insert(0, file_path_)  # Insert the selected file path into the entry

    def open_file_for_content(self):
        file_type = self.file_type_var.get()
        if file_type == "pdf":
            file_path_ = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        elif file_type == "wav":
            file_path_ = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        elif file_type == "csv":
            file_path_ = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        elif file_type == "png":
            file_path_ = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])
        else:
            file_path_ = filedialog.askopenfilename()

        if file_path_:
            self.ma_ban_ro.delete(0, tk.END)  # Clear the current content of the entry
            self.ma_ban_ro.insert(0, file_path_)  # Insert the selected file path into the entry

    def ma_hoa(self):
        file_type = self.file_type_var.get()
        key_public_path = self.ma_key_public.get()
        additional_key_path = self.ma_them_key_public.get()
        input_file_path = self.ma_ban_ro.get()
        output_file_path = self.ma_ban_ma.get()

        if not file_type or not key_public_path or not input_file_path or not output_file_path:
            self.done_window("Vui lòng điền đầy đủ thông tin!", 0)
            return

        if additional_key_path:
            with open(additional_key_path, 'r') as f:
                key_public = f.read()
        else:
            for i in public:
                if i[1] == key_public_path:
                    key_public = i[2]
                    break

        encryptor = EncryptorFactory.get_encryptor(file_type, input_file_path, key_public, self.rsa_private_key)
        if file_type == "docx":
            encryptor.RSA_Ma_Hoa_key(key_public, input_file_path, output_file_path)
        else:
            encryptor.encrypt(input_file_path, output_file_path)
        self.done_window("Mã hóa thành công!", 1)

    def giai_ma_window(self):
        giai_window = tk.Toplevel(self.root)
        giai_window.title('Giải mã')
        giai_window.geometry("500x250")

        tk.Label(giai_window, text="Chọn khóa bí mật:").grid(row=0, column=0, padx=5, pady=5)
        self.giai_key_private = ttk.Combobox(giai_window, values=self.locations_key_private)
        self.giai_key_private.grid(row=0, column=1, pady=5)

        tk.Label(giai_window, text="Thêm khóa khóa bí mật:").grid(row=2, column=0, padx=5, pady=5)
        self.giai_them_key_private = tk.Entry(giai_window, width=40)
        self.giai_them_key_private.grid(row=2, column=1, pady=5)
        tk.Button(giai_window, text=" ...  ",
                  command=partial(self.open_file, self.giai_them_key_private, 'Key file', 'pem')).grid(row=2, column=2,
                                                                                                       padx=5, pady=5)

        tk.Label(giai_window, text="Thêm bản mã").grid(row=3, column=0, padx=5, pady=5)
        self.giai_ban_ma = tk.Entry(giai_window, width=40)
        self.giai_ban_ma.grid(row=3, column=1, pady=5)
        tk.Button(giai_window, text=" ...  ", command=self.open_file_for_cipher).grid(row=3, column=2, padx=5, pady=5)

        tk.Label(giai_window, text="Xuất bản rõ").grid(row=4, column=0, padx=5, pady=5)
        self.giai_ban_giai = tk.Entry(giai_window, width=40)
        self.giai_ban_giai.grid(row=4, column=1, pady=5)
        tk.Button(giai_window, text="Chọn nơi lưu",
                  command=partial(self.save_file, self.giai_ban_giai, 'Word file', 'docx')).grid(row=4, column=2,
                                                                                                 padx=5, pady=5)

        tk.Button(giai_window, text="Giải mã", command=self.giai_ma).grid(row=5, column=1, pady=5, padx=5)

    def open_file_for_cipher(self):
        file_type = self.file_type_var.get()
        file_path_ = filedialog.askopenfilename(filetypes=[("All files", "*.*")])

        if file_path_:
            self.giai_ban_ma.delete(0, tk.END)  # Clear the current content of the entry
            self.giai_ban_ma.insert(0, file_path_)  # Insert the selected file path into the entry

    def giai_ma(self):
        file_type = self.file_type_var.get()
        key_private_path = self.giai_key_private.get()
        additional_key_path = self.giai_them_key_private.get()
        input_file_path = self.giai_ban_ma.get()
        output_file_path = self.giai_ban_giai.get()

        if not file_type or not key_private_path or not input_file_path or not output_file_path:
            self.done_window("Vui lòng điền đầy đủ thông tin!", 0)
            return

        if additional_key_path:
            with open(additional_key_path, 'r') as f:
                key_private = f.read()
        else:
            for i in private:
                if i[1] == key_private_path:
                    key_private = i[2]
                    break

        decryptor = EncryptorFactory.get_encryptor(file_type, input_file_path, self.rsa_public_key, key_private)
        if file_type == "docx":
            decryptor.RSA_Giai_Ma_Key(input_file_path, output_file_path, key_private)
        else:
            decryptor.decrypt(input_file_path, output_file_path)
        self.done_window("Giải mã thành công!", 1)

    @staticmethod
    def open_file(entry, title, duoi):
        file_path_ = filedialog.askopenfilename(filetypes=[(title, "*." + duoi)])
        if file_path_:
            entry.delete(0, tk.END)  # Xóa nội dung hiện tại trong entry
            entry.insert(0, file_path_)  # Chèn đường dẫn đã chọn vào entry

    @staticmethod
    def save_file(entry, title, duoi):
        file_path_ = filedialog.asksaveasfilename(filetypes=[(title, "*." + duoi)])
        if file_path_:  # Kiểm tra xem người dùng đã chọn hay chưa
            entry.delete(0, tk.END)  # Xóa nội dung hiện tại trong entry
            entry.insert(0, file_path_)  # Chèn đường dẫn đã chọn vào entry

    def done_window(self, string, color):
        done = tk.Toplevel(self.root)
        done.title("Done")
        done.geometry("500x80")
        if color == 0:
            tk.Label(done, text=string, fg="red", font=("Arial", 20)).pack(pady=20)
        else:
            tk.Label(done, text=string, fg="green", font=("Arial", 20)).pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    FileSelector(root)
    root.mainloop()
