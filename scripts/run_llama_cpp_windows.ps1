[CmdletBinding(PositionalBinding = $false)]
param(
    [string]$Model = "models\Qwen2.5-0.5B-Instruct-Q4_K_M.gguf",
    [string]$Prompt = "",
    [int]$Threads = 8,
    [int]$Context = 512,
    [int]$Predict = 80,
    [switch]$Chat,
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
$SystemPrompt = "You are the Lightweight LLM public-good assistant running local GGUF model file '$Model'. Answer concisely in Chinese."

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
    "--chat-template", "chatml",
    "-n", $Predict,
    "-c", $Context,
    "-t", $Threads,
    "-ngl", "0",
    "--temp", "0.2",
    "--no-display-prompt",
    "--no-mmap",
    "--no-kv-offload"
)

if ($Prompt) {
    $llamaArgs += @("-p", $Prompt)
}

if (-not $Chat) {
    $llamaArgs += "-st"
}

& $llamaCli @llamaArgs
