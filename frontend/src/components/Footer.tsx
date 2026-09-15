import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="w-full border-t border-slate-200 bg-white py-6 mt-auto">
      <div className="max-w-4xl mx-auto px-4 text-center text-xs text-slate-500 space-y-1">
        <p className="font-semibold text-slate-800">SpamShield</p>
        <p className="text-slate-500">Machine-learning based email spam detection.</p>
      </div>
    </footer>
  );
};
