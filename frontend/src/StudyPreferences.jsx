import React from 'react';
import { Clock3, Settings2 } from 'lucide-react';

const days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];

export default function StudyPreferences({ value, onChange }) {
  const set = patch => onChange({...value,...patch});
  const toggleDay = day => {
    const next=value.studyDays.includes(day)?value.studyDays.filter(item=>item!==day):[...value.studyDays,day].sort((a,b)=>a-b);
    if(next.length)set({studyDays:next});
  };
  return <section className="panel preferences-panel"><div className="panel-head compact"><div><h2><Settings2 size={16}/> Study preferences</h2><p>Shape your suggested weekly workload.</p></div></div>
    <label className="preference-hours"><span>Daily study capacity</span><span><input type="number" min="0.5" max="16" step="0.5" value={value.hoursPerDay} onChange={event=>set({hoursPerDay:Math.min(16,Math.max(.5,Number(event.target.value)||.5))})}/> hours</span></label>
    <div className="preference-label">Preferred study days</div><div className="preference-days">{days.map((day,index)=><button type="button" aria-pressed={value.studyDays.includes(index+1)} className={value.studyDays.includes(index+1)?'chosen':''} key={day} onClick={()=>toggleDay(index+1)}>{day}</button>)}</div>
    <label className="preference-hours"><span><Clock3 size={14}/> Preferred focus block</span><select value={value.focusMinutes} onChange={event=>set({focusMinutes:Number(event.target.value)})}><option value={25}>25 minutes</option><option value={45}>45 minutes</option><option value={60}>60 minutes</option><option value={90}>90 minutes</option></select></label>
    <small className="preference-note">Saved in this browser. Time estimates are suggestions.</small>
  </section>;
}
