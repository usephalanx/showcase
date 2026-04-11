/**
 * HelloWorld component.
 * Renders a styled <h1> heading with modern typography.
 */
import React from "react";
import styles from "./HelloWorld.module.css";

const HelloWorld: React.FC = () => {
  return <h1 className={styles.heading}>Hello World</h1>;
};

export default HelloWorld;
