app_type: spa
coverage_applies: false
coverage_source: null
coverage_threshold: 0
coverage_tool: none
install_steps:
- cd /tmp/forge-repos/hello-world-react-app-e30fc2a0
- npm install
lint_tool: none
notes: Verify that all tests in the test suite pass for the Hello World React app
  using Vitest.
stack: TypeScript/React+Vite
test_files:
- src/components/HelloWorld.test.tsx
- src/App.test.tsx
test_runner: npx vitest run
workspace: /tmp/forge-repos/hello-world-react-app-e30fc2a0
