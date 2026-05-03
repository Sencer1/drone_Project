import math
# #  burası merkezleri takip etmek için şu an sadece her frame de detectionlara id veriyor
# class CentroidTracker:
#     def __init__(self):
#         self.nextObjectId = 1
#         self.objects = {}


#     def update(self, detections):
#         updatedObjects = {}

#         for detection in detections:
#             x, y, w, h = detection[:4]

#             centerX = x + w // 2
#             centerY = y + h // 2

#             objectId = self.nextObjectId
#             self.nextObjectId += 1

#             updatedObjects[objectId] = (centerX, centerY, detection)

#         self.objects = updatedObjects

#         return self.objects

# ---------------------------------------------------------------------------------------------
# burası bir frame ile takip ettiğimiz kısım
# class CentroidTracker:
#     def __init__(self, maxDistance=50):
#         self.nextObjectId = 1
#         self.object = {}
#         self.maxDistance = maxDistance

#     def mesafeHesapla(self, center1, center2):
#         x1, y1 = center1
#         x2, y2 = center2

#         return math.sqrt((x1-x2)**2 + (y1-y2)**2)
    
#     # bu update in amacı yeni frame ve detectionlari alıp ordan eski objelerle eşleştirip aynı objeye aynı id yi vermek yenilere de yeni id vermek 

#     def update(self, detections):
#         updatedObjects = {}
#         usedObjectIds = set()

#         for detection in detections:
#             x, y, w, h = detection[:4]
#             # yeni görüntüdeki objeleri bulduk merkezlerini
#             centerX = x + w // 2
#             centerY = y + h // 2
#             newCenter = (centerX, centerY)
#             # burası eşleşme için hazırlık
#             # ve eşleşme için uzaklık limiti koyduk
#             bestObjectId = None
#             bestDisatance = self.maxDistance
#             # eski bulunan objeleri alıyoruz burda
#             for objectId, oldData in self.object.items():
#                 oldCenterX, oldCenterY, oldDetection = oldData
#                 oldCenter = (oldCenterX, oldCenterY)
#                 # eski objelerin burda sırayla merkezlerini yeni framedeki objenin merkeziyle kıyaslıyoruz
#                 distance = self.mesafeHesapla(newCenter, oldCenter)
#                 # objeye yakın ve daha önce bu id kullanıldı mı diye bakıyoruz
#                 if distance < bestDisatance and objectId not in usedObjectIds:
#                     bestDisatance = distance
#                     bestObjectId = objectId
#             # eğer bu obje eski objelerden biriyle eşleşiyorsa bunu kaydediyoruz yeni merkez olarak ve bu id kullanıldı olarak işaretliyoruz
#             if bestObjectId is not None:
#                 updatedObjects[bestObjectId] = (centerX, centerY, detection)
#                 usedObjectIds.add(bestObjectId)
#             else:
#                 # eğer eşleşme yoksa bu objeye bir id veriyoruz
#                 objectId =self.nextObjectId
#                 # yeni obje için yeni id yi güncelliyoruz
#                 self.nextObjectId += 1
#                 # bunu objeclere farklı id olarak kaydediyoruz
#                 updatedObjects[objectId] = (centerX, centerY, detection)
#                 # bu id kullanıldı olarak işaretliyoruz
#                 usedObjectIds.add(objectId)
#         # en sona da bu objeleri saklamak için tutuyoruz
#         self.object = updatedObjects

#         return self.object
    
#     # ----------------------------------------------------------------------------------------------
#     # burası daha iyileştirilmiş hali tek frame değil birden fazla frame takibi


class CentroidTracker:
    def __init__(self, maxDistance=80, maxMissingFrame=10):
        self.nextObjectId = 1
        self.objects = {}
        self.missingFrames = {}
        self.maxDistance = maxDistance
        self.maxMissingFrame = maxMissingFrame

    def mesafeHesapla(self, center1, center2):
        x1, y1 = center1
        x2, y2 = center2

        return math.sqrt((x1-x2)**2 + (y1-y2)**2)
    
    def yeniObjeEkle(self, centerX, centerY, detection):

        objectId = self.nextObjectId
        self.nextObjectId += 1

        self.objects[objectId] = (centerX, centerY, detection)
        self.missingFrames[objectId] = 0

    def objeSil(self, objectId):
        del self.objects[objectId]
        del self.missingFrames[objectId]

    def update(self, detections):
        updatedObjects = {}
        usedObjectIds = set()

        for detection in detections:
            x, y, w, h = detection[:4]

            centerX = x + w // 2
            centerY = y + h // 2

            newCenter = (centerX, centerY)
            # best object id bizim baktığımız framede yeni bulduğumuz objenin id si 
            bestObjectId = None
            bestDistance = self.maxDistance

            for objectId, oldData in self.objects.items():
                if objectId in usedObjectIds:
                    continue

                oldCenterX, oldCenterY, oldDetection = oldData
                oldCenter = (oldCenterX, oldCenterY)

                distance = self.mesafeHesapla(newCenter, oldCenter)
                # burda eski framlerdeki objelerle kıyas yaptı yeni frame de bulduğu detection ile
                # en yakın olanın id sini aldı hiçbiri ona yakın değilse none olarak kaldı bestObjectid
                
                if distance < bestDistance:
                    bestDistance = distance
                    bestObjectId = objectId

            if bestObjectId is not None:
                # framede bulduğumuz ve önceki framedeki objelerle eşleşen objeyi kaydediyoruz updatedObject e
                updatedObjects[bestObjectId] = (centerX, centerY, detection)
                # bu objeyi bu framede gördüğümüz missingframesdeki değerini sıfır yaptık yani en son kaç frame önce gördüğümüzü tutuyordu
                # en son baktığımız framede gördüğümzü için değeri 0
                self.missingFrames[bestObjectId] = 0
                # bu objeyi bir objeyle eşleştiridk aynı objeyle başka obje eşlelşmesin diye de kayıt ettik usedObject e
                usedObjectIds.add(bestObjectId)
            else:
                # önceki framelerden eşleşen obje bulamadığımız için bu objeyi yeni obje olarak ekledik
                self.yeniObjeEkle(centerX, centerY, detection)
        # list olarak almamızın sebebi obje silinirse loop o objeyi vermeye çalışırken hata yaşar
        # loop a başlamadan önce self.objects.keys() burda sabit boyut belirttik ama değişebilir ilerde
        # list yapınca kopyasını almış oluyoruz ve silsek de sıkıntı olmuyor
        for objectId in list(self.objects.keys()):
            # burda objectte olan yani daha önceki framelerde bulduğumuz tüm objeleri sırayla kontrol ediyoruz
            # bu obje kullanılmış yoksa 10 framedir bu objeye rastlamadık mı diye
            if objectId not in updatedObjects and objectId not in usedObjectIds:
                # eğer bu objeye rastlamadıysak bu framede 1 attıryoruz bu framede görmedim sayısını
                self.missingFrames[objectId] += 1
                # bu obje max missing frame yani en son baktğığmız tüm framelerde üst sınır aştı mı diye kontorl ediyoruz
                if self.missingFrames[objectId] <= self.maxMissingFrame:
                    # eğer sınırı aşmadıysa kaybolmasın diye onu updatedobject e kaydediyoruz böyleyece sonraki framede tekrar kontorl edebilmmeiz için
                    # objecte tekrar verebilecek updated object sayesinde
                    updatedObjects[objectId] = self.objects[objectId]
                else:
                    # eğer sınır aştıysa siliyoruz bu objeyi daha fazla saklayıp kıyas yapmamak için
                    self.objeSil(objectId)
        
        self.objects = updatedObjects

        return self.objects