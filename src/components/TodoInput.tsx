/**
 * TodoInput — controlled text input with an "Add" button.
 *
 * Maintains local state for the input text. On submit (button press or
 * keyboard submit), calls `onAdd` with trimmed text and clears the input.
 * Empty / whitespace-only strings are silently rejected.
 */

import React, { useState } from 'react';
import {
  StyleSheet,
  TextInput,
  TouchableOpacity,
  Text,
  View,
} from 'react-native';

/**
 * Props accepted by the TodoInput component.
 */
export interface TodoInputProps {
  /** Callback invoked with the trimmed title string when the user submits. */
  onAdd: (title: string) => void;
}

/**
 * A row containing a text input and an "Add" button.
 *
 * The component keeps the current input value in local state. When the
 * user presses the button or triggers a keyboard submit the trimmed value
 * is forwarded to `onAdd` and the field is cleared.  Blank input is
 * silently ignored.
 */
const TodoInput: React.FC<TodoInputProps> = ({ onAdd }) => {
  const [text, setText] = useState<string>('');

  /**
   * Validate, forward to parent callback, and reset the field.
   */
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
        placeholder="Add a new todo…"
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
        testID="todo-add-button"
      >
        <Text style={styles.buttonText}>Add</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 16,
    backgroundColor: '#fff',
  },
  button: {
    backgroundColor: '#4a90d9',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 8,
    marginLeft: 8,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});

export default TodoInput;
