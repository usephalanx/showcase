import React from 'react';

export interface HelloWorldProps {
  /** The text to display inside the h1 element. Defaults to 'Hello World'. */
  text?: string;
  /** Optional CSS class name to apply to the h1 element. */
  className?: string;
}

const HelloWorld: React.FC<HelloWorldProps> = ({ text = 'Hello World', className }) => {
  return <h1 className={className}>{text}</h1>;
};

export default HelloWorld;
