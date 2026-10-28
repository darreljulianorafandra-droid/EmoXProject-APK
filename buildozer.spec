[app]
title = EmoXProject
package.name = emoxproject
package.domain = org.oxzstudios
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 3.5.6

# PENTING BUAT PYGAME: Pake python 3.10 biar gak error
requirements = python3==3.10.12,pygame,pyjnius,android
orientation = portrait
fullscreen = 1

android.permissions = INTERNET,WAKE_LOCK
android.api = 31
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1