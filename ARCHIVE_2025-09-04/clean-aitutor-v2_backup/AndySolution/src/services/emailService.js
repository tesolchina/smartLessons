import { config } from './config.js';

// Placeholder for future EmailJS integration
// Keep API simple for later wiring without UI changes

export function isEmailConfigured() {
  return config.isEmailEnabled();
}

export async function sendReportEmail({ to, subject, html, text, cc }) {
  if (!isEmailConfigured()) {
    console.warn('[emailService] Not configured. Skipping email send.');
    return { success: false, error: 'NOT_CONFIGURED' };
  }
  // Stub: we will wire EmailJS later using keys from config.getEmailJsConfig()
  return { success: false, error: 'NOT_IMPLEMENTED' };
}

