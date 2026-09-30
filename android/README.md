# RHA Connect — Native Android client

RHA Connect is a premium native Kotlin + Jetpack Compose client for Android 9–14 (API 26+). It includes:

- Simple Gmail/email entry screen
- Feed, reels/discover, chat list and chat detail surfaces
- Audio/video call entry points and permission center
- Voice-message recording interaction in chat
- `@username` profile search and profile-ready UI
- Cloudinary unsigned upload abstraction for image/video/audio assets
- Existing RHA voice-engine foreground service retained for local assistant mode

## Build

Open `android/` in Android Studio or use the repository workflow. GitHub Actions builds `assembleDebug` on every push to `main`.

```bash
gradle assembleDebug
```

The sandbox has no Android SDK, so APK verification is performed by GitHub Actions after push.

## Cloudinary

Set these properties privately in `~/.gradle/gradle.properties` or CI secrets:

```properties
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_UPLOAD_PRESET=your_unsigned_preset
```

`CloudinaryMediaClient` uses unsigned uploads and supports `auto` resource type for images, video and audio. Configure authenticated/server-side transformations and moderation before production.

## Realtime backend boundary

The UI is production-oriented and the existing WebSocket voice service remains available. Actual multi-user identity, presence, push notifications, message persistence, WebRTC media negotiation and TURN require a backend (Firebase/Supabase/custom WebSocket + TURN). No credentials were present in the repository, so the app does not invent or hard-code a provider account.
