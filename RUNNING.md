# Running the Todo App

## TEAM_BRIEF
stack: TypeScript/React Native (Expo)
test_runner: npx jest
lint_tool: npx eslint .
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js 18+
- npm
- Expo Go app on your phone (or Android/iOS emulator)

## Setup

```bash
# Install dependencies
npm install

# Install Expo-specific peer dependencies
npx expo install @react-native-async-storage/async-storage \
  @react-navigation/native \
  @react-navigation/native-stack \
  react-native-screens \
  react-native-safe-area-context
```

## Running the App

```bash
npx expo start
```

Then:
- Scan the QR code with Expo Go on your phone, or
- Press `a` for Android emulator, or
- Press `i` for iOS simulator, or
- Press `w` for web (localhost:8081)

## Running Tests

```bash
npx jest
```

## Project Structure

See `PLANNING.md` for the full architecture and file responsibilities.
