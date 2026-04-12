/**
 * TodoList — renders a scrollable list of todo items using FlatList.
 *
 * Accepts the todo array and callbacks for toggling and deleting items.
 * Displays an empty-state message when no todos exist.
 */

import React from 'react';
import { FlatList, StyleSheet, Text, View } from 'react-native';

import { Todo } from '../types/Todo';
import { TodoItem } from './TodoItem';

/** Props for the TodoList component. */
export interface TodoListProps {
  /** Array of todo items to display. */
  todos: Todo[];
  /** Callback invoked when a todo's completion status should be toggled. */
  onToggle: (id: string) => void;
  /** Callback invoked when a todo should be deleted. */
  onDelete: (id: string) => void;
}

/**
 * FlatList-based todo list with empty-state handling.
 *
 * Each item is rendered via the TodoItem component.
 */
export const TodoList: React.FC<TodoListProps> = ({ todos, onToggle, onDelete }) => {
  if (todos.length === 0) {
    return (
      <View style={styles.emptyContainer}>
        <Text style={styles.emptyText}>No todos yet. Add one above!</Text>
      </View>
    );
  }

  return (
    <FlatList
      data={todos}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => (
        <TodoItem
          todo={item}
          onToggle={onToggle}
          onDelete={onDelete}
        />
      )}
      contentContainerStyle={styles.list}
      showsVerticalScrollIndicator={false}
      testID="todo-list"
    />
  );
};

const styles = StyleSheet.create({
  list: {
    paddingBottom: 24,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingTop: 48,
  },
  emptyText: {
    fontSize: 16,
    color: '#999',
  },
});

export default TodoList;
