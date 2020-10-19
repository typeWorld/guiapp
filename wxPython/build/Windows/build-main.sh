set -e

echo "Python build"
python wxPython/build/Windows/setup.py build > nul # muting too much output

echo "/build content"
dir build

echo "Add Windows App Manifest"
"$WINDOWSKITBIN\\mt.exe" -manifest "wxPython/build/Windows/windowsAppManifest.xml" -outputresource:build\\TypeWorld.exe;#1

echo "Copy Google Code"
dir "$SITEPACKAGES"
echo 1
echo "$SITEPACKAGES\\google" "build\\lib\\google" /i /e /h
xcopy "$SITEPACKAGES\\google" "build\\lib\\google" /i /e /h
echo 2
xcopy "$SITEPACKAGES\\googleapis_common_protos-1.52.0.dist-info" "build\\lib\\googleapis_common_protos-1.52.0.dist-info" /i /e /h
echo 3
xcopy "$SITEPACKAGES\\google_api_core-1.22.4.dist-info" "build\\lib\\google_api_core-1.22.4.dist-info" /i /e /h
echo 4
xcopy "$SITEPACKAGES\\google_auth-1.22.1.dist-info" "build\\lib\\google_auth-1.22.1.dist-info" /i /e /h
echo 5
xcopy "$SITEPACKAGES\\google_cloud_pubsub-2.1.0.dist-info" "build\\lib\\google_cloud_pubsub-2.1.0.dist-info" /i /e /h

echo "Copy ynlib"
xcopy ynlib "build\\lib\\ynlib" /i /e /h

echo "Copy importlib_metadata"
xcopy "$SITEPACKAGES\\importlib_metadata" "build\\lib\\importlib_metadata"  /i /e /h
xcopy "$SITEPACKAGES\\importlib_metadata-1.7.0.dist-info" "build\\lib\\importlib_metadata-1.7.0.dist-info" /i /e /h

echo "Signing TypeWorld.exe"
"$WINDOWSKITBIN\\signtool.exe" sign /tr http://timestamp.digicert.com /debug /td sha256 /fd SHA256 /f jan_gerner.p12 /p $JANGERNER_P12_PASSWORD "build\\TypeWorld.exe"
# $WINDOWSKITBIN\\signtool.exe" sign /tr http://timestamp.digicert.com /debug /td sha256 /fd SHA256 /n "Jan Gerner" "build\\TypeWorld.exe"',

echo "Signing TypeWorld Subscription Opener.exe"
"$WINDOWSKITBIN\\signtool.exe" sign /tr http://timestamp.digicert.com /debug /td sha256 /fd SHA256 /f jan_gerner.p12 /p $JANGERNER_P12_PASSWORD "build\\TypeWorld Subscription Opener.exe"
# $WINDOWSKITBIN\\signtool.exe" sign /tr http://timestamp.digicert.com /debug /td sha256 /fd SHA256 /n "Jan Gerner" "build\\TypeWorld Subscription Opener.exe"',

echo "Verify signature"
"$WINDOWSKITBIN\\signtool.exe" verify /pa /v "build\\TypeWorld.exe"
"$WINDOWSKITBIN\\signtool.exe" verify /pa /v "build\\TypeWorld Subscription Opener.exe"


    # if "agent" in profile:
    #     executeCommands(
    #         [
    #             [
    #                 "Signing TypeWorld Taskbar Agent.exe",
    #                 $WINDOWSKITBIN\\signtool.exe" sign /tr http://timestamp.digicert.com /debug /td sha256 /fd SHA256 /a /n "Jan Gerner" "build\\TypeWorld Taskbar Agent.exe"',
    #                 True,
    #             ],
    #             [
    #                 "Verify signature",
    #                 $WINDOWSKITBIN\\signtool.exe" verify /pa /v "build\\TypeWorld Taskbar Agent.exe"',
    #                 True,
    #             ],
    #         ]        )

echo "App Self Test"
"build\\TypeWorld.exe" selftest
