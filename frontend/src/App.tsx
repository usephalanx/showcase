import React from 'react';
import { ProjectsPage } from './components/ProjectsPage';

/**
 * Root application component.
 */
const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <ProjectsPage />
    </div>
  );
};

export default App;
