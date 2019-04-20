#!/bin/bash

HEADERPATH="/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk/System/Library/Frameworks/HomeKit.framework/Headers"

echo "import UIKit" > extract.swift
echo "import HomeKit" >> extract.swift
for SYMBOL in `cat $HEADERPATH/*Types.h | grep HM_EXTERN | sed 's/HM_EXTERN NSString \* const //' | sed 's/ .*//' `
do 
	echo "print(\"$SYMBOL\", $SYMBOL)"
done >> extract.swift
