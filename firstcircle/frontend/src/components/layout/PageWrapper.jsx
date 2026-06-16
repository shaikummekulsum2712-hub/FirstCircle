import Navbar from "./Navbar.jsx";

export default function PageWrapper({ children, className = "" }) {
  return (
    <div className="min-h-screen">
      <Navbar />
      <main className={`mx-auto max-w-7xl px-5 py-8 ${className}`}>
        {children}
      </main>
    </div>
  );
}