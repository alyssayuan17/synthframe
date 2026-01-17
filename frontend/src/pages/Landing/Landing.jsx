import React, { useEffect, useState } from 'react';
import './Landing.css';

const Landing = () => {
    const [scrollY, setScrollY] = useState(0);

    useEffect(() => {
        let scrollTimeout;
        const handleScroll = () => {
            setScrollY(window.scrollY);

            // Show scrollbar on scroll
            document.body.classList.add('is-scrolling');
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                document.body.classList.remove('is-scrolling');
            }, 1000);
        };

        window.addEventListener('scroll', handleScroll, { passive: true });
        return () => {
            window.removeEventListener('scroll', handleScroll);
            clearTimeout(scrollTimeout);
            document.body.classList.remove('is-scrolling');
        };
    }, []);

    // Calculate dynamic positions and scales based on scroll
    const orb1Style = {
        transform: `translate(${Math.sin(scrollY * 0.001) * 100}px, ${scrollY * 0.3}px) scale(${1 + Math.sin(scrollY * 0.002) * 0.3})`,
        opacity: 0.18 + Math.sin(scrollY * 0.003) * 0.08,
    };

    const orb2Style = {
        transform: `translate(${Math.cos(scrollY * 0.0015) * 150}px, ${-scrollY * 0.2}px) scale(${1 + Math.cos(scrollY * 0.002) * 0.2})`,
        opacity: 0.18 + Math.cos(scrollY * 0.003) * 0.08,
    };

    const orb3Style = {
        transform: `translate(${Math.sin(scrollY * 0.002) * 80}px, ${Math.cos(scrollY * 0.002) * 80}px) scale(${1 + Math.sin(scrollY * 0.0025) * 0.25})`,
        opacity: 0.18 + Math.sin(scrollY * 0.004) * 0.08,
    };

    return (
        <div className="landing">
            {/* Background Gradient Orbs with Scroll Animation */}
            <div className="bg-gradient-orb orb-1" style={orb1Style}></div>
            <div className="bg-gradient-orb orb-2" style={orb2Style}></div>
            <div className="bg-gradient-orb orb-3" style={orb3Style}></div>

            {/* Navigation / Logo */}
            <nav className="navbar">
                <h1 className="nav-logo">SynthFrame</h1>
            </nav>

            {/* Hero Section */}
            <section className="hero">
                <div className="hero-content">
                    <p className="hero-subtitle">
                        Transform your creative vision with cutting-edge synthesis technology.
                    </p>
                    <button className="cta-button">
                        Get Started
                    </button>
                </div>
            </section>


        </div>
    );
};

export default Landing;
