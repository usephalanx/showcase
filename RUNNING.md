# TodoApp — Setup & Running Instructions

## TEAM_BRIEF

stack: TypeScript/React Native (Expo)
test_runner: cd mobile && npm test
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

---

## Prerequisites

- **Node.js** 18+ (LTS recommended)
- **npm** 9+ (bundled with Node.js 18+)
- **Expo Go** app installed on your physical device (iOS App Store / Google Play),
  **or** an Android emulator / iOS Simulator configured locally

---

## Initial Setup

```bash
# 1. Navigate to the mobile project directory
cd mobile

# 2. Install all dependencies
npm install
```

> **Note**: Do NOT run `npx create-expo-app` — the project is already scaffolded.
> Just install dependencies with `npm install`.

---

## Running the App

```bash
# Start the Expo development server
npx expo start
```

Then choose one of:

| Target              | Action                                                |
| ------------------- | ----------------------------------------------------- |
| **Physical device** | Scan the QR code with Expo Go (Android) or Camera (iOS) |
| **Android emulator**| Press `a` in the terminal                             |
| **iOS Simulator**   | Press `i` in the terminal (macOS only)                |
| **Web browser**     | Press `w` in the terminal                             |

The development server runs on `http://localhost:8081` by default.

---

## Running Tests

```bash
cd mobile
npm test
```

This runs Jest with the `jest-expo` preset. Tests are located in `__tests__/`.

---

## TypeScript Check

```bash
cd mobile
npm run ts:check
```

Runs `tsc --noEmit` to verify type correctness without emitting files.

---

## Project Structure

See [PLANNING.md](./PLANNING.md) for the full architecture, data model,
component hierarchy, and file responsibility map.

---

## Environment Variables

No environment variables or secrets are required for the mobile app.
All data is stored locally via AsyncStorage.
