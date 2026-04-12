# Running the Todo Mobile App

## TEAM_BRIEF
stack: TypeScript/React Native (Expo)
test_runner: npm test
lint_tool: npx expo lint
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- **Node.js** 18+ and **npm**
- **Expo Go** app on a physical device (iOS / Android), **or** an Android emulator / iOS simulator

## Setup

```bash
# 1. Install JavaScript dependencies
npm install

# 2. Install native/Expo-specific dependencies
npx expo install @react-native-async-storage/async-storage \
  @react-navigation/native @react-navigation/native-stack \
  react-native-screens react-native-safe-area-context
```

## Running

```bash
npx expo start
```

- Scan the QR code with **Expo Go** on your device, or
- Press **a** for Android emulator, **i** for iOS simulator, **w** for web.

## Testing

```bash
npm test
```

## Project Structure

See [PLANNING.md](./PLANNING.md) for the full architecture and file map.
