import React from 'react';
import './ChatWindow.css';

function ChatWindow({ messages, chatEndRef }) {
  return (
    <div className="chat-window">
      {messages.map((msg) => (
        <div key={msg.id} className={`message ${msg.type}`}>
          {msg.type === 'user' && (
            <div className="message-content">
              <div className="message-text">{msg.text}</div>
              <div className="message-time">{formatTime(msg.time)}</div>
            </div>
          )}

          {msg.type === 'bot' && (
            <div className="message-content">
              <div className="bot-avatar">🤖</div>
              <div className="message-body">
                <div className="message-text">{msg.text}</div>
                
                {msg.sources && (
                  <div className="sources">
                    <strong>📖 Sources:</strong>
                    <pre>{msg.sources}</pre>
                  </div>
                )}

                {msg.intent && (
                  <div className="metadata">
                    <span className="intent">Intent: {msg.intent}</span>
                    <span className="confidence">Confidence: {(msg.confidence * 100).toFixed(0)}%</span>
                  </div>
                )}

                <div className="message-time">{formatTime(msg.time)}</div>
              </div>
            </div>
          )}

          {msg.type === 'system' && (
            <div className="system-message">
              <div className="message-text">{msg.text}</div>
            </div>
          )}
        </div>
      ))}
      <div ref={chatEndRef} />
    </div>
  );
}

function formatTime(date) {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

export default ChatWindow;
