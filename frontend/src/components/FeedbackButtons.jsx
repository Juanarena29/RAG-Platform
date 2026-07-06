import { useState } from 'react'
import { ThumbsDown, ThumbsUp } from 'lucide-react'
import { submitFeedback } from '../api.js'

export default function FeedbackButtons({ traceId, onFeedbackSent }) {
  const [feedback, setFeedback] = useState(null)
  const [sent, setSent] = useState(false)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  if (!traceId) {
    return null
  }

  async function handleFeedback(value) {
    if (sent || loading) {
      return
    }

    setLoading(true)
    setError(null)

    try {
      await submitFeedback(traceId, value)
      setFeedback(value)
      setSent(true)
      onFeedbackSent?.()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'No se pudo enviar el feedback')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mt-2">
      <div className="flex items-center gap-1">
        <button
          type="button"
          onClick={() => handleFeedback('positive')}
          disabled={sent || loading}
          aria-label="Feedback positivo"
          className={`rounded p-1.5 transition-colors disabled:cursor-not-allowed disabled:opacity-50 ${
            feedback === 'positive'
              ? 'text-success'
              : 'text-muted-foreground hover:text-foreground'
          }`}
        >
          <ThumbsUp className="h-4 w-4" />
        </button>
        <button
          type="button"
          onClick={() => handleFeedback('negative')}
          disabled={sent || loading}
          aria-label="Feedback negativo"
          className={`rounded p-1.5 transition-colors disabled:cursor-not-allowed disabled:opacity-50 ${
            feedback === 'negative'
              ? 'text-destructive'
              : 'text-muted-foreground hover:text-foreground'
          }`}
        >
          <ThumbsDown className="h-4 w-4" />
        </button>
      </div>
      {error && <p className="mt-1 text-xs text-destructive">{error}</p>}
    </div>
  )
}
