import os
import gdown


class Config:

    def __init__(self) -> None:
        self.__downloads()

    
    def __downloads(self,) -> bool:

        files = [("./downloads/sample","1Z5te6CPHoStw-9Tm-DT2D6xf6EE-6BLB"), ("./downloads/amazon-meta.txt", "1Ru21bKkHhjRi8QV2pX7n6SdPxrs9UOlC"), ]

        for file, id in files:

            if not os.path.exists(file):
                self.__download_drive(id,file)

    def __download_drive(self, id_val, output):

        url = "https://drive.google.com/uc?id="
        full_url = f"{url}{id_val}"
        gdown.download(full_url, output=output)         
        
