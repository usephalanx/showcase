# Running the React Native Todo App

## TEAM_BRIEF
stack: TypeScript/React Native (Expo)
test_runner: npx jest --passWithNoTests
lint_tool: npx eslint . --ext .ts,.tsx
coverage_tool: npx jest --coverage
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- **Node.js** 18+ (LTS recommended)
- **npm** 9+ (ships with Node.js 18+)
- **Expo Go** app on your physical device (iOS App Store / Google Play Store), **or** an Android emulator / iOS Simulator

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
  react-native-safe-area-context \
  expo-crypto
```

## Running the App

```bash
# Start the Expo development server
npx expo start
```

- **Physical device**: Scan the QR code with Expo Go.
- **Android emulator**: Press `a` in the terminal.
- **iOS Simulator**: Press `i` in the terminal.
- **Web** (experimental): Press `w` in the terminal (opens at `http://localhost:8081`).

## Running Tests

```bash
# Run the full test suite
npx jest --passWithNoTests

# Run with coverage report
npx jest --coverage
```

## Linting

```bash
npx eslint . --ext .ts,.tsx
```

## Project Structure

See [PLANNING.md](./PLANNING.md) for the full architecture, component hierarchy, and data model documentation.
