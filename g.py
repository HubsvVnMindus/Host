import random
import os
import time
import json
import math
import platform
import requests
from colorama import Fore, Style, init

# Khởi tạo colorama
init(autoreset=True)

# Định nghĩa màu sắc RGB cho hàm prints
def prints(r, g, b, text="text", end="\n"):
    print(f"\033[38;2;{r};{g};{b}m{text}\033[0m", end=end)

# Mapping tên phòng
ROOM_NAMES = {
    1: 'Nhà kho', 2: 'Phòng họp', 3: 'Phòng giám đốc', 4: 'Phòng trò chuyện',
    5: 'Phòng giám sát', 6: 'Văn phòng', 7: 'Phòng tài vụ', 8: 'Phòng nhân sự'
}

def clear_screen():
    os.system('cls' if platform.system() == "Windows" else 'clear')

def draw_line():
    prints(247, 255, 97, " ✨" + "═" * 50 + "✨")

def banner(game):
    # Banner được tối ưu lại với màu gradient cyan -> blue
    clear_screen()
    text_banner = [
        "   ██╗░░██╗██╗░░██╗███╗░░██╗░██████╗░",
        "   ██║░░██║██║░░██║████╗░██║██╔════╝░",
        "   ███████║██║░░██║██╔██╗██║██║░░██╗░",
        "   ██╔══██║██║░░██║██║╚████║██║░░╚██╗",
        "   ██║░░██║╚██████╔╝██║░╚███║╚██████╔╝",
        "   ╚═╝░░╚═╝░╚═════╝░╚═╝░░╚══╝░╚═════╝░"
    ]
    for line in text_banner:
        x, y, z = 100, 200, 255
        for char in line:
            prints(x, y, z, char, end='')
            if x < 250: x += 2
        print()
    
    draw_line()
    prints(32, 230, 151, f"🚀 XWORLD - {game} PRO V5.2 🚀".center(52))
    draw_line()
    prints(7, 205, 240, f" 👤 Admin: Thành Công | 📺 YouTube: @Tool-Xworld ".center(52))
    draw_line()

def load_data_vth():
def load_data_vth():
    filename = 'data-xw-vth.txt'
    if os.path.exists(filename):
        prints(0, 255, 243, ' 📂 Phát hiện dữ liệu cũ. Sử dụng lại? (y/n): ', end='')
        if input().lower() == 'y':
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
    
    instr = """
    📝 HƯỚNG DẪN LẤY LINK:
    1. Truy cập xworld.io -> Đăng nhập
    2. Vào game 'Vua Thoát Hiểm' -> Nhấn 'Truy cập'
    3. Copy toàn bộ URL và dán vào bên dưới.
    """
    prints(218, 255, 125, instr)
    draw_line()
    prints(125, 255, 168, ' 🔗 Nhập link của bạn: ', end='')
    link = input()
    try:
        user_id = link.split('userId=')[1].split('&')[0]
        user_secretkey = link.split('secretKey=')[1].split('&')[0]
        data = {'user-id': user_id, 'user-secret-key': user_secretkey}
        with open(filename, 'w+', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return data
    except:
        prints(255, 50, 50, " ❌ Link không hợp lệ!")
        time.sleep(2)
        return load_data_vth()

def load_config_vth():
    filename = 'config_vth_ctool.txt'
    if os.path.exists(filename):
        prints(0, 255, 243, ' ⚙️ Sử dụng cấu hình cược cũ? (y/n): ', end='')
        if input().lower() == 'y':
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)

    prints(219, 237, 138, "\n 💰 CHỌN LOẠI TIỀN: [1] USDT | [2] BUILD | [3] WORLD")
    choice = input(" -> Lựa chọn: ")
    coin = {"1": "USDT", "2": "BUILD", "3": "WORLD"}.get(choice, "WORLD")
    
    prints(219, 237, 138, f" 🤖 Bật chế độ tự động đặt cược {coin}? (y/n): ", end='')
    status = input().lower()
    
    conf = {'Coin': coin, 'status_bet': status}
    if status == 'y':
        prints(255, 50, 50, " [!] LƯU Ý: Rủi ro tự chịu. Không nên đặt quá thấp.")
        conf.update({
            'coins1': float(input(f' -> Mức cược tối thiểu: ')),
            'coins2': float(input(f' -> Mức cược tối đa: ')),
            'start_bet': float(input(' -> Bắt đầu cược từ chuỗi thắng: ')),
            'end_bet': float(input(' -> Kết thúc cược ở chuỗi thắng: ')),
            'stop_bet': float(input(f' -> Chốt lời ({coin}): ')),
            'stop_bet2': -1 * float(input(f' -> Cắt lỗ ({coin}): ')),
            'up_bet': -1 * float(input(f' -> Lỗ bao nhiêu thì tăng cược: ')),
            'up_bet2': float(input(f' -> Mức cược tăng thêm: '))
        })
    else:
        conf.update({'coins1':0,'coins2':0,'start_bet':999999,'end_bet':999999,'stop_bet':999999,'stop_bet2':-999999,'up_bet':-999999,'up_bet2':0})
        
    with open(filename, 'w+', encoding='utf-8') as f:
        json.dump(conf, f, indent=4, ensure_ascii=False)
    return conf

# --- Các hàm Logic Giữ Nguyên ---
def user_asset(s, headers):
    try:
        json_data = {'user_id': int(headers['user-id']), 'source': 'home'}
        response = requests.post('https://wallet.3games.io/api/wallet/user_asset', headers=headers, json=json_data).json()
        return {k: response['data']['user_asset'][k] for k in ['USDT', 'WORLD', 'BUILD']}
    except: return user_asset(s, headers)

def top10_vth(s, headers, Coin):
    try:
        res = s.get('https://api.escapemaster.net/escape_game/recent_10_issues', params={'asset': Coin}, headers=headers).json()
        return [i['issue_id'] for i in res['data']], [i['killed_room_id'] for i in res['data']]
    except: return top10_vth(s, headers, Coin)

def top100_vth(s, headers, Coin):
    try:
        res = s.get('https://api.escapemaster.net/escape_game/recent_100_issues', params={'asset': Coin}, headers=headers).json()
        return res['data']['room_id_2_killed_times']
    except: return top100_vth(s, headers, Coin)

def chon_phong(data_top10, data_top100):
    dem = [0]*8
    for j in data_top10[1]: dem[j-1] += 1
    x1 = dem.index(min(dem)) + 1
    
    min2 = data_top100['1']; x2 = 1
    for i in range(2, 9):
        if min2 >= data_top100[str(i)]:
            min2 = data_top100[str(i)]; x2 = i
    return random.choice([x1, x2])

def bet_vth(s, headers, room_id, config, stats):
    asset = user_asset(s, headers)
    profit = asset[config['Coin']] - stats['asset_0']
    
    if profit <= config['stop_bet2']:
        prints(255, 50, 50, " [!] Đã chạm ngưỡng cắt lỗ. Dừng tool."); exit()
        
    if config['status_bet'] == 'y' and config['start_bet'] <= stats['streak'] <= config['end_bet']:
        if profit <= config['up_bet']:
            bet_amount = config['up_bet2']
        else:
            c1, c2 = config['coins1'], config['coins2']
            if config['Coin'] == 'BUILD':
                bet_amount = random.choice([i for i in range(int(math.ceil(c1/100)*100), int(math.floor(c2/100)*100)+1, 100)]) if c2 >= 100 else round(random.uniform(c1, c2))
            else:
                bet_amount = round(random.uniform(c1, c2), 1)

        try:
            payload = {'asset_type': config['Coin'], 'user_id': headers['user-id'], 'room_id': room_id, 'bet_amount': float(bet_amount)}
            res = s.post('https://api.escapemaster.net/escape_game/bet', headers=headers, json=payload).json()
            if res['code'] == 0:
                prints(0, 255, 255, f" ✅ ĐẶT CƯỢC: {bet_amount} {config['Coin']} -> Phòng {room_id}")
            else:
                prints(255, 50, 50, f" ❌ Lỗi: {res['msg']}")
        except Exception as e: prints(255, 0, 0, f" ❌ Lỗi kết nối: {e}")

def main_vth():
    s = requests.Session()
    banner("VUA THOÁT HIỂM")
    data = load_data_vth()
    config = load_config_vth()
    
    headers = {
        'accept': '*/*', 'country-code': 'vn', 'origin': 'https://xworld.info',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36',
        'user-id': data['user-id'], 'user-secret-key': data['user-secret-key'],
        'xb-language': 'vi-VN'
    }

    asset_init = user_asset(s, headers)
    stats = {'win':0, 'lose':0, 'streak':0, 'max_streak':0, 'asset_0': asset_init[config['Coin']]}

    while True:
        banner("VUA THOÁT HIỂM")
        curr_asset = user_asset(s, headers)
        
        # Giao diện ví tiền
        print(f" {Fore.YELLOW}💰 TÀI KHOẢN: {Fore.WHITE}USDT: {curr_asset['USDT']:.2f} | WORLD: {curr_asset['WORLD']:.2f} | BUILD: {curr_asset['BUILD']:.2f}")
        draw_line()

        # Thống kê
        profit = curr_asset[config['Coin']] - stats['asset_0']
        win_rate = (stats['win'] / (stats['win'] + stats['lose']) * 100) if (stats['win'] + stats['lose']) > 0 else 0
        
        print(f" {Fore.CYAN}📊 THỐNG KÊ:")
        print(f"  • Thắng/Bại: {Fore.GREEN}{stats['win']}{Fore.WHITE}/{Fore.RED}{stats['lose']} {Fore.WHITE}({win_rate:.1f}%)")
        print(f"  • Chuỗi hiện tại: {Fore.YELLOW}{stats['streak']} {Fore.WHITE}(Max: {stats['max_streak']})")
        color_p = Fore.GREEN if profit >= 0 else Fore.RED
        print(f"  • Lợi nhuận: {color_p}{profit:.2f} {config['Coin']}")
        draw_line()

        # Phân tích & Dự đoán
        d10 = top10_vth(s, headers, config['Coin'])
        d100 = top100_vth(s, headers, config['Coin'])
        prints(22, 247, 236, f" 🔍 Đang phân tích kì: {d10[0][0]+1}")
        
        kq = chon_phong(d10, d100)
        prints(255, 255, 0, f" 🎯 Dự đoán: Phòng {kq} ({ROOM_NAMES[kq]})")
        
        bet_vth(s, headers, kq, config, stats)
        
        # Chờ kết quả
        start_wait = time.time()
        while True:
            prints(200, 200, 200, f" ⏳ Đang đợi kết quả... ({int(time.time()-start_wait)}s)", end='\r')
            time.sleep(2)
            check_d10 = top10_vth(s, headers, config['Coin'])
            
            if check_d10[0][0] == d10[0][0] + 1:
                killed_room = check_d10[1][0]
                print(f"\n {Fore.MAGENTA}💀 Sát thủ vào phòng: {killed_room} ({ROOM_NAMES[killed_room]})")
                
                if int(kq) == int(killed_room):
                    prints(255, 50, 50, " ➜ KẾT QUẢ: THUA (LOSE) ❌")
                    stats['lose'] += 1; stats['streak'] = 0
                else:
                    prints(50, 255, 50, " ➜ KẾT QUẢ: THẮNG (WIN) ✅")
                    stats['win'] += 1; stats['streak'] += 1
                    stats['max_streak'] = max(stats['max_streak'], stats['streak'])
                
                if profit >= config['stop_bet']:
                    prints(0, 255, 0, " [!] Đã đạt mục tiêu chốt lời. Nghỉ ngơi thôi!"); exit()
                
                time.sleep(5)
                break

if __name__ == "__main__":
    try:
        main_vth()
    except KeyboardInterrupt:
        print("\n [!] Đã dừng Tool.")

