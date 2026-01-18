import React from 'react';
import { Link } from 'react-router-dom';

const TopNavigation = () => {
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
                <button className="nav-btn preview-btn" title="Preview">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                        <circle cx="12" cy="12" r="3" />
                    </svg>
                    Preview
                </button>
                <button className="nav-btn publish-btn" title="Publish">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" />
                        <polyline points="17 8 12 3 7 8" />
                        <line x1="12" y1="3" x2="12" y2="15" />
                    </svg>
                    Publish
                </button>
            </div>
        </div>
    );
};

export default TopNavigation;
