// Lightweight loading screen — single static logo + thin progress bar.
// No video, no animated gradients, no media bigger than a few KB.
import loadingLogo from '../../assets/loading-logo.png'
import './Loading.css'

export default function Loading() {
  return (
    <div className="loading-container">
      <div className="loading-content">
        <img src={loadingLogo} alt="Symbolos" className="loading-logo" />
        <div className="loading-bar"><span /></div>
      </div>
    </div>
  )
}
