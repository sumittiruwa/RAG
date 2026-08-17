import React, { useState } from 'react';
import axios from 'axios';
import './DocumentUpload.css';

function DocumentUpload({ onUploadSuccess }) {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const API_BASE_URL = 'http://localhost:8000/api';

  const handleFileSelect = (e) => {
    const selectedFiles = Array.from(e.target.files).filter(
      file => file.type === 'application/pdf'
    );

    if (selectedFiles.length === 0) {
      setMessage('❌ Please select PDF files only');
      return;
    }

    setFiles(selectedFiles);
    setMessage(`✓ ${selectedFiles.length} file(s) selected`);
  };

  const handleUpload = async () => {
    if (files.length === 0) {
      setMessage('❌ No files selected');
      return;
    }

    setUploading(true);
    setMessage('Uploading...');

    try {
      for (const file of files) {
        const formData = new FormData();
        formData.append('file', file);

        await axios.post(`${API_BASE_URL}/documents/upload`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
      }

      setMessage('✓ Documents uploaded successfully!');
      setFiles([]);
      onUploadSuccess();

      // Clear message after 3 seconds
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      console.error('Upload error:', error);
      setMessage('❌ Upload failed. Make sure backend is running.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="document-upload">
      <div className="upload-area">
        <input
          type="file"
          id="file-input"
          multiple
          accept=".pdf"
          onChange={handleFileSelect}
          disabled={uploading}
          hidden
        />
        <label htmlFor="file-input" className="upload-label">
          <div className="upload-icon">📄</div>
          <div className="upload-text">
            <strong>Click to select PDF files</strong>
            <p>or drag and drop</p>
          </div>
        </label>
      </div>

      {files.length > 0 && (
        <div className="files-list">
          <strong>Selected Files:</strong>
          {files.map((file, idx) => (
            <div key={idx} className="file-item">
              📄 {file.name}
            </div>
          ))}
        </div>
      )}

      {message && (
        <div className={`message ${message.includes('✓') ? 'success' : 'error'}`}>
          {message}
        </div>
      )}

      <button
        className="upload-button"
        onClick={handleUpload}
        disabled={uploading || files.length === 0}
      >
        {uploading ? '⏳ Uploading...' : '📤 Upload Documents'}
      </button>
    </div>
  );
}

export default DocumentUpload;
