# Set execution policy to allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force

# Ensure we are in the script's directory
Set-Location $PSScriptRoot

# Check if virtualenv is installed
if (-not (Get-Command virtualenv -ErrorAction SilentlyContinue)) {
    Write-Host "Installing virtualenv..."
    pip install virtualenv
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path ".\ifts_my_env")) {
    Write-Host "Creating virtual environment..."
    virtualenv ifts_my_env
}

# Activate virtual environment
Write-Host "Activating virtual environment..."
.\venv\Scripts\Activate.ps1

# Install requirements
Write-Host "Installing requirements..."
pip install -r control_acceso/requirements.txt

# Change to the Django project directory
Set-Location .\control_acceso

# Run Django server
Write-Host "Starting Django development server..."
python manage.py runserver