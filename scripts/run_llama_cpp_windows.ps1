[CmdletBinding(PositionalBinding = $false)]
param(
    [string]$Model = "models\DeepSeek-R1-Distill-Qwen-1.5B-Q4_K_M.gguf",
    [string]$Prompt = "",
    [int]$Threads = 8,
    [int]$Context = 512,
    [int]$Predict = 320,
    [switch]$Chat,
    [switch]$RawOutput,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Question
)

$ErrorActionPreference = "Stop"

function Decode-Utf8Base64([string]$Value) {
    return [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($Value))
}

if ($Question.Count -gt 0) {
    $Prompt = $Question -join " "
}

if ((-not $Prompt) -and (-not $Chat)) {
    $Prompt = Decode-Utf8Base64 "6K+355So5Lik5Y+l6K+d5LuL57uN6L276YeP5aSn5qih5Z6L6L+Z5Liq5YWs55uK6aG555uu44CC"
}
$SystemPrompt = "You are the Lightweight LLM public-good assistant running local GGUF model file '$Model'. Answer concisely in Chinese. Do not reveal private chain-of-thought; give a short answer or brief reasoning summary."

$llamaCli = Get-Command llama-cli -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty Source
if (-not $llamaCli) {
    $llamaCli = Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Recurse -Filter llama-cli.exe -ErrorAction SilentlyContinue |
        Select-Object -First 1 -ExpandProperty FullName
}

if (-not $llamaCli) {
    throw "llama-cli.exe not found. Install it with: winget install --id ggml.llamacpp -e --source winget"
}

if (-not (Test-Path -LiteralPath $Model)) {
    throw "Model file not found: $Model"
}

$llamaArgs = @(
    "-m", $Model,
    "-sys", $SystemPrompt,
    "-cnv",
    "-n", $Predict,
    "-c", $Context,
    "-t", $Threads,
    "-ngl", "0",
    "--temp", "0.2",
    "--no-display-prompt",
    "--no-mmap",
    "--no-kv-offload",
    "--reasoning-format", "deepseek",
    "--reasoning", "off",
    "--reasoning-budget", "0"
)

if ($Prompt) {
    $llamaArgs += @("-p", $Prompt)
}

if (-not $Chat) {
    $llamaArgs += "-st"
}

if ($Chat -or $RawOutput) {
    & $llamaCli @llamaArgs
    exit $LASTEXITCODE
}

$output = & $llamaCli @llamaArgs 2>&1
$exitCode = $LASTEXITCODE
$lines = @($output | ForEach-Object { "$_" })

function First-LineIndex([string[]]$Lines, [string]$Pattern, [int]$StartAt = 0) {
    for ($i = $StartAt; $i -lt $Lines.Count; $i++) {
        if ($Lines[$i] -match $Pattern) {
            return $i
        }
    }
    return -1
}

$answerStart = First-LineIndex $lines '^\[End thinking\]' 0
if ($answerStart -ge 0) {
    $answerStart += 1
} else {
    $thinkingStart = First-LineIndex $lines '^\[Start thinking\]' 0
    if ($thinkingStart -ge 0) {
        Write-Output (Decode-Utf8Base64 "5qih5Z6L6L+Y5Zyo5oCd6ICD6Zi25q615bCx6KKr5oiq5pat5LqG44CC6K+35oqKIC1QcmVkaWN0IOiwg+Wkp++8jOS+i+Wmgu+8mi1QcmVkaWN0IDQwMA==")
        exit $exitCode
    }
    $promptLine = First-LineIndex $lines '^> ' 0
    $answerStart = if ($promptLine -ge 0) { $promptLine + 1 } else { 0 }
}

$answerEnd = First-LineIndex $lines '^\[ Prompt:' $answerStart
if ($answerEnd -lt 0) {
    $answerEnd = First-LineIndex $lines '^Exiting\.\.\.' $answerStart
}
if ($answerEnd -lt 0) {
    $answerEnd = $lines.Count
}

$answer = @()
for ($i = $answerStart; $i -lt $answerEnd; $i++) {
    $line = $lines[$i]
    if ($line -match '^\[Start thinking\]') { continue }
    if ($line -match '^\[End thinking\]') { continue }
    $answer += $line
}

$text = ($answer -join [Environment]::NewLine).Trim()
if ($text) {
    Write-Output $text
} else {
    $lines | ForEach-Object { Write-Output $_ }
}

exit $exitCode
