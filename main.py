__version__ = "1.0.0"

import json
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform

if platform == "android":
    from jnius import autoclass
    from android.permissions import request_permissions

    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    BuildVersion = autoclass("android.os.Build$VERSION")
    BleScanner = autoclass("org.nearby.scanner.BleScanner")


class NearbyScannerApp(App):
    def build(self):
        self.scanning = False
        self.root_box = BoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(10)
        )

        header = Label(
            text="[b]NEARBY SCANNER[/b]",
            markup=True,
            font_size="24sp",
            size_hint_y=None,
            height=dp(48)
        )
        self.status = Label(
            text="جاهز. اضغط بدء البحث.",
            font_size="16sp",
            size_hint_y=None,
            height=dp(42)
        )

        self.scan_button = Button(
            text="بدء البحث",
            size_hint_y=None,
            height=dp(52)
        )
        self.scan_button.bind(on_press=self.toggle_scan)

        self.results_label = Label(
            text="لا توجد أجهزة بعد.",
            markup=True,
            size_hint_y=None,
            halign="left",
            valign="top"
        )
        self.results_label.bind(
            texture_size=lambda instance, size:
            setattr(instance, "height", size[1] + dp(20))
        )
        self.results_label.text_size = (None, None)

        scroll = ScrollView()
        self.results_label.size_hint_x = 1
        scroll.add_widget(self.results_label)

        self.root_box.add_widget(header)
        self.root_box.add_widget(self.status)
        self.root_box.add_widget(self.scan_button)
        self.root_box.add_widget(scroll)

        if platform != "android":
            self.status.text = "هذا الإصدار مخصص للتشغيل على Android."
        return self.root_box

    def toggle_scan(self, *_):
        if platform != "android":
            self.status.text = "شغّل التطبيق على هاتف Android."
            return

        if self.scanning:
            self.stop_scan()
        else:
            self.request_scan_permissions()

    def request_scan_permissions(self):
        sdk = int(BuildVersion.SDK_INT)
        if sdk >= 31:
            perms = [
                "android.permission.BLUETOOTH_SCAN",
                "android.permission.BLUETOOTH_CONNECT",
            ]
        else:
            perms = [
                "android.permission.ACCESS_FINE_LOCATION",
                "android.permission.BLUETOOTH",
                "android.permission.BLUETOOTH_ADMIN",
            ]

        request_permissions(perms, self.on_permissions)

    def on_permissions(self, permissions, grant_results):
        # Android returns True for granted permissions.
        if not all(bool(x) for x in grant_results):
            self.status.text = "لم تُمنح صلاحيات Bluetooth. فعّلها من إعدادات التطبيق."
            return

        try:
            activity = PythonActivity.mActivity
            BleScanner.start(activity)
            self.scanning = True
            self.scan_button.text = "إيقاف البحث"
            self.status.text = "يبحث الآن عن إعلانات Bluetooth LE القريبة..."
            self.results_label.text = "جارٍ البحث..."
            self.poll_event = Clock.schedule_interval(self.refresh_results, 1.0)
        except Exception as exc:
            self.status.text = "تعذر بدء الماسح: " + str(exc)

    def refresh_results(self, _dt):
        try:
            raw = BleScanner.getResultsJson()
            devices = json.loads(str(raw))
            if not devices:
                self.results_label.text = (
                    "لم تُكتشف أجهزة بعد.\n"
                    "تأكد من تشغيل Bluetooth، وقرّب جهازاً يعلن BLE."
                )
                return

            lines = []
            for item in devices:
                name = item.get("name") or "اسم غير معلن"
                address = item.get("address") or "غير متاح"
                rssi = item.get("rssi", "?")
                lines.append(
                    f"[b]{name}[/b]\n"
                    f"العنوان: {address}\n"
                    f"قوة الإشارة: {rssi} dBm\n"
                    "------------------------------"
                )
            self.results_label.text = "\n".join(lines)
        except Exception as exc:
            self.status.text = "خطأ في قراءة النتائج: " + str(exc)

    def stop_scan(self):
        try:
            BleScanner.stop()
        except Exception:
            pass
        if hasattr(self, "poll_event"):
            self.poll_event.cancel()
        self.scanning = False
        self.scan_button.text = "بدء البحث"
        self.status.text = "تم إيقاف البحث."

    def on_stop(self):
        if platform == "android" and self.scanning:
            self.stop_scan()


if __name__ == "__main__":
    NearbyScannerApp().run()
