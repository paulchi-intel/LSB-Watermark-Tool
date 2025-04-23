import cv2
import numpy as np
import mss
import pygetwindow as gw
import os
import socket
import platform
import sys  # 添加sys模組的導入，用於__exit方法
import random  # 用於偽隨機數生成



class CMain:

    # ------------------------------------------------------------------------------------
    #    __init__()
    #        FUNCTION： constructor，define data members, generate input and output folder if doesn't exist
    #        IN: None
    #        RETURN: None
    # ------------------------------------------------------------------------------------
    def __init__(self):
        print("constructor")
        self.device_name = socket.gethostname()  # 在初始化時就獲取設備名稱
        self.watermark = self.device_name  # 預設使用設備名稱作為浮水印

    # ------------------------------------------------------------------------------------
    #    __del__()
    #        FUNCTION： Destructor
    # ------------------------------------------------------------------------------------
    def __del__(self):
        print("destructor")

    # ------------------------------------------------------------------------------------
    #    __exit()
    #        FUNCTION：
    #        IN: None
    #        RETURN: None
    # ------------------------------------------------------------------------------------
    def __exit(self):
        print("__exit")
        sys.exit()

    # ------------------------------------------------------------------------------------
    #    __invalid()
    #        FUNCTION：
    #        IN: None
    #        RETURN: None
    # ------------------------------------------------------------------------------------
    def __invalid(self):
        print("__invalid")



    def __capture_screen(self, window_title=None, save_path="screenshot.bmp", show=True):
        """
        擷取全螢幕或特定視窗畫面，並儲存為 BMP 或 JPEG 格式
        :param window_title: 指定視窗標題，若為 None 則擷取全螢幕
        :param save_path: 儲存檔案的路徑 (支援 .bmp 或 .jpg)
        :param show: 是否顯示擷取的畫面
        """
        with mss.mss() as sct:
            if window_title:
                # 取得特定視窗的範圍
                window = None
                for win in gw.getWindowsWithTitle(window_title):
                    if window_title in win.title:
                        window = win
                        break
                
                if not window:
                    print(f"找不到視窗: {window_title}")
                    return
                
                monitor = {
                    "left": window.left,
                    "top": window.top,
                    "width": window.width,
                    "height": window.height
                }
            else:
                # 擷取全螢幕
                monitor = sct.monitors[1]  # 第 1 個螢幕 (sct.monitors[0] 是全部的範圍)

            # 擷取畫面
            screenshot = sct.grab(monitor)

            # 轉換為 numpy 陣列 (RGB)
            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # 轉換成 BGR 格式 (OpenCV 格式)

            # 顯示擷取畫面
            if show:
                cv2.imshow("Screenshot", img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            # 儲存成 BMP 或 JPEG
            ext = os.path.splitext(save_path)[1].lower()
            if ext in [".bmp", ".jpg", ".jpeg"]:
                cv2.imwrite(save_path, img)
                print(f"擷取畫面已儲存至 {save_path}")
            else:
                print("錯誤：不支援的檔案格式，請使用 .bmp 或 .jpg")

    def __get_device_name(self):
        """
        獲取並顯示當前設備名稱
        """
        print(f"\n設備名稱: {self.device_name}")
        # print(f"系統資訊: {platform.system()} {platform.release()}\n")

    def __set_watermark(self):
        """
        設定自定義的浮水印文字
        """
        print(f"\n目前的浮水印文字: {self.watermark}")
        new_watermark = input("請輸入新的浮水印文字 (直接按 Enter 則維持不變): ")
        if new_watermark:
            self.watermark = new_watermark
            print(f"浮水印已更新為: {self.watermark}\n")
        else:
            print("保持原有的浮水印文字\n")

    def __add_watermark_lsb(self):
        """
        使用 LSB 技術將浮水印文字嵌入截圖中
        """
        # 先截圖
        self.__capture_screen(save_path="screenshot.bmp", show=False)
        
        # 讀取圖片
        img = cv2.imread("screenshot.bmp")
        if img is None:
            print("無法讀取截圖檔案")
            return

        # 準備要嵌入的文字，添加特殊的結束標記
        watermark = self.watermark + '\0'  # 添加空字符作為結束標記
        watermark_bin = ''.join([format(ord(char), '08b') for char in watermark])
        
        # 檢查影格大小是否足夠
        if img.shape[0] * img.shape[1] * 3 < len(watermark_bin):
            print("圖片太小，無法嵌入完整的浮水印")
            return
        
        # 複製影格以避免修改原始資料
        result = img.copy()
        
        # 嵌入浮水印
        watermark_idx = 0
        for i in range(result.shape[0]):
            for j in range(result.shape[1]):
                for k in range(3):  # RGB channels
                    if watermark_idx < len(watermark_bin):
                        # 修改最低位
                        result[i, j, k] = (result[i, j, k] & 0xFE) | int(watermark_bin[watermark_idx])
                        watermark_idx += 1
                    else:
                        # 儲存含有浮水印的圖片
                        cv2.imwrite("watermarked.bmp", result)
                        print(f"\n浮水印已嵌入，檔案已儲存為 watermarked.bmp")
                        print(f"嵌入的浮水印文字為: {self.watermark}\n")
                        
                        # 顯示圖片
                        cv2.imshow("Watermarked Image", result)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        return
        
        # 如果執行到這裡，表示已完成所有像素的處理
        cv2.imwrite("watermarked.bmp", result)
        print(f"\n浮水印已嵌入，檔案已儲存為 watermarked.bmp")
        print(f"嵌入的浮水印文字為: {self.watermark}\n")
        
        # 顯示圖片
        cv2.imshow("Watermarked Image", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def __extract_watermark(self):
        """
        從浮水印圖片中提取隱藏文字
        """
        # 讀取浮水印圖片
        img = cv2.imread("watermarked.bmp")
        if img is None:
            print("無法讀取浮水印圖片檔案")
            return

        # 提取浮水印
        binary_data = ""
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                for k in range(3):  # RGB channels
                    # 提取最低位
                    binary_data += str(img[i, j, k] & 1)
                    
                    # 每8位檢查一次是否為結束標記
                    if len(binary_data) % 8 == 0:
                        # 檢查最後一個字符是否為結束標記
                        if len(binary_data) >= 8:
                            char_value = int(binary_data[-8:], 2)
                            if char_value == 0:  # 檢測到 '\0'
                                # 將二進制轉換回文字
                                extracted_text = ""
                                for idx in range(0, len(binary_data)-8, 8):
                                    char = chr(int(binary_data[idx:idx+8], 2))
                                    extracted_text += char
                                print(f"\n從浮水印圖片中提取的文字: {extracted_text}")
                                return
        
        print("無法從圖片中提取完整的浮水印")

    def __add_watermark_lsb_redundancy(self):
        """
        使用 LSB 技術將浮水印文字嵌入截圖中，採用分散式嵌入
        """
        # 先截圖
        self.__capture_screen(save_path="screenshot.bmp", show=False)
        
        # 讀取圖片
        img = cv2.imread("screenshot.bmp")
        if img is None:
            print("無法讀取截圖檔案")
            return

        # 準備要嵌入的文字，添加特殊的結束標記
        watermark = self.watermark + '\0'  # 添加空字符作為結束標記
        watermark_bin = ''.join([format(ord(char), '08b') for char in watermark])
        
        # 確保圖片夠大來存放浮水印
        if img.shape[0] * img.shape[1] * 3 < len(watermark_bin) * 10:  # 預留足夠空間
            print("圖片太小，無法嵌入完整的浮水印")
            return

        # 固定種子以確保提取時能復現相同的隨機序列
        seed_value = 42
        random.seed(seed_value)
        
        # 創建圖像大小的偽隨機排列用於嵌入
        height, width = img.shape[:2]
        positions = []
        
        # 建立像素位置列表 (行, 列, 通道)
        for i in range(height):
            for j in range(width):
                for k in range(3):  # RGB通道
                    positions.append((i, j, k))
        
        # 隨機化位置順序
        random.shuffle(positions)
        
        # 確保每一位浮水印信息至少有10個不同位置
        redundancy = 10
        
        # 嵌入浮水印（每個位元重複嵌入10次）
        for watermark_idx in range(len(watermark_bin)):
            bit = int(watermark_bin[watermark_idx])
            # 將相同的位元嵌入多個不同位置以提高魯棒性
            for r in range(redundancy):
                if watermark_idx * redundancy + r < len(positions):
                    i, j, k = positions[watermark_idx * redundancy + r]
                    img[i, j, k] = (img[i, j, k] & 0xFE) | bit
        
        # 在文件開頭存儲種子值和冗餘度（用於提取時恢復）
        # 我們使用前20個預定位置來存儲這些數據
        # 存儲種子值（32位整數）
        seed_bin = format(seed_value, '032b')
        for idx, bit in enumerate(seed_bin):
            i, j, k = idx // 3, (idx % 3) // 3, idx % 3
            img[i, j, k] = (img[i, j, k] & 0xFE) | int(bit)
            
        # 存儲冗餘度（8位整數）
        redundancy_bin = format(redundancy, '08b')
        for idx, bit in enumerate(redundancy_bin):
            i, j, k = (idx + 32) // 3, ((idx + 32) % 3) // 3, (idx + 32) % 3
            img[i, j, k] = (img[i, j, k] & 0xFE) | int(bit)

        # 儲存含有浮水印的圖片
        cv2.imwrite("watermarked.bmp", img)
        print(f"\n浮水印已嵌入，檔案已儲存為 watermarked.bmp")
        print(f"嵌入的浮水印文字為: {self.watermark}\n")
        print(f"浮水印數據已分散嵌入到整個圖像中，每個位元重複嵌入{redundancy}次")

        # 顯示圖片
        cv2.imshow("Watermarked Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def __compare_images(self):
        """
        比較原始截圖和浮水印圖片的差異
        """
        # 讀取兩張圖片
        original = cv2.imread("screenshot.bmp")
        watermarked = cv2.imread("watermarked.bmp")
        
        if original is None or watermarked is None:
            print("無法讀取圖片檔案，請確認 screenshot.bmp 和 watermarked.bmp 都存在")
            return
            
        if original.shape != watermarked.shape:
            print("兩張圖片大小不同，無法比較")
            return
            
        # 計算差異
        difference = cv2.absdiff(original, watermarked)
        
        # 為了讓差異更容易看到，將差異值放大
        # 先轉換為浮點數類型，再進行放大
        difference = difference.astype(np.float32) * 1000
        # 將超過255的值限制在255
        difference = np.clip(difference, 0, 255).astype(np.uint8)
        
        # 儲存差異圖片
        cv2.imwrite("difference.bmp", difference)
        print("\n差異圖片已儲存為 difference.bmp")
        
        # 顯示原圖、浮水印圖和差異圖
        cv2.imshow("Original", original)
        cv2.imshow("Watermarked", watermarked)
        cv2.imshow("Difference (x1000)", difference)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def __extract_watermark_redundancy(self):
        """
        從浮水印圖片中提取分散嵌入的隱藏文字
        """
        # 讀取浮水印圖片
        img = cv2.imread("watermarked.bmp")
        if img is None:
            print("無法讀取浮水印圖片檔案")
            return

        # 首先從前20個預定位置讀取種子值和冗餘度
        # 讀取種子值（32位整數）
        seed_bin = ""
        for idx in range(32):
            i, j, k = idx // 3, (idx % 3) // 3, idx % 3
            seed_bin += str(img[i, j, k] & 1)
        seed_value = int(seed_bin, 2)
        
        # 讀取冗餘度（8位整數）
        redundancy_bin = ""
        for idx in range(8):
            i, j, k = (idx + 32) // 3, ((idx + 32) % 3) // 3, (idx + 32) % 3
            redundancy_bin += str(img[i, j, k] & 1)
        redundancy = int(redundancy_bin, 2)
        
        # 設置相同的隨機種子以重現嵌入時的隨機序列
        random.seed(seed_value)
        
        # 創建與嵌入時相同的偽隨機序列
        height, width = img.shape[:2]
        positions = []
        
        # 建立像素位置列表
        for i in range(height):
            for j in range(width):
                for k in range(3):  # RGB通道
                    positions.append((i, j, k))
        
        # 隨機化位置順序（與嵌入時相同的順序）
        random.shuffle(positions)
        
        # 提取浮水印數據（考慮冗餘性）
        max_chars = 100  # 設定最大可能的字符數量
        binary_data = ""
        
        # 每redundancy個位置代表一個浮水印位元，使用多數投票決定
        for bit_idx in range(max_chars * 8):
            # 對於每個位元，讀取冗餘的多個位置
            votes = []
            for r in range(redundancy):
                pos_idx = bit_idx * redundancy + r
                if pos_idx < len(positions):
                    i, j, k = positions[pos_idx]
                    votes.append(img[i, j, k] & 1)
            
            # 如果沒有足夠的冗餘數據，中止提取
            if len(votes) < redundancy // 2:
                break
                
            # 多數投票決定實際的位元值
            bit = 1 if sum(votes) > len(votes) // 2 else 0
            binary_data += str(bit)
            
            # 每8位檢查一次是否為結束標記
            if len(binary_data) % 8 == 0:
                # 檢查最後一個字符是否為結束標記
                if len(binary_data) >= 8:
                    char_value = int(binary_data[-8:], 2)
                    if char_value == 0:  # 檢測到 '\0'
                        break
        
        # 將二進制轉換回文字，直到遇到結束標記 '\0'
        extracted_text = ""
        for i in range(0, len(binary_data), 8):
            if i + 8 <= len(binary_data):
                byte = binary_data[i:i+8]
                char = chr(int(byte, 2))
                if char == '\0':  # 檢測到結束標記
                    break
                extracted_text += char

        print(f"\n從浮水印圖片中提取的文字: {extracted_text}")
        print(f"使用的隨機種子: {seed_value}, 冗餘度: {redundancy}")

    def __add_visible_watermark(self):
        """
        在截圖上直接繪製可見的浮水印文字
        """
        # 先截圖
        self.__capture_screen(save_path="screenshot.bmp", show=False)
        
        # 讀取圖片
        img = cv2.imread("screenshot.bmp")
        if img is None:
            print("無法讀取截圖檔案")
            return

        # 設定文字屬性
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2.0  # 改回原來的大小
        font_thickness = 2  # 改回原來的粗細
        text = self.watermark
        
        # 獲取文字大小
        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, font_thickness)
        
        # 計算文字位置（正中央）
        x = (img.shape[1] - text_width) // 2
        y = (img.shape[0] + text_height) // 2
        
        # 繪製白色背景（提高可讀性）
        cv2.rectangle(img, 
                     (x - 10, y - text_height - 10),
                     (x + text_width + 10, y + 10),
                     (255, 255, 255),
                     -1)
        
        # 繪製文字
        cv2.putText(img, text, (x, y), font, font_scale, (0, 0, 0), font_thickness)
        
        # 儲存圖片
        cv2.imwrite("no_hide.bmp", img)
        print(f"\n可見浮水印已加入，檔案已儲存為 no_hide.bmp")
        print(f"浮水印文字: {self.watermark}\n")
        
        # 顯示圖片
        cv2.imshow("Visible Watermark", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # ------------------------------------------------------------------------------------
    #    run()
    #        FUNCTION：
    #        IN: None
    #        RETURN: None
    # ------------------------------------------------------------------------------------
    def run(self):
        print("run")

        while True:
            menu = {"1": ("capture screen", self.__capture_screen),
                    "2": ("show device name", self.__get_device_name),
                    "3": ("set watermark", self.__set_watermark),
                    "4": ("add watermark to screenshot", self.__add_watermark_lsb),
                    "5": ("add watermark to screenshot with redundancy", self.__add_watermark_lsb_redundancy),
                    "6": ("compare images", self.__compare_images),
                    "7": ("extract watermark", self.__extract_watermark),
                    "8": ("extract watermark with redundancy", self.__extract_watermark_redundancy),
                    "9": ("add visible watermark", self.__add_visible_watermark),
                    "0": ("exit", self.__exit)
                    }

            # 印出menu
            for key in menu.keys():
                print(key + ": " + menu[key][0])

            # 取得使用者輸入
            ans = input(">>> ")

            # 根據使用者輸入，取得對應的function pointer: [1] ([0]是menu item)，並呼叫之： ()
            menu.get(ans, [None, self.__invalid])[1]()


# ------------------------------------------------------------------------------------
# if __name__ == "__main__":
#    FUNCTION： Entry point of program
# ------------------------------------------------------------------------------------
if __name__ == "__main__":
    os.system("chcp 950")  # Switch to Chinese Mode

    CMain().run()
