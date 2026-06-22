Write-Host ""
Write-Host "Building CareerLedger stack without cache..." -ForegroundColor Cyan

docker compose build --no-cache

if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker build failed." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Starting all services from docker-compose.yml..." -ForegroundColor Cyan

docker compose up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker compose up failed." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Checking PostgreSQL container..." -ForegroundColor Yellow

$postgresRunning = docker inspect -f "{{.State.Running}}" careerledger-postgres 2>$null

if ($postgresRunning -ne "true") {
    Write-Host "careerledger-postgres is not running." -ForegroundColor Red
    docker ps -a
    exit 1
}

Write-Host "careerledger-postgres is running." -ForegroundColor Green

Write-Host ""
Write-Host "Waiting for PostgreSQL to accept connections..." -ForegroundColor Yellow

$maxAttempts = 30
$attempt = 0

do {
    $attempt++

    $ready = docker exec careerledger-postgres pg_isready -U postgres 2>$null

    if ($ready -match "accepting connections") {
        break
    }

    Write-Host "Waiting for PostgreSQL... attempt $attempt/$maxAttempts" -ForegroundColor DarkYellow
    Start-Sleep -Seconds 2

} while ($attempt -lt $maxAttempts)

if ($ready -notmatch "accepting connections") {
    Write-Host "PostgreSQL did not become ready." -ForegroundColor Red
    docker logs careerledger-postgres --tail 80
    exit 1
}

Write-Host "PostgreSQL is ready." -ForegroundColor Green

function Ensure-Database {
    param (
        [string]$DatabaseName
    )

    Write-Host ""
    Write-Host "Checking database: $DatabaseName" -ForegroundColor Cyan

    $exists = docker exec careerledger-postgres psql -U postgres -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$DatabaseName';"

    if ($exists.Trim() -eq "1") {
        Write-Host "$DatabaseName already exists." -ForegroundColor Green
    }
    else {
        Write-Host "$DatabaseName does not exist. Creating..." -ForegroundColor Yellow

        docker exec careerledger-postgres psql -U postgres -d postgres -c "CREATE DATABASE $DatabaseName;"

        if ($LASTEXITCODE -ne 0) {
            Write-Host "Failed to create $DatabaseName." -ForegroundColor Red
            exit 1
        }

        Write-Host "$DatabaseName created." -ForegroundColor Green
    }
}

Ensure-Database "auth_db"
Ensure-Database "application_db"

Write-Host ""
Write-Host "Altering auth tables if they exist..." -ForegroundColor Cyan

docker exec careerledger-postgres psql -U postgres -d auth_db -c "ALTER TABLE IF EXISTS users ADD COLUMN IF NOT EXISTS is_verified BOOLEAN DEFAULT FALSE;"
docker exec careerledger-postgres psql -U postgres -d auth_db -c "ALTER TABLE IF EXISTS users ADD COLUMN IF NOT EXISTS auth_provider VARCHAR DEFAULT 'local';"

docker exec careerledger-postgres psql -U postgres -d auth_db -c "ALTER TABLE IF EXISTS otp_codes ADD COLUMN IF NOT EXISTS is_used BOOLEAN DEFAULT FALSE;"
docker exec careerledger-postgres psql -U postgres -d auth_db -c "ALTER TABLE IF EXISTS otp_codes ADD COLUMN IF NOT EXISTS expires_at TIMESTAMP;"
docker exec careerledger-postgres psql -U postgres -d auth_db -c "ALTER TABLE IF EXISTS otp_codes ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;"
docker exec careerledger-postgres psql -U postgres -d auth_db -c "ALTER TABLE IF EXISTS otp_codes ADD COLUMN IF NOT EXISTS purpose VARCHAR DEFAULT 'login';"

Write-Host ""
Write-Host "CareerLedger local stack is ready." -ForegroundColor Green

Write-Host ""
docker ps