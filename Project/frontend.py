import streamlit as st
from langchain_core.messages import HumanMessage
from main import app


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Travel Expert AI",
    page_icon="✈️",
    layout="wide"
)


# ---------------- CSS ----------------

st.markdown(
"""
<style>

.stApp{
    background:#0b1220;
}

.title{
    color:white;
    font-size:42px;
    font-weight:700;
}

.subtitle{
    color:#94a3b8;
    font-size:18px;
}

.card{
    background:#172033;
    padding:20px;
    border-radius:15px;
    border:1px solid #26334d;
}

</style>

""",
unsafe_allow_html=True
)



# ---------------- SIDEBAR ----------------


with st.sidebar:

    st.markdown(
    """
    <h2 style="color:white">
    🌍 Travel Expert AI
    </h2>
    """,
    unsafe_allow_html=True
    )


    st.divider()


    st.markdown(
    """
    <div class="card">

    <h3 style="color:white">
    👩‍💻 Created By
    </h3>

    <p style="color:#cbd5e1">
    Manasi
    </p>

    </div>
    """,
    unsafe_allow_html=True
    )


    st.write("")


    st.markdown(
    """
    <div class="card">

    <h3 style="color:white">
    🛠 Technology
    </h3>

    <p style="color:#cbd5e1">

    🔗 LangGraph<br>
    🧠 LangChain<br>
    🤖 LLM Agents<br>
    🗄️ PostgreSQL Memory

    </p>

    </div>
    """,
    unsafe_allow_html=True
    )


    st.write("")


    st.markdown(
    """
    <div class="card">

    <h3 style="color:white">
    ⚙ Agent Flow
    </h3>

    <p style="color:#cbd5e1">

    User Query<br>
    ↓<br>
    Flight Agent<br>
    ↓<br>
    Hotel Agent<br>
    ↓<br>
    Itinerary Agent<br>
    ↓<br>
    Final Travel Plan

    </p>

    </div>
    """,
    unsafe_allow_html=True
    )



# ---------------- MAIN PAGE ----------------


st.markdown(
"""
<div class="title">
✈️ Travel Expert AI
</div>

<div class="subtitle">

Your personal AI travel planner powered by LangGraph + LangChain.

</div>

""",
unsafe_allow_html=True
)


st.write("")



# ---------------- INPUT ----------------


query = st.text_area(
    "🔎 Tell me about your trip",

    placeholder=
"""
Example:

Plan a 7 day trip to Mauritius.
Budget 2 lakh.
Need hotels, activities and itinerary.

""",

height=160
)



user_id = st.text_input(
    "User ID",
    value="manasi_user"
)



button = st.button(
    "🚀 Plan My Trip"
)



# ---------------- RUN LANGGRAPH ----------------


if button:


    if query.strip():


        config = {

            "configurable":{

                "thread_id": user_id

            }

        }



        initial_state = {


            "messages":[
                HumanMessage(
                    content=query
                )
            ],


            "user_query":query,


            # Required by TravelState

            "flight_result":"",

            "hotel_result":"",

            "itinerary_result":"",

            "llm_calls":0

        }



        try:


            with st.spinner(
                "🤖 Travel Expert is preparing your plan..."
            ):


                result = app.invoke(
                    initial_state,
                    config=config
                )



            st.success(
                "Trip Generated Successfully! 🎉"
            )


            st.divider()


            st.subheader(
                "🌎 Your Travel Plan"
            )



            # Get final response

            messages = result.get(
                "messages",
                []
            )


            if messages:

                final_answer = messages[-1].content

                st.markdown(
                    final_answer
                )


            else:

                st.warning(
                    "No response generated."
                )



        except Exception as e:


            st.error(
                f"Error occurred: {e}"
            )


    else:

        st.warning(
            "Please enter your travel requirement."
        )