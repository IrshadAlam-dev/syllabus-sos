import React from 'react';
import { AlertTriangle, CalendarDays } from 'lucide-react';
import './review.css';

const iso = date => `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;

export default function WeeklyWorkload({ days, schedule, capacity, selectedDate, onSelect }) {
  return <section className="panel workload-panel"><div className="panel-head compact"><div><h2><CalendarDays size={16}/> Workload this week</h2><p>Suggested blocks based on your capacity and due dates.</p></div></div>
    <div className="workload-days">{days.map(day=>{
      const key=iso(day);const items=schedule.filter(item=>item.date===key);const hours=items.reduce((sum,item)=>sum+item.hours,0);const overloaded=hours>capacity;
      return <button type="button" className={`workload-day ${selectedDate===key?'selected':''}`} key={key} onClick={()=>onSelect(day)}>
        <span className="workload-day-name">{day.toLocaleDateString('en-US',{weekday:'short'})} <b>{day.getDate()}</b></span>
        <span className="workload-meter"><i className={overloaded?'overloaded':''} style={{width:`${Math.min(100,hours/capacity*100)}%`}}/></span>
        <span className="workload-hours">{hours.toFixed(1)}h{overloaded&&<AlertTriangle size={12}/>}</span>
      </button>;
    })}</div>
    <div className="workload-tasks">{schedule.filter(item=>item.date===selectedDate).map((item,index)=><div key={`${item.title}-${index}`}><span/><b>{item.title}</b><small>{item.course} · {item.hours.toFixed(1)}h</small></div>)}
      {!schedule.some(item=>item.date===selectedDate)&&<p>No study blocks suggested for this day.</p>}
    </div>
    <small className="workload-foot">Estimates are approximate. Over-capacity days are highlighted; move or edit tasks to fit your week.</small>
  </section>;
}
