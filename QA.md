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
notes: Verify that the App component renders an <h1> heading containing the text 'Hello
  World'.
stack: TypeScript/React+Vite
test_files:
- src/App.test.jsx
test_runner: npx vitest run
workspace: /tmp/forge-repos/hello-world-react-app-02ad6163
