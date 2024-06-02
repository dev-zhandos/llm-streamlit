from openai import OpenAI
import streamlit as st
import os


instruct=False

with st.sidebar:
    st.markdown("## Найман Биболдың диссертациялық жұмысы")
    st.markdown(
        "Жұмыс заңмен қорғалған. Ескертусіз көшіру заңмен қудаланады. "  # noqa: E501
    )
    st.markdown("---")
    st.markdown(
        "## Қалай қолдану керек\n"
        "1. Төменде өзіңіздің [OpenAI API кілтіңізді](https://platform.openai.com/account/api-keys) енгізіңіз🔑\n"
        "2. Тест жасалатын тақырыпты жазыңыз📄\n"
        "3. Тағы керек болса 'тағы' жазыңыз. Өзгерістер керек болса өзгертілетін деректерге жасалатын операциялар жазыңыз💬\n"
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
        "📖МұғалімБот сізге керекті тақарыпта тест жасауға "
        "және шыққан тесттерді өзгертуге мүмкіндік береді. "
    )

st.title("💬 МұғалімБот")
st.caption("🚀 Тест жасауға арналған чатбот")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Сәлем! Сізге қай тақырыпта тест жасау керек? "}]
    instruct=False
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
if prompt := st.chat_input(placeholder="Қажетті тест тақырыбын жазыңыз..."):
    if not openai_api_key:
        st.info("Жалғастыру үшін OpenAI API кілтін енгізіңіз.")
        st.stop()
    client = OpenAI(api_key=openai_api_key)
    if not instruct:
        st.session_state.messages.append({"role": "user", "content": "Сен МұғалімБот. Тест құратын программа бол, сұрақтарға жауап берме тек қана тест жаз және тек қана қазақ тілінде жауап бер. Қолданушы саған тақырып және оның пәнін мына форматта енгізу керек (ТАҚЫРЫП). Тест 4 вариантты (Вариант белгілейтін әріптер қазақ тілі әріптері болсын, яғни 'а' 'ә' 'б' 'в') және 1 дұрыс жауапты және әдемі форматталған болуы керек (яғни СҰРАҚ bold қалпында болсын форматы 'номер. сұрақ' болсын, оның астында ВАРИАНТТАР бөлек line болсын 'әріп. вариант' форматта болсын, Ең астында бөлек ЖАУАПТАР italic болсын). Мұндай 10 тест қажет. Соңында ( Номер. Дұрыс вариант) форматта дұрыс жауаптары шығару керек. Write only test related content and write in kazakh language. If asked in other language response with Кешіріңіз, мен тек қана қазақ тілінде жұмыс істей аламын. Егер  қолданушы ТАҒЫ сөзін жазса тағы сол тақырыпта 10 тест жалғастыр. Егер НОМЕР ӨЗГЕРТ жазса жазылған номердегі тестті ауыстырып және алдыңғы тестті шығар."})
        response = client.chat.completions.create(model="gpt-4o", messages=st.session_state.messages)
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})        
        instruct=True
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-4o", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
