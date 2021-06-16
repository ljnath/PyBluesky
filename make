#!/bin/sh
# make file for PyBluesky android project
# author - ljnath (www.ljnath.com)

APK_NAME=PyBluesky__armeabi-v7a-debug-1.0.0-.apk

PACKAGE_NAME=com.ljnath.pybluesky
ACTIVITY_NAME=org.kivy.android.PythonActivity

echo "***********************************************\nStarting PyBluesky build script\n***********************************************"
echo
echo Cleaning existing build artifact
rm -f $APK_NAME
echo
echo Building apk ...
python setup.py apk
echo
echo Un-installing APK from target device
adb uninstall $PACKAGE_NAME
echo
echo Installing APK in target device
adb install $APK_NAME
echo
echo Starting APK in target device
adb shell am start -n $PACKAGE_NAME/$ACTIVITY_NAME
echo
echo "***********************************************\nExiting PyBluesky build script\n***********************************************"
