import './Legal.css'

export default function TermsOfService({ onClose }) {
  return (
    <div className="legal-overlay" onClick={onClose}>
      <div className="legal-modal" onClick={e => e.stopPropagation()}>
        <div className="legal-header">
          <div className="legal-logo">SY</div>
          <div>
            <h1 className="legal-title">Terms of Service</h1>
            <p className="legal-subtitle">Last updated: March 2026</p>
          </div>
          {onClose && (
            <button className="legal-close" onClick={onClose} aria-label="Close">✕</button>
          )}
        </div>

        <div className="legal-body">
          <div className="legal-disclaimer-banner">
            <strong>Not affiliated with McGill University.</strong> Symbolos is an independent student tool. We are not endorsed by, sponsored by, or connected to McGill University in any official capacity.
          </div>

          <section className="legal-section">
            <h2>1. Acceptance of Terms</h2>
            <p>By accessing or using Symbolos ("the Service"), you agree to be bound by these Terms of Service. If you do not agree, do not use the Service. These terms apply to all users of Symbolos.</p>
          </section>

          <section className="legal-section">
            <h2>2. Description of Service</h2>
            <p>Symbolos is an independent academic planning tool that provides AI-powered course recommendations, degree progress tracking, calendar management, and community features for McGill University students. Symbolos is <strong>not affiliated with, endorsed by, or sponsored by McGill University</strong>.</p>
          </section>

          <section className="legal-section">
            <h2>3. Eligibility</h2>
            <p>You must be at least 13 years of age to use Symbolos. By using the Service, you represent that you meet this requirement. The Service is designed for McGill University students, though anyone may register.</p>
          </section>

          <section className="legal-section">
            <h2>4. Account Responsibilities</h2>
            <ul>
              <li>You are responsible for maintaining the confidentiality of your account credentials.</li>
              <li>You are responsible for all activity that occurs under your account.</li>
              <li>You must provide accurate information when registering.</li>
              <li>You must not share your account with others or use another person's account.</li>
              <li>You must notify us immediately of any unauthorized use of your account.</li>
            </ul>
          </section>

          <section className="legal-section">
            <h2>5. Acceptable Use</h2>
            <p>You agree not to use Symbolos to:</p>
            <ul>
              <li>Violate any applicable laws or regulations</li>
              <li>Harass, bully, or harm other users</li>
              <li>Post false, misleading, or defamatory content in the community forum or clubs</li>
              <li>Attempt to gain unauthorized access to our systems or other users' accounts</li>
              <li>Upload malicious files, viruses, or harmful code</li>
              <li>Scrape, crawl, or systematically extract data from the Service</li>
              <li>Impersonate McGill University, its staff, or other users</li>
              <li>Spam or send unsolicited messages to other users</li>
              <li>Use the AI advisor to generate academic work you intend to submit as your own (academic integrity is your responsibility)</li>
            </ul>
          </section>

          <section className="legal-section">
            <h2>6. AI Advisor — Disclaimer &amp; Limitations</h2>
            <div className="legal-warning-box">
              <strong>⚠️ Important:</strong> The AI advisor is for informational and planning purposes only. It is not a substitute for official McGill academic advising.
            </div>
            <ul>
              <li>AI-generated advice may contain errors, outdated information, or inaccuracies.</li>
              <li>Always verify course requirements, prerequisites, and deadlines directly with McGill's official resources (eCalendar, Minerva, your departmental advisor).</li>
              <li>Symbolos is not responsible for academic decisions made based on AI-generated content.</li>
              <li>Course grade data is crowdsourced and may not be accurate or current.</li>
              <li>RateMyProfessors ratings are third-party data and reflect individual opinions.</li>
            </ul>
          </section>

          <section className="legal-section">
            <h2>7. User-Generated Content</h2>
            <p>By posting content on Symbolos (forum posts, club submissions, etc.), you grant us a non-exclusive, royalty-free license to display and distribute that content as part of the Service. You retain ownership of your content.</p>
            <p>You are solely responsible for content you post. We reserve the right to remove any content that violates these Terms or our community guidelines, without notice.</p>
          </section>

          <section className="legal-section">
            <h2>8. Intellectual Property</h2>
            <p>Symbolos, its logo, design, and original content are the intellectual property of the Symbolos developers. McGill University course codes, names, and catalog data are the property of McGill University. Symbolos does not claim ownership of any McGill University content.</p>
          </section>

          <section className="legal-section">
            <h2>9. Disclaimer of Warranties</h2>
            <p>THE SERVICE IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED. WE DO NOT WARRANT THAT THE SERVICE WILL BE UNINTERRUPTED, ERROR-FREE, OR FREE OF HARMFUL COMPONENTS. USE OF THE SERVICE IS AT YOUR OWN RISK.</p>
          </section>

          <section className="legal-section">
            <h2>10. Limitation of Liability</h2>
            <p>TO THE MAXIMUM EXTENT PERMITTED BY LAW, SYMBOLOS AND ITS DEVELOPERS SHALL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES ARISING FROM YOUR USE OF THE SERVICE, INCLUDING BUT NOT LIMITED TO ACADEMIC DECISIONS, COURSE REGISTRATION ERRORS, OR RELIANCE ON AI-GENERATED ADVICE.</p>
            <p>OUR TOTAL LIABILITY TO YOU FOR ANY CLAIM ARISING FROM THE SERVICE SHALL NOT EXCEED $0, AS SYMBOLOS IS PROVIDED FREE OF CHARGE.</p>
          </section>

          <section className="legal-section">
            <h2>11. Termination</h2>
            <p>We reserve the right to suspend or terminate your account at any time, with or without notice, for violations of these Terms. You may delete your account at any time from the Settings tab.</p>
          </section>

          <section className="legal-section">
            <h2>12. Changes to Terms</h2>
            <p>We may update these Terms at any time. Continued use of the Service after changes constitutes acceptance. We will notify users of material changes via email where possible.</p>
          </section>

          <section className="legal-section">
            <h2>13. Governing Law</h2>
            <p>These Terms are governed by the laws of the Province of Quebec and the federal laws of Canada applicable therein, without regard to conflict of law principles.</p>
          </section>

          <section className="legal-section">
            <h2>14. Contact</h2>
            <p>Questions about these Terms? Contact us at: <a href="mailto:legal@symbolos.ca">legal@symbolos.ca</a></p>
          </section>
        </div>
      </div>
    </div>
  )
}