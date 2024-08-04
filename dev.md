# Developer Guide

docker run -it --entrypoint /bin/bash -v $(pwd)/.cache/audition-firebase.json:/key/notification-svc.json \
    -v $(pwd)/.cache/audition-toolkit-storage.json:/key/storage.json \
    -v $(pwd)/.cache/audition-toolkit-pub-sub-subscriber.json:/key/pub-sub.json \
    spleeter:v2.4.0

```json
{
        "data": {"file_name": "kanne-maniye.zip"},
        "event": "file_uploaded"
}
```

Android dependencies

dependencies {
    // Import the BoM for the Firebase platform
    implementation(platform("com.google.firebase:firebase-bom:33.1.2"))

    // Add the dependencies for the In-App Messaging and Analytics libraries
    // When using the BoM, you don't specify versions in Firebase library dependencies
    implementation("com.google.firebase:firebase-inappmessaging-display")
    implementation("com.google.firebase:firebase-analytics")
}