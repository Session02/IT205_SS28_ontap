# VALIDATE NGƯỜI DÙNG BỎ TRỐNG
def check_space(prompt):
    while True:
        value = input (prompt)
        if len(value.strip()) == 0:
            print ("Dữ liệu đầu vào không được để trống!")
        else:
            return value

# VALIDATE NGƯỜI DÙNG NHẬP SỐ TRONG TÊN
def check_num_in_string(prompt):
    while True:
        value = check_space(prompt).strip()
        has_num = True
        for char in value:
            if char.isdigit() == True:
                has_num = False
                break
        if has_num == False:
            print ("Dữ liệu đầu vào không được chứa số!")
        else:
            return value

# VALIDATE NGƯỜI DÙNG NHẬP SỐ
def change_into_int(prompt):
    while True:
        try:
            value = int(check_space(prompt))
            if value < 0:
                print ("Dữ liệu đầu vào phải lớn hơn 0!")
            else:
                return value
        except ValueError:
            print ("Dữ liệu đầu vào không được chứa ký tự!")

# VALIDATE NGƯỜI DÙNG NHẬP KHOẢNG CÁCH
def check_distance(prompt):
    while True:
        try:
            value = int(check_space(prompt))
            if value < 1 or value > 5000:
                print ("Khoảng cách phải nằm trong khoảng từ 1 đến 5000 Km!")
            else:
                return value
        except ValueError:
            print ("Dữ liệu đầu vào không được chứa ký tự!")

class DeliveryOrder:
    def __init__(self, order_id, receiver_name, base_fee, distance, surcharge):
        self.order_id = order_id
        self.receiver_name = receiver_name
        self.base_fee = base_fee
        self.distance = distance
        self.surcharge = surcharge
        self.total_delivery_cost = 0
        self.delivery_status = ""
    
    def calculate_total_cost(self):
        self.total_delivery_cost = (self.base_fee * self.distance) + self.surcharge
    
    def classify_delivery_status(self):
        if self.total_delivery_cost < 100000:
            self.delivery_status = "Đơn hàng Tiêu chuẩn (Nội thành)"
        elif self.total_delivery_cost >= 100000 and self.total_delivery_cost < 300000:
            self.delivery_status = "Đơn hàng Cận tỉnh"
        elif self.total_delivery_cost >= 300000 and self.total_delivery_cost < 600000:
            self.delivery_status = "Đơn hàng Đường dài (Cần giám sát)"
        else:
            self.delivery_status = "Đơn hàng Đặc biệt (Ưu tiên cao - Rủi ro cao)"

class OrderManager:
    def __init__(self):
        self.orders: list[DeliveryOrder] = []
    
    # HIỂN THỊ
    def show_all_orders(self):
        if len(self.orders) == 0:
            print ("Hiện chưa có đơn hàng nào.")
        else:
            print ("=== DANH SÁCH ĐƠN HÀNG ===")
            for o in self.orders:
                print (f"{o.order_id} | Tên người nhận: {o.receiver_name:<12} | Cước phí nền: {o.base_fee:,} VND | Khoảng cách: {o.distance} Km | Phụ phí: {o.surcharge:,} VND | Chi phí vận chuyển: {o.total_delivery_cost:,} VND | Trạng thái: {o.delivery_status}")
    
    # THÊM MỚI
    def add_order(self):
        list_id = [o.order_id for o in self.orders]
        while True:
            new_id = check_space("Nhập ID đơn hàng mới: ")
            if new_id.strip().upper() in list_id:
                print ("ID đơn hàng đã tồn tại!")
            else:
                break
        name_receiver = check_num_in_string("Nhập tên người nhận: ")
        base_fee = change_into_int("Nhập cước phí nền: ")
        distance_input = check_distance("Nhập khoảng cách: ")
        surcharge_input = change_into_int("Nhập phụ phí: ")
        new_order = DeliveryOrder(new_id.strip().upper(), name_receiver.strip().title(), base_fee, distance_input, surcharge_input)
        new_order.calculate_total_cost()
        new_order.classify_delivery_status()
        self.orders.append(new_order)
        print ("Thêm đơn hàng thành công!")

    # CẬP NHẬT
    def update_order(self):
        if len(self.orders) == 0:
            print ("Hiện chưa có đơn hàng nào.")
        else:
            found = False
            id_update = check_space("Nhập mã cần sửa: ")
            for o in self.orders:
                if id_update.strip().upper() == o.order_id:
                    found = True
                    o.base_fee = change_into_int("Nhập cước phí mới: ")
                    o.distance = check_distance("Nhập khoảng cách mới: ")
                    o.surcharge = change_into_int("Nhập phụ phí mới: ")
                    o.calculate_total_cost()
                    o.classify_delivery_status()
                    print ("Cập nhật đơn hàng thành công!")
                    break
            if found == False:
                print ("Không tìm thấy đơn hàng!")
    
    # XÓA ĐƠN HÀNG
    def delete_order(self):
        if len(self.orders) == 0:
            print ("Hiện chưa có đơn hàng nào.")
        else:
            found = False
            del_id = check_space("Nhập mã cần xóa: ")
            for o in self.orders:
                if del_id.strip().upper() == o.order_id:
                    found = True
                    del_choice = check_space("Bạn có chắc muốn xóa không (Y/N)?: ").upper()
                    match del_choice:
                        case "Y":
                            self.orders.remove(o)
                            print ("Xóa đơn hàng thành công!")
                        case "N":
                            print ("Hủy thao tác!")
                            return
                        case _:
                            print ("Lựa chọn không hợp lệ!")
                    break
            if found == False:
                print ("Không tìm thấy đơn hàng!")

    # TÌM ĐƠN HÀNG
    def search_order(self):
        if len(self.orders) == 0:
            print ("Hiện chưa có đơn hàng nào.")
        else:
            found = False
            name_find = check_space("Nhập tên người nhận cần tìm: ")
            for o in self.orders:
                if name_find.strip().lower() in o.receiver_name.lower():
                    found = True
                    print (f"{o.order_id} | Tên người nhận: {o.receiver_name} | Cước phí nền: {o.base_fee:,} VND | Khoảng cách: {o.distance} Km | Phụ phí: {o.surcharge:,} VND | Chi phí vận chuyển: {o.total_delivery_cost:,} VND | Trạng thái: {o.delivery_status}")
            if found == False:
                print (f"Không tìm thấy người nhận!")

def main():
    order_manager = OrderManager()
    sample_orders = [
        DeliveryOrder("HD01", "Nguyen Van A", 15000, 5, 10000),   
        DeliveryOrder("HD02", "Tran Thi B", 20000, 8, 25000),     
        DeliveryOrder("HD03", "Le Van C", 12000, 35, 40000),      
        DeliveryOrder("HD04", "Pham Minh D", 25000, 40, 100000)   
    ]
    
    for order in sample_orders:
        order.calculate_total_cost()
        order.classify_delivery_status()
        order_manager.orders.append(order)
    while True:
        print (""" 
================ MENU ================
1. Hiển thị danh sách vận đơn trong hệ thống
2. Nhập vận đơn mới
3. Cập nhật thông tin vận đơn
4. Xóa vận đơn khỏi hệ thống
5. Tìm kiếm vận đơn theo tên người nhận
6. Thoát
=====================================""")
        choice = input ("Nhập lựa chọn của bạn: ")
        match choice:
            case "1":
                order_manager.show_all_orders()
            case "2":
                order_manager.add_order()
            case "3":
                order_manager.update_order()
            case "4":
                order_manager.delete_order()
            case "5":
                order_manager.search_order()
            case "6":
                print ("Thoát chương trình!")
                break
            case _:
                print ("Lựa chọn không hợp lệ!")
main()