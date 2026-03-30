import { FaTimes } from 'react-icons/fa'
import './Legal.css'

export default function PrivacyPolicy({ onClose }) {
  return (
    <div className="legal-overlay" onClick={onClose}>
      <div className="legal-modal" onClick={e => e.stopPropagation()}>
        <div className="legal-header">
          <div className="legal-logo">SY</div>
          <div>
            <h1 className="legal-title">Privacy Policy</h1>
            <p className="legal-subtitle">Last updated: March 2026</p>
          </div>
          {onClose && (
            <button className="legal-close" onClick={onClose} aria-label="Close">
              <FaTimes />
            </button>
          )}
        </div>
        <div className="legal-body">
          <div className="legal-disclaimer-banner">
            <strong>Not affiliated with McGill University.</strong> Symbolos is an independent student tool. We are not endorsed by, sponsored by, or connected to McGill University in any official capacity.
          </div>
          <section className="legal-section">
            <h2>1. Who We Are</h2>
            <p>Symbolos ("we", "our", "us") is an independent academic planning tool built for McGill University students. We are a student-run project and are not affiliated with, endorsed by, or sponsored by McGill University.</p>
          </section>
          <section className="legal-section">
            <h2>2. Information We Collect</h2>
            <h3>Account Information</h3>
            <p>When you register, we collect your email address, username, and password (stored securely via Supabase Auth). You may also voluntarily provide your faculty, major, year of study, GPA, and academic interests to personalize your experience.</p>
            <h3>Academic Data</h3>
            <p>If you use our degree planning features, you may upload your unofficial McGill transcript or course syllabuses. This data is processed to populate your course history and calendar. We do not share this data with McGill or any third party.</p>
            <h3>Usage Data</h3>
            <p>We collect standard server logs (IP addresses, browser type, pages visited, timestamps) to maintain and improve the service. We do not sell this data.</p>
            <h3>AI Conversations</h3>
            <p>Messages you send to our AI advisor are processed by Anthropic's Claude API. Please review <a href="https://www.anthropic.com/privacy" target="_blank" rel="noopener noreferrer">Anthropic's Privacy Policy</a> for details on how they handle API data. We do not permanently store your individual chat messages beyond your session history in our database.</p>
          </section>
          <section className="legal-section">
            <h2>3. How We Use Your Information</h2>
            <ul>
              <li>To provide personalized academic advice and course recommendations</li>
              <li>To track your degree progress and completed courses</li>
              <li>To send calendar reminders and notifications you have opted into</li>
              <li>To improve the platform and fix bugs</li>
              <li>To prevent abuse and enforce our Terms of Service</li>
            </ul>
            <p>We do not sell, rent, or trade your personal information to third parties for marketing purposes.</p>
          </section>
          <section className="legal-section">
            <h2>4. Third-Party Services</h2>
            <p>We use the following third-party services to operate Symbolos:</p>
            <ul>
              <li><strong>Supabase</strong> — Database and authentication (data stored in Canada/US)</li>
              <li><strong>Anthropic Claude API</strong> — AI-powered chat and advisor cards</li>
              <li><strong>Resend</strong> — Transactional email delivery (verification, notifications)</li>
              <li><strong>Vercel</strong> — Hosting and serverless functions</li>
              <li><strong>Twilio</strong> — Optional SMS notifications (only if you provide a phone number)</li>
            </ul>
            <p>Each of these services has its own privacy policy governing how they handle data.</p>
          </section>
          <section className="legal-section">
            <h2>5. Data Retention &amp; Deletion</h2>
            <p>Your account and all associated data (courses, grades, calendar events, preferences) are retained for as long as your account is active. You may delete your account at any time from the Settings tab, which will permanently remove all your data from our systems within 30 days.</p>
            <p>You may also export all your data as a JSON file from the Settings tab before deleting your account.</p>
          </section>
          <section className="legal-section">
            <h2>6. Security</h2>
            <p>We implement industry-standard security measures including HTTPS encryption, JWT-based authentication, database row-level security (RLS) via Supabase, and rate limiting. However, no system is perfectly secure. Please use a strong, unique password and do not share your credentials.</p>
          </section>
          <section className="legal-section">
            <h2>7. Children's Privacy</h2>
            <p>Symbolos is intended for university students (18+). We do not knowingly collect data from anyone under the age of 13. If you believe we have inadvertently collected such information, please contact us immediately.</p>
          </section>
          <section className="legal-section">
            <h2>8. Your Rights</h2>
            <p>Depending on your jurisdiction, you may have rights to access, correct, or delete your personal data. To exercise these rights, please contact us at the email below. We will respond within 30 days.</p>
          </section>
          <section className="legal-section">
            <h2>9. Changes to This Policy</h2>
            <p>We may update this Privacy Policy from time to time. We will notify registered users of material changes via email. Continued use of Symbolos after changes constitutes your acceptance of the updated policy.</p>
          </section>
          <section className="legal-section">
            <h2>10. Contact</h2>
            <p>Questions about this Privacy Policy? Reach us at: <a href="mailto:symbolosadvsry@gmail.com">symbolosadvsry@gmail.com</a></p>
          </section>
        </div>
      </div>
    </div>
  )
}
