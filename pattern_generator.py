from PIL import Image, ImageEnhance
import numpy as np
import os
import arabic_reshaper
from bidi import algorithm as bidi_algorithm

def display_farsi(text):
    """
    متن فارسی را برای نمایش در ترمینال آماده می‌کند.
    :param text: متن فارسی
    :return: متن آماده‌شده برای نمایش
    """
    reshaped_text = arabic_reshaper.reshape(text)  # تغییر شکل متن فارسی
    bidi_text = bidi_algorithm.get_display(reshaped_text)  # تبدیل به راست‌به‌چپ
    return bidi_text

def get_image_size_in_cm(image, dpi=300):
    """
    اندازه تصویر را بر حسب سانتی‌متر محاسبه می‌کند.
    :param image: تصویر ورودی (از نوع PIL.Image)
    :param dpi: تعداد پیکسل در هر اینچ (پیش‌فرض: 300)
    :return: اندازه تصویر بر حسب سانتی‌متر (عرض، ارتفاع)
    """
    inch_to_cm = 2.54  # هر اینچ معادل 2.54 سانتی‌متر است
    width_px, height_px = image.size  # اندازه تصویر بر حسب پیکسل
    width_cm = (width_px / dpi) * inch_to_cm  # عرض بر حسب سانتی‌متر
    height_cm = (height_px / dpi) * inch_to_cm  # ارتفاع بر حسب سانتی‌متر
    return width_cm, height_cm

def increase_quality(image, sharpness_factor=2, contrast_factor=1, brightness_factor=1, Saturation_factor=1.5):
    """
   افزایش میفیت تصویر در حالت RGB انجام میشود
    :param image: تصویر ورودی (از نوع PIL.Image در حالت CMYK)
    :param sharpness_factor: فاکتور افزایش شارپنس (پیش‌فرض: 2.0)
    :param contrast_factor: فاکتور افزایش کنتراست (پیش‌فرض: 1.5)
    :param brightness_factor: فاکتور افزایش روشنایی (پیش‌فرض: 1.1)
    :param brightness_factor: فاکتور افزایش شدت رنگها (پیش فرض :1.5)
    :return: تصویر بهبود یافته (در حالت CMYK)
    """
    
    # تبدیل تصویر به RGB برای سازگاری با توابع افزایش کیفیت
    image_rgb = image.convert('RGB')
    
    # افزایش شارپنس
    enhancer = ImageEnhance.Sharpness(image_rgb)
    image_rgb = enhancer.enhance(sharpness_factor)
    
    # افزایش کنتراست
    enhancer = ImageEnhance.Contrast(image_rgb)
    image_rgb = enhancer.enhance(contrast_factor)

    # # افزایش روشنایی
    enhancer = ImageEnhance.Brightness(image_rgb)
    image_rgb = enhancer.enhance(brightness_factor)

    # افزایش اشباع رنگ (Saturation)
    enhancer = ImageEnhance.Color(image_rgb)
    image_rgb = enhancer.enhance(Saturation_factor)
    
    # # تبدیل مجدد به CMYK اگر نیاز است
    return image_rgb.convert('CMYK')

def create_pattern(input_image_path, output_image_path, pattern_size_cm=(100, 150), repeat_every_cm=10):
    print(display_farsi("شروع ایجاد الگو..."))

    # بررسی وجود فایل ورودی
    if not os.path.exists(input_image_path):
        print(display_farsi(f"خطا: فایل {input_image_path} یافت نشد!"))
        return

    print(display_farsi("باز کردن تصویر ورودی..."))
    try:
        # بارگیری تصویر با وضوح بالا
        input_image = Image.open(input_image_path)
        print(display_farsi("تصویر ورودی با موفقیت باز شد."))
    except Exception as e:
        print(display_farsi(f"خطا در باز کردن تصویر: {e}"))
        return

    # بررسی DPI تصویر ورودی
    dpi = input_image.info.get('dpi', (300, 300))[0]  # DPI تصویر یا پیش‌فرض 300
    print(display_farsi(f"DPI تصویر ورودی: {dpi}"))

    # فراخوانی تابع برای محاسبه اندازه تصویر ورودی بر حسب سانتی‌متر
    width_cm, height_cm = get_image_size_in_cm(input_image, dpi)
    print(display_farsi(f"اندازه تصویر ورودی: {width_cm:.2f} x {height_cm:.2f} سانتی‌متر"))

    print(display_farsi("تبدیل اندازه‌ها به پیکسل..."))
    cm_to_inch = 0.393701
    pattern_size_px = (int(pattern_size_cm[0] * dpi * cm_to_inch), int(pattern_size_cm[1] * dpi * cm_to_inch))
    repeat_every_px = int(repeat_every_cm * dpi * cm_to_inch)

    print(display_farsi(f"اندازه پترن خروجی (پیکسل): {pattern_size_px}"))
    print(display_farsi(f"اندازه تکرار (پیکسل): {repeat_every_px}"))

    print(display_farsi("تغییر اندازه تصویر ورودی با حفظ کیفیت..."))
    # تغییر اندازه با الگوریتم LANCZOS (بالاترین کیفیت)
    input_image = input_image.resize((repeat_every_px, repeat_every_px), Image.LANCZOS)

    print(display_farsi("ایجاد تصویر خالی..."))
    pattern_image = Image.new('RGB', pattern_size_px)  # حالت رنگ rgb

    print(display_farsi("تکرار تصویر ورودی..."))
    for y in range(0, pattern_size_px[1], repeat_every_px):
        for x in range(0, pattern_size_px[0], repeat_every_px):
            pattern_image.paste(input_image, (x, y))

    print(display_farsi("افزایش کیفیت تصویر و تبدیل به CMYK ..."))
    pattern_image = increase_quality(pattern_image)

    print(display_farsi("ذخیره‌ی تصویر نهایی..."))
    try:
        # ذخیره‌سازی با فرمت TIFF و بدون فشرده‌سازی
        pattern_image.save(output_image_path, format='TIFF', compression='tiff_deflate')
        print(display_farsi(f"تصویر خروجی با موفقیت در {output_image_path} ذخیره شد."))
    except Exception as e:
        print(display_farsi(f"خطا در ذخیره‌ی تصویر خروجی: {e}"))

# مثال استفاده از تابع
input_image_path = 'input_image.jpg'  # مسیر تصویر ورودی
output_image_path = 'output_pattern.tiff'  # مسیر تصویر خروجی
print(display_farsi("شروع ایجاد الگو..."))
create_pattern(input_image_path, output_image_path)
print(display_farsi("پروسه کامل شد."))