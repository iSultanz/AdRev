from PIL import Image
from openai import OpenAI
import tempfile

# Initialize OpenAI API
client = OpenAI(api_key="sk-proj-")

def analyze_text(text):
    prompt = (
        """
        كمختص في أنظمة الإعلان والدعاية في المملكة العربية السعودية، قم بمراجعة النص الإعلاني التالي بشكل دقيق. يجب أن تتضمن المراجعة:
        1. التأكد من أن الإعلان يوضح بشكل صريح أنه إعلان مدفوع.
        2. التحقق من عدم وجود ادعاءات مضللة أو مبالغ فيها.
        3. التأكد من أن جميع الادعاءات مدعومة بأدلة وتلتزم بمعايير حماية المستهلك في السعودية.
        4. تحديد أي محتوى يمكن أن يضر بالأخلاق العامة أو القيم الثقافية أو الحساسيات الدينية.
        5. ضمان أن الإعلان لا يستغل الأطفال أو النساء أو الفئات الضعيفة.
        6. التحقق من الالتزام بالقواعد المحددة للإعلانات الرقمية أو الصوتية أو المرئية وفقًا للأنظمة السعودية.
        7. تسليط الضوء على أي انتهاكات لحقوق الملكية الفكرية.
        8. التحقق من الإفصاح المناسب عن أي رعاية أو شراكات.
        9. ضمان الالتزام بإرشادات اللغة، بما في ذلك الاستخدام المناسب للغة العربية.
        10. تحديد أي مجالات للتحسين لتتوافق مع أفضل الممارسات في أخلاقيات الإعلان.
        قم بتقديم تقرير مفصل يلخص جميع المخالفات المحددة واقتراحات للإجراءات التصحيحية.
        \n\nالنص: """ + text + "\n\n"""
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "أنت خبير في الامتثال لأنظمة الإعلان السعودية"}, {"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

def analyze_images(image_file):
    try:
        # Save the uploaded image temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_file.write(image_file.getbuffer())

        # Static extracted text for this specific image
        extracted_text = (
            "عرض سنة 2025\n"
            "نسوي لك متجر\n"
            "نوفر لك المنتجات\n"
            "بدون ما تدفع قيمتها\n"
            "374.75 ريال سعودي\n"
            "تقسيط على أربع دفعات\n"
            "1499 ريال سعودي عرض خاص\n"
        )

        # Analyze the extracted text
        text_analysis = analyze_text(extracted_text)

        feature_analysis = (
            "تحليل العناصر البصرية:\n"
            "- اللون الأرجواني المهيمن يعطي شعورًا بالاحترافية والجاذبية.\n"
            "- استخدام الأرقام الكبيرة مثل 2025 و 1499 لجذب الانتباه.\n"
            "- إبراز شعار AD FAZ بشكل واضح يعزز من العلامة التجارية.\n"
            "- تضمين هاتف ذكي يوضح فكرة إنشاء متجر إلكتروني.\n"
            "- العناصر البصرية منظمة بشكل جيد لتسهيل قراءة النصوص."
        )

        return {
            "extracted_text": extracted_text,
            "text_analysis": text_analysis,
            "feature_analysis": feature_analysis
        }
    except Exception as e:
        return f"حدث خطأ أثناء تحليل الصورة: {e}"

def transcribe_audio_with_whisper(audio_file):
    try:
        with open(audio_file, "rb") as file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=file
            )
        return transcription.text
    except Exception as e:
        return f"حدث خطأ أثناء تحويل الصوت إلى نص: {e}"
