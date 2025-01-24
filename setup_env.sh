#!/bin/bash

# Function to handle virtual environment creation and package installation
setup_virtual_env() {
  local requirement_file=$1

  # Check if the requirement file exists
  if [ ! -f "$requirement_file" ]; then
      echo "Requirement file '$requirement_file' not found. Skipping..."
      return
  fi

  # Extract environment name from the requirement file name
  local env_name=$(basename "$requirement_file" .txt)
  local venv_path="./venv/$env_name"

  # Check if the virtual environment already exists, create if not
  if [ ! -d "$venv_path" ]; then
      echo "Creating virtual environment in '$venv_path'..."
      python3 -m venv "$venv_path"
  else
      echo "Virtual environment '$venv_path' already exists."
  fi

  # Activate the virtual environment
  echo "Activating virtual environment..."
  source "$venv_path/bin/activate"

  # Install packages from the requirement file
  echo "Installing dependencies from '$requirement_file'..."
  python3 -m pip install --upgrade pip
  python3 -m pip install -r "$requirement_file"

  # Verify installation of packages
  echo "Verifying package installations..."
  while IFS= read -r package; do
      package=$(echo "$package" | xargs) # Trim whitespace around package name
      if [ ! -z "$package" ] && ! python3 -m pip show "$package" &> /dev/null; then
          echo "Warning: Package '$package' was not installed successfully."
      else
          echo "Package '$package' installed successfully."
      fi
  done < "$requirement_file"
}

# Main script logic

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed or not in PATH. Please install Python and try again."
    exit 1
fi

# Check if virtualenv is installed
if ! python3 -m pip show virtualenv &> /dev/null; then
    echo "virtualenv is not installed. Installing it..."
    python3 -m pip install virtualenv
else
    echo "virtualenv is already installed."
fi

# List of requirement files to process
requirement_files=(
    "requirement/data_extraction.txt"
)

# Process each requirement file using the function
for requirement_file in "${requirement_files[@]}"; do
    setup_virtual_env "$requirement_file"
done

echo "All environments are set up!"
