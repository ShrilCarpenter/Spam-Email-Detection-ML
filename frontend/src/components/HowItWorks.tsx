import React from 'react';

export const HowItWorks: React.FC = () => {
  return (
    <div className="w-full max-w-[640px] mx-auto mt-12 text-center">
      <h3 className="text-sm font-semibold text-slate-800 mb-2">
        How does it work?
      </h3>
      <p className="text-xs sm:text-sm text-slate-500 leading-relaxed max-w-md mx-auto">
        The message is analyzed by a machine-learning model trained to distinguish spam from legitimate messages.
      </p>
    </div>
  );
};
