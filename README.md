# Nearby Scanner (Android / Kivy)

## What it does
- Scans nearby Bluetooth Low Energy (BLE) advertisements.
- Shows advertised device name (if provided), Bluetooth address (if Android exposes it), and RSSI.
- Does not identify people or retrieve social-media accounts.

## Important
A phone appears only if it emits a BLE advertisement that the Android scanner can receive. Many phones do not continuously advertise in a discoverable way. RSSI is signal strength, not a reliable distance measurement.

## Build an APK using only your phone
Buildozer's Android toolchain is officially intended for Linux/macOS, so this project uses GitHub Actions as the build machine. You can manage the source and download the APK from your phone browser.

1. Extract this ZIP on your phone.
2. Sign in to GitHub in your phone browser and create a new **public or private** repository named `nearby-scanner`.
3. Upload the extracted project files and folders to the repository root. Make sure `.github/workflows/android.yml` is included. If the GitHub mobile upload page hides dot-folders, use the browser's desktop-site mode.
4. Open the repository's **Actions** tab.
5. Select **Build Nearby Scanner APK** and tap **Run workflow** (or push to `main`).
6. Wait for the workflow to finish successfully.
7. Open the completed workflow run, find **Artifacts**, and download `Nearby-Scanner-APK`.
8. Extract the artifact ZIP, tap the `.apk`, and allow installation from that browser/file manager when Android asks.

## First launch
- Turn Bluetooth on.
- Open Nearby Scanner and grant Bluetooth permissions.
- Tap Start Scan.
- Test with another BLE advertising device nearby.

## Project files
- `main.py`: Kivy UI and Android permission flow.
- `src/org/nearby/scanner/BleScanner.java`: native Android BLE scanner.
- `buildozer.spec`: APK build settings.
- `.github/workflows/android.yml`: cloud build workflow.
