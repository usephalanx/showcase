app_type: spa
coverage_applies: false
coverage_source: null
coverage_threshold: 0
coverage_tool: none
install_steps:
- npm install
- npm install --save-dev @testing-library/jest-dom @testing-library/react @testing-library/user-event
  jsdom vitest @vitest/coverage-v8
lint_tool: none
notes: Verify that all main components render and user interactions work as expected
  in the real estate SPA.
stack: TypeScript/React+Vite
test_files:
- src/__tests__/App.test.tsx
- src/__tests__/RecentSales.test.tsx
- src/__tests__/ContactInfo.test.tsx
test_runner: npx vitest run
workspace: /tmp/forge-repos/website-for-realestate-single-page-with--c91683d9
