from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from bs4 import BeautifulSoup
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.factory import Factory
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ListProperty, ObjectProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivymd.uix.behaviors import CircularRippleBehavior, DeclarativeBehavior
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.tooltip import MDTooltip


KV = '''
<TooltipMDIconButton@MDIconButton+MDTooltip>:
<MultiSelectOption@MDRaisedButton+MDToggleButton>:
    background_color: app.theme_cls.primary_color
    background_normal: [.5, .2, .5, .5]
    background_down: [.5, .3, .5, 1]
    #font_color_normal: [1, 1, .5, .5]
    #font_color_down: [.5, .5, .5, 1]
    spacing: "15dp"
    size_hint: None, None
    height: '40dp'
    #allow_no_selection: True
MDScreenManager:
    HomePage:
    About:
<HomePage>:
    MDScreen:
        name: "screen A"
        #md_bg_color: "lightblue"
        orientation: 'vertical'

        MDHeroFrom:
            id: hero_from
            tag: "hero"
            size_hint: None, None
            size: "120dp", "120dp"
            pos_hint: {"top": .98}
            x: 24
        MDBottomNavigation:
            #panel_color: "#eeeaea"
            selected_color_background: app.theme_cls.primary_color
            text_color_active: "lightgrey"
            orientation: 'vertical'
            MDBottomNavigationItem:
                name: 'Home'
                text: 'Home'
                icon: "home"
                #badge_icon: "numeric-0"
                orientation: 'vertical'
                on_tab_press:
                    root.current_heroes = ["hero"]
                    root.current = "screen A"
                MDTopAppBar:
                    title: "Home"
                    radius: 12
                    #md_bg_color: app.theme_cls.primary_color #app.theme_cls.accent_color #
                    elevation: 5
                    use_overflow: True
                    #left_action_items:[['menu',lambda x: app.navigation_draw()]]
                    right_action_items:
                        [
                        ["home", lambda x: app.callback_topappbar(x), "Home"],
                        ["message-star", lambda x: app.callback_topappbar(x), "Message star"],
                        ["message-question", lambda x: app.callback_topappbar(x), "Message question"],
                        ["message-reply", lambda x: app.callback_topappbar(x), "Message reply"],
                        ['logout',lambda x: app.on_exit(), "Exit"]
                        ]
                    pos_hint: {'center_x': .5, 'center_y': .98}
                RstDocument:
                    id: result
                    background_color: app.theme_cls.primary_color
                    text: '\\n'.join(("Horoscope Text", "========", "Content of the horoscope:"))
                    font_size: 20
                    pos_hint: {'center_x': .5, 'center_y': .64}
                    size_hint: .95, .40
                MultiSelectSpinner:
                    id: zodiac
                    values: '1. Aries', '2. Taurus', '3. Gemini','4. Cancer', '5. Leo', '6. Virgo', '7. Libra', '8. Scorpio', '9. Sagittarius', '10. Capricorn', '11. Aquarius', '12. Pisces'
                    size_hint: 0.5, 0.1
                    pos_hint: {'center_x': .5, 'center_y': .35}
                    background_color: app.theme_cls.primary_color
                    text: 'Choose Zodiac'
                    font_size: 20
                MultiSelectSpinner:
                    id: day
                    values: 'Today', 'Yesterday', 'Tomorrow',
                    size_hint: 0.5, 0.1
                    pos_hint: {'center_x': .5, 'center_y': .2}
                    background_color: app.theme_cls.primary_color
                    text: 'Choose Day'
                    font_size: 20
                MDRaisedButton:
                    md_bg_color: app.theme_cls.primary_color
                    id: horoscope
                    pos_hint: {'center_x': .5, 'center_y': .08}
                    font_size: 20
                    text: 'Request'
                    on_release:
                        root.current_heroes = ["hero"]
                        root.current = root.request_button_press()
                        #on_touch_down: app.on_touch_up()
                MDSwitch:
                    tooltip_text: "Theme"
                    active: False
                    icon_active: "check"
                    icon_active_color: "white"
                    icon_inactive: "close"
                    icon_inactive_color: "grey"
                    thumb_color_active: "brown"
                    track_color_active: app.theme_cls.primary_color
                    disabled: False
                    track_color_disabled: "lightgrey"
                    disabled: False
                    thumb_down: app.switch_theme_style(self, self.active)
                    #on_active: app.switch_theme_style(self, self.active) #root.switch_click(self, self.active)
                    widget_style: "android"
                    id: switch
                    font_size: 20
                    pos_hint: {'center_x': .87, 'center_y': .87}
                    background_color: app.theme_cls.primary_color
                    #thumb_color: 1, 0, 1, 1
                    #thumb_color_down: 1, 0, 1, 1
                    #on_touch_down: app.home_button()
                    #on_touch_up: root.switch_callback()
            MDBottomNavigationItem:
                name: 'About'
                text: 'About'
                icon: "book"
                #badge_icon: "numeric-0"
                orientation: 'vertical'
                #on_tab_press:
                #root.current_heroes = ["hero"]
                #root.current = "screen A"
                RstDocument:
                    font_size: 24
                    text: '\\n'.join(("========","About", "========", "**Daily Horoscope**", "=======", "Developed by Taiwo Owolanke"))
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    size_hint: 1, 1
'''


class TooltipMDIconButton(MDIconButton, MDTooltip):
    pass


class DeclarativeStyleBoxLayout(DeclarativeBehavior, BoxLayout):
    pass


class About(Screen):
    pass


class Item(OneLineAvatarIconListItem):
    left_icon = StringProperty()
    right_icon = StringProperty()
    right_text = StringProperty()


class HomePage(Screen):  # root Widget

    base_url = 'https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-{}.aspx?sign={}'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.html = None
        self.req = None
        self.result = None

    def request_button_press(self):  # button function/method
        pass

        zodiac_sign = self.ids.zodiac.text[0:1].strip()
        day = self.ids.day.text.lower()

        if zodiac_sign == 'C' or zodiac_sign == 'P' or zodiac_sign == "" or zodiac_sign == str \
                or zodiac_sign is None or day == 'choose day' or day is None or day == "":
            self.ids.result.text = "Opps! Seems you forgot to pick either your Zodiac sign or day"
            return
        else:
            Clock.stop_clock()  # Start the Kivy clock
            req = UrlRequest(self.base_url.format(day, zodiac_sign),
                             on_success=None, on_failure=None, on_error=None,
                             on_progress=None, req_body=None, req_headers=None,
                             method='GET')  # get request thread
            while not req.is_finished:  # start while loop to test is_finished
                Clock.tick()  # tick clock per cycle
            Clock.stop_clock()  # Stop the clock
            soup = BeautifulSoup(req.result, "html.parser")
            # Html parser - scrape/extract data from the HTML page
            self.ids.result.text = soup.find("div",
                                             class_="main-horoscope").p.text
            # find a div content in the HTML page after scraping & pass the output to result textfield.


class MultiSelectSpinner(MDRaisedButton):
    dropdown = ObjectProperty(None)

    values = ListProperty([])

    selected_values = ListProperty([])

    def __init__(self, **kwargs):
        self.bind(dropdown=self.update_dropdown)
        self.bind(values=self.update_dropdown)
        super(MultiSelectSpinner, self).__init__(**kwargs)
        self.bind(on_release=self.toggle_dropdown)

    def toggle_dropdown(self, *args):
        if self.dropdown.parent:
            self.dropdown.dismiss()
        else:
            self.dropdown.open(self)

    def update_dropdown(self, *args):
        if not self.dropdown:
            self.dropdown = DropDown()
        values = self.values
        if values:
            if self.dropdown.children:
                self.dropdown.clear_widgets()
            for value in values:
                b = Factory.MultiSelectOption(text=value)
                b.bind(state=self.select_value)
                self.dropdown.add_widget(b)

    def select_value(self, instance, value):
        if value == 'down':
            if instance.text not in self.selected_values:
                self.selected_values.append(instance.text)
        else:
            if instance.text in self.selected_values:
                self.selected_values.remove(instance.text)

    def on_selected_values(self, instance, value):
        if value:
            self.text = ', '.join(value)
        else:
            self.text = ''


class HoroScope(MDApp):

    def __init__(self):
        super().__init__()

    def build(self):  # Main app build function
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.4
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "Cyan"
        return Builder.load_string(KV)

    def menu_callback(self, text_item):
        print(text_item)
        return text_item

    def switch_theme_style(self, switchObject, switchValue):  # Switch theme function
        if switchValue:
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

    def callback_topappbar(self, instance_action_top_appbar_button):  # TopAppBar buttons callback function
        pass

    def navigation_draw(self):  # lambda Function
        pass


ma = HoroScope()
ma.run()
