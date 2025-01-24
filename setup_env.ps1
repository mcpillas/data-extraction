# Function to handle virtual environment creation and package installation
function Setup-VirtualEnv {
    param (
        [string]$RequirementFile
    )

    # Check if the requirement file exists
    if (-not (Test-Path -Path $RequirementFile)) {
        Write-Output "Requirement file '$RequirementFile' not found. Skipping..."
        return
    }

    # Extract environment name from the requirement file name
    $EnvName = Split-Path -Leaf $RequirementFile -Resolve | ForEach-Object { $_ -replace '.txt$', '' }
    $VenvPath = Join-Path -Path "./venv" -ChildPath $EnvName

    # Check if the virtual environment already exists, create if not
    if (-not (Test-Path -Path $VenvPath)) {
        Write-Output "Creating virtual environment in '$VenvPath'..."
        python -m venv $VenvPath
    } else {
        Write-Output "Virtual environment '$VenvPath' already exists."
    }

    # Activate the virtual environment
    Write-Output "Activating virtual environment..."
    & "$VenvPath/Scripts/Activate"

    # Install packages from the requirement file
    Write-Output "Installing dependencies from '$RequirementFile'..."
    python -m pip install --upgrade pip
    python -m pip install -r $RequirementFile

    # Verify installation of packages
    Write-Output "Verifying package installations..."
    Get-Content $RequirementFile | ForEach-Object {
        $Package = $_.Trim()
        if ($Package -ne "" -and (-not (python -m pip show $Package))) {
            Write-Warning "Package '$Package' was not installed successfully."
        } else {
            Write-Output "Package '$Package' installed successfully."
        }
    }
}

# Main script logic

# Check if Python is installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Output "Python is not installed or not in PATH. Please install Python and try again."
    exit 1
}

# Check if virtualenv is installed
if (-not (python -m pip show virtualenv)) {
    Write-Output "virtualenv is not installed. Installing it..."
    python -m pip install virtualenv
} else {
    Write-Output "virtualenv is already installed."
}

# List of requirement files to process
$RequirementFiles = @(
    "requirement/data_extraction.txt"
)

# Process each requirement file
foreach ($RequirementFile in $RequirementFiles) {
    Setup-VirtualEnv -RequirementFile $RequirementFile
}

Write-Output "All environments are set up!"
