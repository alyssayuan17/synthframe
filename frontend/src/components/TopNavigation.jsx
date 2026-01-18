import React from 'react';
import { Link } from 'react-router-dom';

const TopNavigation = ({ onSave }) => {
    return (
        <div className="top-navigation">
            <div className="nav-left">
                <Link to="/" className="brand">
                    <img src="/synthframe logo.svg" alt="SynthFrame Logo" className="brand-logo" />
                    SynthFrame
                </Link>
            </div>

            <div className="nav-center"></div>

            <div className="nav-right">
                <button className="nav-btn" title="Undo">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M3 7v6h6" />
                        <path d="M21 17a9 9 0 00-9-9 9 9 0 00-6 2.3L3 13" />
                    </svg>
                </button>
                <button className="nav-btn" title="Redo">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M21 7v6h-6" />
                        <path d="M3 17a9 9 0 019-9 9 9 0 016 2.3l3 2.7" />
                    </svg>
                </button>
                <div className="divider" style={{ width: '1px', height: '24px', backgroundColor: 'var(--color-slate-700)', margin: '0 8px' }}></div>
                <button className="nav-btn" onClick={onSave} title="Save">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M19 21H5a2 2 0 01-2-2V5a2 2 0 012-2h11l5 5v11a2 2 0 01-2 2z" />
                        <polyline points="17 21 17 13 7 13 7 21" />
                        <polyline points="7 3 7 8 15 8" />
                    </svg>
                    Save
                </button>
                <button className="nav-btn" title="Download">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" />
                        <polyline points="7 10 12 15 17 10" />
                        <line x1="12" y1="15" x2="12" y2="3" />
                    </svg>
                    Download
                </button>
                <Link to="/gallery" className="nav-btn publish-btn" title="Project Gallery">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <rect x="3" y="3" width="7" height="7" />
                        <rect x="14" y="3" width="7" height="7" />
                        <rect x="14" y="14" width="7" height="7" />
                        <rect x="3" y="14" width="7" height="7" />
                    </svg>
                    Project Gallery
                </Link>
            </div>
        </div>
    );
};

export default TopNavigation;
