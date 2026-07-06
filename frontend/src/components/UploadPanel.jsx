import { useEffect, useRef, useState } from 'react'
import { CheckCircle2, Loader2 } from 'lucide-react'
import { getDocuments, uploadDocument } from '../api.js'

const STATUS_STYLES = {
  pending: 'bg-yellow-100 text-yellow-800',
  processing: 'bg-blue-100 text-blue-800',
  completed: 'bg-green-100 text-green-800',
  failed: 'bg-red-100 text-red-800',
}

const STATUS_LABELS = {
  pending: 'Pendiente',
  processing: 'Procesando',
  completed: 'Listo',
  failed: 'Error',
}

function formatDate(value) {
  if (!value) {
    return ''
  }

  return new Date(value).toLocaleString('es-AR', {
    day: '2-digit',
    month: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export default function UploadPanel({ documents, onDocumentReady }) {
  const inputRef = useRef(null)
  const pollRef = useRef(null)

  const [panelState, setPanelState] = useState('idle')
  const [errorMessage, setErrorMessage] = useState('')
  const [uploadedFilename, setUploadedFilename] = useState('')

  useEffect(() => {
    return () => {
      if (pollRef.current) {
        clearInterval(pollRef.current)
      }
    }
  }, [])

  function handleDragOver(event) {
    event.preventDefault()
    if (panelState === 'idle' || panelState === 'error' || panelState === 'done') {
      setPanelState('dragging')
    }
  }

  function handleDragLeave(event) {
    event.preventDefault()
    if (panelState === 'dragging') {
      setPanelState('idle')
    }
  }

  function handleDrop(event) {
    event.preventDefault()
    const file = event.dataTransfer.files?.[0]
    if (file) {
      handleFile(file)
    } else {
      setPanelState('idle')
    }
  }

  function handleFileSelect(event) {
    const file = event.target.files?.[0]
    if (file) {
      handleFile(file)
    }
    event.target.value = ''
  }

  async function handleFile(file) {
    if (file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) {
      setPanelState('error')
      setErrorMessage('Solo se aceptan archivos PDF')
      return
    }

    setPanelState('uploading')
    setErrorMessage('')
    setUploadedFilename(file.name)

    try {
      const result = await uploadDocument(file)
      setUploadedFilename(result.original_filename ?? file.name)
      setPanelState('processing')
      startPolling(result.document_id)
    } catch (err) {
      setPanelState('error')
      setErrorMessage(err instanceof Error ? err.message : 'Error al subir el archivo')
    }
  }

  function startPolling(documentId) {
    if (pollRef.current) {
      clearInterval(pollRef.current)
    }

    pollRef.current = setInterval(async () => {
      try {
        const data = await getDocuments()
        const doc = data.documents?.find((item) => item.id === documentId)

        if (!doc) {
          return
        }

        if (doc.status === 'completed') {
          clearInterval(pollRef.current)
          pollRef.current = null
          setPanelState('done')
          onDocumentReady?.()
        } else if (doc.status === 'failed') {
          clearInterval(pollRef.current)
          pollRef.current = null
          setPanelState('error')
          setErrorMessage('El procesamiento del documento falló')
          onDocumentReady?.()
        }
      } catch {
        // Keep polling; transient errors should not stop the workflow.
      }
    }, 3000)
  }

  const dropZoneClasses = {
    idle: 'border-dashed border-gray-300 bg-white text-gray-500 hover:border-gray-400',
    dragging: 'border-blue-400 bg-blue-50 text-blue-700',
    uploading: 'border-blue-300 bg-blue-50 text-blue-700',
    processing: 'border-blue-300 bg-blue-50 text-blue-700',
    done: 'border-green-300 bg-green-50 text-green-700',
    error: 'border-red-300 bg-red-50 text-red-600',
  }

  return (
    <div className="space-y-4">
      <div
        role="button"
        tabIndex={0}
        onClick={() => inputRef.current?.click()}
        onKeyDown={(event) => {
          if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault()
            inputRef.current?.click()
          }
        }}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`flex min-h-40 cursor-pointer flex-col items-center justify-center rounded-xl border-2 p-6 text-center transition-colors ${dropZoneClasses[panelState] ?? dropZoneClasses.idle}`}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf"
          className="hidden"
          onChange={handleFileSelect}
        />

        {panelState === 'idle' && (
          <p className="text-sm">Arrastrá tu PDF aquí o hacé click</p>
        )}

        {panelState === 'dragging' && (
          <p className="text-sm font-medium">Soltá el archivo aquí</p>
        )}

        {(panelState === 'uploading' || panelState === 'processing') && (
          <div className="flex flex-col items-center gap-2">
            <Loader2 className="h-6 w-6 animate-spin" aria-hidden="true" />
            <p className="text-sm font-medium">
              {panelState === 'uploading' ? 'Subiendo...' : 'Procesando documento...'}
            </p>
          </div>
        )}

        {panelState === 'done' && (
          <div className="flex flex-col items-center gap-2">
            <CheckCircle2 className="h-6 w-6 text-green-600" aria-hidden="true" />
            <p className="text-sm font-medium">{uploadedFilename}</p>
          </div>
        )}

        {panelState === 'error' && (
          <p className="text-sm font-medium">{errorMessage}</p>
        )}
      </div>

      <div>
        <h2 className="mb-2 text-sm font-semibold text-gray-700">Documentos</h2>
        {documents.length === 0 ? (
          <p className="text-sm text-gray-400">Todavía no hay documentos subidos.</p>
        ) : (
          <ul className="space-y-2">
            {documents.map((doc) => (
              <li
                key={doc.id}
                className="rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm"
              >
                <div className="flex items-start justify-between gap-2">
                  <span className="min-w-0 truncate font-medium text-gray-800">
                    {doc.original_filename}
                  </span>
                  <span
                    className={`shrink-0 rounded-full px-2 py-0.5 text-xs font-medium ${STATUS_STYLES[doc.status] ?? 'bg-gray-100 text-gray-700'}`}
                  >
                    {STATUS_LABELS[doc.status] ?? doc.status}
                  </span>
                </div>
                <div className="mt-1 flex items-center justify-between text-xs text-gray-400">
                  <span>{formatDate(doc.created_at)}</span>
                  {doc.status === 'completed' && doc.chunk_count != null && (
                    <span>{doc.chunk_count} chunks</span>
                  )}
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}
