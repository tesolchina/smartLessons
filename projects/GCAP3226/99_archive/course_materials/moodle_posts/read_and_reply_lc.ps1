param(
  [string]$SubjectContains = 'LC website content update',
  [int]$ScanCount = 200,
  [switch]$Preview,
  [switch]$DryRun,
  [string]$FromAccount
)

function Connect-Outlook {
  try { return [Runtime.InteropServices.Marshal]::GetActiveObject('Outlook.Application') } catch { return (New-Object -ComObject Outlook.Application) }
}

function Get-AccountByMatch($app, $match) {
  if (-not $match) { return $null }
  try {
    foreach ($a in $app.Session.Accounts) {
      if (($a.SmtpAddress -and $a.SmtpAddress -ieq $match) -or ($a.DisplayName -ieq $match)) { return $a }
    }
  } catch {}
  return $null
}

function Get-SenderPrimarySmtp($mail) {
  try {
    if ($mail.SenderEmailAddress -and $mail.SenderEmailType -ne 'EX') { return $mail.SenderEmailAddress }
    $ae = $mail.Sender
    if ($ae -and $null -ne $ae.AddressEntryUserType) {
      $ex = $ae.GetExchangeUser()
      if ($ex -and $ex.PrimarySmtpAddress) { return $ex.PrimarySmtpAddress }
    }
  } catch {}
  return $mail.SenderEmailAddress
}

function Find-LatestMessage($app, $subjectLike, $scan) {
  $session = $app.Session
  $folders = @(
    $session.GetDefaultFolder(6),  # Inbox
    $session.GetDefaultFolder(5)   # Sent Mail
  )
  foreach ($f in $folders) {
    try {
      $items = $f.Items
      try { $items.Sort('[ReceivedTime]', $true) } catch { try { $items.Sort('[ReceivedTime]') } catch {} }
      $count = 0
      foreach ($it in $items) {
        if ($null -eq $it) { continue }
        if ($it.MessageClass -notlike 'IPM.Note*') { continue }
        if ($it.Subject -and ($it.Subject -like ("*{0}*" -f $subjectLike))) {
          return $it
        }
        $count++
        if ($count -ge $scan) { break }
      }
    } catch {}
  }
  return $null
}

function New-ReplyHtml($origMail) {
  $senderName = $origMail.SenderName
  if (-not $senderName) { $senderName = 'there' }
  $greetName = $senderName.Split(' ')[0]
  $html = @"
<div style='font-family: Arial, sans-serif; font-size: 14px; line-height: 1.5;'>
  <p>Hi $greetName,</p>
  <p>Thanks for the information.</p>
  <p>We're looking to <strong>automate the process of updating certain LC webpages</strong> to reduce manual effort and keep content consistently up to date. Could you advise how pricing typically works for this type of work?</p>
  <ul>
    <li>Is the fee a <strong>one-off implementation</strong>, or is there also a <strong>recurrent/maintenance</strong> component?</li>
    <li>If recurrent, what does it cover (e.g., monitoring for CMS changes, small fixes, security updates), and what's the usual cadence (monthly/annual)?</li>
    <li>Could you share a <strong>ballpark estimate</strong> for the initial setup and any ongoing maintenance?</li>
  </ul>
  <p>For context, we're initially thinking a small set of pages (e.g., 3-5) pulling from structured data (API/CSV/RSS), with updates daily or weekly. We can provide data endpoints and arrange staging before changes go live.</p>
  <p>Happy to jump on a quick call if easier.</p>
  <p>Best regards,<br/>Simon</p>
</div>
"@
  return $html
}

# Main
$outlook = Connect-Outlook
if (-not $outlook) { Write-Error 'Outlook is not available.'; exit 1 }

$msg = Find-LatestMessage -app $outlook -subjectLike $SubjectContains -scan $ScanCount
if (-not $msg) {
  Write-Error "No email found with subject containing: $SubjectContains"
  exit 2
}

# Print a short summary of the found email
$fromSmtp = Get-SenderPrimarySmtp $msg
Write-Output ("Found email: '{0}' from {1} <{2}> at {3}" -f $msg.Subject, $msg.SenderName, $fromSmtp, $msg.ReceivedTime)

# Show first ~20 lines of body (plain text) for quick context
try {
  $lines = ($msg.Body -split "\r?\n") | Where-Object { $_ -ne '' } | Select-Object -First 20
  Write-Output '--- Context preview (first lines) ---'
  $lines | ForEach-Object { Write-Output $_ }
  Write-Output '--- end preview ---'
} catch {}

if ($DryRun) { exit 0 }

# Create a Reply All draft with our message on top
$reply = $msg.ReplyAll()
$bodyTop = New-ReplyHtml -origMail $msg
# Ensure our content is inserted above original thread
$reply.HTMLBody = $bodyTop + '<br/>' + $reply.HTMLBody

# Optionally set From account for the draft
if ($FromAccount) {
  $acct = Get-AccountByMatch -app $outlook -match $FromAccount
  if ($acct) { try { $reply.SendUsingAccount = $acct } catch {} }
}

# Display draft for manual review and sending
$reply.Display($true) | Out-Null
Write-Output 'Reply draft opened in Outlook.'
