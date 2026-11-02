[app]

title = Nearby Scanner
package.name = nearbyscanner
package.domain = org.nearby
source.dir = .
source.include_exts = py,java,kv,png,jpg
version = 1.0.0
requirements = python3,kivy,pyjnius
orientation = portrait
fullscreen = 0

android.api = 35
android.minapi = 23
android.ndk = 27c
android.archs = arm64-v8a
android.permissions = BLUETOOTH_SCAN,BLUETOOTH_CONNECT,ACCESS_FINE_LOCATION,BLUETOOTH,BLUETOOTH_ADMIN
android.add_src = src
android.accept_sdk_license = True

p4a.branch = develop

[buildozer]
log_level = 2
warn_on_root = 1
