# RUNNING — React Native Todo App

## TEAM_BRIEF

stack: TypeScript/React Native (Expo)
test_runner: npx jest
lint_tool: npx eslint .
coverage_tool: jest --coverage
coverage_threshold: 60
coverage_applies: true

## Prerequisites

- Node.js 18+
- npm (or yarn)
- Expo Go app on a physical device, or Android / iOS emulator

## Setup

```bash
# 1. Install dependencies
npm install

# 2. Install Expo-specific native packages
npx expo install @react-native-async-storage/async-storage \
  @react-navigation/native \
  @react-navigation/native-stack \
  react-native-screens \
  react-native-safe-area-context
```

## Run

```bash
npx expo start
```

Then:
- Scan the QR code with Expo Go (Android / iOS)
- Press `a` for Android emulator
- Press `i` for iOS simulator
- Press `w` for web (localhost:8081)

## Test

```bash
npx jest
```

## Lint

```bash
npx eslint .
```
