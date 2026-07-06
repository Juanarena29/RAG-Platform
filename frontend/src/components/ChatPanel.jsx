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
          className="rounded bg-blue-100 px-1 font-mono text-sm text-blue-700"
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
      <span className="h-2 w-2 animate-pulse rounded-full bg-gray-400" />
      <span className="h-2 w-2 animate-pulse rounded-full bg-gray-400 [animation-delay:150ms]" />
      <span className="h-2 w-2 animate-pulse rounded-full bg-gray-400 [animation-delay:300ms]" />
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
    <div className="flex h-full min-h-[32rem] flex-col rounded-xl border border-gray-200 bg-white shadow-sm">
      <div className="flex-1 overflow-y-auto p-4">
        {!hasCompletedDocs ? (
          <div className="flex h-full flex-col items-center justify-center text-center">
            <p className="text-base font-medium text-gray-700">
              Subí un PDF para empezar a chatear
            </p>
            <p className="mt-2 max-w-sm text-sm text-gray-400">
              Una vez que el documento termine de procesarse, podés hacer preguntas sobre su
              contenido.
            </p>
          </div>
        ) : messages.length === 0 && !isLoading ? (
          <div className="flex h-full flex-col items-center justify-center text-center">
            <p className="text-base font-medium text-gray-700">¿Qué querés saber?</p>
            <p className="mt-2 max-w-sm text-sm text-gray-400">
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
                      ? 'rounded-2xl rounded-tr-sm bg-gray-100 px-4 py-2 text-gray-800'
                      : 'rounded-2xl rounded-tl-sm border border-gray-200 bg-white px-4 py-3 text-gray-800'
                  }`}
                >
                  <div className="whitespace-pre-wrap text-sm leading-relaxed">
                    {message.role === 'assistant'
                      ? renderAnswerWithCitations(message.content)
                      : message.content}
                  </div>

                  {message.role === 'assistant' && message.sources?.length > 0 && (
                    <div className="mt-3 border-t border-gray-100 pt-3">
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
                <div className="rounded-2xl rounded-tl-sm border border-gray-200 bg-white px-4 py-2">
                  <ThinkingDots />
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        )}

        {error && (
          <p className="mt-4 text-sm text-red-500" role="alert">
            {error}
          </p>
        )}
      </div>

      <form
        onSubmit={handleSubmit}
        className="sticky bottom-0 border-t border-gray-200 bg-white p-4"
      >
        <div className="flex items-center gap-2">
          <input
            type="text"
            value={input}
            onChange={(event) => setInput(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Hacé una pregunta sobre tus documentos..."
            disabled={!hasCompletedDocs || isLoading}
            className="flex-1 rounded-lg border border-gray-200 px-4 py-2.5 text-sm text-gray-800 placeholder:text-gray-400 focus:border-blue-400 focus:outline-none disabled:cursor-not-allowed disabled:bg-gray-50"
          />
          <button
            type="submit"
            disabled={!hasCompletedDocs || isLoading || !input.trim()}
            aria-label="Enviar pregunta"
            className="flex items-center justify-center rounded-lg bg-blue-600 px-3 py-2.5 text-white transition-colors hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
      </form>
    </div>
  )
}
