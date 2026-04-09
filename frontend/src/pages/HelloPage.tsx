/**
 * HelloPage component.
 *
 * Displays the main "Hello World" greeting. Serves as the single
 * page of the application.
 */
import React from 'react';

/**
 * HelloPage — renders the Hello World heading.
 *
 * @returns A main element containing the greeting heading.
 */
function HelloPage(): React.JSX.Element {
  return (
    <main>
      <h1 data-testid="hello-heading">Hello World</h1>
    </main>
  );
}

export default HelloPage;
