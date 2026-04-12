import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import HomeScreen from '../screens/HomeScreen';
import { RootStackParamList } from './types';

const Stack = createNativeStackNavigator<RootStackParamList>();

/**
 * AppNavigator defines the root native stack navigator for the application.
 *
 * Currently contains a single screen (Home) with the title "Todo App".
 * The navigator is structured to support future screen additions by
 * extending RootStackParamList and adding new Stack.Screen entries.
 */
const AppNavigator: React.FC = () => {
  return (
    <Stack.Navigator
      initialRouteName="Home"
      screenOptions={{
        headerStyle: {
          backgroundColor: '#4A90D9',
        },
        headerTintColor: '#fff',
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      }}
    >
      <Stack.Screen
        name="Home"
        component={HomeScreen}
        options={{ title: 'Todo App' }}
      />
    </Stack.Navigator>
  );
};

export default AppNavigator;
