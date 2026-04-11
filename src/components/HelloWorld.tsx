import React from 'react';
import styles from './HelloWorld.module.css';

/**
 * HelloWorld component.
 *
 * Renders a styled <h1> heading with the text "Hello World".
 * Uses CSS modules for scoped styling.
 */
const HelloWorld: React.FC = () => {
  return <h1 className={styles.heading}>Hello World</h1>;
};

export default HelloWorld;
