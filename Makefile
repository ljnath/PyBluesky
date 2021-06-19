# Makefile for PyBluesky android project
# author - ljnath (www.ljnath.com)

ADB = adb
PYTHON = python
APK_NAME = PyBluesky__armeabi-v7a-debug-1.0.0-.apk

PACKAGE_NAME = com.ljnath.pybluesky
ACTIVITY_NAME = org.kivy.android.PythonActivity

all:
	clean
	build
	uninstall
	install
	start

build:
	echo Building project
	$(PYTHON) setup.py apk

uninstall:
	echo Un-installing app with package name $(PACKAGE_NAME) from target device
	$(ADB) uninstall $(PACKAGE_NAME)

install:
	echo Installing $(APK_NAME) in target device
	$(ADB) install $(APK_NAME)

start:
	echo Starting $(APK_NAME) in target device
	$(ADB) shell am start -n $(PACKAGE_NAME)/$(ACTIVITY_NAME)

clean:
	echo Deleting $(APK_NAME)
	rm -f $(APK_NAME) 
