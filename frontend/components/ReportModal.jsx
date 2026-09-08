import React from 'react';
import { marked } from 'marked';

export default function ReportModal({
  isOpen,
  report,
  onClose
}) {
  if (!isOpen || !report) return null;

  const handleDownload = () => {
    if (!report?.markdown) return;
    const blob = new Blob([report.markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const safeTitle = (report.title || 'investigation-report')
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-');
    a.download = `${safeTitle}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const htmlContent = report.markdown ? marked.parse(report.markdown) : '';

  return (
    <div className="modal-overlay" id="reportModal" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3 id="reportModalTitle">{report.title || "Investigation Report Preview"}</h3>
          <button className="modal-close-btn" onClick={onClose} type="button">
            &times;
          </button>
        </div>

        <div
          className="modal-body"
          id="reportModalBody"
          dangerouslySetInnerHTML={{ __html: htmlContent }}
        />

        <div className="modal-footer">
          <button className="btn-outline" onClick={handleDownload} type="button">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" style={{ width: 13, height: 13 }}>
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="7 10 12 15 17 10" />
              <line x1="12" y1="15" x2="12" y2="3" />
            </svg>
            Download Markdown
          </button>
          <button className="btn-send" onClick={onClose} type="button" style={{ transform: 'none' }}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
