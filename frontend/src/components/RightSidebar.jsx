import React, { useState, useRef, useEffect } from 'react';
import UploadWidget from './widgets/UploadWidget';
import StatusWidget from './widgets/StatusWidget';

const RightSidebar = ({ currentWireframeId, onWireframeUpdate }) => {
    const [messages, setMessages] = useState([
        {
            id: 1,
            type: 'assistant',
            text: 'Hello! I\'m your AI assistant. I can help you build your website by suggesting components, layouts, and design improvements. What would you like to create today? You can also upload a sketch!',
        },
    ]);
    const [inputValue, setInputValue] = useState('');
    const [showUpload, setShowUpload] = useState(false);
    const [status, setStatus] = useState(null); // 'processing', 'success', 'error'
    const [statusData, setStatusData] = useState({});

    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, showUpload, status]);

    const handleSend = async () => {
        if (inputValue.trim()) {
            const userText = inputValue;
            const userMessage = {
                id: Date.now(),
                type: 'user',
                text: userText,
            };

            setMessages((prev) => [...prev, userMessage]);
            setInputValue('');
            setStatus('processing');

            try {
                let response;

                // DECISION LOGIC: Generate vs Update
                if (currentWireframeId) {
                    // We have an active wireframe -> UPDATE IT
                    response = await fetch('http://localhost:8001/api/update', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            wireframe_id: currentWireframeId,
                            instruction: userText
                        })
                    });
                } else {
                    // No active wireframe -> GENERATE NEW
                    response = await fetch('http://localhost:8001/api/generate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ prompt: userText })
                    });
                }

                const data = await response.json();

                if (response.ok) {
                    setStatus('success');
                    setStatusData({
                        message: data.message,
                        component_count: data.component_count || (data.components ? data.components.length : 0),
                        wireframe_id: data.wireframe_id
                    });

                    const aiMessage = {
                        id: Date.now() + 1,
                        type: 'assistant',
                        text: data.message || (currentWireframeId ? "Updated your wireframe!" : "Generated a new wireframe!"),
                    };
                    setMessages((prev) => [...prev, aiMessage]);

                    if (onWireframeUpdate) {
                        onWireframeUpdate(data.components, data.wireframe_id);
                    }
                } else {
                    setStatus('error');
                    setStatusData({ error: data.detail || "Unknown error" });
                }
            } catch (error) {
                setStatus('error');
                setStatusData({ error: "Network error: Unable to reach SynthFrame backend." });
            }
        }
    };

    const handleUpload = async (base64Image) => {
        setShowUpload(false);
        setStatus('processing');

        // Add a message for the upload
        setMessages(prev => [...prev, {
            id: Date.now(),
            type: 'user',
            text: 'Uploaded a sketch for analysis.'
        }]);

        try {
            // Remove prefix if present (data:image/png;base64,) as server might expect raw or full
            // Actually our server expects whatever, but let's send full string
            const response = await fetch('http://localhost:8001/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image_base64: base64Image, prompt: "Analyze this sketch" })
            });

            const data = await response.json();

            if (response.ok) {
                setStatus('success');
                setStatusData({
                    message: data.message,
                    component_count: data.component_count,
                    wireframe_id: data.wireframe_id
                });

                const aiMessage = {
                    id: Date.now() + 1,
                    type: 'assistant',
                    text: `I've analyzed your sketch and found ${data.component_count} components!`,
                };
                setMessages((prev) => [...prev, aiMessage]);

                if (onWireframeUpdate) {
                    onWireframeUpdate(data.components);
                }
            } else {
                setStatus('error');
                setStatusData({ error: data.detail || "Analysis failed" });
            }
        } catch (error) {
            setStatus('error');
            setStatusData({ error: "Network error: Unable to upload sketch." });
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

                {/* Widgets appear in stream */}
                {showUpload && (
                    <div className="widget-container">
                        <UploadWidget
                            onUpload={handleUpload}
                            onClose={() => setShowUpload(false)}
                        />
                    </div>
                )}

                {status && (
                    <div className="widget-container">
                        <StatusWidget
                            status={status}
                            data={statusData}
                            onOpenEditor={() => setStatus(null)} // Dismiss on click
                        />
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            <div className="chat-input-container">
                <button
                    className="icon-btn"
                    onClick={() => setShowUpload(!showUpload)}
                    title="Upload Sketch"
                    style={{ marginRight: '8px', background: 'none', border: 'none', cursor: 'pointer', color: '#666' }}
                >
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48" />
                    </svg>
                </button>

                <input
                    type="text"
                    className="chat-input"
                    placeholder="Describe a layout..."
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
