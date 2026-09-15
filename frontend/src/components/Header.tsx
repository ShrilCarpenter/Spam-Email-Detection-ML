import React from 'react';
import { ShieldCheck } from 'lucide-react';

interface HeaderProps {
  activeTab: 'detector' | 'about';
  onTabChange: (tab: 'detector' | 'about') => void;
}

export const Header: React.FC<HeaderProps> = ({ activeTab, onTabChange }) => {
  return (
    <header className="w-full border-b border-slate-200 bg-white sticky top-0 z-30 shadow-xs">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
        {/* Left: Brand / Logo */}
        <button
          onClick={() => onTabChange('detector')}
          className="flex items-center space-x-2 focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 rounded p-1"
          aria-label="SpamShield Home"
        >
          <div className="w-7 h-7 rounded-md bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-600">
            <ShieldCheck className="w-4 h-4" strokeWidth={2.2} />
          </div>
          <span className="font-semibold text-slate-900 text-base tracking-tight">
            SpamShield
          </span>
        </button>

        {/* Right: Minimal Navigation */}
        <nav className="flex items-center space-x-1 sm:space-x-2" aria-label="Main Navigation">
          <button
            type="button"
            onClick={() => onTabChange('detector')}
            className={`px-3 py-1.5 rounded-md text-xs sm:text-sm font-medium transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 ${
              activeTab === 'detector'
                ? 'bg-slate-100 text-slate-900 font-semibold'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
            }`}
          >
            Detector
          </button>
          <button
            type="button"
            onClick={() => onTabChange('about')}
            className={`px-3 py-1.5 rounded-md text-xs sm:text-sm font-medium transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 ${
              activeTab === 'about'
                ? 'bg-slate-100 text-slate-900 font-semibold'
                : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
            }`}
          >
            About
          </button>
        </nav>
      </div>
    </header>
  );
};
