# Madhuri Real Estate - Single Page Application

## TEAM_BRIEF
stack: TypeScript/React
test_runner: npx jest --verbose
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Overview
A React-based single-page application for Madhuri Real Estate, featuring a logo, company name, agent profile, recent sales showcase, and contact form.

## Prerequisites
- Node.js 18+
- npm

## Setup
```bash
npm install
```

## Running Tests
```bash
npm test
```

## Project Structure
```
src/
├── App.tsx                    # Main application component
├── components/
│   ├── Logo.tsx               # Logo display component
│   ├── CompanyName.tsx        # Company name heading component
│   ├── Profile.tsx            # Agent profile component
│   ├── RecentSales.tsx        # Recent sales grid component
│   └── ContactInfo.tsx        # Contact info and form component
├── styles/
│   └── global.css             # Global styles
├── __tests__/
│   ├── App.test.tsx           # App composition tests
│   ├── RecentSales.test.tsx   # Recent sales rendering tests
│   └── ContactInfo.test.tsx   # Contact form validation tests
└── __mocks__/
    └── fileMock.ts            # Static file mock for Jest
public/
└── logo.svg                   # Company logo asset
```
