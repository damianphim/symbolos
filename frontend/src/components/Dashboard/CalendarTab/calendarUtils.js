// ICS export and Google Calendar URL utilities

function toICSDate(dateStr, timeStr) {
  const [y, m, d] = dateStr.split('-')
  if (timeStr) {
    const [h, min] = timeStr.split(':')
    return `${y}${m.padStart(2,'0')}${d.padStart(2,'0')}T${h.padStart(2,'0')}${(min||'00').padStart(2,'0')}00`
  }
  return `${y}${m.padStart(2,'0')}${d.padStart(2,'0')}`
}

function toICSDateUTC(dateStr, timeStr) {
  const local = toICSDate(dateStr, timeStr)
  return timeStr ? local + 'Z' : local
}

function escapeICS(str) {
  return (str || '').replace(/[\\,;]/g, c => '\\' + c).replace(/\n/g, '\\n')
}

export function generateICS(events) {
  const lines = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//Symbolos//McGill Advisor//EN',
    'CALSCALE:GREGORIAN',
    'METHOD:PUBLISH',
    'X-WR-CALNAME:McGill Academic Calendar',
  ]

  events.forEach((ev, i) => {
    const dtstart = toICSDateUTC(ev.date, ev.time)
    const dtend = ev.end_time
      ? toICSDateUTC(ev.date, ev.end_time)
      : ev.time
        ? toICSDateUTC(ev.date, ev.time)
        : dtstart

    lines.push('BEGIN:VEVENT')
    lines.push(`UID:symbolos-${ev.id || i}-${ev.date}@mcgill.symbolos.ca`)
    lines.push(`DTSTAMP:${toICSDateUTC(new Date().toISOString().split('T')[0], new Date().toTimeString().slice(0,5))}`)

    if (ev.time) {
      lines.push(`DTSTART:${dtstart}`)
      if (!ev.end_time) {
        const [h, min] = ev.time.split(':').map(Number)
        const endHour = String(h + 1).padStart(2,'0')
        lines.push(`DTEND:${toICSDateUTC(ev.date, endHour + ':' + String(min).padStart(2,'0'))}`)
      } else {
        lines.push(`DTEND:${toICSDateUTC(ev.date, ev.end_time)}`)
      }
    } else {
      lines.push(`DTSTART;VALUE=DATE:${dtstart}`)
      lines.push(`DTEND;VALUE=DATE:${dtstart}`)
    }

    lines.push(`SUMMARY:${escapeICS(ev.title)}`)
    if (ev.description) lines.push(`DESCRIPTION:${escapeICS(ev.description)}`)
    if (ev.location)    lines.push(`LOCATION:${escapeICS(ev.location)}`)
    if (ev.category)    lines.push(`CATEGORIES:${escapeICS(ev.category)}`)
    lines.push('END:VEVENT')
  })

  lines.push('END:VCALENDAR')
  return lines.join('\r\n')
}

export function downloadICS(events, filename = 'mcgill-calendar.ics') {
  const content = generateICS(events)
  const blob = new Blob([content], { type: 'text/calendar;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = Object.assign(document.createElement('a'), { href: url, download: filename })
  document.body.appendChild(a); a.click(); document.body.removeChild(a); URL.revokeObjectURL(url)
}

export function googleCalendarUrl(event) {
  const fmt = (s) => encodeURIComponent(s || '')
  const dtstart = toICSDate(event.date, event.time)
  let dates
  if (event.time) {
    const [h, min] = event.time.split(':').map(Number)
    const endHour = event.end_time
      ? event.end_time.split(':').map(Number)
      : [h + 1, min]
    const dtend = toICSDate(event.date, endHour[0] + ':' + String(endHour[1] || 0).padStart(2,'0'))
    dates = `${dtstart}/${dtend}`
  } else {
    dates = `${dtstart}/${dtstart}`
  }
  return `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${fmt(event.title)}&dates=${dates}&details=${fmt(event.description)}&location=${fmt(event.location)}`
}
