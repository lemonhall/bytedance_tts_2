# 合并所有WAV文件并转换为高质量MP3的PowerShell脚本
# 作者: GitHub Copilot
# 用途: 将当前目录下所有WAV文件合并为一个高质量MP3文件

param(
    [string]$OutputFile = "all_audio_combined.mp3",
    [int]$BitRate = 320,
    [string]$Quality = "0"  # 0是最高质量，9是最低质量
)

Write-Host "🎵 WAV文件合并转MP3工具" -ForegroundColor Cyan
Write-Host "=" * 50

# 检查FFmpeg是否安装
try {
    $ffmpegVersion = & ffmpeg -version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "FFmpeg not found"
    }
    Write-Host "✅ FFmpeg已安装" -ForegroundColor Green
} catch {
    Write-Host "❌ 错误: 未找到FFmpeg，请先安装FFmpeg" -ForegroundColor Red
    Write-Host "💡 下载地址: https://ffmpeg.org/download.html" -ForegroundColor Yellow
    exit 1
}

# 查找WAV文件
$wavFiles = Get-ChildItem -Path "." -Filter "*.wav"
if ($wavFiles.Count -eq 0) {
    Write-Host "❌ 当前目录下没有找到WAV文件" -ForegroundColor Red
    exit 1
}

Write-Host "📁 找到 $($wavFiles.Count) 个WAV文件:" -ForegroundColor Yellow
$wavFiles | ForEach-Object { Write-Host "   - $($_.Name)" }

# 生成文件列表
$fileListPath = "temp_filelist.txt"
try {
    $wavFiles | ForEach-Object { "file '$($_.Name)'" } | Out-File -FilePath $fileListPath -Encoding UTF8
    Write-Host "📝 生成文件列表: $fileListPath" -ForegroundColor Green

    # 执行FFmpeg合并和转换
    Write-Host "🔄 开始合并和转换..." -ForegroundColor Yellow
    Write-Host "⚙️  参数: 比特率=${BitRate}k, 质量=${Quality}" -ForegroundColor Cyan
    
    $ffmpegArgs = @(
        "-f", "concat",
        "-safe", "0", 
        "-i", $fileListPath,
        "-c:a", "libmp3lame",
        "-b:a", "${BitRate}k",
        "-q:a", $Quality,
        "-y",  # 覆盖输出文件
        $OutputFile
    )
    
    & ffmpeg @ffmpegArgs
    
    if ($LASTEXITCODE -eq 0) {
        # 获取输出文件信息
        $outputInfo = Get-ChildItem $OutputFile
        $sizeKB = [math]::Round($outputInfo.Length / 1024, 1)
        $sizeMB = [math]::Round($outputInfo.Length / 1024 / 1024, 2)
        
        Write-Host ""
        Write-Host "✅ 转换成功!" -ForegroundColor Green
        Write-Host "📁 输出文件: $OutputFile" -ForegroundColor Cyan
        Write-Host "📊 文件大小: ${sizeKB} KB (${sizeMB} MB)" -ForegroundColor Cyan
        Write-Host "🎵 音频质量: ${BitRate}k比特率, 质量级别${Quality}" -ForegroundColor Cyan
        
        # 显示音频时长信息（如果需要）
        try {
            $duration = & ffprobe -v quiet -show_entries format=duration -of csv=p=0 $OutputFile
            if ($duration -match "^\d+\.?\d*$") {
                $minutes = [math]::Floor([double]$duration / 60)
                $seconds = [math]::Round([double]$duration % 60, 1)
                Write-Host "⏱️  时长: ${minutes}分${seconds}秒" -ForegroundColor Cyan
            }
        } catch {
            # 忽略时长获取失败
        }
        
    } else {
        Write-Host "❌ 转换失败!" -ForegroundColor Red
        exit 1
    }
    
} catch {
    Write-Host "❌ 错误: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
} finally {
    # 清理临时文件
    if (Test-Path $fileListPath) {
        Remove-Item $fileListPath -ErrorAction SilentlyContinue
        Write-Host "🧹 清理临时文件: $fileListPath" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "🎉 操作完成!" -ForegroundColor Green