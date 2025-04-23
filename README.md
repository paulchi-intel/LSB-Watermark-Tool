# LSB Watermark Tool

A Python-based tool for embedding and extracting digital watermarks using the Least Significant Bit (LSB) technique.

[繁體中文](#繁體中文) | [English](#english)

## 繁體中文

### 簡介
這是一個使用最低有效位（LSB）技術來在圖片中嵌入和提取數位浮水印的工具。該工具支援螢幕截圖功能，可以直接在截取的畫面中嵌入浮水印，並提供多種浮水印嵌入方式。

### 功能特點
- 螢幕截圖功能（支援全螢幕或指定視窗）
- LSB 浮水印嵌入（基本版本）
- LSB 浮水印嵌入（具有冗餘保護）
- 可見浮水印添加
- 浮水印提取功能
- 圖片比較功能
- 自訂浮水印文字
- 支援使用設備名稱作為預設浮水印

### 系統需求
- Python 3.8 或更高版本
- Windows 作業系統

### 安裝步驟
1. 克隆專案到本地：
```bash
git clone https://github.com/paulchi-intel/LSB-Watermark-Tool.git
cd LSB-Watermark-Tool
```

2. 安裝所需套件：
```bash
pip install -r requirements.txt
```

### 使用方法
1. 執行主程式：
```bash
python main.py
```

2. 在主選單中選擇所需功能：
   - 1: 螢幕截圖
   - 2: 顯示設備名稱
   - 3: 設定浮水印
   - 4: 使用 LSB 技術嵌入浮水印
   - 5: 使用具有冗餘保護的 LSB 技術嵌入浮水印
   - 6: 比較原始圖片和浮水印圖片
   - 7: 提取浮水印
   - 8: 提取具有冗餘保護的浮水印
   - 9: 添加可見浮水印
   - 0: 退出程式

### 使用範例
1. 基本 LSB 浮水印：
```
>>> 1  # 先截取螢幕畫面
>>> 3  # 設定浮水印文字
請輸入新的浮水印文字: Hello World
>>> 4  # 使用 LSB 技術嵌入浮水印
>>> 7  # 提取浮水印檢視結果
```

2. 具有冗餘保護的浮水印：
```
>>> 1  # 先截取螢幕畫面
>>> 3  # 設定浮水印文字
請輸入新的浮水印文字: Protected Text
>>> 5  # 使用具有冗餘保護的 LSB 技術嵌入浮水印
>>> 8  # 提取具有冗餘保護的浮水印
```

3. 可見浮水印：
```
>>> 1  # 先截取螢幕畫面
>>> 3  # 設定浮水印文字
請輸入新的浮水印文字: Visible Mark
>>> 9  # 添加可見浮水印
```

### 注意事項
- 建議在嵌入浮水印前先進行螢幕截圖
- 浮水印提取時需要使用相同的方法（基本/冗餘）
- 圖片檔案將以 BMP 格式儲存以避免壓縮損失

## English

### Introduction
This is a tool for embedding and extracting digital watermarks in images using the Least Significant Bit (LSB) technique. The tool includes screen capture functionality and supports multiple watermarking methods.

### Features
- Screen capture (full screen or specific window)
- Basic LSB watermarking
- LSB watermarking with redundancy protection
- Visible watermarking
- Watermark extraction
- Image comparison
- Custom watermark text
- Device name as default watermark

### Requirements
- Python 3.8 or higher
- Windows OS

### Installation
1. Clone the repository:
```bash
git clone https://github.com/paulchi-intel/LSB-Watermark-Tool.git
cd LSB-Watermark-Tool
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

### Usage
1. Run the main program:
```bash
python main.py
```

2. Choose from the main menu:
   - 1: Capture screen
   - 2: Show device name
   - 3: Set watermark
   - 4: Add LSB watermark
   - 5: Add LSB watermark with redundancy
   - 6: Compare images
   - 7: Extract watermark
   - 8: Extract watermark with redundancy
   - 9: Add visible watermark
   - 0: Exit

### Usage Examples
1. Basic LSB Watermark:
```
>>> 1  # Capture screen first
>>> 3  # Set watermark text
Enter new watermark text: Hello World
>>> 4  # Add LSB watermark
>>> 7  # Extract watermark to verify
```

2. Watermark with Redundancy Protection:
```
>>> 1  # Capture screen first
>>> 3  # Set watermark text
Enter new watermark text: Protected Text
>>> 5  # Add LSB watermark with redundancy
>>> 8  # Extract watermark with redundancy
```

3. Visible Watermark:
```
>>> 1  # Capture screen first
>>> 3  # Set watermark text
Enter new watermark text: Visible Mark
>>> 9  # Add visible watermark
```

### Notes
- It's recommended to capture the screen before adding watermarks
- Use the same method (basic/redundancy) for embedding and extracting watermarks
- Images are saved in BMP format to avoid compression losses

## License
MIT License

## Author
Paul Chi

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request. 