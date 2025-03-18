import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpRequest
from pytube import YouTube
from pytube.exceptions import VideoUnavailable

def download_video(video_url):
    media_path = os.path.join(settings.MEDIA_ROOT, "downloads")
    os.makedirs(media_path, exist_ok=True)  # إنشاء المجلد إذا لم يكن موجودًا

    try:
        # التحقق من أن الرابط صالح
        yt = YouTube(video_url)

        # التحقق من أن الفيديو غير محذوف أو غير متاح
        if yt.streams.filter(progressive=True, file_extension="mp4").count() == 0:
            return "الفيديو غير متاح أو تم حذفه"

        # اختيار أفضل جودة فيديو وصوت
        stream = yt.streams.filter(progressive=True, file_extension="mp4").get_highest_resolution()

        # تحديد مسار الحفظ
        output_path = os.path.join(media_path, f"{yt.title}.mp4")
        
        # تحميل الفيديو
        stream.download(output_path=media_path)

        return f"تم التنزيل بنجاح: {yt.title}"
    except VideoUnavailable:
        return "الفيديو غير متاح أو تم حذفه"
    except Exception as e:
        # إضافة رسائل خطأ مفصلة
        return f"حدث خطأ: {str(e)}"

def home_page(request: HttpRequest):
    if request.method == "POST":
        video_url = request.POST.get('video_url', '').strip()
        if video_url:
            try:
                message = download_video(video_url)
                return render(request, "main/home.html", {"message": message})
            except Exception as e:
                return render(request, "main/home.html", {"error": f"حدث خطأ: {str(e)}"})

    return render(request, "main/home.html")
