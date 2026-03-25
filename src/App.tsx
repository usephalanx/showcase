import HomePage from './pages/HomePage'
import './index.css'

/**
 * Root application component.
 *
 * Imports and renders the HomePage component as the main view.
 */
function App(): JSX.Element {
  return (
    <div className="app">
      <HomePage />
    </div>
  )
}

export default App
