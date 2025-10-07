import React from 'react';
import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <div className="text-center">
      <h1>Welcome to XU-News-AI-RAG</h1>
      <p className="lead">Your intelligent assistant for personalized news consumption and knowledge management.</p>
      <hr />
      <p>
        <Link to="/register" className="btn btn-primary me-2">Get Started</Link>
        <Link to="/login" className="btn btn-secondary">Login</Link>
      </p>
    </div>
  );
};

export default HomePage;
