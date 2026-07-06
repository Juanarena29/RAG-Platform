import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft, Sparkles } from 'lucide-react'
import { checkHealth, getDocuments } from '../api.js'
import ChatPanel from '../components/ChatPanel.jsx'
import UploadPanel from '../components/UploadPanel.jsx'

export default function ChatPage() {
  const [documents, setDocuments] = useState([])
  const [isLoadingDocs, setIsLoadingDocs] = useState(true)
  const [docsError, setDocsError] = useState(null)
  const [backendStatus, setBackendStatus] = useState('checking')

  const loadDocuments = useCallback(async () => {
    setIsLoadingDocs(true)
    setDocsError(null)

    try {
      const data = await getDocuments()
      setDocuments(data.documents ?? [])
    } catch (err) {
      setDocsError(err instanceof Error ? err.message : 'No se pudieron cargar los documentos')
    } finally {
      setIsLoadingDocs(false)
    }
  }, [])

  useEffect(() => {
    loadDocuments()
  }, [loadDocuments])

  useEffect(() => {
    checkHealth()
      .then(() => setBackendStatus('online'))
      .catch(() => setBackendStatus('offline'))
  }, [])

  const hasCompletedDocs = documents.some((doc) => doc.status === 'completed')

  return (
    <div className="flex min-h-screen flex-col bg-background bg-mesh">
      <header className="sticky top-0 z-20 border-b border-border-subtle glass">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6">
          <div className="flex items-center gap-4">
            <Link
              to="/"
              className="flex items-center gap-1.5 rounded-lg px-2 py-1.5 text-sm text-muted-foreground transition-colors hover:bg-surface-elevated hover:text-foreground"
              aria-label="Volver al inicio"
            >
              <ArrowLeft className="h-4 w-4" aria-hidden="true" />
              <span className="hidden sm:inline">Inicio</span>
            </Link>
            <div className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/15 ring-1 ring-primary/25">
                <Sparkles className="h-3.5 w-3.5 text-primary" aria-hidden="true" />
              </div>
              <h1 className="font-heading text-lg font-semibold text-foreground">RAG Platform</h1>
            </div>
          </div>
          <span
            className={`rounded-full px-3 py-1 text-xs font-medium ring-1 ${
              backendStatus === 'online'
                ? 'bg-success/10 text-success ring-success/20'
                : backendStatus === 'offline'
                  ? 'bg-destructive/10 text-destructive ring-destructive/20'
                  : 'bg-surface-elevated text-muted-foreground ring-border-subtle'
            }`}
          >
            {backendStatus === 'online'
              ? 'Backend online'
              : backendStatus === 'offline'
                ? 'Backend offline'
                : 'Verificando...'}
          </span>
        </div>
      </header>

      <main className="mx-auto grid w-full max-w-7xl flex-1 gap-6 px-4 py-6 sm:px-6 lg:grid-cols-[minmax(280px,30%)_1fr]">
        <aside className="space-y-4">
          <div className="rounded-[var(--card-radius)] border border-border bg-surface p-4">
            <UploadPanel documents={documents} onDocumentReady={loadDocuments} />
          </div>
          {isLoadingDocs && (
            <p className="text-xs text-muted-foreground">Actualizando lista de documentos...</p>
          )}
          {docsError && (
            <p className="text-sm text-destructive" role="alert">
              {docsError}
            </p>
          )}
        </aside>

        <section className="min-h-[32rem]">
          <ChatPanel hasCompletedDocs={hasCompletedDocs} />
        </section>
      </main>
    </div>
  )
}
