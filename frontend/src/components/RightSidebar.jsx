import React, { useState, useRef, useEffect } from 'react';

const RightSidebar = () => {
    const [messages, setMessages] = useState([
        {
            id: 1,
            type: 'assistant',
            text: 'Hello! I\'m your AI assistant. I can help you build your website by suggesting components, layouts, and design improvements. What would you like to create today?',
        },
    ]);
    const [inputValue, setInputValue] = useState('');
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = () => {
        if (inputValue.trim()) {
            const userMessage = {
                id: Date.now(),
                type: 'user',
                text: inputValue,
            };

            setMessages((prev) => [...prev, userMessage]);
            setInputValue('');

            // Simulate AI response
            setTimeout(() => {
                const aiMessage = {
                    id: Date.now() + 1,
                    type: 'assistant',
                    text: 'I understand you want to ' + inputValue + '. Let me help you with that! (This is a placeholder response. Connect to an AI service for real responses.)',
                };
                setMessages((prev) => [...prev, aiMessage]);
            }, 500);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="right-sidebar">
            <div className="sidebar-header">
                <h2>AI Assistant</h2>
                <div className="status-indicator">
                    <span className="status-dot"></span>
                    <span className="status-text">Ready</span>
                </div>
            </div>

            <div className="chat-messages">
                {messages.map((message) => (
                    <div key={message.id} className={`message ${message.type}`}>
                        <div className="message-content">{message.text}</div>
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>

            <div className="chat-input-container">
                <input
                    type="text"
                    className="chat-input"
                    placeholder="Ask me anything..."
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={handleKeyPress}
                />
                <button
                    className="send-btn"
                    onClick={handleSend}
                    disabled={!inputValue.trim()}
                    title="Send"
                >
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <line x1="22" y1="2" x2="11" y2="13" />
                        <polygon points="22 2 15 22 11 13 2 9 22 2" />
                    </svg>
                </button>
            </div>
        </div>
    );
};

export default RightSidebar;
