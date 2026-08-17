import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import ChatWindow from './components/ChatWindow';
import DocumentUpload from './components/DocumentUpload';
import Sidebar from './components/Sidebar';

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      text: "Hello! I'm your University Assistant. I can help you with information about courses, attendance, exams, admission, and more. Upload some university documents to get started!",
      time: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({ documents_indexed: 0 });
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const chatEndRef = useRef(null);

  const API_BASE_URL = 'http://localhost:8000/api';

  // Fetch stats on load
  useEffect(() => {
    fetchStats();
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/chat/stats`);
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    
    if (!input.trim()) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      type: 'user',
      text: input,
      time: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      // Call backend API
      const response = await axios.post(`${API_BASE_URL}/chat/ask`, {
        message: input,
        history: messages
      });

      const { answer, sources, intent, confidence } = response.data;

      // Add bot response
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: answer,
        sources: sources,
        intent: intent,
        confidence: confidence,
        time: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error:', error);
      
      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: 'Sorry, I encountered an error. Please make sure the backend is running and documents are uploaded.',
        time: new Date()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleDocumentsUploaded = () => {
    fetchStats();
    // Add notification
    const notificationMessage = {
      id: Date.now(),
      type: 'system',
      text: 'Documents uploaded successfully! You can now ask questions about them.',
      time: new Date()
    };
    setMessages(prev => [...prev, notificationMessage]);
  };

  const clearChat = () => {
    setMessages([
      {
        id: 1,
        type: 'bot',
        text: 'Chat cleared. Ready to help!',
        time: new Date()
      }
    ]);
  };

  return (
    <div className="app">
      {sidebarOpen && (
        <Sidebar
          stats={stats}
          onDocumentsUploaded={handleDocumentsUploaded}
          onClearChat={clearChat}
        />
      )}
      
      <div className="main-content">
        <header className="header">
          <button 
            className="sidebar-toggle"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            ☰
          </button>
          <h1>🎓 University Assistant</h1>
          <div className="header-info">
            {stats.documents_indexed > 0 && (
              <span className="status">📚 {stats.documents_indexed} chunks indexed</span>
            )}
          </div>
        </header>

        <ChatWindow 
          messages={messages}
          chatEndRef={chatEndRef}
        />

        <form className="input-area" onSubmit={sendMessage}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about your university..."
            disabled={loading}
            className="chat-input"
          />
          <button 
            type="submit" 
            disabled={loading || !input.trim()}
            className="send-button"
          >
            {loading ? '⏳' : '📤'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
