import React, { useState } from 'react';
import { Loader2, AlertCircle, ShieldCheck } from 'lucide-react';
import { predictEmail, PredictionResponse } from '../api/spamApi';
import { ResultCard } from './ResultCard';

const SAMPLE_SPAM =
  "Congratulations! You have been selected to receive an exclusive $1,000 gift card reward. Claim your prize immediately by clicking the verification link below: http://claim-prize-rewards.com. Offer valid for 24 hours only.";

const SAMPLE_HAM =
  "Hi David, hope you're having a productive week. Could you please review the updated project proposal and budget report before our team meeting on Thursday at 2 PM? Let me know if you have any questions.";

export const Detector: React.FC = () => {
  const [emailText, setEmailText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<PredictionResponse | null>(null);

  const handleClear = () => {
    setEmailText('');
    setError(null);
    setResult(null);
  };

  const handleCheck = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    const trimmed = emailText.trim();
    if (!trimmed) {
      setError('Please enter an email message.');
      return;
    }

    setLoading(true);

    try {
      const res = await predictEmail(trimmed);
      setResult(res);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('Something went wrong while analyzing the email.');
      }
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const loadSample = (sample: string) => {
    setEmailText(sample);
    setError(null);
    setResult(null);
  };

  const charCount = emailText.length;

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-8">
        <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-slate-900">
          Detect Email Spam Instantly
        </h1>
        <p className="text-sm sm:text-base text-slate-600 mt-2.5 max-w-lg mx-auto">
          Paste an email below and our machine learning model will classify it as spam or not spam.
        </p>
      </div>

      {/* Main Detector Card */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs p-5 sm:p-7">
        <form onSubmit={handleCheck} className="space-y-4">
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label
                htmlFor="email-content"
                className="block text-sm font-semibold text-slate-800"
              >
                Email Content
              </label>

              {/* Sample Quick-fill Buttons */}
              <div className="flex items-center space-x-2 text-xs">
                <span className="text-slate-400 hidden sm:inline">Samples:</span>
                <button
                  type="button"
                  onClick={() => loadSample(SAMPLE_SPAM)}
                  className="text-slate-500 hover:text-indigo-600 hover:underline transition-colors focus:outline-none focus-visible:ring-1 focus-visible:ring-indigo-500 rounded px-1"
                >
                  Try Spam Example
                </button>
                <span className="text-slate-300">·</span>
                <button
                  type="button"
                  onClick={() => loadSample(SAMPLE_HAM)}
                  className="text-slate-500 hover:text-indigo-600 hover:underline transition-colors focus:outline-none focus-visible:ring-1 focus-visible:ring-indigo-500 rounded px-1"
                >
                  Try Legitimate Example
                </button>
              </div>
            </div>

            <textarea
              id="email-content"
              rows={8}
              value={emailText}
              onChange={(e) => {
                setEmailText(e.target.value);
                if (error) setError(null);
              }}
              placeholder="Paste your email message here..."
              className="w-full px-3.5 py-3 text-sm sm:text-base text-slate-900 bg-white rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600 transition-colors placeholder:text-slate-400 resize-y"
              aria-required="true"
            />
          </div>

          {/* Character Count & Clear */}
          <div className="flex items-center justify-between text-xs text-slate-500 pt-0.5">
            <span>{charCount.toLocaleString()} characters</span>
            <button
              type="button"
              onClick={handleClear}
              disabled={loading || (!emailText && !result && !error)}
              className="font-medium text-slate-500 hover:text-slate-800 hover:underline transition-colors disabled:opacity-40 disabled:hover:no-underline focus:outline-none"
            >
              Clear
            </button>
          </div>

          {/* Action Buttons */}
          <div className="pt-2 flex flex-col sm:flex-row items-center justify-center gap-3">
            <button
              type="submit"
              disabled={loading}
              className="w-full sm:w-auto min-w-[180px] inline-flex items-center justify-center px-6 py-2.5 text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800 rounded-lg transition-colors disabled:opacity-60 disabled:cursor-not-allowed shadow-xs focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:ring-offset-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  <span>Analyzing...</span>
                </>
              ) : (
                <span>Check Email</span>
              )}
            </button>

            {result && (
              <button
                type="button"
                onClick={handleClear}
                className="w-full sm:w-auto px-4 py-2.5 text-sm font-medium text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors"
              >
                Clear
              </button>
            )}
          </div>

          {/* Privacy Message */}
          <div className="pt-2 text-center">
            <p className="text-xs text-slate-400 flex items-center justify-center gap-1.5">
              <ShieldCheck className="w-3.5 h-3.5 text-slate-400 shrink-0" />
              <span>Your email content is analyzed for classification and is not stored.</span>
            </p>
          </div>
        </form>

        {/* Inline Error Message */}
        {error && (
          <div
            className="mt-5 p-3 rounded-lg bg-red-50 border border-red-200 text-red-700 text-xs sm:text-sm flex items-center space-x-2"
            role="alert"
          >
            <AlertCircle className="w-4 h-4 shrink-0 text-red-500" />
            <span>{error}</span>
          </div>
        )}

        {/* Result Card */}
        {result && !loading && <ResultCard result={result} />}
      </div>
    </div>
  );
};
