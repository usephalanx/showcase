/**
 * TodoItem — renders a single todo with toggle and delete actions.
 *
 * Tap to toggle completion. Long-press or tap the delete button to remove.
 */

import React from 'react';
import {
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';

import { Todo } from '../types/Todo';

/** Props for the TodoItem component. */
export interface TodoItemProps {
  /** The todo item to render. */
  todo: Todo;
  /** Callback invoked when the todo should be toggled. */
  onToggle: (id: string) => void;
  /** Callback invoked when the todo should be deleted. */
  onDelete: (id: string) => void;
}

/**
 * Single todo row with toggle-on-press and delete button.
 */
export const TodoItem: React.FC<TodoItemProps> = ({ todo, onToggle, onDelete }) => {
  return (
    <TouchableOpacity
      style={styles.container}
      onPress={() => onToggle(todo.id)}
      onLongPress={() => onDelete(todo.id)}
      activeOpacity={0.7}
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
        hitSlop={{ top: 8, bottom: 8, left: 8, right: 8 }}
        testID={`delete-button-${todo.id}`}
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
    backgroundColor: '#FFF',
    borderRadius: 8,
    padding: 12,
    marginBottom: 8,
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
    borderColor: '#4A90D9',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  checkboxText: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#4A90D9',
  },
  title: {
    flex: 1,
    fontSize: 16,
    color: '#1A1A1A',
  },
  titleCompleted: {
    textDecorationLine: 'line-through',
    color: '#999',
  },
  deleteButton: {
    marginLeft: 12,
    width: 28,
    height: 28,
    justifyContent: 'center',
    alignItems: 'center',
  },
  deleteText: {
    fontSize: 16,
    color: '#E74C3C',
    fontWeight: 'bold',
  },
});

export default TodoItem;
