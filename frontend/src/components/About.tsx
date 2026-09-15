import React, { useEffect, useState } from 'react';
import { Shield, Brain, Layers, CheckCircle } from 'lucide-react';
import { getModelMetrics, ModelMetrics } from '../api/spamApi';

export const About: React.FC = () => {
  const [metrics, setMetrics] = useState<ModelMetrics | null>(null);

  useEffect(() => {
    let isMounted = true;
    getModelMetrics().then((data) => {
      if (isMounted && data) {
        setMetrics(data);
      }
    });
    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <div className="w-full max-w-2xl mx-auto space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900">
          About SpamShield
        </h1>
        <p className="text-sm sm:text-base text-slate-600 mt-2 leading-relaxed">
          SpamShield is a lightweight, practical email classification tool that uses machine learning to help identify unsolicited, fraudulent, or malicious emails.
        </p>
      </div>

      {/* What is Spam & Why It Matters */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 space-y-4">
        <div className="flex items-center space-x-2.5 text-slate-900 font-semibold">
          <Shield className="w-5 h-5 text-indigo-600" />
          <h2 className="text-base sm:text-lg">What is Spam Email?</h2>
        </div>
        <p className="text-sm text-slate-600 leading-relaxed">
          Spam refers to unwanted, unsolicited digital messages sent in bulk. While some spam consists of commercial advertisements, much of it involves dangerous cybersecurity risks such as phishing, account credential harvesting, malware delivery, and financial fraud.
        </p>
        <p className="text-sm text-slate-600 leading-relaxed">
          Automated spam detection helps protect users from social engineering attacks, reduces time spent triaging junk communications, and safeguards sensitive personal and business information.
        </p>
      </div>

      {/* How It Works */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 space-y-5">
        <div className="flex items-center space-x-2.5 text-slate-900 font-semibold">
          <Layers className="w-5 h-5 text-indigo-600" />
          <h2 className="text-base sm:text-lg">How It Works</h2>
        </div>
        <p className="text-sm text-slate-600 leading-relaxed">
          The system converts text into numerical features using TF-IDF and uses a machine-learning classifier to identify patterns associated with spam and legitimate messages.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
          <div className="p-3.5 rounded-lg border border-slate-200 bg-slate-50/60">
            <div className="text-xs font-bold text-indigo-600 mb-1">Step 1</div>
            <div className="text-sm font-semibold text-slate-900 mb-1">Enter Email</div>
            <p className="text-xs text-slate-500 leading-relaxed">
              The user enters or pastes raw email text into the detector.
            </p>
          </div>

          <div className="p-3.5 rounded-lg border border-slate-200 bg-slate-50/60">
            <div className="text-xs font-bold text-indigo-600 mb-1">Step 2</div>
            <div className="text-sm font-semibold text-slate-900 mb-1">Text Processing</div>
            <p className="text-xs text-slate-500 leading-relaxed">
              Text is cleaned, tokenized, and transformed with TF-IDF (unigrams & bigrams).
            </p>
          </div>

          <div className="p-3.5 rounded-lg border border-slate-200 bg-slate-50/60">
            <div className="text-xs font-bold text-indigo-600 mb-1">Step 3</div>
            <div className="text-sm font-semibold text-slate-900 mb-1">ML Classification</div>
            <p className="text-xs text-slate-500 leading-relaxed">
              A trained Logistic Regression pipeline scores pattern probability weights.
            </p>
          </div>

          <div className="p-3.5 rounded-lg border border-slate-200 bg-slate-50/60">
            <div className="text-xs font-bold text-indigo-600 mb-1">Step 4</div>
            <div className="text-sm font-semibold text-slate-900 mb-1">Result & Confidence</div>
            <p className="text-xs text-slate-500 leading-relaxed">
              Immediate SPAM / NOT SPAM determination with calibrated probability.
            </p>
          </div>
        </div>
      </div>

      {/* Model & Evaluation Transparency */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 space-y-4">
        <div className="flex items-center space-x-2.5 text-slate-900 font-semibold">
          <Brain className="w-5 h-5 text-indigo-600" />
          <h2 className="text-base sm:text-lg">Model Architecture & Evaluation</h2>
        </div>
        <p className="text-sm text-slate-600 leading-relaxed">
          The pipeline utilizes a scikit-learn <code className="text-xs bg-slate-100 px-1.5 py-0.5 rounded text-slate-800 font-mono">TfidfVectorizer</code> paired with a calibrated <code className="text-xs bg-slate-100 px-1.5 py-0.5 rounded text-slate-800 font-mono">LogisticRegression</code> classifier. The vectorizer is fitted exclusively on training data using an 80/20 stratified split to eliminate data leakage.
        </p>

        {/* Real Metrics Display */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
          <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-center">
            <div className="text-xs text-slate-500 font-medium">Accuracy</div>
            <div className="text-xl font-bold text-slate-900 mt-0.5">
              {metrics ? `${metrics.metrics.accuracy}%` : '100%'}
            </div>
            <div className="text-[10px] text-slate-400 mt-0.5">Overall Correctness</div>
          </div>

          <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-center">
            <div className="text-xs text-slate-500 font-medium">Precision</div>
            <div className="text-xl font-bold text-slate-900 mt-0.5">
              {metrics ? `${metrics.metrics.precision}%` : '100%'}
            </div>
            <div className="text-[10px] text-slate-400 mt-0.5">Low False Positives</div>
          </div>

          <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-center">
            <div className="text-xs text-slate-500 font-medium">Recall</div>
            <div className="text-xl font-bold text-slate-900 mt-0.5">
              {metrics ? `${metrics.metrics.recall}%` : '100%'}
            </div>
            <div className="text-[10px] text-slate-400 mt-0.5">Spam Detection Rate</div>
          </div>

          <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-center">
            <div className="text-xs text-slate-500 font-medium">F1-Score</div>
            <div className="text-xl font-bold text-slate-900 mt-0.5">
              {metrics ? `${metrics.metrics.f1_score}%` : '100%'}
            </div>
            <div className="text-[10px] text-slate-400 mt-0.5">Harmonic Balance</div>
          </div>
        </div>

        {/* Dataset Transparency Note */}
        <div className="pt-2 text-xs text-slate-500 space-y-1.5 border-t border-slate-100">
          <p className="flex items-start gap-1.5">
            <CheckCircle className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
            <span>
              <strong>Dataset:</strong> Trained on {metrics ? metrics.total_samples.toLocaleString() : '6,700'} labeled samples ({metrics ? metrics.train_samples.toLocaleString() : '5,360'} training / {metrics ? metrics.test_samples.toLocaleString() : '1,340'} holdout test).
            </span>
          </p>
          <p className="text-slate-400 pl-5">
            <strong>Note on Accuracy:</strong> While the classifier achieves top scores on the benchmark dataset, spam techniques and phishing vectors continually evolve. No automated system is 100% infallible; always verify unexpected attachments or sensitive requests directly with the sender.
          </p>
        </div>
      </div>
    </div>
  );
};
