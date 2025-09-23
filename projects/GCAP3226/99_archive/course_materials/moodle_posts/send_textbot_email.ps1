param(
  [string]$To = 'nancyguo@hkbu.edu.hk',
  [string]$Cc = 'zhang_kt@hkbu.edu.hk',
  [string]$Link = 'https://textbot.hkbu.tech/chat/ParaphrasingTeacher',
  [string]$FromAccount,
  [switch]$Preview
)

try { $outlook = [Runtime.InteropServices.Marshal]::GetActiveObject('Outlook.Application') } catch { $outlook = New-Object -ComObject Outlook.Application }
if (-not $outlook) { Write-Error 'Outlook is not available.'; exit 1 }

function Set-SendUsingAccountIfProvided { param($mailItem) if ($FromAccount) { try { foreach ($a in $outlook.Session.Accounts) { if (($a.SmtpAddress -and $a.SmtpAddress -ieq $FromAccount) -or ($a.DisplayName -ieq $FromAccount)) { $mailItem.SendUsingAccount = $a; break } } } catch {} } }

$subject = 'TextBot (ParaphrasingTeacher) ready for testing'
$body = @"
<div style='font-family: Arial, sans-serif; font-size: 14px;'>
  <p>Hi Nancy,</p>
  <p>The chatbot is ready for testing:</p>
  <p><a href='$Link'>$Link</a></p>
  <p>I’ll try to set up an info page. If not, we can ask students to try it directly.</p>
  <p>Please try a bit first, especially:</p>
  <ul>
    <li>Reviewing chat history</li>
    <li>Generating reports</li>
  </ul>
  <p>Thanks!<br/>Simon</p>
</div>
"@

try {
  $mail = $outlook.CreateItem(0)
  $mail.To = $To
  $mail.CC = $Cc
  $mail.Subject = $subject
  $mail.HTMLBody = $body
  Set-SendUsingAccountIfProvided -mailItem $mail
  if ($Preview) { $mail.Display($true) | Out-Null; Write-Output 'TextBot email draft opened.' } else { $mail.Send(); Write-Output 'TextBot email sent.' }
} catch { Write-Error "Failed to prepare/send email: $($_.Exception.Message)" }
