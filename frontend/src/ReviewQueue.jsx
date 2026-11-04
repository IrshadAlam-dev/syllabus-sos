import React from 'react';
import { AlertCircle, Check, CheckCheck, FileText, X } from 'lucide-react';
import './review.css';

const keyFor = (value='') => value.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();

export default function ReviewQueue({ items, sourceName, existing, onChange, onApprove, onReject, onApproveMatched, onClose }) {
  const matchedCount = items.filter(item => item.evidence_status === 'source_matched' && item.deadline_confidence === 'high').length;
  const findDuplicate = item => existing.findIndex(saved => {
    const left=keyFor(saved.assignment_title);const right=keyFor(item.assignment_title);if(left===right)return true;
    const leftParts=(saved.assignment_title||'').split(' · ');const rightParts=(item.assignment_title||'').split(' · ');
    if(leftParts.length<2||rightParts.length<2||keyFor(leftParts[0])!==keyFor(rightParts[0]))return false;
    const a=new Set(keyFor(leftParts.slice(1).join(' ')).split(' ').filter(Boolean));const b=new Set(keyFor(rightParts.slice(1).join(' ')).split(' ').filter(Boolean));
    const overlap=[...a].filter(token=>b.has(token)).length;return overlap/Math.max(1,new Set([...a,...b]).size)>=.8;
  });

  return <div className="review-backdrop">
    <section className="review-dialog" role="dialog" aria-modal="true" aria-labelledby="review-title">
      <header className="review-header">
        <div><span className="review-kicker">CHECK BEFORE ADDING</span><h2 id="review-title">Review extracted assignments</h2><p>Muse Spark’s results stay in review until you approve them. Check dates against the source.</p></div>
        <button className="review-close" onClick={onClose} aria-label="Close review"><X size={19}/></button>
      </header>
      <div className="review-source"><FileText size={15}/><span>Source document</span><b>{sourceName}</b><span className="review-count">{items.length} to review</span></div>
      {matchedCount > 0 && <button className="review-approve-matched" onClick={onApproveMatched}><CheckCheck size={16}/> Approve {matchedCount} with matched high-confidence deadlines</button>}
      {!items.length ? <div className="review-empty"><Check size={20}/><b>Review complete</b><p>You approved or rejected every extracted assignment.</p><button onClick={onClose}>Return to study plan</button></div> :
        <div className="review-list">{items.map((item,index) => {
          const duplicateIndex = findDuplicate(item);
          const updateExisting = duplicateIndex >= 0;
          const update = (field,value) => onChange(index,{...item,[field]:value});
          const updateDeadline = value => onChange(index,{...item,extracted_deadline:value||null,deadline_source:value?'Entered by you':item.deadline_source,deadline_confidence:value?'high':item.deadline_confidence,evidence_status:value?'student_confirmed':(item.evidence_status==='student_confirmed'?'manual_review':item.evidence_status)});
          return <article className="review-item" key={`${item.assignment_title}-${index}`}>
            <div className="review-item-top"><div><span className={`evidence-chip ${item.evidence_status}`}>
              {item.evidence_status === 'source_matched' ? 'Quote matched in PDF' : item.evidence_status === 'no_deadline' ? 'No deadline found' : 'Manual check required'}
            </span>{item.source_page && <span className="evidence-page">Page {item.source_page}</span>}</div>
              {updateExisting && <span className="duplicate-note"><AlertCircle size={13}/> Similar assignment exists; approval updates it.</span>}
            </div>
            <div className="review-fields">
              <label>Assignment title<input value={item.assignment_title} onChange={event=>update('assignment_title',event.target.value)} /></label>
              <label>Due date<input type="date" value={item.extracted_deadline||''} onChange={event=>updateDeadline(event.target.value)} /></label>
              <label className="review-wide">Description<textarea rows="2" value={item.description} onChange={event=>update('description',event.target.value)} /></label>
              <label>Requirements<textarea rows="3" value={(item.requirements||[]).join('\n')} onChange={event=>update('requirements',event.target.value.split('\n').map(value=>value.trim()).filter(Boolean))} /></label>
              <label>Estimated hours<input type="number" min="0" max="200" step="0.5" value={item.estimated_hours} onChange={event=>update('estimated_hours',Number(event.target.value))} /></label>
            </div>
            <div className="review-evidence">
              <b>Evidence and confidence</b>
              {item.evidence_status === 'student_confirmed' ? <p>You entered or confirmed this date during review.</p> : item.deadline_source ? <blockquote>“{item.deadline_source}”</blockquote> : <p>{item.evidence_status === 'no_deadline' ? 'No deadline was extracted. Confirm in your course portal if needed.' : 'No supporting text quote was matched. Confirm the date in the source document.'}</p>}
              {item.evidence_status === 'manual_review' && <p className="review-warning">This date needs your confirmation; no supporting text match was possible.</p>}
              <small>{item.source_document || sourceName} · {item.deadline_confidence || 'uncertain'} confidence · AI estimates may be inaccurate.</small>
            </div>
            {item.missing_information?.length > 0 && <p className="review-missing"><AlertCircle size={14}/>{item.missing_information.join(' · ')}</p>}
            <div className="review-actions"><button className="review-reject" onClick={()=>onReject(index)}>Reject</button><button className="review-approve" onClick={()=>onApprove(index)}><Check size={15}/>{updateExisting?'Approve and update existing':'Approve assignment'}</button></div>
          </article>;
        })}</div>}
    </section>
  </div>;
}
