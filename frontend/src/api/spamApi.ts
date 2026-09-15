export interface Probabilities {
  ham: number;
  spam: number;
}

export interface PredictionResponse {
  prediction: string;
  label: 'SPAM' | 'NOT SPAM' | string;
  probability: number;
  is_spam: boolean;
  confidence: number;
  probabilities: Probabilities;
}

export interface HealthResponse {
  status: string;
  model_loaded: boolean;
}

export interface ModelMetrics {
  model_type: string;
  dataset_name: string;
  total_samples: number;
  ham_samples: number;
  spam_samples: number;
  train_samples: number;
  test_samples: number;
  metrics: {
    accuracy: number;
    precision: number;
    recall: number;
    f1_score: number;
    true_negatives: number;
    false_positives: number;
    false_negatives: number;
    true_positives: number;
  };
  pipeline_config?: {
    ngram_range: number[];
    max_features: number;
    sublinear_tf: boolean;
    classifier: string;
  };
}

const API_BASE_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/+$/, '');

export async function predictEmail(text: string): Promise<PredictionResponse> {
  const trimmed = text.trim();
  if (!trimmed) {
    throw new Error('Please enter an email message.');
  }

  let response: Response;
  const urlsToTry = [
    `${API_BASE_URL}/api/predict`,
    `${API_BASE_URL}/predict`
  ];

  // If localhost fails in development, also provide 127.0.0.1 fallback
  if (API_BASE_URL.includes('localhost')) {
    const fallbackBase = API_BASE_URL.replace('localhost', '127.0.0.1');
    urlsToTry.push(`${fallbackBase}/api/predict`);
    urlsToTry.push(`${fallbackBase}/predict`);
  }

  let successResponse: Response | null = null;

  for (const url of urlsToTry) {
    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: trimmed }),
      });

      // If endpoint exists (even if 400 validation error), stop trying other urls
      if (res.status !== 404) {
        successResponse = res;
        break;
      }
    } catch {
      // Continue to next candidate URL
    }
  }

  if (!successResponse) {
    throw new Error('Unable to connect to the spam detection service. Please try again.');
  }

  response = successResponse;

  if (!response.ok) {
    if (response.status === 400 || response.status === 422) {
      try {
        const errorData = await response.json();
        if (typeof errorData?.detail === 'string') {
          throw new Error(errorData.detail);
        }
      } catch (parseErr) {
        if (parseErr instanceof Error && parseErr.message !== 'Please enter an email message.') {
          // ignore json parse error
        } else {
          throw parseErr;
        }
      }
      throw new Error('Please enter an email message.');
    }

    if (response.status === 503) {
      throw new Error('The spam detection model is currently initializing. Please try again in a moment.');
    }

    throw new Error('Something went wrong while analyzing the email.');
  }

  const data: PredictionResponse = await response.json();

  // Normalize label and is_spam if backend returned variants
  const isSpam = data.is_spam ?? (String(data.prediction).toLowerCase() === 'spam');
  const label = data.label || (isSpam ? 'SPAM' : 'NOT SPAM');

  return {
    ...data,
    is_spam: isSpam,
    label: label as 'SPAM' | 'NOT SPAM',
  };
}

export async function getHealth(): Promise<HealthResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/health`);
    if (response.ok) {
      return await response.json();
    }
  } catch {
    // Fallback attempt
    try {
      const fallback = await fetch(`${API_BASE_URL}/health`);
      if (fallback.ok) return await fallback.json();
    } catch {
      // offline
    }
  }
  return { status: 'offline', model_loaded: false };
}

export async function getModelMetrics(): Promise<ModelMetrics | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/metrics`);
    if (response.ok) {
      return await response.json();
    }
    const fallback = await fetch(`${API_BASE_URL}/metrics`);
    if (fallback.ok) {
      return await fallback.json();
    }
  } catch {
    // return null if unable to reach
  }
  return null;
}
