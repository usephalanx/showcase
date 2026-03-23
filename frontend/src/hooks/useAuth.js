import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

/**
 * Custom hook to access the AuthContext.
 *
 * @returns {import('../context/AuthContext').AuthContextValue} The auth context value.
 * @throws {Error} If used outside of an AuthProvider.
 */
export default function useAuth() {
  const context = useContext(AuthContext);
  if (context === null) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
