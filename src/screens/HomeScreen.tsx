/**
 * HomeScreen — the main screen composing TodoInput and TodoList with useTodos hook.
 *
 * Renders a SafeAreaView container with a title header ('My Todos'),
 * the TodoInput component wired to addTodo, and the TodoList component
 * wired to todos/toggleTodo/deleteTodo. Shows an ActivityIndicator while loading.
 */

import React from 'react';
import {
  ActivityIndicator,
  SafeAreaView,
  StyleSheet,
  Text,
  View,
} from 'react-native';

import { TodoInput } from '../components/TodoInput';
import { TodoList } from '../components/TodoList';
import { useTodos } from '../hooks/useTodos';

/**
 * HomeScreen component.
 *
 * Serves as the main application screen, orchestrating the todo input form
 * and the scrollable todo list. Uses the useTodos hook for all state management
 * including loading state, adding, toggling, and deleting todos.
 */
export const HomeScreen: React.FC = () => {
  const { todos, loading, addTodo, toggleTodo, deleteTodo } = useTodos();

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#4A90D9" testID="loading-indicator" />
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.header}>My Todos</Text>
        <TodoInput onAdd={addTodo} />
        <TodoList
          todos={todos}
          onToggle={toggleTodo}
          onDelete={deleteTodo}
        />
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  content: {
    flex: 1,
    paddingHorizontal: 16,
    paddingTop: 16,
  },
  header: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#1A1A1A',
    marginBottom: 16,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default HomeScreen;
