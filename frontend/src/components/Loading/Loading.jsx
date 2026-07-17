// Lightweight loading screen — single static logo with a pulse of light
// travelling through the red/green sigma. No video, no heavy media.
import loadingLogo from '../../assets/loading-logo.png'
import './Loading.css'

export default function Loading() {
  return (
    <div className="loading-container">
      <div className="loading-content">
        <div className="loading-logo-wrap">
          <img src={loadingLogo} alt="Symbolos" className="loading-logo" />
          <div className="loading-pulse" aria-hidden="true" />
        </div>
      </div>
    </div>
  )
}
