
import os
import csv
import tkinter as tk
from tkinter import messagebox
from collections import defaultdict
from datetime import datetime

fereastra = tk.Tk()
fereastra.title("Asistent Concurs Method Feeder v7.4 - Final Pro")
fereastra.geometry("580x880")
fereastra.configure(bg="#e6f2ff")

date_pescari = []
index_in_editare = None
ultimul_fisier_salvat = None

def actualizeaza_numarator():
    unic_echipe = len(set(p["echipa"] for p in date_pescari if p["echipa"]))
    eticheta_numarator.config(text=f"Pescari: {len(date_pescari)} | Echipe: {unic_echipe}")
    
    if date_pescari:
        captura = max(date_pescari, key=lambda x: x["peste_mare"])
        if captura["peste_mare"] > 0:
            eticheta_cmmc.config(text=f"🏆 CMMC Curent: {captura['nume']} ({captura['echipa']}) - {captura['peste_mare']:.2f} kg [{captura['sector']}{captura['stand']}]")
        else:
            eticheta_cmmc.config(text="🏆 CMMC Curent: Niciun pește înregistrat")
    else:
        eticheta_cmmc.config(text="🏆 CMMC Curent: -")

def adauga_sau_salveaza_modificare():
    global index_in_editare
    
    echipa = intrare_echipa.get().strip()
    nume = intrare_nume.get().strip()
    sector = intrare_sector.get().strip().upper()
    stand = intrare_stand.get().strip()
    total_kg = intrare_kg.get().strip()
    peste_mare = intrare_peste_mare.get().strip()
    
    if not echipa or not nume or not sector or not stand or not total_kg or not peste_mare:
        messagebox.showwarning("Atenție", "Completează toate câmpurile!")
        return
    
    try:
        val_stand = int(stand)
        val_kg = float(total_kg)
        val_cmmc = float(peste_mare)
        
        # Verificare dublură pe sector și stand (doar dacă nu suntem în editare)
        if index_in_editare is None:
            for p in date_pescari:
                if p["sector"] == sector and p["stand"] == val_stand:
                    messagebox.showwarning("Atentie", f"Standul {sector}{val_stand} este deja ocupat de {p['nume']}!")
                    return
        
        date_pescar = {
            "echipa": echipa,
            "nume": nume,
            "sector": sector,
            "stand": val_stand,
            "kg": val_kg,
            "peste_mare": val_cmmc
        }
        
        text_afisat = f"[{echipa}] {nume} ({sector}{val_stand}) - {val_kg} kg | CMMC: {val_cmmc} kg"
        
        if index_in_editare is None:
            date_pescari.append(date_pescar)
            lista_afisare.insert(tk.END, text_afisat)
        else:
            date_pescari[index_in_editare] = date_pescar
            lista_afisare.delete(index_in_editare)
            lista_afisare.insert(index_in_editare, text_afisat)
            
            index_in_editare = None
            buton_adauga.config(text="➕ Adaugă Pescar", bg="#28a745")
        
        goleste_campuri()
        actualizeaza_numarator()
        
    except ValueError:
        messagebox.showerror("Eroare", "Standul și greutățile trebuie să fie numere valide!")

def incarca_pentru_modificare():
    global index_in_editare
    
    selectie = lista_afisare.curselection()
    if not selectie:
        messagebox.showwarning("Atenție", "Selectează un pescar din listă pentru a-l modifica!")
        return
    
    index_in_editare = selectie[0]
    pescar = date_pescari[index_in_editare]
    
    goleste_campuri()
    intrare_echipa.insert(0, pescar["echipa"])
    intrare_nume.insert(0, pescar["nume"])
    intrare_sector.insert(0, pescar["sector"])
    intrare_stand.insert(0, pescar["stand"])
    intrare_kg.insert(0, pescar["kg"])
    intrare_peste_mare.insert(0, pescar["peste_mare"])
    
    buton_adauga.config(text="💾 Salvează Modificarea", bg="#ffc107")

def sterge_pescar():
    global index_in_editare
    
    selectie = lista_afisare.curselection()
    if not selectie:
        messagebox.showwarning("Atenție", "Selectează un pescar din listă pentru a-l șterge!")
        return
    
    index = selectie[0]
    del date_pescari[index]
    lista_afisare.delete(index)
    
    if index_in_editare == index:
        index_in_editare = None
        goleste_campuri()
        buton_adauga.config(text="➕ Adaugă Pescar", bg="#28a745")
        
    actualizeaza_numarator()

def concurs_nou():
    global index_in_editare
    if not date_pescari:
        return
    
    if messagebox.askyesno("Concurs Nou", "Ești sigur că vrei să ștergi toți pescarii și să începi un concurs nou?"):
        date_pescari.clear()
        lista_afisare.delete(0, tk.END)
        goleste_campuri()
        index_in_editare = None
        buton_adauga.config(text="➕ Adaugă Pescar", bg="#28a745")
        actualizeaza_numarator()

def goleste_campuri():
    intrare_echipa.delete(0, tk.END)
    intrare_nume.delete(0, tk.END)
    intrare_sector.delete(0, tk.END)
    intrare_stand.delete(0, tk.END)
    intrare_kg.delete(0, tk.END)
    intrare_peste_mare.delete(0, tk.END)

def salveaza_si_genereaza():
    global ultimul_fisier_salvat
    
    if not date_pescari:
        messagebox.showwarning("Atenție", "Nu ai adăugat niciun pescar!")
        return
    
    titlu_concurs = intrare_titlu_concurs.get().strip() or "Concurs Method Feeder"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nume_fisier_txt = f"rezultate_concurs_{timestamp}.txt"
    nume_fisier_csv = f"rezultate_concurs_{timestamp}.csv"
    ultimul_fisier_salvat = nume_fisier_txt
    
    # 1. Calcul Clasament per Sector
    sectoare = defaultdict(list)
    for p in date_pescari:
        sectoare[p["sector"]].append(p)
    
    clasament_sectoare = {}
    for nume_sector, pescari_sector in sectoare.items():
        pescari_sortati = sorted(pescari_sector, key=lambda x: x["kg"], reverse=True)
        for loc, p in enumerate(pescari_sortati, start=1):
            p["puncte_sector"] = loc
        clasament_sectoare[nume_sector] = pescari_sortati

    # 2. Calcul Clasament ECHIPE (Puncte -> Kg)
    echipe_dict = defaultdict(lambda: {"puncte_totale": 0, "kg_totale": 0, "membri": []})
    for p in date_pescari:
        nume_eq = p["echipa"]
        echipe_dict[nume_eq]["puncte_totale"] += p["puncte_sector"]
        echipe_dict[nume_eq]["kg_totale"] += p["kg"]
        echipe_dict[nume_eq]["membri"].append(p)

    clasament_echipe = sorted(
        echipe_dict.items(),
        key=lambda x: (x[1]["puncte_totale"], -x[1]["kg_totale"])
    )

    captura = max(date_pescari, key=lambda x: x["peste_mare"])
    
    # --- RAPORT TEXT ---
    with open(nume_fisier_txt, "w", encoding="utf-8") as f:
        f.write("==================================================\n")
        f.write(f"   🎣 {titlu_concurs.upper()} 🎣\n")
        f.write(f"   Data Salvării: {datetime.now().strftime('%d.%m.%Y - %H:%M')}\n")
        f.write("==================================================\n\n")
        
        for nume_sector, pescari in sorted(clasament_sectoare.items()):
            f.write(f"--- SECTORUL {nume_sector} ---\n")
            for p in pescari:
                f.write(f"  Locul {p['puncte_sector']}: {p['nume']} ({p['echipa']}) - Stand {p['stand']} - {p['kg']:.2f} kg [CMMC: {p['peste_mare']:.2f} kg]\n")
            f.write("\n")
            
        f.write("==================================================\n")
        f.write("🏆 CLASAMENT GENERAL ECHIPE (Puncte Sector -> Kg Totale):\n")
        f.write("==================================================\n")
        for loc, (nume_eq, date_eq) in enumerate(clasament_echipe, start=1):
            f.write(f"  LOCUL {loc}: {nume_eq} -> {date_eq['puncte_totale']} pct. total ({date_eq['kg_totale']:.2f} kg total)\n")
            for m in date_eq["membri"]:
                f.write(f"      - {m['nume']} (Sector {m['sector']}, Stand {m['stand']}): Locul {m['puncte_sector']} ({m['kg']:.2f} kg)\n")
            f.write("\n")
            
        f.write("==================================================\n")
        f.write("🏆 CAPTURA CONCURSULUI (CMMC):\n")
        f.write(f"  Câștigător: {captura['nume']} ({captura['echipa']}) - Sector {captura['sector']}, Stand {captura['stand']} -> {captura['peste_mare']:.2f} kg\n")
        f.write("==================================================\n")
        
    # --- EXPORT EXCEL (.csv) ---
    with open(nume_fisier_csv, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Concurs", titlu_concurs])
        writer.writerow(["Echipa", "Nume Pescar", "Sector", "Stand", "Total Kg", "CMMC", "Loc Sector"])
        for p in date_pescari:
            writer.writerow([p["echipa"], p["nume"], p["sector"], p["stand"], p["kg"], p["peste_mare"], p["puncte_sector"]])

    messagebox.showinfo("Succes", f"Clasamentul pentru '{titlu_concurs}' a fost salvat în TXT și Excel!")

def deschide_fisier():
    if ultimul_fisier_salvat and os.path.exists(ultimul_fisier_salvat):
        os.startfile(ultimul_fisier_salvat)
    else:
        messagebox.showwarning("Atenție", "Nu există niciun raport generat recent. Apasă pe Salvează!")

def deschide_folder():
    os.startfile(os.getcwd())

# --- INTERFAȚA GRAFICĂ ---
titlu = tk.Label(fereastra, text="🎣 Concurs Method Feeder", font=("Arial", 14, "bold"), bg="#e6f2ff", fg="#003366")
titlu.pack(pady=8)

cadru_titlu = tk.Frame(fereastra, bg="#e6f2ff")
cadru_titlu.pack(pady=2)
tk.Label(cadru_titlu, text="Nume Concurs / Balta:", bg="#e6f2ff", font=("Arial", 9, "bold")).grid(row=0, column=0, padx=5)
intrare_titlu_concurs = tk.Entry(cadru_titlu, width=30)
intrare_titlu_concurs.insert(0, "Cupa Method Feeder 2026")
intrare_titlu_concurs.grid(row=0, column=1)

cadru = tk.Frame(fereastra, bg="#e6f2ff")
cadru.pack(pady=8)

tk.Label(cadru, text="Nume Echipă:", bg="#e6f2ff", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w", pady=2)
intrare_echipa = tk.Entry(cadru, width=25)
intrare_echipa.grid(row=0, column=1, pady=2)

tk.Label(cadru, text="Nume Pescar:", bg="#e6f2ff").grid(row=1, column=0, sticky="w", pady=2)
intrare_nume = tk.Entry(cadru, width=25)
intrare_nume.grid(row=1, column=1, pady=2)

tk.Label(cadru, text="Sector (ex: A, B):", bg="#e6f2ff").grid(row=2, column=0, sticky="w", pady=2)
intrare_sector = tk.Entry(cadru, width=25)
intrare_sector.grid(row=2, column=1, pady=2)

tk.Label(cadru, text="Număr Stand:", bg="#e6f2ff").grid(row=3, column=0, sticky="w", pady=2)
intrare_stand = tk.Entry(cadru, width=25)
intrare_stand.grid(row=3, column=1, pady=2)

tk.Label(cadru, text="Total Kg Prins:", bg="#e6f2ff").grid(row=4, column=0, sticky="w", pady=2)
intrare_kg = tk.Entry(cadru, width=25)
intrare_kg.grid(row=4, column=1, pady=2)

tk.Label(cadru, text="CMMC (kg):", bg="#e6f2ff").grid(row=5, column=0, sticky="w", pady=2)
intrare_peste_mare = tk.Entry(cadru, width=25)
intrare_peste_mare.grid(row=5, column=1, pady=2)

buton_adauga = tk.Button(fereastra, text="➕ Adaugă Pescar", command=adauga_sau_salveaza_modificare, bg="#28a745", fg="white", font=("Arial", 10, "bold"))
buton_adauga.pack(pady=8)

eticheta_numarator = tk.Label(fereastra, text="Pescari: 0 | Echipe: 0", bg="#e6f2ff", font=("Arial", 10, "bold"))
eticheta_numarator.pack()

eticheta_cmmc = tk.Label(fereastra, text="🏆 CMMC Curent: -", bg="#e6f2ff", fg="#d9534f", font=("Arial", 9, "bold"))
eticheta_cmmc.pack(pady=2)

lista_afisare = tk.Listbox(fereastra, width=64, height=7)
lista_afisare.pack(pady=5)

cadru_editare = tk.Frame(fereastra, bg="#e6f2ff")
cadru_editare.pack(pady=5)

buton_modifica = tk.Button(cadru_editare, text="✏️ Modifică Selectat", command=incarca_pentru_modificare, bg="#ffc107", fg="black", font=("Arial", 9, "bold"))
buton_modifica.grid(row=0, column=0, padx=4)

buton_sterge = tk.Button(cadru_editare, text="❌ Șterge Selectat", command=sterge_pescar, bg="#dc3545", fg="white", font=("Arial", 9, "bold"))
buton_sterge.grid(row=0, column=1, padx=4)

buton_reset = tk.Button(cadru_editare, text="🧹 Concurs Nou", command=concurs_nou, bg="#6c757d", fg="white", font=("Arial", 9, "bold"))
buton_reset.grid(row=0, column=2, padx=4)

cadru_butoane = tk.Frame(fereastra, bg="#e6f2ff")
cadru_butoane.pack(pady=12)

buton_salveaza = tk.Button(cadru_butoane, text="💾 Salvează Clasament", command=salveaza_si_genereaza, bg="#007bff", fg="white", font=("Arial", 10, "bold"))
buton_salveaza.grid(row=0, column=0, padx=4)

buton_deschide = tk.Button(cadru_butoane, text="📄 Deschide Raport", command=deschide_fisier, bg="#17a2b8", fg="white", font=("Arial", 10, "bold"))
buton_deschide.grid(row=0, column=1, padx=4)

buton_folder = tk.Button(cadru_butoane, text="📁 Deschide Folder", command=deschide_folder, bg="#343a40", fg="white", font=("Arial", 10, "bold"))
buton_folder.grid(row=0, column=2, padx=4)

fereastra.mainloop()