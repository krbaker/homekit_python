cd /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk/System/Library/Frameworks/HomeKit.framework/Headers
cat *Types.h
for SYMBOL in `cat *Types.h | grep HM_EXTERN | sed 's/HM_EXTERN NSString \* const //' | sed 's/ .*//' `; do echo "print(\"$SYMBOL\", $SYMBOL)"; done > ~/Documents/homekit_python/iOS/retrieveInformation.playground/Contents.swift
