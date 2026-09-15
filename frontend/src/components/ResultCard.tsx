import React from 'react';
import { AlertTriangle, CheckCircle2 } from 'lucide-react';
import { PredictionResponse } from '../api/spamApi';

interface ResultCardProps {
  result: PredictionResponse;
}

export const ResultCard: React.FC<ResultCardProps> = ({ result }) => {
  const isSpam = result.is_spam;
  const label = isSpam ? 'SPAM' : 'NOT SPAM';
  const supportingText = isSpam
    ? 'This email is likely to be spam.'
    : 'This email appears to be legitimate.';

  const confidencePercent = result.confidence.toFixed(1);
  const spamProb = result.probabilities.spam;
  const hamProb = result.probabilities.ham;

  return (
    <div
      className={`mt-6 p-5 sm:p-6 rounded-lg border transition-all ${
        isSpam
          ? 'bg-red-50/70 border-red-200 text-red-950'
          : 'bg-emerald-50/70 border-emerald-200 text-emerald-950'
      }`}
      role="region"
      aria-live="polite"
      aria-label="Email Spam Prediction Result"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-start space-x-3.5">
          <div
            className={`mt-0.5 w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
              isSpam ? 'bg-red-100 text-red-700' : 'bg-emerald-100 text-emerald-700'
            }`}
            aria-hidden="true"
          >
            {isSpam ? (
              <AlertTriangle className="w-4 h-4" strokeWidth={2.4} />
            ) : (
              <CheckCircle2 className="w-4 h-4" strokeWidth={2.4} />
            )}
          </div>
          <div>
            <div className="text-xs font-semibold uppercase tracking-wider text-slate-500 mb-0.5">
              Prediction
            </div>
            <div
              className={`text-xl sm:text-2xl font-bold tracking-tight ${
                isSpam ? 'text-red-700' : 'text-emerald-700'
              }`}
            >
              {label}
            </div>
            <p className="text-sm font-medium text-slate-700 mt-1">
              {supportingText}
            </p>
          </div>
        </div>

        {/* Model Confidence Badge */}
        <div className="text-right shrink-0">
          <span
            className={`inline-block px-2.5 py-1 text-xs font-semibold rounded-md border ${
              isSpam
                ? 'bg-red-100/80 border-red-200 text-red-800'
                : 'bg-emerald-100/80 border-emerald-200 text-emerald-800'
            }`}
          >
            {confidencePercent}% Confidence
          </span>
        </div>
      </div>

      {/* Probability Distribution */}
      <div className="mt-5 pt-4 border-t border-slate-200/80">
        <div className="grid grid-cols-2 gap-3 text-xs">
          <div className="p-2.5 rounded bg-white/70 border border-slate-200">
            <div className="flex justify-between font-medium text-slate-600 mb-1">
              <span>Legitimate (Ham)</span>
              <span className="font-semibold tabular-nums text-slate-800">{hamProb.toFixed(1)}%</span>
            </div>
            <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
              <div
                className="h-full bg-emerald-500 rounded-full transition-all duration-300"
                style={{ width: `${Math.max(hamProb, 1)}%` }}
              />
            </div>
          </div>

          <div className="p-2.5 rounded bg-white/70 border border-slate-200">
            <div className="flex justify-between font-medium text-slate-600 mb-1">
              <span>Spam Probability</span>
              <span className="font-semibold tabular-nums text-slate-800">{spamProb.toFixed(1)}%</span>
            </div>
            <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
              <div
                className="h-full bg-red-500 rounded-full transition-all duration-300"
                style={{ width: `${Math.max(spamProb, 1)}%` }}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
