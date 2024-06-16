import tkinter as tk
from tkinter import filedialog, Toplevel, Label, Button
from PIL import Image, ImageTk
from Cryptodome.PublicKey import RSA
from file_encryption import EncryptorFactory


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Ứng dụng mã hóa dữ liệu")
        self.geometry("600x600")  # Larger window size

        self.public_key = None
        self.private_key = None

        self.create_widgets()

    def create_widgets(self):
        # Load and display the image
        image_path = "res/441956724_1233076297664250_2744444318462441104_n.png"
        image = Image.open(image_path)
        image = image.resize((550, 250))
        self.photo = ImageTk.PhotoImage(image)

        self.image_label = tk.Label(self, image=self.photo)
        self.image_label.pack(pady=10)

        button_width = 20  # Width of the buttons
        button_height = 2  # Height of the buttons
        padding = 10  # Padding between buttons

        self.generate_keys_btn = tk.Button(self, text="Tạo cặp khóa", command=self.generate_keys,
                                           width=button_width, height=button_height, bg='lightblue', fg='black')
        self.generate_keys_btn.pack(pady=padding)

        self.save_keys_btn = tk.Button(self, text="Lưu trữ khóa", command=self.save_keys, state=tk.DISABLED,
                                       width=button_width, height=button_height, bg='lightgreen', fg='black')
        self.save_keys_btn.pack(pady=padding)

        self.load_keys_btn = tk.Button(self, text="Tải khóa RSA", command=self.load_keys,
                                       width=button_width, height=button_height, bg='lightcyan', fg='black')
        self.load_keys_btn.pack(pady=padding)

        self.encrypt_file_btn = tk.Button(self, text="Mã hóa File", command=self.encrypt_file,
                                          width=button_width, height=button_height, bg='lightcoral', fg='black')
        self.encrypt_file_btn.pack(pady=padding)

        self.decrypt_file_btn = tk.Button(self, text="Giải mã File", command=self.decrypt_file,
                                          width=button_width, height=button_height, bg='lightgoldenrodyellow', fg='black')
        self.decrypt_file_btn.pack(pady=padding)

    def generate_keys(self):
        key = RSA.generate(2048)
        self.public_key = key.publickey().export_key()
        self.private_key = key.export_key()

        self.show_custom_message("RSA Keys Generated", "RSA Public and Private keys have been generated.")
        self.save_keys_btn.config(state=tk.NORMAL)

    def save_keys(self):
        public_key_file = filedialog.asksaveasfilename(defaultextension=".pem", filetypes=[("PEM files", "*.pem")])
        if public_key_file:
            with open(public_key_file, 'wb') as f:
                f.write(self.public_key)

        private_key_file = filedialog.asksaveasfilename(defaultextension=".pem", filetypes=[("PEM files", "*.pem")])
        if private_key_file:
            with open(private_key_file, 'wb') as f:
                f.write(self.private_key)

        self.show_custom_message("Keys Saved", "RSA keys have been saved successfully.")

    def load_keys(self):
        key_file = filedialog.askopenfilename(filetypes=[("PEM files", "*.pem")])
        if key_file:
            with open(key_file, 'rb') as f:
                key_data = f.read()
                try:
                    rsa_key = RSA.import_key(key_data)
                    if rsa_key.has_private():
                        self.private_key = key_data
                        self.public_key = rsa_key.publickey().export_key()
                        self.show_custom_message("Keys Loaded", "Public and Private keys have been loaded successfully.")
                    else:
                        self.public_key = key_data
                        self.show_custom_message("Public Key Loaded", "Public key has been loaded successfully.")
                except ValueError as e:
                    self.show_custom_message("Invalid Key", "The selected file does not contain a valid RSA key.")

    def encrypt_file(self):
        if not self.public_key:
            self.load_keys()
            if not self.public_key:
                self.show_custom_message("No Public Key", "Please load or generate a public key before encrypting.")
                return

        input_file = filedialog.askopenfilename()
        if input_file:
            output_file = filedialog.asksaveasfilename(defaultextension=f".{input_file.split('.')[-1]}", filetypes=[("All files", "*.*")])
            if output_file:
                file_type = input_file.split('.')[-1]
                encryptor = EncryptorFactory.get_encryptor(file_type, self.public_key, self.private_key)
                encryptor.encrypt(input_file, output_file)
                self.show_custom_message("File Encrypted", f"File '{input_file}' has been encrypted and saved as '{output_file}'.")

    def decrypt_file(self):
        if not self.private_key:
            self.load_keys()
            if not self.private_key:
                self.show_custom_message("No Private Key", "Please load a private key before decrypting.")
                return

        input_file = filedialog.askopenfilename()
        if input_file:
            output_file = filedialog.asksaveasfilename(defaultextension=f".{input_file.split('.')[-1]}", filetypes=[("All files", "*.*")])
            if output_file:
                file_type = input_file.split('.')[-1]
                encryptor = EncryptorFactory.get_encryptor(file_type, self.public_key, self.private_key)
                encryptor.decrypt(input_file, output_file)
                self.show_custom_message("File Decrypted", f"File '{input_file}' has been decrypted and saved as '{output_file}'.")

    def show_custom_message(self, title, message):
        popup = Toplevel(self)
        popup.title(title)
        popup.geometry("300x150")
        label = Label(popup, text=message, pady=20)
        label.pack()
        button = Button(popup, text="OK", command=popup.destroy, width=10)
        button.pack(pady=10)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
