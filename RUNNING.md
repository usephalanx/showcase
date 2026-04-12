# Running the Todo App

## TEAM_BRIEF
stack: TypeScript/React Native (Expo)
test_runner: npx jest
lint_tool: npx eslint .
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Features

- **Add todos** — Type a title and tap the add button to create a new todo item
- **Toggle completion** — Tap a todo to mark it as completed or incomplete
- **Delete todos** — Long-press (or swipe) a todo to remove it permanently
- **Persistent storage with AsyncStorage** — Todos survive app restarts; data is stored locally on-device via `@react-native-async-storage/async-storage`

## Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| **Node.js** | 18+ | [Download](https://nodejs.org/) |
| **npm** | 9+ (ships with Node 18+) | Or use **yarn** (`npm install -g yarn`) |
| **Expo CLI** | latest | Installed automatically via `npx expo` — no global install required |
| **Expo Go** (optional) | latest | Install on your physical device from the App Store / Google Play |
| **iOS Simulator** (optional) | Xcode 15+ | macOS only — install Xcode from the Mac App Store |
| **Android Emulator** (optional) | Android Studio | Install Android Studio and create an AVD via the Device Manager |

## Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd <repository-directory>

# 2. Install JavaScript dependencies
npm install

# 3. Install Expo-specific peer dependencies
npx expo install @react-native-async-storage/async-storage \
  @react-navigation/native \
  @react-navigation/native-stack \
  react-native-screens \
  react-native-safe-area-context
```

> **Yarn users:** replace `npm install` with `yarn` and `npx expo install …` stays the same.

## Running the App

### Start the Expo development server

```bash
npx expo start
```

This prints a QR code in the terminal and opens the Expo DevTools.

### Run on a physical device (Expo Go)

1. Install **Expo Go** on your iOS or Android device.
2. Scan the QR code shown in the terminal:
   - **iOS** — use the built-in Camera app.
   - **Android** — use the Expo Go app's built-in scanner.
3. The app will bundle and launch on your device.

### Run on iOS Simulator (macOS only)

```bash
# Option A: press 'i' in the terminal after `npx expo start`
# Option B: launch directly
npx expo start --ios
```

> Requires Xcode with a valid iOS Simulator runtime installed.

### Run on Android Emulator

```bash
# Option A: press 'a' in the terminal after `npx expo start`
# Option B: launch directly
npx expo start --android
```

> Requires Android Studio with an AVD (Android Virtual Device) running.

### Run in the web browser

```bash
# Press 'w' in the terminal after `npx expo start`, or:
npx expo start --web
```

The app will be available at `http://localhost:8081`.

## Running Tests

```bash
npx jest
```

Tests use **Jest** and **React Native Testing Library**. See `PLANNING.md` for the full testing strategy.

## Running the Python Backend (API)

The project also contains a FastAPI backend (used during development/testing):

```bash
# Install Python dependencies
pip install fastapi uvicorn pydantic

# Start the API server
uvicorn main:app --reload --port 8000
```

Run Python tests with:

```bash
pytest tests/
```

## Project Structure

See `PLANNING.md` for the full architecture, component hierarchy, and file responsibilities.

## Troubleshooting

| Problem | Solution |
|---|---|
| `expo: command not found` | Use `npx expo start` instead of a global `expo` command |
| Metro bundler port conflict | Run `npx expo start --port 8082` to pick a different port |
| iOS Simulator won't launch | Open Xcode → Settings → Platforms and install a simulator runtime |
| Android emulator not detected | Ensure an AVD is running in Android Studio before pressing `a` |
| AsyncStorage data not persisting | Ensure `@react-native-async-storage/async-storage` is installed with `npx expo install` (not plain `npm install`) |
