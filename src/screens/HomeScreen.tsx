import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

/**
 * HomeScreen is the main screen of the Todo App.
 *
 * Displays the todo list interface. Currently renders a placeholder view
 * that will be populated with TodoInput, TodoList, and TodoItem components
 * in subsequent implementation tasks.
 */
const HomeScreen: React.FC = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.placeholder}>Welcome to Todo App</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  placeholder: {
    fontSize: 18,
    color: '#333',
  },
});

export default HomeScreen;
