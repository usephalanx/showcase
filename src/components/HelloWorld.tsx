import React from 'react';
import styles from './HelloWorld.module.css';

/**
 * Reusable HelloWorld component.
 *
 * Renders a styled <h1> heading displaying "Hello World".
 * Uses CSS modules for scoped styling.
 */
const HelloWorld: React.FC = () => {
  return (
    <h1 className={styles.heading} data-testid="hello-heading">
      Hello World
    </h1>
  );
};

export default HelloWorld;
