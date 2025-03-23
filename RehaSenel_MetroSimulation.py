from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional
import random

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if id not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)

    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """BFS algoritması kullanarak en az aktarmalı rotayı bulur

        Bu fonksiyonu tamamlayın:
        1. Başlangıç ve hedef istasyonların varlığını kontrol edin
        2. BFS algoritmasını kullanarak en az aktarmalı rotayı bulun
        3. Rota bulunamazsa None, bulunursa istasyon listesi döndürün
        4. Fonksiyonu tamamladıktan sonra, # TODO ve pass satırlarını kaldırın

        İpuçları:
        - collections.deque kullanarak bir kuyruk oluşturun, HINT: kuyruk = deque([(baslangic, [baslangic])])
        - Ziyaret edilen istasyonları takip edin
        - Her adımda komşu istasyonları keşfedin
        """
        
        # check if the baslangic_id and hedef_id exists in self.istasyonlar 
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        ziyaret_edildi = {baslangic}
        queue = deque([(baslangic, [baslangic])])


        while queue:
            # return the first element in to queue
            node, rota = queue.popleft()

            # check if we have arrived at our target
            if node == hedef:
                return rota
                
            # check if it's already visited
            if node.idx in ziyaret_edildi:
                continue

            ziyaret_edildi.add(node)

            # node.komsular return a tuple but I only need the komsu here
            for komsu, _ in node.komsular:
                if komsu.idx not in ziyaret_edildi:
                    # add the neighbors to the queue only if they are not visited
                    queue.append((komsu, rota + [komsu]))
        
        return None

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        """A* algoritması kullanarak en hızlı rotayı bulur

        Bu fonksiyonu tamamlayın:
        1. Başlangıç ve hedef istasyonların varlığını kontrol edin
        2. A* algoritmasını kullanarak en hızlı rotayı bulun
        3. Rota bulunamazsa None, bulunursa (istasyon_listesi, toplam_sure) tuple'ı döndürün
        4. Fonksiyonu tamamladıktan sonra, # TODO ve pass satırlarını kaldırın

        İpuçları:
        - heapq modülünü kullanarak bir öncelik kuyruğu oluşturun, HINT: pq = [(0, id(baslangic), baslangic, [baslangic])]
        - Ziyaret edilen istasyonları takip edin
        - Her adımda toplam süreyi hesaplayın
        - En düşük süreye sahip rotayı seçin
        """
        
        # check if the baslangic_id and hedef_id exists in self.istasyonlar 
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        ziyaret_edildi = set()
        pq = [(0, id(baslangic), baslangic, [baslangic])] # [(cost, id, current station, path)]
        heapq.heapify(pq)

        # make the heuristic a function that returns 0.
        heuristic = lambda station: 0

        best_f = {baslangic.idx: 0}

        while pq:
            # return the current station with the lowest cost.
            current_f, _, current, path = heapq.heappop(pq)

            # heuristic returns 0
            current_g = current_f

            # continue if already visited
            if current.idx in ziyaret_edildi:
                continue

            # store the unvisited nodes in ziyaret_edildi
            ziyaret_edildi.add(current.idx)

            # if the goal is reached return the path and the cost
            if current == hedef:
                return path, current_f

            # explore each neighbors
            for komsu, sure in current.komsular:
                if komsu.idx not in ziyaret_edildi:
                    # calculate the new cumulative cost
                    new_g = current_f + sure
                    new_f = new_g + heuristic(komsu) # or just new_f = new_g since heuristic return 0.

                    # push the new route onto the priority queue.
                    heapq.heappush(pq, (new_f, id(komsu), komsu, path + [komsu]))

        return None # No path found

    # Specific Scenario Including aktarma_suresi
    def compute_heuristic(self, current: Istasyon, hedef: Istasyon) -> int:
        """
        heuristic function that returns a penalty when switching metro lines

        - If the current and target line are on the same metro line return 0 for the time
        - If a transfer is needed return a random time between 3, 10
        """
        
        aktarma_suresi = random.randint(3,10)
        return 0 if current.hat == hedef.hat else aktarma_suresi

    def aktarma_sureli_en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
       
        # check if the baslangic_id and hedef_id exists in self.istasyonlar 
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        ziyaret_edildi = set()
        pq = [(0, id(baslangic), baslangic, [baslangic])] # [(cost, id, current station, path)]
        heapq.heapify(pq)

        best_f = {baslangic.idx: 0}

        while pq:
            # return the current station with the lowest cost.
            current_f, _, current, path = heapq.heappop(pq)

            # retrieve the best known cumulative cost (g) for the current station.
            current_g = best_f[current.idx]

            # continue if already visited
            if current.idx in ziyaret_edildi:
                continue
                
            # store the unvisited nodes in ziyaret_edildi
            ziyaret_edildi.add(current.idx)

            # if the goal is reached return the path and the cost
            if current == hedef:
                return path, current_f

            # explore each neighbors
            for komsu, sure in current.komsular:
                if komsu.idx not in ziyaret_edildi:
                    # calculate the new cumulative cost including the penalty for transferring times
                    new_g = current_g + sure
                    heuristic = self.compute_heuristic(current, hedef)
                    new_f = new_g + heuristic # f = g + h

                # if this neighbor hasn't been reached before or a cheaper path is found
                # update the best cost and push the new route onto the priority queue.
                if komsu.idx not in best_f:
                    best_f[komsu.idx] = new_f
                    heapq.heappush(pq, (new_f, id(komsu), komsu, path + [komsu]))

        return None # No path found




# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()

    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")

    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")

    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")

    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB

    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar

    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören

    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma

    # Test senaryoları
    print("\n=== Test Senaryoları ===")

    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))

    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

    sonuc_2 = metro.aktarma_sureli_en_hizli_rota_bul("M1", "K4")  # Random aktarma süreli
    if sonuc_2:
        rota, sure = sonuc_2
        print(f"Aktarma süreli en hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))

    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

    sonuc_2 = metro.aktarma_sureli_en_hizli_rota_bul("T1", "T4")  # Random aktarma süreli
    if sonuc_2:
        rota, sure = sonuc_2
        print(f"Aktarma süreli en hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))


    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))

    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

    sonuc_2 = metro.aktarma_sureli_en_hizli_rota_bul("T4", "M1")  # Random aktarma süreli
    if sonuc_2:
        rota, sure = sonuc_2
        print(f"Aktarma süreli en hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))


    # Senaryo 4: Batıkent'ten AŞTİ'ye (T1 -> M1)
    print("\n4. Batıkent'ten AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T1", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))

    sonuc = metro.en_hizli_rota_bul("T1", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

    sonuc_2 = metro.aktarma_sureli_en_hizli_rota_bul("T1", "M1")  # Random aktarma süreli
    if sonuc_2:
        rota, sure = sonuc_2
        print(f"Aktarma süreli en hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
