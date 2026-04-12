# Running the React Native Todo App

## TEAM_BRIEF

stack: TypeScript/React Native (Expo)
test_runner: npx jest --passWithNoTests
lint_tool: npx eslint . --ext .ts,.tsx
coverage_tool: npx jest --coverage
coverage_threshold: 60
coverage_applies: true

## Prerequisites

- **Node.js** 18 or later
- **npm** (bundled with Node.js)
- **Expo Go** app installed on a physical device, **or** an Android emulator / iOS Simulator

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
npx expo start
```

Then:

- **Physical device**: Scan the QR code with Expo Go.
- **Android emulator**: Press `a` in the terminal.
- **iOS Simulator**: Press `i` in the terminal.
- **Web**: Press `w` (opens at `http://localhost:8081`).

## Running Tests

```bash
npm test
# or
npx jest --passWithNoTests
```

## Running the Linter

```bash
npx eslint . --ext .ts,.tsx
```

## Project Structure

See [PLANNING.md](./PLANNING.md) for the full architecture and file layout.
