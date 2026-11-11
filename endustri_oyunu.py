import tkinter as tk
from tkinter import messagebox
import random

class MukemmelEndustriOyunu:
    def __init__(self, root):
        self.root = root
        self.root.title("Endüstri Mühendisliği - Yay & Soru Modülü")
        self.root.geometry("680x750")
        self.root.configure(bg="#0f172a")

        self.score = 0
        self.hearts = 5  # İstediğin gibi toplam can hakkı 5 yapıldı
        self.wrong_count = 0  # Yapılan yanlış sayısı
        self.etap = 1
        self.max_etap = 6
        self.remaining_seconds = 591  # 09:51
        
        # Yay hareket mekaniği
        self.bow_y = 150
        self.bow_direction = 3
        self.is_running = True

        # Soru havuzu
        self.all_questions = [
            {
                "q": "Üretim hattında darboğazı (bottleneck) çözmek için ilk ne yapılır?",
                "options": ["En yavaş istasyon optimize edilir", "Tüm makineler yenilenir", "İşçi sayısı azaltılır", "Mesai kaldırılır"],
                "correct": 0
            },
            {
                "q": "Aşağıdakilerden hangisi bir Yöneylem Araştırması tekniğidir?",
                "options": ["Doğrusal Programlama", "HTML Kodlama", "Bilanço Çıkarma", "Peyzaj Düzenleme"],
                "correct": 0
            },
            {
                "q": "Stok maliyetlerini minimize etmek için hangi model sıkça kullanılır?",
                "options": ["EOQ (Ekonomik Sipariş Miktarı)", "SWOT Analizi", "Gantt Şeması", "Monte Carlo"],
                "correct": 0
            },
            {
                "q": "İş etüdünde 'Kronometre Etüdü' ne amaçla yapılır?",
                "options": ["Standart zamanı saptamak", "Fabrika boyasını seçmek", "Pazarlama bütçesi hazırlamak", "Müşteri memnuniyeti ölçmek"],
                "correct": 0
            },
            {
                "q": "Toplam Kalite Yönetimi'nin temel odak noktası nedir?",
                "options": ["Müşteri memnuniyeti ve sürekli iyileştirme", "Sadece üretimi durdurmak", "Maliyetleri artırmak", "Denetimden kaçmak"],
                "correct": 0
            },
            {
                "q": "Tedarik zinciri yönetiminde 'Just-In-Time' (Tam Zamanında Üretim) sisteminin ana hedefi nedir?",
                "options": ["Stok seviyelerini sıfıra yakın tutmak", "Depo alanını büyütmek", "Üretimi yavaşlatmak", "Çalışan sayısını artırmak"],
                "correct": 0
            },
            {
                "q": "Ergonomi bilimi çalışma ortamında neyi amaçlar?",
                "options": ["İşçinin fizyolojik ve psikolojik uyumunu sağlamak", "Fabrika maliyetlerini iki katına çıkarmak", "Çalışma saatlerini uzatmak", "Makineleri ortadan kaldırmak"],
                "correct": 0
            }
        ]
        self.questions = []
        self.prepare_questions()

        self.create_game_layout()
        self.start_timer()
        self.animate_bow()

    def prepare_questions(self):
        self.questions = list(self.all_questions)
        random.shuffle(self.questions)
        self.current_q_index = 0

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            if widget != getattr(self, 'top_frame', None):
                widget.destroy()

    def create_game_layout(self):
        # Üst Sabit Bar
        self.top_frame = tk.Frame(self.root, bg="#1e293b", height=45)
        self.top_frame.pack(fill="x", padx=15, pady=10)

        self.heart_label = tk.Label(self.top_frame, text=f"❤️ Can: {self.hearts}", font=("Segoe UI", 12, "bold"), fg="#ef4444", bg="#1e293b")
        self.heart_label.pack(side="left", padx=15)

        self.score_label = tk.Label(self.top_frame, text=f"Puan: {self.score}", font=("Segoe UI", 12, "bold"), fg="#f472b6", bg="#1e293b")
        self.score_label.pack(side="left", padx=20)

        self.time_label = tk.Label(self.top_frame, text="Süre: 09:51", font=("Segoe UI", 11, "bold"), fg="#f472b6", bg="#1e293b")
        self.time_label.pack(side="right", padx=15)

        self.show_archery_screen()

    def start_timer(self):
        def update_time():
            if self.remaining_seconds > 0 and self.is_running:
                self.remaining_seconds -= 1
                m = self.remaining_seconds // 60
                s = self.remaining_seconds % 60
                self.time_label.config(text=f"Süre: {m:02d}:{s:02d}")
                self.root.after(1000, update_time)
        update_time()

    def show_archery_screen(self):
        self.clear_widgets()

        # Canvas Alanı
        self.canvas = tk.Canvas(self.root, width=620, height=320, bg="#1e293b", highlightthickness=0)
        self.canvas.pack(padx=15, pady=10)
        self.draw_scene(75, self.bow_y)

        # Etap ve Yönerge Çerçevesi
        info_frame = tk.Frame(self.root, bg="#1e293b", bd=1, relief="solid")
        info_frame.pack(fill="x", padx=15, pady=10)

        etap_title = tk.Label(info_frame, text=f"📍 ETAP {self.etap}/{self.max_etap}", font=("Segoe UI", 12, "bold"), fg="#f472b6", bg="#1e293b")
        etap_title.pack(anchor="w", padx=15, pady=5)

        instruction = tk.Label(info_frame, text="🎯 Harekete geçen potaya karşı yayın konumunu bekle\n(Oku Fırlat butonuna basarak okun hedefe gidişini izle)", font=("Segoe UI", 10), fg="#cbd5e1", bg="#1e293b", justify="left")
        instruction.pack(anchor="w", padx=15, pady=5)

        # Oku Fırlat Butonu (Pembe)
        shoot_btn = tk.Button(self.root, text="🏹 Oku Fırlat", font=("Segoe UI", 13, "bold"), bg="#db2777", fg="white", bd=0, padx=20, pady=10, command=self.fire_arrow)
        shoot_btn.pack(pady=15)

        self.root.bind("<space>", lambda event: self.fire_arrow())

    def draw_scene(self, arrow_x, arrow_y):
        self.canvas.delete("all")
        
        self.canvas.create_line(20, 30, 600, 30, dash=(4, 4), fill="#475569")
        self.canvas.create_line(20, 290, 600, 290, dash=(4, 4), fill="#475569")

        # Hedef Pota
        self.canvas.create_oval(500, 110, 580, 190, fill="#ef4444", outline="white", width=2)
        self.canvas.create_oval(520, 130, 560, 170, fill="#ffffff", outline="")
        self.canvas.create_oval(532, 142, 548, 158, fill="#db2777", outline="")
        self.canvas.create_text(540, 90, text="HEDEF POTA", fill="#f8fafc", font=("Segoe UI", 9, "bold"))

        # Yay
        self.canvas.create_arc(50, arrow_y - 40, 100, arrow_y + 40, start=270, extent=180, style="arc", outline="#db2777", width=5)
        
        # Ok Uçuşu
        self.canvas.create_line(arrow_x, arrow_y, arrow_x + 65, arrow_y, fill="#f8fafc", width=3)
        self.canvas.create_polygon(arrow_x + 60, arrow_y - 5, arrow_x + 70, arrow_y, arrow_x + 60, arrow_y + 5, fill="#f472b6")

    def animate_bow(self):
        if self.is_running:
            self.bow_y += self.bow_direction
            if self.bow_y > 220:
                self.bow_direction = -3
            elif self.bow_y < 80:
                self.bow_direction = 3
            
            try:
                if hasattr(self, 'canvas') and self.canvas.winfo_exists():
                    self.draw_scene(75, self.bow_y)
            except:
                pass
            
            self.root.after(30, self.animate_bow)

    def fire_arrow(self):
        start_x = 75
        target_x = 510
        current_y = self.bow_y

        def fly(x):
            if x < target_x:
                self.draw_scene(x, current_y)
                self.root.after(15, lambda: fly(x + 35))
            else:
                if 120 <= current_y <= 180:
                    self.score += 50
                    self.score_label.config(text=f"Puan: {self.score}")
                    messagebox.showinfo("Başarılı!", "🎯 12'den vurdun! Şimdi Mühendislik Sorusu geliyor.")
                    self.show_question_screen()
                else:
                    # Atış kaçınca anında can düşmüyor, sadece yanlış sayılıyor veya devam ediliyor
                    messagebox.showwarning("⚠️ DİKKAT!", "Oku kaçırdın ama oyun devam ediyor! Açıyı iyi ayarla.")
                    self.show_archery_screen()

        fly(start_x)

    def show_question_screen(self):
        self.clear_widgets()

        q_data = self.questions[self.current_q_index % len(self.questions)]

        # Pembe Soru Paneli
        q_frame = tk.Frame(self.root, bg="#831843", bd=1, relief="solid")
        q_frame.pack(fill="x", padx=25, pady=20)

        q_title = tk.Label(q_frame, text=f"🌸 Mühendislik Sorusu (Etap {self.etap}):\n{q_data['q']}", font=("Segoe UI", 12, "bold"), fg="#fce7f3", bg="#831843", wraplength=600, justify="left")
        q_title.pack(padx=20, pady=20)

        for idx, opt in enumerate(q_data["options"]):
            btn = tk.Button(self.root, text=opt, font=("Segoe UI", 11), bg="#9d174d", fg="#fdf2f8", activebackground="#be185d", activeforeground="white", bd=0, anchor="w", padx=20, pady=12, command=lambda i=idx: self.check_answer(i, q_data["correct"]))
            btn.pack(fill="x", padx=25, pady=6)

    def check_answer(self, selected, correct):
        if selected == correct:
            self.score += 30
            messagebox.showinfo("Tebrikler!", "✔ Doğru Cevap! Harika ilerliyorsun.")
        else:
            self.wrong_count += 1
            # 3 yanlış yapıldığında can düşer
            if self.wrong_count >= 3:
                self.hearts -= 1
                self.wrong_count = 0  # Sayacı sıfırla
                self.heart_label.config(text=f"❤️ Can: {self.hearts}")
                messagebox.showerror("⚠️ 3 YANLIŞ OLDU!", f"3 kez yanlış yaptığın için 1 canın düştü!\nKalan Can Hakkın: {self.hearts}")
            else:
                messagebox.showwarning("⚠️ YANLIş CEVAP!", f"Yanlış cevap verdin! (Toplam Yanlış: {self.wrong_count}/3)")

        self.current_q_index += 1
        self.etap += 1

        # Eğer canlar 5'ten bittiyse veya etaplar dolduysa oyun biter
        if self.etap > self.max_etap or self.hearts <= 0:
            self.show_game_over()
        else:
            self.show_archery_screen()

    def show_game_over(self):
        self.clear_widgets()
        self.is_running = False

        over_frame = tk.Frame(self.root, bg="#1e293b", bd=2, relief="solid")
        over_frame.pack(fill="both", expand=True, padx=30, pady=30)

        title = tk.Label(over_frame, text="✨ OYUN TAMAMLANDI ✨", font=("Segoe UI", 20, "bold"), fg="#f472b6", bg="#1e293b")
        title.pack(pady=20)

        final_text = tk.Label(over_frame, text=f"Toplam Skorun: {self.score}\nUlaşılan Etap: {self.etap - 1}/{self.max_etap}", font=("Segoe UI", 13), fg="#f8fafc", bg="#1e293b")
        final_text.pack(pady=10)

        chat_box = tk.Label(over_frame, text="❤️ Canların Durum Değerlendirmesi:\n\n"
                                             '• Can 1: "Soruları ve atışları büyük bir dikkatle yönetti!"\n'
                                             '• Can 2: "Pembe temalı bu serüveni harika tamamladık!"', 
                            font=("Segoe UI", 11), fg="#cbd5e1", bg="#1e293b", justify="left")
        chat_box.pack(pady=15)

        # Yeniden oynamak ister misiniz sorusu
        ask_label = tk.Label(over_frame, text="Oyunu yeniden oynamak ister misin?", font=("Segoe UI", 12, "bold"), fg="#fce7f3", bg="#1e293b")
        ask_label.pack(pady=10)

        btn_frame = tk.Frame(over_frame, bg="#1e293b")
        btn_frame.pack(pady=10)

        yes_btn = tk.Button(btn_frame, text="Evet (Yeniden Başla) 🔄", font=("Segoe UI", 11, "bold"), bg="#db2777", fg="white", bd=0, padx=15, pady=8, command=self.restart_game)
        yes_btn.pack(side="left", padx=10)

        no_btn = tk.Button(btn_frame, text="Hayır (Çıkış) ❌", font=("Segoe UI", 11, "bold"), bg="#475569", fg="white", bd=0, padx=15, pady=8, command=self.root.quit)
        no_btn.pack(side="right", padx=10)

    def restart_game(self):
        self.score = 0
        self.hearts = 5
        self.wrong_count = 0
        self.etap = 1
        self.remaining_seconds = 591
        self.is_running = True
        self.prepare_questions()  # Soruları yeniden karıştır
        self.create_game_layout()
        self.animate_bow()

if __name__ == "__main__":
    root = tk.Tk()
    app = MukemmelEndustriOyunu(root)
    root.mainloop()

