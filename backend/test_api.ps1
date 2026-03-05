# API 테스트 스크립트

# 1. 서버 상태 확인
Write-Host "=== 1. 서버 상태 확인 ===" -ForegroundColor Green
$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/" -Method GET
Write-Host "서버 응답: $($response.message)" -ForegroundColor Cyan

# 2. 회원가입 테스트
Write-Host "`n=== 2. 회원가입 테스트 ===" -ForegroundColor Green
$signupBody = @{
    username = "testuser"
    password = "test1234"
    email = "test@example.com"
    nickname = "테스트유저"
    dietary_label = "none"
    allergies = $null
    spicy_threshold = 3
    saltiness_preference = 3
    lunch_budget_max = 12000
    is_adventurous = $true
} | ConvertTo-Json

try {
    $signupResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/signup" -Method POST -ContentType "application/json" -Body $signupBody
    Write-Host "회원가입 성공!" -ForegroundColor Cyan
    Write-Host "사용자 ID: $($signupResponse.user_id)" -ForegroundColor Yellow
    Write-Host "사용자명: $($signupResponse.username)" -ForegroundColor Yellow
} catch {
    $errorDetail = $_.ErrorDetails.Message | ConvertFrom-Json
    if ($errorDetail.detail -match "already exists") {
        Write-Host "이미 존재하는 사용자입니다. 로그인 테스트를 진행합니다." -ForegroundColor Yellow
    } else {
        Write-Host "회원가입 실패: $($errorDetail.detail)" -ForegroundColor Red
    }
}

# 3. 로그인 테스트
Write-Host "`n=== 3. 로그인 테스트 ===" -ForegroundColor Green
$loginBody = "username=testuser&password=test1234"

try {
    $loginResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/login" -Method POST -ContentType "application/x-www-form-urlencoded" -Body $loginBody
    Write-Host "로그인 성공!" -ForegroundColor Cyan
    Write-Host "액세스 토큰: $($loginResponse.access_token.Substring(0,50))..." -ForegroundColor Yellow
    $token = $loginResponse.access_token
} catch {
    Write-Host "로그인 실패: $($_.Exception.Message)" -ForegroundColor Red
    exit
}

# 4. 메뉴 조회 테스트
Write-Host "`n=== 4. 메뉴 조회 테스트 ===" -ForegroundColor Green
try {
    $menusResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/menus?limit=5" -Method GET
    Write-Host "메뉴 조회 성공! 총 $($menusResponse.Count)개 메뉴 조회됨" -ForegroundColor Cyan
    foreach ($menu in $menusResponse) {
        Write-Host "  - $($menu.menu_name) (카테고리: $($menu.category), 가격: $($menu.price)원, 날씨: $($menu.matching_weather))" -ForegroundColor Yellow
    }
} catch {
    Write-Host "메뉴 조회 실패: $($_.Exception.Message)" -ForegroundColor Red
}

# 5. 메뉴 추천 테스트
Write-Host "`n=== 5. 메뉴 추천 테스트 ===" -ForegroundColor Green
$headers = @{
    "Authorization" = "Bearer $token"
}

$recommendBody = @{
    weather = "Rain"
    mood = "Comfortable"
    group_size = 2
    budget = 15000
} | ConvertTo-Json

try {
    $recommendResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/recommend/menus" -Method POST -Headers $headers -ContentType "application/json" -Body $recommendBody
    Write-Host "메뉴 추천 성공! 총 $($recommendResponse.recommendations.Count)개 추천됨" -ForegroundColor Cyan
    $count = 1
    foreach ($rec in $recommendResponse.recommendations) {
        Write-Host "  $count. $($rec.menu_name) (점수: $($rec.score), 이유: $($rec.reason))" -ForegroundColor Yellow
        $count++
        if ($count -gt 5) { break }
    }
} catch {
    Write-Host "메뉴 추천 실패: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "에러 상세: $($_.ErrorDetails.Message)" -ForegroundColor Red
}

# 6. 사용자 프로필 조회 테스트
Write-Host "`n=== 6. 사용자 프로필 조회 테스트 ===" -ForegroundColor Green
try {
    $profileResponse = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/users/me" -Method GET -Headers $headers
    Write-Host "프로필 조회 성공!" -ForegroundColor Cyan
    Write-Host "  사용자명: $($profileResponse.username)" -ForegroundColor Yellow
    Write-Host "  이메일: $($profileResponse.email)" -ForegroundColor Yellow
    Write-Host "  매운맛 선호도: $($profileResponse.preferences.spicy_level)" -ForegroundColor Yellow
} catch {
    Write-Host "프로필 조회 실패: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n=== 테스트 완료 ===" -ForegroundColor Green
Write-Host "`n테스트 계정 정보:" -ForegroundColor Cyan
Write-Host "  아이디: testuser" -ForegroundColor Yellow
Write-Host "  비밀번호: test1234" -ForegroundColor Yellow
