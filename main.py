from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.clock import Clock

import arabic_reshaper
from bidi.algorithm import get_display

from database import create_tables, add_book, get_books, get_books_by_category

# ===== دالة تصحيح العربية (للعرض فقط) =====
def ar(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

# ================= Splash Screen =================
class SplashScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.go_to_main, 5)

    def go_to_main(self, dt):
        self.manager.current = "main"

# ================= Main Screen =================
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = BoxLayout(orientation="vertical", padding=15, spacing=10)

        # ===== اسم التطبيق (عرض فقط) =====
        root.add_widget(Label(
            text=ar("منظم الكتب"),
            font_name="fonts/Amiri-Regular.ttf",
            font_size=34,
            size_hint_y=None,
            height=55
        ))

        # ===== إضافة كتاب (كتابة طبيعية) =====
        self.title_input = TextInput(
            hint_text=ar("عنوان الكتاب"),
            font_name="fonts/Amiri-Regular.ttf",
            font_size=16,
            multiline=False,
            halign="right"
        )
        root.add_widget(self.title_input)

        self.author_input = TextInput(
            hint_text=ar("اسم المؤلف"),
            font_name="fonts/Amiri-Regular.ttf",
            font_size=16,
            multiline=False,
            halign="right"
        )
        root.add_widget(self.author_input)

        self.category_input = TextInput(
            hint_text=ar("التصنيف (قانون، أدب، علوم...)"),
            font_name="fonts/Amiri-Regular.ttf",
            font_size=16,
            multiline=False,
            halign="right"
        )
        root.add_widget(self.category_input)

        add_btn = Button(
            text=ar(" إضافة كتاب"),
            font_name="fonts/Amiri-Regular.ttf",
            size_hint_y=None,
            height=45
        )
        add_btn.bind(on_press=self.save_book)
        root.add_widget(add_btn)

        # ===== لائحة الكتب =====
        root.add_widget(Label(
            text=ar(" لائحة الكتب"),
            font_name="fonts/Amiri-Regular.ttf",
            font_size=24,
            size_hint_y=None,
            height=45
        ))

        self.scroll = ScrollView()
        self.books_layout = GridLayout(cols=1, spacing=8, size_hint_y=None)
        self.books_layout.bind(minimum_height=self.books_layout.setter("height"))
        self.scroll.add_widget(self.books_layout)
        root.add_widget(self.scroll)

        # ===== التصنيفات =====
        cat_box = BoxLayout(size_hint_y=None, height=40, spacing=6)
        for cat in ["الكل", "قانون", "أدب", "علوم"]:
            b = Button(
                text=ar(cat),
                font_name="fonts/Amiri-Regular.ttf"
            )
            b.bind(on_press=self.filter_books)
            cat_box.add_widget(b)

        root.add_widget(cat_box)

        self.add_widget(root)
        self.load_books()

    # ===== الوظائف =====
    def save_book(self, instance):
        if self.title_input.text.strip() == "":
            return

        # نخزنو النص الخام (ما فيه ar)
        add_book(
            self.title_input.text,
            self.author_input.text,
            self.category_input.text,
            ""
        )

        self.title_input.text = ""
        self.author_input.text = ""
        self.category_input.text = ""

        self.load_books()

    def load_books(self, category="الكل"):
        self.books_layout.clear_widgets()

        if category == "الكل":
            books = get_books()
        else:
            books = get_books_by_category(category)

        for title, author, cat, *_ in books:
            self.books_layout.add_widget(Label(
                text=ar(f" {title}\n {author}\n🏷 {cat}"),
                font_name="fonts/Amiri-Regular.ttf",
                font_size=15,
                size_hint_y=None,
                height=80,
                halign="right"
            ))

    def filter_books(self, instance):
        # instance.text راه أصلاً معمولة بـ ar
        self.load_books(instance.text)

# ================= App =================
class MonademAlkotobApp(App):
    def build(self):
        create_tables()

        sm = ScreenManager()

        splash = SplashScreen(name="splash")
        splash.add_widget(Image(
            source="assets/logo.png",
            allow_stretch=True,
            keep_ratio=True
        ))

        main = MainScreen(name="main")

        sm.add_widget(splash)
        sm.add_widget(main)

        sm.current = "splash"
        return sm

MonademAlkotobApp().run()
