import React from 'react';
import { Text, TouchableOpacity, StyleSheet, View } from 'react-native';
import { Todo } from '../types/Todo';

/**
 * Props for the TodoItem component.
 */
export interface TodoItemProps {
  /** The todo item to render. */
  todo: Todo;
  /** Callback invoked when the user taps to toggle completion. */
  onToggle: (id: string) => void;
  /** Callback invoked when the user requests deletion. */
  onDelete: (id: string) => void;
}

/**
 * Renders a single todo item with toggle and delete interactions.
 *
 * - Tap the item to toggle its completed status.
 * - Long-press the item to delete it.
 * - Completed items display with a line-through style.
 */
const TodoItem: React.FC<TodoItemProps> = ({ todo, onToggle, onDelete }) => {
  return (
    <TouchableOpacity
      style={styles.container}
      onPress={() => onToggle(todo.id)}
      onLongPress={() => onDelete(todo.id)}
      testID={`todo-item-${todo.id}`}
    >
      <View style={styles.checkbox}>
        <Text style={styles.checkboxText}>{todo.completed ? '✓' : ' '}</Text>
      </View>
      <Text
        style={[
          styles.title,
          todo.completed && styles.titleCompleted,
        ]}
        numberOfLines={2}
      >
        {todo.title}
      </Text>
      <TouchableOpacity
        style={styles.deleteButton}
        onPress={() => onDelete(todo.id)}
        testID={`todo-delete-${todo.id}`}
      >
        <Text style={styles.deleteText}>✕</Text>
      </TouchableOpacity>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#ffffff',
    paddingVertical: 12,
    paddingHorizontal: 16,
    marginHorizontal: 16,
    marginVertical: 4,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  checkbox: {
    width: 28,
    height: 28,
    borderRadius: 14,
    borderWidth: 2,
    borderColor: '#4a90d9',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 12,
  },
  checkboxText: {
    fontSize: 14,
    color: '#4a90d9',
    fontWeight: '700',
  },
  title: {
    flex: 1,
    fontSize: 16,
    color: '#333333',
  },
  titleCompleted: {
    textDecorationLine: 'line-through',
    color: '#999999',
  },
  deleteButton: {
    marginLeft: 12,
    padding: 4,
  },
  deleteText: {
    fontSize: 18,
    color: '#cc4444',
    fontWeight: '600',
  },
});

export default TodoItem;
