import React from 'react';
import { StatusBar } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';

import AppNavigator from './src/navigation/AppNavigator';

/**
 * App is the root component of the Todo application.
 *
 * It wraps the entire app in a NavigationContainer (required by
 * React Navigation) and renders a StatusBar alongside the
 * AppNavigator stack.
 */
const App: React.FC = () => {
  return (
    <NavigationContainer>
      <StatusBar barStyle="light-content" backgroundColor="#4A90D9" />
      <AppNavigator />
    </NavigationContainer>
  );
};

export default App;
