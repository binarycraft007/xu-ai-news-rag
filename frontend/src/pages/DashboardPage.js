import React, { useState, useEffect, useCallback } from 'react';
import { getDocuments, uploadDocument, deleteDocument, search, getKeywordReport, getFeeds, addFeed, deleteFeed, editDocumentMetadata, batchDeleteDocuments, getClusteringReport } from '../services/api';

const DashboardPage = () => {
  const [documents, setDocuments] = useState([]);
  const [searchResults, setSearchResults] = useState([]);
  const [keywordReport, setKeywordReport] = useState(null);
  const [clusteringReport, setClusteringReport] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [file, setFile] = useState(null);
  const [feeds, setFeeds] = useState([]);
  const [newFeedUrl, setNewFeedUrl] = useState('');
  const [docType, setDocType] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [selectedDocuments, setSelectedDocuments] = useState([]);
  const [editingDoc, setEditingDoc] = useState(null);

  const fetchDocuments = useCallback(async () => {
    try {
      const response = await getDocuments({ type: docType, start_date: startDate, end_date: endDate });
      setDocuments(response.data);
    } catch (error) {
      console.error('Failed to fetch documents', error);
    }
  }, [docType, startDate, endDate]);

  const fetchFeeds = async () => {
    try {
      const response = await getFeeds();
      setFeeds(response.data);
    } catch (error) {
      console.error('Failed to fetch feeds', error);
    }
  };

  useEffect(() => {
    fetchDocuments();
    fetchFeeds();
  }, [fetchDocuments]);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    try {
      await uploadDocument(file);
      fetchDocuments(); // Refresh document list
      setFile(null); // Clear the file input
    } catch (error) {
      console.error('Failed to upload document', error);
    }
  };

  const handleDelete = async (docId) => {
    try {
      await deleteDocument(docId);
      fetchDocuments(); // Refresh document list
    } catch (error) {
      console.error('Failed to delete document', error);
    }
  };

  const handleBatchDelete = async () => {
    try {
      await batchDeleteDocuments(selectedDocuments);
      setSelectedDocuments([]);
      fetchDocuments();
    } catch (error) {
      console.error('Failed to delete documents', error);
    }
  };

  const handleSelectDocument = (docId) => {
    setSelectedDocuments(prev => 
      prev.includes(docId) ? prev.filter(id => id !== docId) : [...prev, docId]
    );
  };

  const handleEditClick = (doc) => {
    setEditingDoc({ ...doc });
  };

  const handleEditChange = (e) => {
    const { name, value } = e.target;
    setEditingDoc(prev => ({ ...prev, [name]: value }));
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    if (!editingDoc) return;
    try {
      await editDocumentMetadata(editingDoc.id, {
        tags: editingDoc.tags,
        source: editingDoc.source,
      });
      setEditingDoc(null);
      fetchDocuments();
    } catch (error) {
      console.error('Failed to update metadata', error);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    try {
      const response = await search(searchQuery);
      setSearchResults(response.data);
    } catch (error) {
      console.error('Failed to perform search', error);
    }
  };

  const handleGetReport = async () => {
    try {
      const response = await getKeywordReport();
      setKeywordReport(response.data);
    } catch (error) {
      console.error('Failed to get keyword report', error);
    }
  };

  const handleGetClusteringReport = async () => {
    try {
      const response = await getClusteringReport();
      setClusteringReport(response.data);
    } catch (error) {
      console.error('Failed to get clustering report', error);
    }
  };

  const handleAddFeed = async (e) => {
    e.preventDefault();
    try {
      await addFeed(newFeedUrl);
      setNewFeedUrl('');
      fetchFeeds();
    } catch (error) {
      console.error('Failed to add feed', error);
    }
  };

  const handleDeleteFeed = async (feedId) => {
    try {
      await deleteFeed(feedId);
      fetchFeeds();
    } catch (error) {
      console.error('Failed to delete feed', error);
    }
  };

  const handleFilterChange = (setter) => (e) => {
    setter(e.target.value);
  };

  const resetFilters = () => {
    setDocType('');
    setStartDate('');
    setEndDate('');
  };

  return (
    <div>
      <h2>Dashboard</h2>

      {/* Search Section */}
      <section className="mb-5">
        <h3>Intelligent Search</h3>
        <form onSubmit={handleSearch}>
          <div className="input-group mb-3">
            <input
              type="text"
              className="form-control"
              placeholder="Ask a question..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button className="btn btn-primary" type="submit">Search</button>
          </div>
        </form>
        {searchResults.length > 0 && (
          <div>
            <h4>Search Results</h4>
            <div className="card">
              <div className="card-body">
                <p className="card-text">{searchResults[0].text}</p>
                <footer className="blockquote-footer">
                  Sources: {searchResults[0].source.join(', ')}
                </footer>
              </div>
            </div>
          </div>
        )}
      </section>

      {/* Knowledge Base Management */}
      <section className="mb-5">
        <h3>Knowledge Base</h3>
        <form onSubmit={handleUpload} className="mb-3">
          <div className="input-group">
            <input type="file" className="form-control" onChange={(e) => setFile(e.target.files[0])} />
            <button className="btn btn-success" type="submit">Upload</button>
          </div>
        </form>
        
        {/* Filtering Section */}
        <div className="mb-3">
          <h4>Filter Documents</h4>
          <div className="row g-2">
            <div className="col-md">
              <select className="form-select" value={docType} onChange={handleFilterChange(setDocType)}>
                <option value="">All Types</option>
                <option value="txt">Text</option>
                <option value="pdf">PDF</option>
                <option value="xlsx">Excel</option>
              </select>
            </div>
            <div className="col-md">
              <input type="date" className="form-control" value={startDate} onChange={handleFilterChange(setStartDate)} />
            </div>
            <div className="col-md">
              <input type="date" className="form-control" value={endDate} onChange={handleFilterChange(setEndDate)} />
            </div>
            <div className="col-md-auto">
              <button className="btn btn-secondary" onClick={resetFilters}>Reset</button>
            </div>
          </div>
        </div>

        <h4>My Documents</h4>
        {selectedDocuments.length > 0 && (
          <button className="btn btn-danger mb-2" onClick={handleBatchDelete}>
            Delete Selected ({selectedDocuments.length})
          </button>
        )}
        <ul className="list-group">
          {documents.map((doc) => (
            <li key={doc.id} className="list-group-item d-flex justify-content-between align-items-center">
              <div>
                <input
                  type="checkbox"
                  className="form-check-input me-2"
                  onChange={() => handleSelectDocument(doc.id)}
                  checked={selectedDocuments.includes(doc.id)}
                />
                {doc.source} - <small className="text-muted">{new Date(doc.uploaded_at).toLocaleDateString()}</small>
              </div>
              <div>
                <button className="btn btn-primary btn-sm me-2" onClick={() => handleEditClick(doc)}>Edit</button>
                <button className="btn btn-danger btn-sm" onClick={() => handleDelete(doc.id)}>Delete</button>
              </div>
            </li>
          ))}
        </ul>
      </section>

      {/* Edit Modal */}
      {editingDoc && (
        <div className="modal" style={{ display: 'block', backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Edit Metadata</h5>
                <button type="button" className="btn-close" onClick={() => setEditingDoc(null)}></button>
              </div>
              <div className="modal-body">
                <form onSubmit={handleEditSubmit}>
                  <div className="mb-3">
                    <label htmlFor="source" className="form-label">Source</label>
                    <input
                      type="text"
                      className="form-control"
                      id="source"
                      name="source"
                      value={editingDoc.source}
                      onChange={handleEditChange}
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="tags" className="form-label">Tags</label>
                    <input
                      type="text"
                      className="form-control"
                      id="tags"
                      name="tags"
                      value={editingDoc.tags}
                      onChange={handleEditChange}
                    />
                  </div>
                  <button type="submit" className="btn btn-primary">Save Changes</button>
                </form>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Data Analysis Report */}
      <section>
        <h3>Data Analysis</h3>
        <button className="btn btn-info me-2" onClick={handleGetReport}>Generate Keyword Report</button>
        <button className="btn btn-info" onClick={handleGetClusteringReport}>Generate Clustering Report</button>
        {keywordReport && (
          <div className="mt-3">
            <h4>Top 10 Keywords</h4>
            <ul className="list-group">
              {keywordReport.top_keywords.map((keyword, index) => (
                <li key={index} className="list-group-item">{keyword}</li>
              ))}
            </ul>
          </div>
        )}
        {clusteringReport && (
          <div className="mt-3">
            <h4>Clustering Report</h4>
            {clusteringReport.clusters.map((cluster) => (
              <div key={cluster.cluster_id} className="mb-3">
                <h5>Cluster {cluster.cluster_id + 1}</h5>
                <ul className="list-group">
                  {cluster.top_terms.map((term, index) => (
                    <li key={index} className="list-group-item">{term}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* RSS Feed Management */}
      <section className="mt-5">
        <h3>RSS Feeds</h3>
        <form onSubmit={handleAddFeed} className="mb-3">
          <div className="input-group">
            <input
              type="url"
              className="form-control"
              placeholder="https://example.com/rss.xml"
              value={newFeedUrl}
              onChange={(e) => setNewFeedUrl(e.target.value)}
              required
            />
            <button className="btn btn-success" type="submit">Add Feed</button>
          </div>
        </form>
        <h4>My Feeds</h4>
        <ul className="list-group">
          {feeds.map((feed) => (
            <li key={feed.id} className="list-group-item d-flex justify-content-between align-items-center">
              {feed.url}
              <button className="btn btn-danger btn-sm" onClick={() => handleDeleteFeed(feed.id)}>Delete</button>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
};

export default DashboardPage;
