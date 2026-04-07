import React from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import About from './components/About';
import RecentSales from './components/RecentSales';
import Contact from './components/Contact';
import Footer from './components/Footer';

/**
 * Root application component.
 * Serves as the top-level layout wrapper composing all page sections
 * in order for a single-page luxury real estate site.
 *
 * Section IDs enable smooth-scroll navigation from the Header nav links.
 */
const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-cream" style={{ backgroundColor: '#FFFDF7' }}>
      <Header />

      <main>
        <section id="hero">
          <Hero />
        </section>

        <section id="about">
          <About />
        </section>

        <section id="recent-sales">
          <RecentSales />
        </section>

        <section id="contact">
          <Contact />
        </section>
      </main>

      <Footer />
    </div>
  );
};

export default App;
