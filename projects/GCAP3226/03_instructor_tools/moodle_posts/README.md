# Moodle post HTML guidelines

Goal: Make forum posts readable on projectors and resilient against Moodle theme CSS.

Recommended structure
- Wrap everything in a single outer <div> with inline styles controlling width, fonts, and spacing. Example:
  <div style="width: 100%; max-width: 1200px; margin: 0 auto; font-family: Arial, sans-serif; font-size: 18px; line-height: 1.6;">
    ...content...
  </div>

Typography
- Use a base font-size on the wrapper (18px is a good classroom default); rely on rem for component sizing so they scale together.
- Prefer relative units for headings and subtext:
  - h1: 2.5rem
  - h2: 1.8rem
  - h3: 1.6–1.8rem
  - body text: 1rem (inherited from wrapper’s 18px)
- Increase line-height to ~1.5–1.7 for readability at distance.

Layout and width
- Set width: 100% and a max-width (e.g., 1200px). If Moodle still constrains it, try max-width: none; and width: 100% !important on the wrapper (use sparingly).
- Tables should use width: 100%; border-collapse: collapse; and font-size: 1rem to inherit base size.

Spacing
- Use padding on section containers (20–30px) and margin-bottom spacing (20–30px) for separation.

Colors and emphasis
- Use high-contrast text and background colors for projector visibility.
- Avoid relying on light tints for text; keep important text at or near #333 or darker.

Images and links
- Ensure images are responsive: max-width: 100%; height: auto.
- Style CTA links with clear contrast and sufficient padding.

Moodle quirks
- Moodle can override external styles; inline styles are most reliable for forum posts.
- Avoid <style> blocks or external CSS — many Moodle forums strip them.
- Use !important only when absolutely necessary to override theme rules.

Copy/paste checklist
- One outer wrapper with width, max-width, font, font-size, line-height.
- Headings and table font-sizes use rem to scale with base.
- Section blocks use adequate padding and margin.
- Tables span full width, readable at distance.

Example wrapper (copy/paste)
<div style="width: 100%; max-width: 1200px; margin: 0 auto; font-family: Arial, sans-serif; font-size: 18px; line-height: 1.6;">
  <!-- content here -->
</div>
