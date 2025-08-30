from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6 import uic
from PyQt6.QtGui import *
from data_io import *

class Alert(QMessageBox):
    def error_message(self, title, message):
        self.setIcon(QMessageBox.Icon.Critical)
        self.setWindowTitle(title)
        self.setText(message)
        self.exec()

    def success_message(self, title, message):
        self.setIcon(QMessageBox.Icon.Information)
        self.setWindowTitle(title)
        self.setText(message)
        self.exec()


class Login(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/login.ui", self)

        self.email_input = self.findChild(QLineEdit,"txt_email")
        self.password_input = self.findChild(QLineEdit, "txt_password")
        self.btn_login = self.findChild(QPushButton,"btn_login")
        self.btn_sign_up = self.findChild(QPushButton,"btn_sign_up")
        self.btn_eye = self.findChild(QPushButton,"btn_eye")
        
        self.btn_eye.clicked.connect(lambda: self.show_password(self.btn_eye, self.password_input))
        self.btn_login.clicked.connect(self.login)
        self.btn_sign_up.clicked.connect(self.show_register)
    
    def show_password(self, button: QPushButton, Input: QLineEdit):
        if Input.echoMode() == QLineEdit.EchoMode.Password:
            Input.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/eye-regular.svg"))
        else:
            Input.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eye-slash-regular.svg"))

    def login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if email == "":
            msg.error_message("Login", "Email is required")
            self.email_input.setFocus()
            return
        if password == "":
            msg.error_message("Login", "Password is required")
            self.password_input.setFocus()
            return
        user = get_user_by_email_and_password(email, password)
        if user:
            msg.success_message("Login", "Welcome to the system")
            self.show_home(user["id"])
            return        
        
        msg.error_message("Login", "Invalid email or password")
        self.email_input.setFocus()
    
    def show_home(self, id):
        self.home = Home(id)
        self.home.show()
        self.close()

    def show_register(self):
        self.register = Register()
        self.register.show()
        self.close()

class Register(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/register.ui", self)

        self.email_input = self.findChild(QLineEdit, "txt_email")
        self.password_input = self.findChild(QLineEdit, "txt_password")
        self.confirm_pass_input = self.findChild(QLineEdit, "txt_confirm_password")
        self.name_input = self.findChild(QLineEdit, "txt_name")
        self.btn_login = self.findChild(QPushButton, "btn_login")
        self.btn_sign_up = self.findChild(QPushButton, "btn_sign_up")
        self.btn_eye = self.findChild(QPushButton, "btn_eye")
        self.btn_eye_cp = self.findChild(QPushButton, "btn_eye_cp")

        self.btn_eye.clicked.connect(lambda: self.show_password(self.btn_eye, self.password_input))
        self.btn_eye_cp.clicked.connect(lambda: self.show_password(self.btn_eye_cp, self.confirm_pass_input))
        self.btn_sign_up.clicked.connect(self.register)
        self.btn_login.clicked.connect(self.show_login)
    def show_password(self, button: QPushButton, Input: QLineEdit):
        if Input.echoMode() == QLineEdit.EchoMode.Password:
            Input.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/eye-regular.svg"))
        else:
            Input.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eye-slash-regular.svg"))

    def register(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        confirm_pass = self.confirm_pass_input.text().strip()
        name = self.name_input.text().strip()

        if email == "":
            msg.error_message("Register", "Email is required")
            self.email_input.setFocus()
            return
        
        if name == "":
            msg.error_message("Register", "Name is required")
            self.name_input.setFocus()
            return
        
        if password == "":
            msg.error_message("Register", "Password is required")
            self.password_input.setFocus()
            return

        if confirm_pass == "":
            msg.error_message("Register", "Confirm Password is required")
            self.confirm_pass_input.setFocus()
            return

        if password != confirm_pass:
            msg.error_message("Register", "Password and Confirm password do not match")
            self.password_input.setFocus()
            return
        
        user = get_user_by_email(email)
        if user:
            msg.error_message("Register", "Email already exists")
            self.email_input.setFocus()
            return
                
        create_user(email,password,name)

        msg.success_message("Register", "Account created successfully")
        self.show_login()

    def show_login(self):
        self.login = Login()
        self.login.show()
        self.close()

class ItemWidget(QWidget):
    def __init__(self, product_data, parent=None):
        super().__init__(parent)
        uic.loadUi("ui/item.ui", self)
        
        self.product_data = product_data
        self.parent = parent
        
        # Set fixed size for consistent layout
        self.setFixedSize(280, 320)
        
        # Set style for better appearance
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }
            QWidget:hover {
                border: 2px solid #007bff;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)
        
        # Connect widgets
        self.lbl_product_name = self.findChild(QLabel, "lbl_product_name")
        self.lbl_product_image = self.findChild(QLabel, "lbl_product_image")
        self.lbl_rating = self.findChild(QLabel, "lbl_rating")
        self.lbl_star_icon = self.findChild(QLabel, "lbl_star_icon")
        self.lbl_price = self.findChild(QLabel, "lbl_price")
        self.btn_view_detail = self.findChild(QPushButton, "btn_view_detail")
        self.btn_add_to_cart = self.findChild(QPushButton, "btn_add_to_cart")
        
        # Connect signals
        self.btn_view_detail.clicked.connect(self.view_detail)
        self.btn_add_to_cart.clicked.connect(self.add_to_cart)
        
        # Load product data
        self.load_product_data()
    
    def load_product_data(self):
        """Load product data into the widget"""
        if self.product_data:
            # Set product name
            name = self.product_data.get("name", "")
            if len(name) > 40:
                name = name[:37] + "..."
            self.lbl_product_name.setText(name)
            
            # Set product image
            image_path = self.product_data.get("image", "")
            if image_path:
                # Convert to proper path format
                if image_path.startswith("Img/"):
                    image_path = image_path.replace("Img/", "img/")
                if not image_path.endswith(('.jpg', '.png', '.webp')):
                    image_path += ".jpg"
                
                try:
                    pixmap = QPixmap(image_path)
                    if not pixmap.isNull():
                        self.lbl_product_image.setPixmap(pixmap.scaled(201, 161, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                except:
                    # Set default image if loading fails
                    pass
            
            # Set rating
            rating = self.product_data.get("rating", 0)
            self.lbl_rating.setText(f"{rating:.1f}")
            
            # Set star icon based on rating
            try:
                if rating >= 4.5:
                    star_path = "img/4.1 star.png"  # 5 star
                elif rating >= 4.0:
                    star_path = "img/4.1 star.png"  # 4 star
                elif rating >= 3.5:
                    star_path = "img/4.1 star.png"  # 3.5 star
                else:
                    star_path = "img/4.1 star.png"  # Default
                
                pixmap = QPixmap(star_path)
                if not pixmap.isNull():
                    self.lbl_star_icon.setPixmap(pixmap.scaled(51, 41, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            except:
                pass
            
            # Set price
            price = self.product_data.get("price", 0)
            if price >= 1000000:
                formatted_price = f"{price/1000000:.1f}M VNĐ"
            elif price >= 1000:
                formatted_price = f"{price/1000:.0f}K VNĐ"
            else:
                formatted_price = f"{price:,} VNĐ"
            self.lbl_price.setText(formatted_price)
    
    def view_detail(self):
        """Navigate to product detail page"""
        if self.parent and hasattr(self.parent, 'navigate_to_detail'):
            self.parent.navigate_to_detail(self.product_data)
    
    def add_to_cart(self):
        """Add product to cart"""
        if self.product_data:
            msg.success_message("Cart", f"Added {self.product_data.get('name', 'Product')} to cart")

class Home(QWidget):
    def __init__(self, id):
        super().__init__()
        uic.loadUi("ui/home.ui", self)

        self.id = id
        self.user = get_user_by_id(id)
        self.load_user_info()

        self.stack_widget = self.findChild(QStackedWidget, "stackedWidget")
        
        self.btn_home = self.findChild(QPushButton, "btn_home")
        self.btn_products = self.findChild(QPushButton, "btn_products")
        self.btn_detail = self.findChild(QPushButton, "btn_detail")
        self.btn_profile = self.findChild(QPushButton, "btn_profile")
        self.btn_save_account = self.findChild(QPushButton, "btn_save_account")
        self.btn_avatar = self.findChild(QPushButton, "btn_avatar")
        
        self.txt_name = self.findChild(QLineEdit, "txt_name")
        self.txt_email = self.findChild(QLineEdit, "txt_email")
        self.txt_birthday = self.findChild(QDateEdit, "txt_birthday")
        self.txt_gender = self.findChild(QComboBox, "txt_gender")
        self.btn_avatar = self.findChild(QPushButton, "btn_avatar")

        self.btn_home.clicked.connect(lambda: self.navigate_screen(self.stack_widget, 0))
        self.btn_products.clicked.connect(lambda: self.navigate_screen(self.stack_widget, 5))
        self.btn_detail.clicked.connect(lambda: self.navigate_screen(self.stack_widget, 3))
        self.btn_profile.clicked.connect(lambda: self.navigate_screen(self.stack_widget, 4))
        self.btn_avatar.clicked.connect(self.update_avatar)
        self.btn_save_account.clicked.connect(self.update_user_info)
        
        # Load products data
        self.load_products()
        
    def navigate_screen(self, stackWidget: QStackedWidget, index: int):
        stackWidget.setCurrentIndex(index)
    
    def navigate_to_detail(self, product_data):
        """Navigate to product detail page and load product data"""
        self.navigate_screen(self.stack_widget, 3)
        
        # Load product data into detail page
        try:
            detail_page = self.stack_widget.widget(3)  # Index 3 is detail page
            
            # Update product name
            name_label = detail_page.findChild(QLabel, "lbl_product_name")
            if name_label and product_data:
                name_label.setText(product_data.get("name", ""))
            
            # Update product description
            desc_label = detail_page.findChild(QLabel, "lbl_product_description")
            if desc_label and product_data:
                desc_label.setText(product_data.get("description", ""))
            
            # Update product image
            image_label = detail_page.findChild(QLabel, "lbl_product_image")
            if image_label and product_data:
                image_path = product_data.get("image", "")
                if image_path:
                    if image_path.startswith("Img/"):
                        image_path = image_path.replace("Img/", "img/")
                    if not image_path.endswith(('.jpg', '.png', '.webp')):
                        image_path += ".jpg"
                    
                    try:
                        pixmap = QPixmap(image_path)
                        if not pixmap.isNull():
                            image_label.setPixmap(pixmap.scaled(381, 281, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                    except:
                        pass
            
            # Update price
            price_label = detail_page.findChild(QLabel, "lbl_current_price")
            if price_label and product_data:
                price = product_data.get("price", 0)
                formatted_price = f"VNĐ {price:,}"
                price_label.setText(formatted_price)
            
            # Update original price if available
            original_price_label = detail_page.findChild(QLabel, "lbl_original_price")
            if original_price_label and product_data:
                original_price = product_data.get("original_price", 0)
                if original_price > price:
                    formatted_original = f"VNĐ {original_price:,}"
                    original_price_label.setText(formatted_original)
                    original_price_label.setVisible(True)
                else:
                    original_price_label.setVisible(False)
            
            # Update specifications
            specs_label = detail_page.findChild(QLabel, "lbl_key_features_content")
            if specs_label and product_data:
                specs = product_data.get("specifications", {})
                if specs:
                    specs_text = f"""
{specs.get('processor', '')}
{specs.get('ram', '')}
{specs.get('storage', '')}
{specs.get('graphics', '')}
{specs.get('os', '')}
{specs.get('ports', '')}
                    """.strip()
                    specs_label.setText(specs_text)
                    
        except Exception as e:
            print(f"Error loading product detail: {e}")
        
    def load_products(self):
        """Load products from JSON and create ItemWidget instances"""
        try:
            import json
            with open('data/data.json', 'r', encoding='utf-8') as f:
                products = json.load(f)
            
            # Get the products page widget
            products_page = self.stack_widget.widget(5)  # Index 5 is products page
            
            # Create a scrollable grid layout for products
            if not hasattr(products_page, 'products_layout'):
                # Remove existing content and create new layout
                for child in products_page.children():
                    if isinstance(child, QWidget) and child != products_page.findChild(QLabel, "label_14"):
                        child.setParent(None)
                
                # Create main layout
                main_layout = QVBoxLayout()
                products_page.setLayout(main_layout)
                
                # Add title
                title_label = products_page.findChild(QLabel, "label_14")
                if title_label:
                    main_layout.addWidget(title_label)
                
                # Create scroll area
                scroll_area = QScrollArea()
                scroll_widget = QWidget()
                scroll_layout = QGridLayout(scroll_widget)
                
                # Set spacing between items
                scroll_layout.setSpacing(20)
                scroll_layout.setContentsMargins(20, 20, 20, 20)
                
                # Create ItemWidget for each product in a grid
                row = 0
                col = 0
                max_cols = 3
                
                for i, product in enumerate(products):
                    item_widget = ItemWidget(product, self)
                    scroll_layout.addWidget(item_widget, row, col)
                    
                    col += 1
                    if col >= max_cols:
                        col = 0
                        row += 1
                
                # Set scroll area properties
                scroll_area.setWidget(scroll_widget)
                scroll_area.setWidgetResizable(True)
                scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
                scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
                
                # Add scroll area to main layout
                main_layout.addWidget(scroll_area)
                
                products_page.products_layout = main_layout
                products_page.scroll_area = scroll_area
                
        except Exception as e:
            print(f"Error loading products: {e}")
        
    def load_user_info(self):
        self.user = get_user_by_id(self.id)
        self.txt_name.setText(self.user["name"])
        self.txt_email.setText(self.user["email"])
        self.txt_birthday.setDate(QDate.fromString(self.user["birthday"], "dd//MM//yyyy"))
        self.txt_gender.setCurrentText(self.user["gender"])
        self.btn_avatar.setIcon(QIcon(self.user["avatar"]))

    def update_avatar(self):
        file,_ = QFileDialog.getOpenFileName(self,"Select Image", "", "Image Files(*.png *.jpg *jpeg *bmp)")
        if file:
            self.user["avatar"] = file
            self.btn_avatar.setIcon(QIcon(file))
            update_user_avatar(self.id, file)
            msg.success_message("Update", "Avatar updated successfully")

    def update_user_info(self):
        name = self.txt_name.text().strip()
        birthday = self.txt_birthday.date().toString("dd//MM//yyyy")
        gender = self.txt_gender.currentText()
        update_user(self.id, name, birthday, gender)
        msg.success_message("Update", "User info updated successfully")
        self.load_user_info()

if __name__ == "__main__":
    app = QApplication([])
    msg = Alert()
    window = Login()
    window = Home(1)
    window.show()
    app.exec()