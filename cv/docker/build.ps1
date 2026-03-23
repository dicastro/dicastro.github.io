$CV_BASE_TAG = "3.6.4.0-alpine"
$CV_MY_IMAGE = "dicastro/pandoc-latex-cv"

Write-Host "Building personalized image based on pandoc/latex:$CV_BASE_TAG..." -ForegroundColor Cyan

docker build --build-arg PANDOC_LATEX_BASE_IMAGE=$CV_BASE_TAG -t "${CV_MY_IMAGE}:${CV_BASE_TAG}" .