import { useState } from 'react'
import { ChevronDown, ChevronUp } from 'lucide-react'

export default function SourceCard({ source }) {
  const [expanded, setExpanded] = useState(false)
  const score = typeof source.score === 'number' ? source.score.toFixed(2) : source.score

  return (
    <div className="mt-2 rounded-lg border border-gray-200 bg-white">
      <button
        type="button"
        onClick={() => setExpanded((prev) => !prev)}
        className="flex w-full items-center justify-between gap-2 px-3 py-2 text-left text-sm text-gray-700 hover:bg-gray-50"
        aria-expanded={expanded}
      >
        <span className="min-w-0 truncate">
          📄 {source.original_filename} — pág. {source.page_number}
        </span>
        <span className="flex shrink-0 items-center gap-2">
          <span className="rounded bg-gray-100 px-2 py-0.5 font-mono text-xs text-gray-600">
            {score}
          </span>
          {expanded ? (
            <ChevronUp className="h-4 w-4 text-gray-400" aria-hidden="true" />
          ) : (
            <ChevronDown className="h-4 w-4 text-gray-400" aria-hidden="true" />
          )}
        </span>
      </button>
      {expanded && (
        <div className="border-t border-gray-100 px-3 pb-3 pt-2">
          <pre className="max-h-32 overflow-y-auto whitespace-pre-wrap rounded bg-gray-50 p-2 font-mono text-xs text-gray-700">
            {source.text}
          </pre>
        </div>
      )}
    </div>
  )
}
