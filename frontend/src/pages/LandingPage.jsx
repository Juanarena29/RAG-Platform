import { Link } from 'react-router-dom'
import { ArrowRight, FileSearch, MessageSquare, Sparkles, Zap } from 'lucide-react'

const FEATURES = [
  {
    icon: FileSearch,
    title: 'Document ingestion',
    description: 'Upload PDFs and let the pipeline chunk, embed, and index them automatically.',
  },
  {
    icon: MessageSquare,
    title: 'Semantic Q&A',
    description: 'Ask natural-language questions and get answers grounded in your corpus.',
  },
  {
    icon: Zap,
    title: 'Source citations',
    description: 'Every response links back to the exact page and passage it came from.',
  },
]

export default function LandingPage() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-background bg-mesh">
      <div
        className="pointer-events-none absolute -left-32 top-20 h-96 w-96 rounded-full bg-primary/10 blur-3xl animate-pulse-glow"
        aria-hidden="true"
      />
      <div
        className="pointer-events-none absolute -right-24 bottom-32 h-80 w-80 rounded-full bg-accent/10 blur-3xl animate-pulse-glow [animation-delay:2s]"
        aria-hidden="true"
      />

      <header className="relative z-10 mx-auto flex max-w-6xl items-center justify-between px-6 py-6">
        <div className="flex items-center gap-2.5">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary/15 ring-1 ring-primary/30">
            <Sparkles className="h-4 w-4 text-primary" aria-hidden="true" />
          </div>
          <span className="font-heading text-lg font-semibold tracking-tight text-foreground">
            RAG Platform
          </span>
        </div>
        <Link
          to="/chat"
          className="hidden text-sm text-muted-foreground transition-colors hover:text-foreground sm:inline-block"
        >
          Go to chat
        </Link>
      </header>

      <main className="relative z-10 mx-auto max-w-6xl px-6 pb-24 pt-12 sm:pt-20">
        <section className="mx-auto max-w-3xl text-center">
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-border-subtle bg-surface/60 px-4 py-1.5 text-xs font-medium text-muted-foreground backdrop-blur-sm">
            <span className="h-1.5 w-1.5 rounded-full bg-success" aria-hidden="true" />
            Retrieval-Augmented Generation
          </div>

          <h1 className="font-heading text-4xl font-bold leading-tight tracking-tight text-foreground sm:text-5xl lg:text-6xl">
            Ask your documents
            <span className="mt-1 block text-gradient">anything.</span>
          </h1>

          <p className="mx-auto mt-6 max-w-xl text-base leading-relaxed text-muted-foreground sm:text-lg">
            Upload PDFs, build a knowledge base, and chat with an AI that answers from your
            sources — with citations you can verify.
          </p>

          <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link
              to="/chat"
              className="glow-button group inline-flex items-center gap-2 rounded-[var(--button-radius)] bg-primary px-8 py-3.5 font-medium text-primary-foreground transition-all duration-200 hover:bg-primary-hover focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background"
            >
              Start
              <ArrowRight
                className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-0.5"
                aria-hidden="true"
              />
            </Link>
            <p className="text-sm text-muted-foreground">No sign-up required</p>
          </div>
        </section>

        <section className="mt-24 grid gap-5 sm:grid-cols-3">
          {FEATURES.map(({ icon: Icon, title, description }) => (
            <article
              key={title}
              className="glass group rounded-[var(--card-radius)] p-6 transition-colors duration-200 hover:border-primary/20"
            >
              <div className="mb-4 flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 text-primary transition-colors group-hover:bg-primary/20">
                <Icon className="h-5 w-5" aria-hidden="true" />
              </div>
              <h2 className="font-heading text-base font-semibold text-foreground">{title}</h2>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{description}</p>
            </article>
          ))}
        </section>

        <section className="mt-24 rounded-2xl border border-border-subtle bg-surface/50 p-8 text-center backdrop-blur-sm sm:p-12">
          <div className="animate-float mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-primary/20 to-accent/20 ring-1 ring-primary/20">
            <MessageSquare className="h-7 w-7 text-primary" aria-hidden="true" />
          </div>
          <h2 className="font-heading text-2xl font-bold text-foreground sm:text-3xl">
            Ready to explore your knowledge base?
          </h2>
          <p className="mx-auto mt-3 max-w-md text-sm text-muted-foreground">
            Jump into the chat, upload a PDF, and start asking questions in seconds.
          </p>
          <Link
            to="/chat"
            className="glow-button mt-8 inline-flex items-center gap-2 rounded-[var(--button-radius)] bg-primary px-8 py-3.5 font-medium text-primary-foreground transition-all duration-200 hover:bg-primary-hover focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            Start chatting
            <ArrowRight className="h-4 w-4" aria-hidden="true" />
          </Link>
        </section>
      </main>

      <footer className="relative z-10 border-t border-border-subtle py-6 text-center text-xs text-muted-foreground">
        RAG Platform — document-grounded AI
      </footer>
    </div>
  )
}
