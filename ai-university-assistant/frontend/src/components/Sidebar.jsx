import React, { useState } from 'react';
import DocumentUpload from './DocumentUpload';
import './Sidebar.css';
import axios from 'axios';

function Sidebar({ stats, onDocumentsUploaded, onClearChat }) {
  const [expandedSection, setExpandedSection] = useState('upload');
  const [loading, setLoading] = useState(false);

  const API_BASE_URL = 'http://localhost:8000/api';

  const handleClearAll = async () => {
    if (confirm('Are you sure? This will delete all indexed documents.')) {
      setLoading(true);
      try {
        await axios.delete(`${API_BASE_URL}/documents/clear`);
        onDocumentsUploaded();
        alert('All documents cleared!');
      } catch (error) {
        alert('Error clearing documents');
      } finally {
        setLoading(false);
      }
    }
  };

  const toggleSection = (section) => {
    setExpandedSection(expandedSection === section ? '' : section);
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>📚 Assistant</h2>
      </div>

      <nav className="sidebar-nav">
        {/* Upload Section */}
        <div className="nav-section">
          <button
            className={`nav-section-title ${expandedSection === 'upload' ? 'expanded' : ''}`}
            onClick={() => toggleSection('upload')}
          >
            <span>📤 Upload Documents</span>
            <span className="toggle-icon">{expandedSection === 'upload' ? '▼' : '▶'}</span>
          </button>
          
          {expandedSection === 'upload' && (
            <div className="section-content">
              <DocumentUpload onUploadSuccess={onDocumentsUploaded} />
            </div>
          )}
        </div>

        {/* Statistics Section */}
        <div className="nav-section">
          <button
            className={`nav-section-title ${expandedSection === 'stats' ? 'expanded' : ''}`}
            onClick={() => toggleSection('stats')}
          >
            <span>📊 Statistics</span>
            <span className="toggle-icon">{expandedSection === 'stats' ? '▼' : '▶'}</span>
          </button>
          
          {expandedSection === 'stats' && (
            <div className="section-content stats">
              <div className="stat-item">
                <div className="stat-label">Indexed Chunks</div>
                <div className="stat-value">{stats.documents_indexed}</div>
              </div>
              <p className="stat-help">
                Upload PDF documents to index them for search.
              </p>
            </div>
          )}
        </div>

        {/* Settings Section */}
        <div className="nav-section">
          <button
            className={`nav-section-title ${expandedSection === 'settings' ? 'expanded' : ''}`}
            onClick={() => toggleSection('settings')}
          >
            <span>⚙️ Settings</span>
            <span className="toggle-icon">{expandedSection === 'settings' ? '▼' : '▶'}</span>
          </button>
          
          {expandedSection === 'settings' && (
            <div className="section-content">
              <button
                className="action-button clear-chat"
                onClick={onClearChat}
              >
                🗑️ Clear Chat
              </button>
              <button
                className="action-button clear-all"
                onClick={handleClearAll}
                disabled={loading}
              >
                {loading ? '⏳ Clearing...' : '🗑️ Clear All Documents'}
              </button>
            </div>
          )}
        </div>

        {/* Help Section */}
        <div className="nav-section">
          <button
            className={`nav-section-title ${expandedSection === 'help' ? 'expanded' : ''}`}
            onClick={() => toggleSection('help')}
          >
            <span>❓ Help</span>
            <span className="toggle-icon">{expandedSection === 'help' ? '▼' : '▶'}</span>
          </button>
          
          {expandedSection === 'help' && (
            <div className="section-content help">
              <h4>How to use:</h4>
              <ul>
                <li>Upload PDF documents about your university</li>
                <li>Ask questions in natural language</li>
                <li>Get answers based on your documents</li>
                <li>See sources for verification</li>
              </ul>
              <h4>Supported Intents:</h4>
              <ul>
                <li>📚 Attendance</li>
                <li>📝 Examination</li>
                <li>🎓 Course</li>
                <li>📋 Admission</li>
                <li>💰 Fee</li>
                <li>📢 Other</li>
              </ul>
            </div>
          )}
        </div>
      </nav>

      <div className="sidebar-footer">
        <p>AI University Assistant v1.0</p>
        <p className="tech-stack">Built with FastAPI & React</p>
      </div>
    </aside>
  );
}

export default Sidebar;
