class User:
    def __init__(self, name):
        self.name = name

    def launch_app(self, app):
        print(f"[사용자] {self.name} 앱 실행")
        app.show_login()

    def enter_login(self, app, id, pw):
        print(f"[사용자] 로그인 정보 입력")
        app.login(id, pw)

    def browse_menu(self, app):
        print(f"[사용자] 음식 메뉴 탐색 요청")
        app.request_menu()

    def place_order(self, app, menu_item):
        print(f"[사용자] 메뉴 선택 및 주문 요청: {menu_item}")
        app.send_order(menu_item)

    def receive_food(self, delivery):
        print(f"[사용자] {delivery}로부터 음식 배달 받음")
        print(f"[사용자] 배달 완료 확인")


class App:
    def __init__(self, auth_server, server):
        self.auth_server = auth_server
        self.server = server

    def show_login(self):
        print("[앱] 로그인 화면 표시")

    def login(self, id, pw):
        print("[앱] 로그인 요청 전송")
        result = self.auth_server.authenticate(id, pw)
        if result:
            print("[앱] 로그인 성공")
        else:
            print("[앱] 로그인 실패")

    def request_menu(self):
        menu = self.server.get_menu()
        print(f"[앱] 메뉴 화면 표시: {menu}")

    def send_order(self, menu_item):
        self.server.process_order(menu_item)


class AuthServer:
    def authenticate(self, id, pw):
        print("[인증서버] 로그인 요청 처리")
        return id == "user" and pw == "pass"


class Server:
    def __init__(self, restaurant, delivery_agent):
        self.restaurant = restaurant
        self.delivery_agent = delivery_agent

    def get_menu(self):
        print("[서버] 메뉴 데이터 요청 처리")
        return ["김치찌개", "비빔밥", "불고기"]

    def process_order(self, menu_item):
        print(f"[서버] 주문 정보 전달: {menu_item}")
        self.restaurant.receive_order(menu_item)
        accepted = self.delivery_agent.assign_delivery()
        self.restaurant.confirm_order()
        print("[서버] 주문 접수 완료 응답")
        print("[앱] 주문 완료 알림")

        self.restaurant.prepare_food()
        self.delivery_agent.pick_up_food(self.restaurant)
        self.delivery_agent.deliver_to_user()


class Restaurant:
    def receive_order(self, item):
        print(f"[식당] 주문 전달받음: {item}")

    def confirm_order(self):
        print("[식당] 주문 접수 확인")

    def prepare_food(self):
        print("[식당] 음식 준비 완료")

class DeliveryAgent:
    def assign_delivery(self):
        print("[배달기사] 배차 요청 수신")
        print("[배달기사] 배차 수락")
        return True

    def pick_up_food(self, restaurant):
        print("[배달기사] 음식 픽업")

    def deliver_to_user(self):
        print("[배달기사] 음식 배달")


# 실행 흐름
auth_server = AuthServer()
restaurant = Restaurant()
delivery_agent = DeliveryAgent()
server = Server(restaurant, delivery_agent)
app = App(auth_server, server)
user = User("홍길동")

# 시나리오 실행
user.launch_app(app)
user.enter_login(app, "user", "pass")
user.browse_menu(app)
user.place_order(app, "비빔밥")
user.receive_food("배달기사")
