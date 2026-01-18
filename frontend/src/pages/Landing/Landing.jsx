import React from 'react';
import { Link } from 'react-router-dom';
import './Landing.css';

const Landing = () => {
    const scrollToFeatures = () => {
        document.getElementById('features').scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    };

    return (
        <div className="landing">
            <nav className="landing-nav">
                <div className="nav-container">
                    <div className="landing-brand">
                        <img src="/synthframe logo.svg" alt="SynthFrame Logo" className="brand-logo" />
                        <span>SynthFrame</span>
                    </div>
                    <div className="nav-actions">
                        <Link to="/sketchpad" className="nav-link">
                            Open Sketchpad
                        </Link>
                    </div>
                </div>
            </nav>

            <main className="landing-main">
                <section className="hero">
                    <h1 className="hero-title">Visual Design Canvas</h1>
                    <p className="hero-subtitle">
                        Create, prototype, and iterate on your designs with an infinite canvas
                    </p>
                    <div className="hero-actions">
                        <Link to="/sketchpad" className="btn-primary">
                            Start Creating
                        </Link>
                        <button className="btn-secondary" onClick={scrollToFeatures}>
                            Learn More
                        </button>
                    </div>
                </section>

                <section className="features" id="features">
                    <div className="features-grid">
                        <div className="feature-card">
                            <div className="feature-icon">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <rect x="3" y="3" width="18" height="18" rx="2"/>
                                    <path d="M9 3v18"/>
                                </svg>
                            </div>
                            <h3 className="feature-title">Infinite Canvas</h3>
                            <p className="feature-description">
                                Unlimited space to bring your ideas to life without constraints
                            </p>
                        </div>

                        <div className="feature-card">
                            <div className="feature-icon">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <rect x="2" y="7" width="20" height="14" rx="2"/>
                                    <path d="M16 3h5v5M21 3l-7 7"/>
                                </svg>
                            </div>
                            <h3 className="feature-title">Frame-Based Design</h3>
                            <p className="feature-description">
                                Organize components within device frames for precise layouts
                            </p>
                        </div>

                        <div className="feature-card">
                            <div className="feature-icon">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
                                </svg>
                            </div>
                            <h3 className="feature-title">Component Library</h3>
                            <p className="feature-description">
                                Pre-built UI components ready to drag and drop into your designs
                            </p>
                        </div>

                        <div className="feature-card">
                            <div className="feature-icon">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <polyline points="16 18 22 12 16 6"/>
                                    <polyline points="8 6 2 12 8 18"/>
                                </svg>
                            </div>
                            <h3 className="feature-title">Export Ready</h3>
                            <p className="feature-description">
                                Generate production-ready code from your visual designs
                            </p>
                        </div>
                    </div>
                </section>

                <section className="cta">
                    <h2 className="cta-title">Ready to start designing?</h2>
                    <p className="cta-description">
                        Join designers building the future of visual development
                    </p>
                    <Link to="/sketchpad" className="btn-primary">
                        Launch Sketchpad
                    </Link>
                </section>
            </main>

            <footer className="landing-footer">
                <div className="footer-container">
                    <div className="footer-content">
                        <p className="footer-brand">SynthFrame</p>
                        <p className="footer-text">
                            Visual design canvas for modern web development
                        </p>
                    </div>
                    <div className="footer-links">
                        <a href="https://github.com/alyssayuan17/synthframe" target="_blank" rel="noopener noreferrer" className="footer-link">GitHub</a>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default Landing;
