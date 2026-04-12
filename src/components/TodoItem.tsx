/**
 * TodoItem component — renders a single todo item as a row.
 *
 * Displays a checkbox-style toggle on the left, the todo title in the
 * centre (with strikethrough when completed), and a red delete button
 * on the right.
 */

import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  type ViewStyle,
  type TextStyle,
} from 'react-native';

import type { Todo } from '../types/Todo';

/**
 * Props accepted by the TodoItem component.
 */
export interface TodoItemProps {
  /** The todo object to render. */
  todo: Todo;
  /** Callback invoked with the todo's id when the toggle button is pressed. */
  onToggle: (id: string) => void;
  /** Callback invoked with the todo's id when the delete button is pressed. */
  onDelete: (id: string) => void;
}

/**
 * Render a single todo item row.
 *
 * Layout (left → right):
 *   [checkbox toggle] — [title text] — [delete button]
 *
 * The title text receives a strikethrough decoration and muted colour
 * when the todo is marked as completed.
 *
 * @param props - {@link TodoItemProps}
 * @returns A React element representing one todo row.
 */
const TodoItem: React.FC<TodoItemProps> = ({ todo, onToggle, onDelete }) => {
  const handleToggle = (): void => {
    onToggle(todo.id);
  };

  const handleDelete = (): void => {
    onDelete(todo.id);
  };

  return (
    <View style={styles.container}>
      {/* Checkbox-style toggle */}
      <TouchableOpacity
        onPress={handleToggle}
        style={styles.checkbox}
        accessibilityRole="checkbox"
        accessibilityState={{ checked: todo.completed }}
        accessibilityLabel={`Toggle ${todo.title}`}
        testID={`toggle-${todo.id}`}
      >
        <Text style={styles.checkboxText}>{todo.completed ? '☑' : '☐'}</Text>
      </TouchableOpacity>

      {/* Title */}
      <Text
        style={[styles.title, todo.completed && styles.titleCompleted]}
        numberOfLines={1}
        testID={`title-${todo.id}`}
      >
        {todo.title}
      </Text>

      {/* Delete button */}
      <TouchableOpacity
        onPress={handleDelete}
        style={styles.deleteButton}
        accessibilityRole="button"
        accessibilityLabel={`Delete ${todo.title}`}
        testID={`delete-${todo.id}`}
      >
        <Text style={styles.deleteText}>✕</Text>
      </TouchableOpacity>
    </View>
  );
};

/**
 * StyleSheet for TodoItem.
 */
const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: '#cccccc',
    backgroundColor: '#ffffff',
  } as ViewStyle,

  checkbox: {
    width: 32,
    height: 32,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  } as ViewStyle,

  checkboxText: {
    fontSize: 22,
    color: '#555555',
  } as TextStyle,

  title: {
    flex: 1,
    fontSize: 16,
    color: '#333333',
  } as TextStyle,

  titleCompleted: {
    textDecorationLine: 'line-through',
    color: '#999999',
  } as TextStyle,

  deleteButton: {
    width: 32,
    height: 32,
    justifyContent: 'center',
    alignItems: 'center',
    marginLeft: 12,
  } as ViewStyle,

  deleteText: {
    fontSize: 18,
    color: '#ff3b30',
    fontWeight: '700',
  } as TextStyle,
});

export default TodoItem;
