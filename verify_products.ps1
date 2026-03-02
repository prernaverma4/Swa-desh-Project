$loginUrl = "http://127.0.0.1:5002/login"
$productsUrl = "http://127.0.0.1:5002/Products2?state=Maharashtra"
$username = "testuser"
$password = "password123"

# Create a session
$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession

# Login
try {
    $loginResponse = Invoke-WebRequest -Uri $loginUrl -Method Post -Body @{username=$username; password=$password} -WebSession $session -ErrorAction Stop
    Write-Host "Login Status: $($loginResponse.StatusCode)"
} catch {
    Write-Error "Login failed: $_"
    exit 1
}

# Fetch Products
try {
    $response = Invoke-WebRequest -Uri $productsUrl -WebSession $session -ErrorAction Stop
    $content = $response.Content

    # Check for products
    $products = @("Kolhapuri Chappals", "Warli Painting", "Solapuri Chaddar", "Nashik Grapes")
    foreach ($product in $products) {
        if ($content -match $product) {
            Write-Host "Found: $product"
        } else {
            Write-Host "MISSING: $product"
        }
    }
} catch {
    Write-Error "Fetch failed: $_"
    exit 1
}
