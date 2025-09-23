param(
    [string]$ReviewTo = 'taliawu17@hkbu.edu.hk',
    [string]$ReminderTo = 'simonwang@hkbu.edu.hk',
    [string]$HtmlPath = 'C:\usage\VibeCoding\DailyAssistant\projects\GCAP3226\MoodlePost\projectTimelineInstructions.html',
    [string]$MoodleUrl = 'https://buelearning.hkbu.edu.hk/mod/forum/discuss.php?d=332411#p519835',
    [datetime]$ReminderTime,
    [string]$CcReviewTo = 'simonwang@hkbu.edu.hk',
    [string]$FromAccount,
    [switch]$ResendWithCc,
    [switch]$Preview,
    [switch]$SkipReview,
    [switch]$SkipReminder
)

function Get-TonightDefaultTime {
    param([int]$Hour = 21, [int]$Minute = 0)
    $now = Get-Date
    $todayTarget = Get-Date -Hour $Hour -Minute $Minute -Second 0
    if ($now -lt $todayTarget) { return $todayTarget }
    # If we're past the target, schedule for next day same time.
    return ($todayTarget).AddDays(1)
}

try {
    $outlook = [Runtime.InteropServices.Marshal]::GetActiveObject('Outlook.Application')
} catch {
    $outlook = New-Object -ComObject Outlook.Application
}

if (-not $outlook) {
    Write-Error 'Outlook is not available on this machine. Please ensure Microsoft Outlook is installed.'
    exit 1
}

function Get-DefaultAccountSmtp {
    try {
        $sess = $outlook.Session
        # Try CurrentUser first
        $ae = $sess.CurrentUser.AddressEntry
        if ($ae -and $ae.Type -eq 'EX') {
            $ex = $ae.GetExchangeUser()
            if ($ex -and $ex.PrimarySmtpAddress) { return $ex.PrimarySmtpAddress }
        }
        # Fallback: any account with SmtpAddress
        foreach ($acct in $sess.Accounts) {
            if ($acct.SmtpAddress) { return $acct.SmtpAddress }
        }
    } catch {}
    return $null
}

function Show-ItemSafely {
    param(
        [Parameter(Mandatory=$true)]$Item,
        [int]$Retry = 1
    )
    try {
        # Save first to ensure it exists in Drafts, then display
        $Item.Save() | Out-Null
        Start-Sleep -Milliseconds 200
        $Item.Display($true) | Out-Null
        return $true
    } catch {
        if ($Retry -gt 0) {
            Start-Sleep -Milliseconds 400
            return (Show-ItemSafely -Item $Item -Retry ($Retry - 1))
        }
        try { $Item.Save() | Out-Null } catch {}
        return $false
    }
}

if (-not $PSBoundParameters.ContainsKey('ReminderTime') -or -not $ReminderTime) {
    $ReminderTime = Get-TonightDefaultTime -Hour 21 -Minute 0
}

# Build the HTML bodies
$reviewSubject = 'Review request: GCAP3226 Moodle forum post (Project Timeline)'
if ($ResendWithCc) { $reviewSubject += ' (CC added)' }
$reviewBody = @"
<div style='font-family: Arial, sans-serif; font-size: 14px;'>
  <p>Hi Talia,</p>
  <p>Could you please review the draft Moodle forum post for GCAP3226?</p>
  <p>Preview link: <a href='$MoodleUrl'>$MoodleUrl</a></p>
  <p>I've attached the HTML version of the content we intend to post.</p>
  <p>Thanks!<br/>Simon</p>
</div>
"@

$reminderSubject = 'Reminder: Finalize and post GCAP3226 timeline to Moodle tonight'
$reminderBody = @"
<div style='font-family: Arial, sans-serif; font-size: 14px;'>
  <p>Hi Simon,</p>
  <p>This is your reminder to finalize the GCAP3226 project timeline post and move it to the forum for student access.</p>
  <ul>
    <li>Review Talia's feedback (if any)</li>
    <li>Finalize the content</li>
    <li>Post to the Moodle forum</li>
  </ul>
  <p>Forum thread: <a href='$MoodleUrl'>$MoodleUrl</a></p>
  <p>— Automated reminder</p>
</div>
"@

# Helper to optionally select sending account
function Set-SendUsingAccountIfProvided {
    param($mailItem)
    if ($FromAccount) {
        try {
            $acct = $null
            foreach ($a in $outlook.Session.Accounts) {
                if (($a.SmtpAddress -and $a.SmtpAddress -ieq $FromAccount) -or ($a.DisplayName -ieq $FromAccount)) { $acct = $a; break }
            }
            if ($acct) { $mailItem.SendUsingAccount = $acct }
        } catch {}
    }
}

if (-not $SkipReview) {
    # Send review email now (or preview)
    try {
        $mail = $outlook.CreateItem(0)
        $mail.To = $ReviewTo
        $mail.Subject = $reviewSubject
        $mail.HTMLBody = $reviewBody
        if ($CcReviewTo) { $mail.CC = $CcReviewTo }
        if (Test-Path -LiteralPath $HtmlPath) {
            $null = $mail.Attachments.Add($HtmlPath)
        } else {
            Write-Warning "HTML file not found at: $HtmlPath (email will send without attachment)"
        }
        $mail.Importance = 2  # High
        Set-SendUsingAccountIfProvided -mailItem $mail
        if ($Preview) {
            if (Show-ItemSafely -Item $mail) {
                Write-Output "Review email draft opened (To: $ReviewTo; CC: $CcReviewTo)."
            } else {
                Write-Warning "Review draft saved to Drafts (could not display)."
            }
        } else {
            $mail.Send()
            $used = $null
            try { if ($mail.SendUsingAccount -and $mail.SendUsingAccount.SmtpAddress) { $used = $mail.SendUsingAccount.SmtpAddress } } catch {}
            if (-not $used) { $used = Get-DefaultAccountSmtp }
            if ($used) { Write-Output "Review email sent to $ReviewTo (cc: $CcReviewTo) via $used." } else { Write-Output "Review email sent to $ReviewTo (cc: $CcReviewTo)." }
        }
    } catch {
        Write-Error "Failed to send review email: $($_.Exception.Message)"
    }
}

if (-not $SkipReminder) {
    # Schedule reminder email for tonight (or open draft)
    try {
        $reminder = $outlook.CreateItem(0)
        $reminder.To = $ReminderTo
        $reminder.Subject = $reminderSubject
        $reminder.HTMLBody = $reminderBody
        $reminder.Importance = 2  # High
        $reminder.DeferredDeliveryTime = $ReminderTime
        Set-SendUsingAccountIfProvided -mailItem $reminder
        if ($Preview) {
            if (Show-ItemSafely -Item $reminder) {
                Write-Output ("Reminder draft opened (scheduled {0})." -f $ReminderTime.ToString('yyyy-MM-dd HH:mm'))
            } else {
                Write-Warning "Reminder draft saved to Drafts (could not display)."
            }
        } else {
            $reminder.Send()
            Write-Output ("Reminder queued to send at {0}" -f $ReminderTime.ToString('yyyy-MM-dd HH:mm'))
        }
    } catch {
        Write-Error "Failed to queue reminder email: $($_.Exception.Message)"
    }
}
