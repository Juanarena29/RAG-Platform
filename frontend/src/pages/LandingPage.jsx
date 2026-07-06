import { Link } from 'react-router-dom'
import { ArrowRight } from 'lucide-react'

export default function LandingPage() {
  return (
    <div className="flex min-h-dvh flex-col bg-background">
      <header className="mx-auto flex w-full max-w-5xl items-center px-6 py-8">
        <span className="font-heading text-sm font-medium tracking-wide text-muted-foreground">
          RAG Platform
        </span>
      </header>

      <main className="flex flex-1 flex-col items-center justify-center px-6 pb-24">
        <div className="w-full max-w-lg text-center">
          <h1 className="font-heading text-4xl font-semibold leading-tight tracking-tight text-foreground sm:text-5xl">
            Ask your documents anything
          </h1>

          <p className="mx-auto mt-5 max-w-md text-base leading-relaxed text-muted-foreground">
            Upload PDFs, build a knowledge base, and chat with answers grounded in your sources.
          </p>

          <div className="mt-10">
            <Link
              to="/chat"
              className="group inline-flex items-center gap-2 rounded-[var(--button-radius)] bg-primary px-8 py-3 text-sm font-medium text-primary-foreground transition-colors duration-200 hover:bg-primary-hover focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background"
            >
              Start
              <ArrowRight
                className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-0.5"
                aria-hidden="true"
              />
            </Link>
          </div>
        </div>
      </main>

      <footer className="border-t border-border-subtle py-6 text-center text-xs text-muted-foreground">
        Document-grounded AI
      </footer>
    </div>
  )
}
