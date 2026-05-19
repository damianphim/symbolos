// Lightweight loading screen — pure CSS, no video.
// The previous version loaded a 25 MB MP4 every visit; this renders instantly
// and keeps the bundle ~25 MB smaller.
import './Loading.css'

export default function Loading() {
  return (
    <div className="loading-container">
      <div className="loading-gradient" />
      <div className="loading-content">
        <div className="loading-mark">S</div>
        <p className="loading-message">Symbolos</p>
        <div className="loading-bar"><span /></div>
      </div>
    </div>
  )
}
