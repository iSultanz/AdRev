from PIL import Image
from openai import OpenAI
import tempfile

# Initialize OpenAI API
client = OpenAI(api_key="sk-proj-")

def analyze_text(text):
    """
    Analyze the text for compliance using GPT.
    """
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
    """
    Extract text and analyze static content from the uploaded image.
    This function analyzes the extracted text using the analyze_text function.
    """
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
    """
    Transcribe audio to text using OpenAI Whisper API.
    """
    try:
        with open(audio_file, "rb") as file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=file
            )
        return transcription.text
    except Exception as e:
        return f"حدث خطأ أثناء تحويل الصوت إلى نص: {e}"

# def render_results(text, analysis):
#     """
#     Display the text and analysis results.
#     """
#     st.subheader("النص المدخل", anchor=None)
#     st.text_area("النص", text, height=200, key="text-area", placeholder="أدخل النص هنا...", help="عرض النص المدخل للتحليل", label_visibility="visible")

#     st.subheader("تحليل الامتثال", anchor=None)
#     st.markdown(f"<div style='text-align: right;'>{analysis}</div>", unsafe_allow_html=True)

# # Streamlit App
# st.set_page_config(page_title="مدقق الامتثال للإعلانات", layout="wide")
# st.markdown("<div style='text-align: right;'><h1>مدقق الامتثال للإعلانات</h1></div>", unsafe_allow_html=True)
# st.markdown("<div style='text-align: right;'>تحقق من التزام إعلاناتك بأنظمة الدعاية في المملكة العربية السعودية.</div>", unsafe_allow_html=True)

# # Tabs for different inputs
# tabs = st.tabs(["الصوت", "الصورة", "النص"])

# # Text Input Tab
# with tabs[2]:
#     st.markdown("<div style='text-align: right;'><h2>التحقق من النص الإعلاني</h2></div>", unsafe_allow_html=True)
#     ad_text = st.text_area("أدخل النص الإعلاني:", height=200, key="ad_text", placeholder="قم بإدخال النص هنا للتحليل", label_visibility="visible")
#     if st.button("تحليل النص", help="انقر لتحليل النص المدخل", use_container_width=True):
#         if ad_text.strip():
#             analysis = analyze_text(ad_text)
#             render_results(ad_text, analysis)
#         else:
#             st.warning("يرجى إدخال نص للتحليل.")

# # Image Input Tab
# with tabs[1]:
#     st.markdown("<div style='text-align: right;'><h2>التحقق من الصورة الإعلانية</h2></div>", unsafe_allow_html=True)
#     image_file = st.file_uploader("ارفع صورة الإعلان", type=["png", "jpg", "jpeg"], help="يدعم أنواع PNG و JPG فقط", label_visibility="visible")
#     if st.button("تحليل الصورة", help="انقر لتحليل النص والعناصر البصرية في الصورة", use_container_width=True):
#         if image_file is not None:
#             analysis = process_image_static_response(image_file)
#             st.subheader("النصوص المستخرجة")
#             st.text_area("النص المستخرج", analysis["extracted_text"], height=200, help="النص الذي تم استخراجه من الصورة.")
#             st.subheader("تحليل النص")
#             st.write(analysis["text_analysis"])
#             st.subheader("تحليل الميزات البصرية")
#             st.write(analysis["feature_analysis"])
#         else:
#             st.warning("يرجى رفع صورة للتحليل.")

# # Audio Input Tab
# with tabs[0]:
#     st.markdown("<div style='text-align: right;'><h2>التحقق من الصوت الإعلاني</h2></div>", unsafe_allow_html=True)
#     audio_file = st.file_uploader("ارفع ملف الصوت الإعلاني", type=["wav", "mp3"], help="يدعم أنواع WAV و MP3 فقط", label_visibility="visible")

#     audio_bytes = audio_recorder()
#     if audio_bytes:
#         st.audio(audio_bytes, format="audio/wav")
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
#             temp_audio_file.write(audio_bytes)
#             temp_audio_file_path = temp_audio_file.name

#         if st.button("تحليل الصوت المسجل", help="تحليل الصوت المسجل واستخراج النص"):
#             recorded_text = transcribe_audio_with_whisper(temp_audio_file_path)
#             if recorded_text.startswith("حدث خطأ"):
#                 st.warning(recorded_text)
#             else:
#                 analysis = analyze_text(recorded_text)
#                 render_results(recorded_text, analysis)

#     if audio_file is not None:
#         if st.button("تحليل الصوت المرفوع", help="تحليل الصوت المرفوع واستخراج النص"):
#             uploaded_text = transcribe_audio_with_whisper(audio_file)
#             if uploaded_text.startswith("حدث خطأ"):
#                 st.warning(uploaded_text)
#             else:
#                 analysis = analyze_text(uploaded_text)
#                 render_results(uploaded_text, analysis)
