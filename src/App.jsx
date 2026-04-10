/**
 * Main App component.
 *
 * Serves as the root component of the application and renders
 * the Counter component.
 */
import Counter from './components/Counter';

/**
 * App functional component.
 *
 * @returns {JSX.Element} The rendered App.
 */
export default function App() {
  return (
    <div>
      <Counter />
    </div>
  );
}
