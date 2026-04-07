/**
 * Root application component.
 *
 * Composes all page sections in the correct order:
 * Header → Hero → About → Recent Sales → Contact → Footer
 */
function App(): JSX.Element {
  return (
    <div className="min-h-screen bg-cream">
      {/* Header */}
      <header
        id="header"
        className="sticky top-0 z-50 border-b border-cream-dark bg-cream/90 backdrop-blur-sm"
      >
        <div className="section-container flex h-16 items-center justify-between md:h-20">
          <a
            href="#hero"
            className="font-playfair text-xl font-bold text-slate-900 md:text-2xl"
          >
            Maddie
          </a>
          <nav className="hidden items-center gap-8 md:flex">
            {['About', 'Sales', 'Contact'].map((item) => (
              <a
                key={item}
                href={`#${item.toLowerCase()}`}
                className="font-inter text-sm font-medium text-slate-500 transition-colors hover:text-gold"
              >
                {item}
              </a>
            ))}
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section
        id="hero"
        className="section-padding relative flex min-h-[80vh] items-center bg-warm-white"
      >
        <div className="section-container">
          <div className="max-w-2xl">
            <h1 className="animate-slide-up text-balance">
              Your Dream Home Awaits
            </h1>
            <p className="mt-6 animate-fade-in text-lg text-slate-500">
              Specializing in luxury properties with a personal touch.
              Let&apos;s find the perfect place for you.
            </p>
            <div className="mt-8 flex gap-4">
              <a href="#contact" className="btn-primary">
                Get in Touch
              </a>
              <a href="#sales" className="btn-secondary">
                View Properties
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="section-padding bg-cream">
        <div className="section-container">
          <h2 className="text-center">About Maddie</h2>
          <p className="mx-auto mt-4 max-w-2xl text-center text-slate-500">
            With over a decade of experience in luxury real estate, I help
            families find their perfect home. My commitment to personalized
            service sets me apart.
          </p>
        </div>
      </section>

      {/* Recent Sales Section */}
      <section id="sales" className="section-padding bg-warm-white">
        <div className="section-container">
          <h2 className="text-center">Recent Sales</h2>
          <p className="mx-auto mt-4 max-w-xl text-center text-slate-500">
            A selection of recently sold properties.
          </p>
          <div className="mt-12 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {/* Property cards will be added in subsequent phases */}
            <div className="rounded-lg border border-cream-dark bg-cream-light p-4 shadow-sm">
              <div className="aspect-[4/3] rounded-md bg-cream-dark" />
              <h3 className="mt-4 text-lg">Coming Soon</h3>
              <p className="mt-1 text-sm text-slate-500">
                Property listings will appear here.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="section-padding bg-cream">
        <div className="section-container text-center">
          <h2>Let&apos;s Connect</h2>
          <p className="mx-auto mt-4 max-w-xl text-slate-500">
            Ready to start your journey? Reach out today and let&apos;s make
            your real estate dreams a reality.
          </p>
          <div className="mt-8">
            <a href="mailto:hello@maddierealty.com" className="btn-primary">
              Contact Maddie
            </a>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-cream-dark bg-cream py-8">
        <div className="section-container text-center">
          <p className="font-playfair text-lg font-semibold text-slate-900">
            Maddie
          </p>
          <p className="mt-2 text-sm text-slate-400">
            &copy; {new Date().getFullYear()} Maddie Real Estate. All rights
            reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
