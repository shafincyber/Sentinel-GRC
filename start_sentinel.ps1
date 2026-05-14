# ==============================================================================
# S E N T I N E L   G R C   v2.0 - Master Boot Sequence
# ==============================================================================

$Host.UI.RawUI.WindowTitle = "SENTINEL-V2: Master Control"
Clear-Host

Write-Host "INITIALIZING SENTINEL-V2 ORCHESTRATION..." -ForegroundColor Green

# 1. Boot Infrastructure
Write-Host "[*] Booting Docker Infrastructure (Kafka, Zookeeper, Neo4j)..." -ForegroundColor Cyan
docker compose up -d

# 2. Wait for Broker and Graph Database
Write-Host "[*] Synchronizing container states (30 seconds)..." -ForegroundColor DarkYellow
Start-Sleep -Seconds 30
Write-Host "[+] Infrastructure Online." -ForegroundColor Green

# 3. Launch API Gateway (Producer)
Write-Host "[*] Spawning API Gateway (Producer)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& { `$Host.UI.RawUI.WindowTitle = 'Sentinel API Gateway'; color 0A; clear; .\venv\Scripts\Activate.ps1; python src/orchestrator/main.py }"

# 4. Launch Kafka Worker (Consumer)
Write-Host "[*] Spawning Kafka Worker (Consumer)..." -ForegroundColor Magenta
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& { `$Host.UI.RawUI.WindowTitle = 'Sentinel Kafka Worker'; color 0D; clear; .\venv\Scripts\Activate.ps1; python src/orchestrator/worker.py }"

Write-Host "==================================================" -ForegroundColor Green
Write-Host "SYSTEM ONLINE. AWAITING CI/CD WEBHOOKS." -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
