$loginUrl = "http://127.0.0.1:5002/login"
$productsUrl = "http://127.0.0.1:5002/Products2?state=Maharashtra"
$username = "testuser"
$password = "password123"
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
    
    # Simple base tag injection to make relative links work
    $content = $response.Content
    if ($content -notmatch "<base") {
        $content = $content -replace "<head>", "<head><base href='http://127.0.0.1:5002/'>"
    }

    $targetFile = "c:\Users\SHREE\Desktop\trial2\trial\captured_products.html"
    $content | Out-File -FilePath $targetFile -Encoding utf8
    Write-Host "Page saved to $targetFile"
} catch {
    Write-Error "Fetch failed: $_"
    exit 1
}
