import { useCallback, useEffect, useState } from 'react'
import { checkHealth, getDocuments } from '../api.js'
import ChatPanel from '../components/ChatPanel.jsx'
import UploadPanel from '../components/UploadPanel.jsx'

export default function App() {
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
    <div className="min-h-screen bg-gray-50">
      <header className="border-b border-gray-200 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6">
          <h1 className="text-lg font-semibold text-gray-900">RAG Platform</h1>
          <span
            className={`rounded-full px-3 py-1 text-xs font-medium ${
              backendStatus === 'online'
                ? 'bg-green-100 text-green-700'
                : backendStatus === 'offline'
                  ? 'bg-red-100 text-red-700'
                  : 'bg-gray-100 text-gray-600'
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

      <main className="mx-auto grid max-w-7xl gap-6 px-4 py-6 sm:px-6 lg:grid-cols-[30%_1fr]">
        <aside className="space-y-4">
          <div className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
            <UploadPanel documents={documents} onDocumentReady={loadDocuments} />
          </div>
          {isLoadingDocs && (
            <p className="text-xs text-gray-400">Actualizando lista de documentos...</p>
          )}
          {docsError && (
            <p className="text-sm text-red-500" role="alert">
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
