import { render, screen } from '@testing-library/react';
import App from './App';

test('renders home page', () => {
  render(<App />);
  const homeElement = screen.getByText(/Welcome to the Chatbot Website/i);
  expect(homeElement).toBeInTheDocument();
});