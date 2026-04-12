# Running the React Native Todo App

## TEAM_BRIEF
stack: TypeScript/React Native (Expo)
test_runner: npx jest
lint_tool: npx eslint .
coverage_tool: jest --coverage
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Node.js 18+ and npm
- Expo Go app on your phone (iOS App Store / Google Play Store)
- Or: Android emulator / iOS simulator (Xcode required for iOS)

## Setup

```bash
# 1. Install dependencies
npm install

# 2. Install required Expo packages
npx expo install @react-native-async-storage/async-storage \
  @react-navigation/native \
  @react-navigation/native-stack \
  react-native-screens \
  react-native-safe-area-context
```

## Running the App

```bash
# Start the Expo development server
npx expo start
```

Then:
- **Physical device**: Scan the QR code with Expo Go
- **Android emulator**: Press `a`
- **iOS simulator**: Press `i`
- **Web**: Press `w` (requires `npx expo install react-native-web react-dom @expo/metro-runtime`)

## Running Tests

```bash
npm test
# or
npx jest
```

## Running with Coverage

```bash
npx jest --coverage
```

## Linting

```bash
npx eslint .
```

## Project Structure

```
src/
├── components/       # Reusable UI components
│   ├── TodoInput.tsx
│   ├── TodoItem.tsx
│   └── TodoList.tsx
├── hooks/            # Custom React hooks
│   └── useTodos.ts
├── screens/          # App screens
│   └── HomeScreen.tsx
├── services/         # Storage and utility services
│   └── todoStorage.ts
└── types/            # TypeScript type definitions
    └── Todo.ts
```
