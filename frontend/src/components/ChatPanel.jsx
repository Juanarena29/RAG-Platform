import { useEffect, useRef, useState } from 'react'
import { Send } from 'lucide-react'
import { queryRAG } from '../api.js'
import FeedbackButtons from './FeedbackButtons.jsx'
import SourceCard from './SourceCard.jsx'

function renderAnswerWithCitations(answer) {
  const parts = answer.split(/(\[\d+\])/g)

  return parts.map((part, index) => {
    if (/^\[\d+\]$/.test(part)) {
      return (
        <span
          key={`${part}-${index}`}
          className="rounded bg-chat-citation-bg px-1 font-mono text-sm text-chat-citation-fg"
        >
          {part}
        </span>
      )
    }

    return <span key={`text-${index}`}>{part}</span>
  })
}

function ThinkingDots() {
  return (
    <div className="flex items-center gap-1 px-1 py-2" aria-label="Pensando">
      <span className="h-2 w-2 animate-pulse rounded-full bg-muted-foreground/60" />
      <span className="h-2 w-2 animate-pulse rounded-full bg-muted-foreground/60 [animation-delay:150ms]" />
      <span className="h-2 w-2 animate-pulse rounded-full bg-muted-foreground/60 [animation-delay:300ms]" />
    </div>
  )
}

export default function ChatPanel({ hasCompletedDocs }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  async function handleSubmit(event) {
    event?.preventDefault()

    const question = input.trim()
    if (!question || isLoading || !hasCompletedDocs) {
      return
    }

    setInput('')
    setError(null)
    setIsLoading(true)

    setMessages((prev) => [...prev, { role: 'user', content: question }])

    try {
      const result = await queryRAG(question)
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: result.answer,
          sources: result.sources ?? [],
          traceId: result.trace_id ?? null,
        },
      ])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al procesar la consulta')
    } finally {
      setIsLoading(false)
    }
  }

  function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className="flex h-full min-h-[32rem] flex-col rounded-[var(--card-radius)] border border-border bg-surface">
      <div className="flex-1 overflow-y-auto p-4">
        {!hasCompletedDocs ? (
          <div className="flex h-full flex-col items-center justify-center text-center">
            <p className="text-base font-medium text-foreground">
              Subí un PDF para empezar a chatear
            </p>
            <p className="mt-2 max-w-sm text-sm text-muted-foreground">
              Una vez que el documento termine de procesarse, podés hacer preguntas sobre su
              contenido.
            </p>
          </div>
        ) : messages.length === 0 && !isLoading ? (
          <div className="flex h-full flex-col items-center justify-center text-center">
            <p className="text-base font-medium text-foreground">¿Qué querés saber?</p>
            <p className="mt-2 max-w-sm text-sm text-muted-foreground">
              Hacé una pregunta sobre tus documentos procesados.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {messages.map((message, index) => (
              <div
                key={`${message.role}-${index}`}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[85%] ${
                    message.role === 'user'
                      ? 'rounded-2xl rounded-tr-sm bg-chat-user-bg px-4 py-2 text-foreground'
                      : 'rounded-2xl rounded-tl-sm border border-border bg-chat-assistant-bg px-4 py-3 text-foreground'
                  }`}
                >
                  <div className="whitespace-pre-wrap text-sm leading-relaxed">
                    {message.role === 'assistant'
                      ? renderAnswerWithCitations(message.content)
                      : message.content}
                  </div>

                  {message.role === 'assistant' && message.sources?.length > 0 && (
                    <div className="mt-3 border-t border-border-subtle pt-3">
                      {message.sources.map((source, sourceIndex) => (
                        <SourceCard
                          key={`${source.document_id}-${source.page_number}-${sourceIndex}`}
                          source={source}
                        />
                      ))}
                      <FeedbackButtons traceId={message.traceId} />
                    </div>
                  )}

                  {message.role === 'assistant' &&
                    (!message.sources || message.sources.length === 0) && (
                      <FeedbackButtons traceId={message.traceId} />
                    )}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex justify-start">
                <div className="rounded-2xl rounded-tl-sm border border-border bg-chat-assistant-bg px-4 py-2">
                  <ThinkingDots />
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        )}

        {error && (
          <p className="mt-4 text-sm text-destructive" role="alert">
            {error}
          </p>
        )}
      </div>

      <form
        onSubmit={handleSubmit}
        className="sticky bottom-0 border-t border-border bg-surface/80 p-4 backdrop-blur-sm"
      >
        <div className="flex items-center gap-2">
          <input
            type="text"
            value={input}
            onChange={(event) => setInput(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Hacé una pregunta sobre tus documentos..."
            disabled={!hasCompletedDocs || isLoading}
            className="flex-1 rounded-[var(--input-radius)] border border-border bg-surface-elevated px-4 py-2.5 text-sm text-foreground placeholder:text-muted-foreground focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-ring/30 disabled:cursor-not-allowed disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={!hasCompletedDocs || isLoading || !input.trim()}
            aria-label="Enviar pregunta"
            className="flex items-center justify-center rounded-[var(--input-radius)] bg-primary px-3 py-2.5 text-primary-foreground transition-colors hover:bg-primary-hover disabled:cursor-not-allowed disabled:opacity-50"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
      </form>
    </div>
  )
}
