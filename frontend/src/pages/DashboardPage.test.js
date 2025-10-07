import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import DashboardPage from './DashboardPage';
import * as api from '../services/api';

// Mock the api module
jest.mock('../services/api');

const mockDocuments = [
  { id: 1, source: 'test.pdf', uploaded_at: '2023-10-27T10:00:00Z' },
  { id: 2, source: 'another.txt', uploaded_at: '2023-10-28T11:00:00Z' },
];

const mockFeeds = [
  { id: 1, url: 'http://example.com/rss.xml' },
];

const mockClusteringReport = {
  clusters: [
    {
      cluster_id: 0,
      top_terms: ['apple', 'banana', 'orange'],
    },
  ],
};

describe('DashboardPage', () => {
  beforeEach(() => {
    // Reset mocks before each test
    api.getDocuments.mockResolvedValue({ data: mockDocuments });
    api.getFeeds.mockResolvedValue({ data: mockFeeds });
    api.getKeywordReport.mockResolvedValue({ data: { top_keywords: ['ai', 'react'] } });
    api.getClusteringReport.mockResolvedValue({ data: mockClusteringReport });
    api.search.mockResolvedValue({ data: [{ text: 'Search result', source: ['test.txt'] }] });
  });

  test('renders dashboard and fetches initial data', async () => {
    render(
      <Router>
        <DashboardPage />
      </Router>
    );

    // Check that the main sections are rendered
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Intelligent Search')).toBeInTheDocument();
    expect(screen.getByText('Knowledge Base')).toBeInTheDocument();
    expect(screen.getByText('Data Analysis')).toBeInTheDocument();
    expect(screen.getByText('RSS Feeds')).toBeInTheDocument();

    // Check that the initial data is fetched and displayed
    await waitFor(() => {
      expect(screen.getByText(/test.pdf/)).toBeInTheDocument();
      expect(screen.getByText(/another.txt/)).toBeInTheDocument();
      expect(screen.getByText('http://example.com/rss.xml')).toBeInTheDocument();
    });
  });

  test('fetches and displays search results', async () => {
    render(
      <Router>
        <DashboardPage />
      </Router>
    );

    fireEvent.change(screen.getByPlaceholderText('Ask a question...'), { target: { value: 'test query' } });
    fireEvent.click(screen.getByText('Search'));

    await waitFor(() => {
      expect(api.search).toHaveBeenCalledWith('test query');
      expect(screen.getByText('Search result')).toBeInTheDocument();
      expect(screen.getByText('Sources: test.txt')).toBeInTheDocument();
    });
  });
});
