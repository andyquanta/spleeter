# Developer Guide


docker build -t spleeter:v2.4.14 .
docker tag spleeter:v2.4.14 us-central1-docker.pkg.dev/audition-toolkit/audition-toolkit/spleeter:v2.4.14
docker push us-central1-docker.pkg.dev/audition-toolkit/audition-toolkit/spleeter:v2.4.14


docker run -it --net=host -e JWT_SECRET="$JWT_SECRET" -v $(pwd)/local/raw:/raw 
 -v $(pwd)/.cache/key:/key spleeter:v2.4.12


docker run -it --entrypoint /bin/bash -v $(pwd)/.cache/audition-firebase.json:/key/notification-svc.json \
    -v $(pwd)/.cache/audition-toolkit-storage.json:/key/storage.json \
    -v $(pwd)/.cache/audition-toolkit-pub-sub-subscriber.json:/key/pub-sub.json -v $(pwd)/models:/model \
    spleeter:v2.4.1

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
