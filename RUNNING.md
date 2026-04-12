# Running the React Native Todo App

## TEAM_BRIEF

stack: TypeScript/React Native (Expo)
test_runner: npx jest --passWithNoTests
lint_tool: npx tsc --noEmit
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- **Node.js** 18 or later
- **npm** (bundled with Node.js)
- **Expo Go** app on your phone (iOS App Store / Google Play), **or** an Android emulator / iOS Simulator

## Setup

```bash
# 1. Install JavaScript dependencies
npm install

# 2. Install Expo-specific native dependencies
npx expo install \
  @react-native-async-storage/async-storage \
  @react-navigation/native \
  @react-navigation/native-stack \
  react-native-screens \
  react-native-safe-area-context
```

## Running the App

```bash
npx expo start
```

- Scan the QR code with **Expo Go** on your phone, **or**
- Press `a` to open the Android emulator, **or**
- Press `i` to open the iOS Simulator, **or**
- Press `w` to open in a web browser (localhost:8081)

## Running Tests

```bash
npm test
```

Or directly:

```bash
npx jest --passWithNoTests
```

## Project Structure

See [PLANNING.md](./PLANNING.md) for the full architecture, component
hierarchy, data model, and file responsibilities.
