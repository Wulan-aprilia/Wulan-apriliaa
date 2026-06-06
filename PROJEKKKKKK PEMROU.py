from abc import ABC, abstractmethod

class PerangkatElektronik(ABC):
    def __init__(self, nama, daya_watt, jam_pakai_per_hari):
        self.nama = nama
        self.daya_watt = daya_watt
        self.jam_pakai_per_hari = jam_pakai_per_hari
        self.__tarif_per_kwh = 1444.70  

    def get_tarif_per_kwh(self):
        return self.__tarif_per_kwh

    def set_tarif_per_kwh(self, tarif_baru):
        if tarif_baru > 0:
            self.__tarif_per_kwh = tarif_baru

    @abstractmethod
    def hitung_kwh_harian(self):
        pass

    def hitung_kwh_bulanan(self):
        return self.hitung_kwh_harian() * 30

    def hitung_biaya_bulanan(self):
        return self.hitung_kwh_bulanan() * self.get_tarif_per_kwh()

    def info(self):
        return (
            f"{self.nama:15} | "
            f"{self.daya_watt:6.1f} W | "
            f"{self.jam_pakai_per_hari:5.1f} jam/hari | "
            f"{self.hitung_kwh_bulanan():8.2f} kWh/bulan | "
            f"Rp {self.hitung_biaya_bulanan():,.0f}"
        )

class PerangkatStatis(PerangkatElektronik):
    """
    Perangkat yang menyala terus menerus,
    misalnya kulkas, modem WiFi.
    """
    def hitung_kwh_harian(self):
        return (self.daya_watt * self.jam_pakai_per_hari) / 1000


class PerangkatIntermiten(PerangkatElektronik):
    """
    Perangkat yang digunakan saat diperlukan,
    misalnya setrika, pompa air.
    """
    def hitung_kwh_harian(self):
    
        return (self.daya_watt * self.jam_pakai_per_hari * 0.95) / 1000


class SistemAnalisisEnergi:
    def __init__(self):
        self.daftar_perangkat = []


    def tambah_perangkat(self, perangkat):
        self.daftar_perangkat.append(perangkat)

    def total_biaya(self):
        return sum(p.hitung_biaya_bulanan() for p in self.daftar_perangkat)

    
    def total_kwh(self):
        return sum(p.hitung_kwh_bulanan() for p in self.daftar_perangkat)


    def tampilkan_laporan(self):
        if not self.daftar_perangkat:
            print("\nBelum ada perangkat yang dimasukkan.")
            return

        print("\n" + "=" * 90)
        print("LAPORAN ANALISIS KONSUMSI ENERGI LISTRIK")
        print("=" * 90)
        print(
            f"{'Nama Perangkat':15} | {'Daya':>6} | {'Jam':>12} | "
            f"{'Konsumsi':>15} | {'Biaya':>15}"
        )
        print("-" * 90)

        for perangkat in self.daftar_perangkat:
            print(perangkat.info())

        print("-" * 90)
        print(f"Total Konsumsi Energi : {self.total_kwh():.2f} kWh/bulan")
        print(f"Estimasi Tagihan PLN  : Rp {self.total_biaya():,.0f}")
        print("=" * 90)


    def perangkat_paling_boros(self):
        if not self.daftar_perangkat:
            return None
        return max(self.daftar_perangkat, key=lambda p: p.hitung_biaya_bulanan())

    def saran_penghematan(self):
        perangkat = self.perangkat_paling_boros()

        if perangkat is None:
            print("\nTidak ada data perangkat.")
            return

        hemat_per_hari = (perangkat.daya_watt * 1) / 1000  
        hemat_per_bulan = hemat_per_hari * 30
        hemat_rupiah = hemat_per_bulan * perangkat.get_tarif_per_kwh()

        print("\nSARAN PENGHEMATAN")
        print("-" * 50)
        print(
            f"Perangkat paling boros adalah {perangkat.nama} "
            f"dengan biaya Rp {perangkat.hitung_biaya_bulanan():,.0f}/bulan."
        )
        print(
            f"Coba kurangi pemakaian {perangkat.nama} "
            f"1 jam per hari agar hemat sekitar "
            f"Rp {hemat_rupiah:,.0f} per bulan."
        )



def menu():
    sistem = SistemAnalisisEnergi()

    while True:
        print("\n===== SISTEM ANALISIS ENERGI LISTRIK =====")
        print("1. Tambah Perangkat")
        print("2. Tampilkan Laporan")
        print("3. Lihat Saran Penghematan")
        print("4. Keluar")

        pilihan = input("Pilih menu (1-4): ")

        if pilihan == "1":
            nama = input("Nama perangkat            : ")
            daya = float(input("Daya (Watt)               : "))
            jam = float(input("Jam pemakaian per hari    : "))

            print("Jenis perangkat:")
            print("1. Perangkat Statis")
            print("2. Perangkat Intermiten")
            jenis = input("Pilih jenis (1/2): ")

            if jenis == "1":
                perangkat = PerangkatStatis(nama, daya, jam)
            else:
                perangkat = PerangkatIntermiten(nama, daya, jam)

            sistem.tambah_perangkat(perangkat)
            print(f"\n{nama} berhasil ditambahkan!")

        elif pilihan == "2":
            sistem.tampilkan_laporan()

        elif pilihan == "3":
            sistem.saran_penghematan()

        elif pilihan == "4":
            print("\nTerima kasih telah menggunakan program.")
            break

        else:
            print("\nPilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    menu()