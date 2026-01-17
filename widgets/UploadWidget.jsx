/**
 * Upload Widget for Athena AI Chat
 * =================================
 *
 * This widget appears in the Athena chat to allow users to upload
 * hand-drawn sketches for analysis.
 *
 * Usage in Athena:
 * - Widget appears when user starts wireframe creation flow
 * - User can drag-and-drop or click to upload
 * - Image is converted to base64 and sent to MCP server
 */

import React, { useState, useCallback } from 'react';

export default function UploadWidget({ onUpload, onClose }) {
    const [isDragging, setIsDragging] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [preview, setPreview] = useState(null);

    const handleFile = useCallback(async (file) => {
        if (!file || !file.type.startsWith('image/')) {
            alert('Please upload an image file');
            return;
        }

        setUploading(true);

        // Convert to base64
        const reader = new FileReader();
        reader.onload = async (e) => {
            const base64 = e.target.result;
            setPreview(base64);

            // Send to Athena (which calls MCP server)
            if (onUpload) {
                await onUpload(base64);
            }

            setUploading(false);
        };

        reader.readAsDataURL(file);
    }, [onUpload]);

    const handleDrop = useCallback((e) => {
        e.preventDefault();
        setIsDragging(false);

        const file = e.dataTransfer.files[0];
        handleFile(file);
    }, [handleFile]);

    const handleFileInput = useCallback((e) => {
        const file = e.target.files[0];
        handleFile(file);
    }, [handleFile]);

    return (
        <div className="upload-widget" style={styles.container}>
            <div className="upload-header" style={styles.header}>
                <h3 style={styles.title}>Upload Your Sketch</h3>
                {onClose && (
                    <button onClick={onClose} style={styles.closeButton}>
                        ×
                    </button>
                )}
            </div>

            <div
                className={`upload-zone ${isDragging ? 'dragging' : ''}`}
                style={{
                    ...styles.uploadZone,
                    ...(isDragging ? styles.uploadZoneDragging : {})
                }}
                onDragOver={(e) => {
                    e.preventDefault();
                    setIsDragging(true);
                }}
                onDragLeave={() => setIsDragging(false)}
                onDrop={handleDrop}
            >
                {preview ? (
                    <div style={styles.previewContainer}>
                        <img src={preview} alt="Sketch preview" style={styles.preview} />
                        <button
                            onClick={() => {
                                setPreview(null);
                                document.getElementById('file-input').value = '';
                            }}
                            style={styles.clearButton}
                        >
                            Upload Different Sketch
                        </button>
                    </div>
                ) : (
                    <>
                        <svg style={styles.uploadIcon} viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                        </svg>
                        <p style={styles.uploadText}>
                            {uploading ? 'Processing...' : 'Drop your sketch here'}
                        </p>
                        <p style={styles.uploadSubtext}>or</p>
                        <label style={styles.browseButton}>
                            Browse Files
                            <input
                                id="file-input"
                                type="file"
                                accept="image/*"
                                onChange={handleFileInput}
                                style={styles.fileInput}
                                disabled={uploading}
                            />
                        </label>
                    </>
                )}
            </div>

            <div style={styles.tips}>
                <p style={styles.tipTitle}>Tips for best results:</p>
                <ul style={styles.tipList}>
                    <li>Draw clear boxes for components</li>
                    <li>Use good lighting when photographing</li>
                    <li>Supported formats: JPG, PNG, HEIC</li>
                </ul>
            </div>
        </div>
    );
}

// Inline styles (for easy embedding in Athena)
const styles = {
    container: {
        width: '100%',
        maxWidth: '500px',
        padding: '20px',
        backgroundColor: '#ffffff',
        borderRadius: '12px',
        boxShadow: '0 2px 12px rgba(0,0,0,0.1)',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    },
    header: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '16px',
    },
    title: {
        margin: 0,
        fontSize: '18px',
        fontWeight: 600,
        color: '#1a1a1a',
    },
    closeButton: {
        background: 'none',
        border: 'none',
        fontSize: '24px',
        cursor: 'pointer',
        color: '#666',
        padding: 0,
        width: '28px',
        height: '28px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
    uploadZone: {
        border: '2px dashed #d1d5db',
        borderRadius: '8px',
        padding: '40px 20px',
        textAlign: 'center',
        backgroundColor: '#f9fafb',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
    },
    uploadZoneDragging: {
        borderColor: '#3b82f6',
        backgroundColor: '#eff6ff',
    },
    uploadIcon: {
        width: '48px',
        height: '48px',
        margin: '0 auto 12px',
        color: '#9ca3af',
    },
    uploadText: {
        margin: '0 0 8px',
        fontSize: '16px',
        color: '#4b5563',
        fontWeight: 500,
    },
    uploadSubtext: {
        margin: '0 0 16px',
        fontSize: '14px',
        color: '#9ca3af',
    },
    browseButton: {
        display: 'inline-block',
        padding: '10px 24px',
        backgroundColor: '#3b82f6',
        color: '#ffffff',
        borderRadius: '6px',
        fontWeight: 500,
        cursor: 'pointer',
        transition: 'background-color 0.2s ease',
        fontSize: '14px',
    },
    fileInput: {
        display: 'none',
    },
    previewContainer: {
        textAlign: 'center',
    },
    preview: {
        maxWidth: '100%',
        maxHeight: '300px',
        borderRadius: '8px',
        marginBottom: '16px',
    },
    clearButton: {
        padding: '8px 16px',
        backgroundColor: '#f3f4f6',
        border: 'none',
        borderRadius: '6px',
        cursor: 'pointer',
        fontSize: '14px',
        color: '#374151',
        fontWeight: 500,
    },
    tips: {
        marginTop: '20px',
        padding: '16px',
        backgroundColor: '#f0f9ff',
        borderRadius: '8px',
        border: '1px solid #bfdbfe',
    },
    tipTitle: {
        margin: '0 0 8px',
        fontSize: '14px',
        fontWeight: 600,
        color: '#1e40af',
    },
    tipList: {
        margin: 0,
        paddingLeft: '20px',
        fontSize: '13px',
        color: '#1e40af',
    },
};
