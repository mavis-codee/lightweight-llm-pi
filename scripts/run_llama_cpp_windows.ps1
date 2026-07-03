param(
    [string]$Model = "models\Qwen2.5-0.5B-Instruct-Q4_K_M.gguf",
    [string]$Prompt = "",
    [int]$Threads = 8,
    [int]$Context = 512,
    [int]$Predict = 80
)

$ErrorActionPreference = "Stop"

function Decode-Utf8Base64([string]$Value) {
    return [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($Value))
}

if (-not $Prompt) {
    $Prompt = Decode-Utf8Base64 "6K+355So5Lik5Y+l6K+d5LuL57uN6L276YeP5aSn5qih5Z6L6L+Z5Liq5YWs55uK6aG555uu44CC"
}
$SystemPrompt = Decode-Utf8Base64 "5L2g5piv6L276YeP5aSn5qih5Z6L5YWs55uK5Yqp5omL77yM6K+355So566A5rSB5Lit5paH5Zue562U44CC"

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

& $llamaCli `
    -m $Model `
    -p $Prompt `
    -sys $SystemPrompt `
    -st `
    -cnv `
    --chat-template chatml `
    -n $Predict `
    -c $Context `
    -t $Threads `
    -ngl 0 `
    --temp 0.2 `
    --no-display-prompt `
    --no-mmap `
    --no-kv-offload
