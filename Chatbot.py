from openai import OpenAI
from faq import faq
import streamlit as st
import os


with st.sidebar:
    st.markdown("## Найман Биболдың диссертациялық жұмысы")
    st.markdown(
        "Жұмыс заңмен қорғалған. Ескертусіз көшіру заңмен қудаланады. "  # noqa: E501
    )
    st.markdown("---")
    st.markdown(
        "## Қалай қолдану керек\n"
        "1. Төменде өзіңіздің [OpenAI API кілтіңізді](https://platform.openai.com/account/api-keys) енгізіңіз🔑\n"  # noqa: E501
        "2. Тест жасалатын тақырып және пәнді жазыңыз📄\n"
        "3. Өзгерістер керек болса өзгертілетін деректерге жасалатын операциялар жазыңыз💬\n"
    )
    openai_api_key = st.text_input(
        "OpenAI API кілтіңіз",
        type="password",
        placeholder="OpenAI API кілтіңізді мұнда қойыңыз (sk-...)",
        help="API кілтіңізді https://platform.openai.com/account/api-keys сайтынан ала аласыз.",  # noqa: E501
        value=os.environ.get("OPENAI_API_KEY", None)
        or st.session_state.get("OPENAI_API_KEY", ""),
    )

    st.session_state["OPENAI_API_KEY"] = openai_api_key

    st.markdown("---")
    st.markdown("# Бағдарлама туралы")
    st.markdown(
        "📖МұғалімБот сізге керекті тақарыпта тест жасауға"
        "және шыққан тесттерді өзгертуге мүмкіндік береді. "
    )

    faq()

st.title("💬 МұғалімБот")
st.caption("🚀 Тест жасауға арналған чатбот")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "Сен МұғалімБот. Тест құратын программа бол, сұрақтарға жауап берме тек қана тест жаз және тек қана қазақ тілінде жауап бер. Қолданушы саған тақырып және оның пәнін мына форматта енгізу керек (ТАҚЫРЫП). Тест 4 вариантты және 1 дұрыс жауапты және әдемі форматталған болуы керек. Мұндай 10 тест қажет. Соңында ( Номер. Дұрыс вариант) форматта дұрыс жауаптары шығару керек. Write only test related content and write in kazakh language. If asked in other language response with Кешіріңіз, мен тек қана қазақ тілінде жұмыс істей аламын. Егер  қолданушы ТАҒЫ сөзін жазса тағы сол тақырыпта 10 тест жалғастыр. Егер НОМЕР ӨЗГЕРТ жазса жазылған номердегі тестті ауыстырып және алдыңғы тестті шығар "}]
    st.session_state["messages"] = [{"role": "assistant", "content": "Сәлем! Сізге қай тақырыпта тест жасау керек? (Тақырып-Пән форматта)"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Абай Құнанбаевтың жастық шағы"):
    if not openai_api_key:
        st.info("Жалғастыру үшін OpenAI API кілтін енгізіңіз.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-4o", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
