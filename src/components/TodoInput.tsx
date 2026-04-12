/**
 * TodoInput — a text input with an add button for creating new todos.
 *
 * Accepts an `onAdd` callback that is invoked with the trimmed title
 * when the user taps the add button or submits via keyboard.
 * Clears the input field after a successful submission.
 */

import React, { useState } from 'react';
import {
  StyleSheet,
  TextInput,
  TouchableOpacity,
  Text,
  View,
} from 'react-native';

/** Props for the TodoInput component. */
export interface TodoInputProps {
  /** Callback invoked with the new todo title. */
  onAdd: (title: string) => void;
}

/**
 * Controlled text input with an "Add" button.
 *
 * Trims whitespace and rejects empty strings before invoking onAdd.
 */
export const TodoInput: React.FC<TodoInputProps> = ({ onAdd }) => {
  const [text, setText] = useState<string>('');

  const handleSubmit = (): void => {
    const trimmed = text.trim();
    if (trimmed.length === 0) {
      return;
    }
    onAdd(trimmed);
    setText('');
  };

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder="Add a new todo..."
        placeholderTextColor="#999"
        value={text}
        onChangeText={setText}
        onSubmitEditing={handleSubmit}
        returnKeyType="done"
        testID="todo-input"
      />
      <TouchableOpacity
        style={styles.button}
        onPress={handleSubmit}
        activeOpacity={0.7}
        testID="add-button"
      >
        <Text style={styles.buttonText}>Add</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    marginBottom: 16,
  },
  input: {
    flex: 1,
    height: 48,
    borderWidth: 1,
    borderColor: '#CCC',
    borderRadius: 8,
    paddingHorizontal: 12,
    fontSize: 16,
    backgroundColor: '#FFF',
    color: '#1A1A1A',
  },
  button: {
    marginLeft: 8,
    height: 48,
    paddingHorizontal: 20,
    backgroundColor: '#4A90D9',
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
  },
  buttonText: {
    color: '#FFF',
    fontSize: 16,
    fontWeight: '600',
  },
});

export default TodoInput;
