import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
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
    <div className="flex h-dvh flex-col overflow-hidden bg-background">
      <header className="shrink-0 border-b border-border-subtle bg-surface">
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
            <h1 className="font-heading text-base font-medium text-foreground">Chat</h1>
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
              ? 'Online'
              : backendStatus === 'offline'
                ? 'Offline'
                : 'Checking...'}
          </span>
        </div>
      </header>

      <main className="mx-auto grid w-full max-w-7xl flex-1 min-h-0 gap-6 px-4 py-6 sm:px-6 lg:grid-cols-[minmax(260px,28%)_1fr]">
        <aside className="flex min-h-0 flex-col gap-4 overflow-y-auto chat-scrollbar lg:max-h-full">
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

        <section className="flex min-h-0 flex-1 flex-col">
          <ChatPanel hasCompletedDocs={hasCompletedDocs} />
        </section>
      </main>
    </div>
  )
}
