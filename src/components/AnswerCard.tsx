import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import type { Citation, Message } from "../api"

type Answer = Omit<Message, "id">

const SOURCE_LABEL: Record<string, string> = {
  documents: "From your documents",
  web: "From a web search",
  ai_knowledge: "Not in your documents — general AI knowledge",
}

function citationLabel(citation: Citation) {
  if (citation.source_type === "web") return citation.title || citation.url || "Web result"
  const page = citation.page_number ? ` · page ${citation.page_number}` : ""
  return `${citation.document_name}${page} · chunk ${citation.chunk_index}`
}

// The Gemini verify step only runs on answers built from documents or the web.
function Verdict({ answer }: { answer: Answer }) {
  if (answer.source === "ai_knowledge" || answer.source === "none") {
    return <span className="stamp neutral">Not checked — no matching text in your documents</span>
  }
  return answer.grounded ? (
    <span className="stamp ok">✓ Checked by Gemini — supported by the source text</span>
  ) : (
    <span className="stamp warn">⚠ Gemini flagged claims the source text doesn't support</span>
  )
}

export default function AnswerCard({
  answer,
  onFollowUp,
}: {
  answer: Answer
  onFollowUp: (question: string) => void
}) {
  const showConfidence = answer.source !== "ai_knowledge" && answer.confidence > 0

  return (
    <article className="answer">
      <div className="answer-meta">
        <span className="source">{SOURCE_LABEL[answer.source] ?? answer.source}</span>
        {showConfidence && <span className="confidence">Confidence {Math.round(answer.confidence)}%</span>}
      </div>

      <div className="markdown">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{answer.answer}</ReactMarkdown>
      </div>

      <Verdict answer={answer} />

      {answer.citations.length > 0 && (
        <div className="sources">
          <h3>Sources used</h3>
          {answer.citations.map((citation, index) => (
            <details key={index}>
              <summary>{citationLabel(citation)}</summary>
              <p>
                <mark>{citation.text}</mark>
              </p>
              {citation.url && (
                <a href={citation.url} target="_blank" rel="noreferrer">
                  Open page
                </a>
              )}
            </details>
          ))}
        </div>
      )}

      <div className="receipt" aria-label="Steps the RAG pipeline ran">
        <span className="receipt-label">Pipeline</span>
        <ol>
          {answer.trace.map((step, index) => (
            <li key={index}>{step}</li>
          ))}
        </ol>
        {answer.response_time_ms > 0 && (
          <span className="receipt-time">{(answer.response_time_ms / 1000).toFixed(1)} s</span>
        )}
      </div>

      {answer.follow_up_questions.length > 0 && (
        <div className="follow-ups">
          {answer.follow_up_questions.map((question) => (
            <button key={question} className="chip" onClick={() => onFollowUp(question)}>
              {question}
            </button>
          ))}
        </div>
      )}
    </article>
  )
}
