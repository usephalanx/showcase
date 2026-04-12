import React from 'react';
import { FlatList, Text, StyleSheet, View } from 'react-native';
import { Todo } from '../types/Todo';
import TodoItem from './TodoItem';

/**
 * Props for the TodoList component.
 */
export interface TodoListProps {
  /** Array of todo items to render. */
  todos: Todo[];
  /** Callback invoked when a todo's completion status should be toggled. */
  onToggle: (id: string) => void;
  /** Callback invoked when a todo should be deleted. */
  onDelete: (id: string) => void;
}

/**
 * Renders the list of todos using a React Native FlatList.
 *
 * - Uses `keyExtractor` with `todo.id` for stable list keys.
 * - Delegates individual item rendering to the `TodoItem` component.
 * - Displays an empty state message ('No todos yet! Add one above.')
 *   via `ListEmptyComponent` when the list has no items.
 */
const TodoList: React.FC<TodoListProps> = ({ todos, onToggle, onDelete }) => {
  /**
   * Extracts the unique key for each todo item.
   */
  const keyExtractor = (item: Todo): string => item.id;

  /**
   * Renders a single todo item row.
   */
  const renderItem = ({ item }: { item: Todo }) => (
    <TodoItem todo={item} onToggle={onToggle} onDelete={onDelete} />
  );

  /**
   * Renders the empty state when no todos exist.
   */
  const renderEmptyComponent = () => (
    <View style={styles.emptyContainer} testID="todo-list-empty">
      <Text style={styles.emptyText}>No todos yet! Add one above.</Text>
    </View>
  );

  return (
    <FlatList
      data={todos}
      keyExtractor={keyExtractor}
      renderItem={renderItem}
      ListEmptyComponent={renderEmptyComponent}
      contentContainerStyle={todos.length === 0 ? styles.emptyListContent : styles.listContent}
      testID="todo-list"
    />
  );
};

const styles = StyleSheet.create({
  listContent: {
    paddingVertical: 8,
  },
  emptyListContent: {
    flexGrow: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  emptyContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 48,
    paddingHorizontal: 32,
  },
  emptyText: {
    fontSize: 16,
    color: '#999999',
    textAlign: 'center',
  },
});

export default TodoList;
