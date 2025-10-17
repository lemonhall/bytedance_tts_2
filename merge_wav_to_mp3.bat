@echo off
REM 合并所有WAV文件并转换为高质量MP3
REM 使用FFmpeg进行音频处理

echo 🎵 WAV文件合并转MP3工具
echo ==================================================

REM 检查FFmpeg是否可用
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到FFmpeg，请先安装FFmpeg
    echo 💡 下载地址: https://ffmpeg.org/download.html
    pause
    exit /b 1
)

echo ✅ FFmpeg已安装

REM 生成WAV文件列表
echo 📝 正在扫描WAV文件...
(for %%f in (*.wav) do echo file '%%f') > temp_filelist.txt

REM 检查是否有WAV文件
if not exist "temp_filelist.txt" (
    echo ❌ 当前目录下没有找到WAV文件
    pause
    exit /b 1
)

REM 显示找到的文件
echo 📁 找到以下WAV文件:
for %%f in (*.wav) do echo    - %%f

echo.
echo 🔄 开始合并和转换...
echo ⚙️ 参数: 320k比特率, 最高质量

REM 执行FFmpeg合并转换
ffmpeg -f concat -safe 0 -i temp_filelist.txt -c:a libmp3lame -b:a 320k -q:a 0 -y all_audio_combined.mp3

if %errorlevel% equ 0 (
    echo.
    echo ✅ 转换成功!
    echo 📁 输出文件: all_audio_combined.mp3
    
    REM 显示文件大小
    for %%f in (all_audio_combined.mp3) do (
        set /a size_kb=%%~zf/1024
        echo 📊 文件大小: !size_kb! KB
    )
    
    echo 🎵 音频质量: 320k比特率, 最高质量级别
) else (
    echo ❌ 转换失败!
)

REM 清理临时文件
if exist "temp_filelist.txt" del "temp_filelist.txt"

echo.
echo 🎉 操作完成!
pause