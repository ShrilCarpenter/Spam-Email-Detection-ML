import React, { useState } from 'react';
import { Header } from './components/Header';
import { Detector } from './components/Detector';
import { About } from './components/About';
import { Footer } from './components/Footer';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'detector' | 'about'>('detector');

  return (
    <div className="min-h-screen flex flex-col bg-[#fbfbfb] text-slate-900 font-sans antialiased">
      <Header activeTab={activeTab} onTabChange={setActiveTab} />

      <main className="flex-1 flex flex-col justify-center px-4 sm:px-6 py-10 sm:py-14">
        {activeTab === 'detector' ? <Detector /> : <About />}
      </main>

      <Footer />
    </div>
  );
};

export default App;
