import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

/**
 * Root application component.
 *
 * Renders a placeholder screen. Navigation and screens will be
 * added in subsequent tasks.
 */
export default function App(): React.JSX.Element {
  return (
    <View style={styles.container}>
      <Text>TodoApp</Text>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
