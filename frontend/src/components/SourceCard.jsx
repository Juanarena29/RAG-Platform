import { useState } from 'react'
import { ChevronDown, ChevronUp } from 'lucide-react'

export default function SourceCard({ source }) {
  const [expanded, setExpanded] = useState(false)
  const score = typeof source.score === 'number' ? source.score.toFixed(2) : source.score

  return (
    <div className="mt-2 rounded-lg border border-border bg-surface-elevated/50">
      <button
        type="button"
        onClick={() => setExpanded((prev) => !prev)}
        className="flex w-full items-center justify-between gap-2 px-3 py-2 text-left text-sm text-foreground transition-colors hover:bg-surface-elevated"
        aria-expanded={expanded}
      >
        <span className="min-w-0 truncate">
          📄 {source.original_filename} — pág. {source.page_number}
        </span>
        <span className="flex shrink-0 items-center gap-2">
          <span className="rounded bg-surface px-2 py-0.5 font-mono text-xs text-muted-foreground">
            {score}
          </span>
          {expanded ? (
            <ChevronUp className="h-4 w-4 text-muted-foreground" aria-hidden="true" />
          ) : (
            <ChevronDown className="h-4 w-4 text-muted-foreground" aria-hidden="true" />
          )}
        </span>
      </button>
      {expanded && (
        <div className="border-t border-border-subtle px-3 pb-3 pt-2">
          <pre className="max-h-32 overflow-y-auto whitespace-pre-wrap rounded bg-background/60 p-2 font-mono text-xs text-muted-foreground">
            {source.text}
          </pre>
        </div>
      )}
    </div>
  )
}
