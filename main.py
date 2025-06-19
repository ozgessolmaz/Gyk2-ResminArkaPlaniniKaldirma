import cv2
import numpy as np
import tkinter as tk # Arayüz kütüphanesi
from tkinter import filedialog, messagebox 
from PIL import Image # Pillow kütüphanesi 

#Görsel seçme
def select_image():
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if path:
        process_image(path)

def process_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        messagebox.showerror("Hata", "Görsel okunamadı.")
        return

    h, w = img.shape[:2]
    rect = (1, 1, w-2, h-2)  # Tüm görsel neredeyse

    # GrabCut için hazırlık
    mask = np.zeros(img.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    # GrabCut çalıştır
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

    # Ön plan ve arka plan maskesi
    foreground_mask = (mask == 1) | (mask == 3)  # 1: probable foreground, 3: sure foreground

    # Beyaz zeminli görsel oluştur
    white_background = np.ones_like(img, dtype=np.uint8) * 255
    output = np.where(foreground_mask[:, :, np.newaxis], img, white_background)

    # Kaydetme
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        Image.fromarray(cv2.cvtColor(output, cv2.COLOR_BGR2RGB)).save(save_path)
        messagebox.showinfo("Başarılı", f"Arka plan beyaz yapıldı:\n{save_path}")
    else:
        messagebox.showwarning("İptal", "Kaydetme işlemi iptal edildi.")

    img = cv2.imread(image_path)
    if img is None:
        messagebox.showerror("Hata", "Görsel okunamadı.")
        return

    # Görüntü Boyutları
    h, w = img.shape[:2]
    rect = (int(w*0.1), int(h*0.1), int(w*0.8), int(h*0.8))

    # GrabCut Segmentasyonu
    mask = np.zeros(img.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0), 0, 255).astype("uint8")

    # Renk kanallarını RGBA olarak düzelt
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    r, g, b = cv2.split(img_rgb)
    alpha = mask2
    rgba = cv2.merge((r, g, b, alpha))

    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        Image.fromarray(rgba).save(save_path)
        messagebox.showinfo("Başarılı", f"PNG olarak kaydedildi:\n{save_path}")
    else:
        messagebox.showwarning("İptal", "Kaydetme işlemi iptal edildi.")

    img = cv2.imread(image_path)
    if img is None:
        messagebox.showerror("Hata", "Görsel okunamadı.")
        return

    # Görüntü Boyutları
    h, w = img.shape[:2]
    rect = (int(w*0.1), int(h*0.1), int(w*0.8), int(h*0.8))

    # GrabCut Segmentasyonu
    mask = np.zeros(img.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0), 0, 255).astype("uint8")

    b, g, r = cv2.split(img)
    alpha = mask2
    rgba = cv2.merge((b, g, r, alpha))

    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        Image.fromarray(rgba).save(save_path)
        messagebox.showinfo("Başarılı", f"PNG olarak kaydedildi:\n{save_path}")
    else:
        messagebox.showwarning("İptal", "Kaydetme işlemi iptal edildi.")

root = tk.Tk()
root.title("Arka Plan Kaldırma Uygulaması")
root.geometry("400x200")

label = tk.Label(root, text="Görsel seçin", wraplength=350)
label.pack(pady=20)

select_button = tk.Button(root, text="Görsel Seç", command=select_image, width=20, height=2, bg="lightblue")
select_button.pack()

root.mainloop()
