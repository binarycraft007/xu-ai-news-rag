import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import LoginPage from './LoginPage';
import * as api from '../services/api';

// Mock the api module
jest.mock('../services/api');

describe('LoginPage', () => {
  test('renders login form and handles submission', async () => {
    render(
      <Router>
        <LoginPage />
      </Router>
    );

    // Check that the form elements are rendered
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();

    // Simulate user input
    fireEvent.change(screen.getByLabelText(/username/i), { target: { value: 'testuser' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'password' } });

    // Simulate form submission
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    // Check that the login function was called with the correct arguments
    expect(api.login).toHaveBeenCalledWith('testuser', 'password');
  });
});
