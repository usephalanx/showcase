app_type: spa
coverage_applies: false
coverage_source: null
coverage_threshold: 0
coverage_tool: none
install_steps:
- cd /tmp/forge-repos/hello-world-react-app-6edb1fb8
- npm install
lint_tool: none
notes: Verify that the App renders a centered 'Hello World' heading and a white background,
  and that all tests in src/App.test.tsx pass.
stack: TypeScript/React+Vite
test_files:
- src/App.test.tsx
test_runner: npx vitest run
workspace: /tmp/forge-repos/hello-world-react-app-6edb1fb8
