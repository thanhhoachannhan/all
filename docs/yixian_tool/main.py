import requests
from bs4 import BeautifulSoup
import csv
import os
import time  # Thêm thư viện time để sử dụng sleep

# Đường dẫn đến folder lưu ảnh
media_folder = 'media'
if not os.path.exists(media_folder):
    os.makedirs(media_folder)

# Tạo file CSV để lưu kết quả
csv_file = 'yixian_cards.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Image URL', 'Image Local Path'])

    # Lặp qua id từ 0 đến 1000
    for card_id in range(5000):
        url = f"https://www.iyingdi.com/tz/tool/general/yixian/{card_id}"
        print(f"Đang xử lý ID: {card_id}")
        
        retry_count = 0
        max_retries = 1  # Chỉ thử lại 1 lần nếu gặp lỗi
        
        while retry_count <= max_retries:
            try:
                # Gửi yêu cầu HTTP
                response = requests.get(url)
                if response.status_code == 404:
                    print(f"ID {card_id} không tồn tại, bỏ qua.")
                    break  # Nếu gặp 404 thì bỏ qua ID này, không thử lại

                # Phân tích HTML bằng BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')

                # Kiểm tra sự tồn tại của phần tử "弈仙牌单卡查询"
                if soup.find("span", class_="text-blue-500 cursor-pointer nuxt-link-active", string="弈仙牌单卡查询") or soup.find("div", string="弈仙牌单卡查询"):
                    # Tìm div chứa thẻ ảnh
                    card_div = soup.find("div", class_="marvel-card-detail-page")
                    if card_div:
                        img_tag = card_div.find("img", class_="card-img")
                        if img_tag:
                            alt_text = img_tag['alt']
                            img_url = img_tag['src']

                            # Tải ảnh về và lưu vào folder media
                            img_response = requests.get(img_url)
                            img_name = img_url.split('/')[-1]
                            img_path = os.path.join(media_folder, img_name)

                            with open(img_path, 'wb') as img_file:
                                img_file.write(img_response.content)

                            # Ghi vào file CSV
                            writer.writerow([alt_text, img_url, img_path])
                            print(f"Lưu: {alt_text}, {img_url}, {img_path}")

                # Nếu thành công, thoát khỏi vòng lặp
                break

            except Exception as e:
                print(f"Đã xảy ra lỗi với ID {card_id}: {e}")
                retry_count += 1
                if retry_count <= max_retries:
                    print(f"Thử lại ID {card_id} sau 5 giây...")
                    time.sleep(5)  # Đợi 5 giây trước khi thử lại
                else:
                    print(f"Thất bại sau khi thử lại ID {card_id}. Bỏ qua.")
                    break

print(f"Quá trình crawl hoàn thành. Dữ liệu được lưu vào {csv_file}.")
