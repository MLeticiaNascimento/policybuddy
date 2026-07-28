import streamlit as st


def setup_page():

    st.set_page_config(
        page_title="PolicyBuddy",
        page_icon="🛡️",
        layout="centered",
    )

    apply_theme()


def apply_theme():

    st.markdown(
        """
        <style>

        /* Background */

        .stApp {

            background:
            linear-gradient(
                135deg,
                #0B1120,
                #111827
            );

            color: #E5E7EB;
        }


        /* Main width */

        .block-container {

            max-width: 900px;

            padding-top: 3rem;
        }


        /* Header */

        .hero {

            background:
            linear-gradient(
                135deg,
                rgba(30,41,59,0.95),
                rgba(15,23,42,0.95)
            );

            padding: 40px;

            border-radius: 22px;

            border: 1px solid #334155;

            margin-bottom: 35px;

        }
        .hero-title {
            font-size: 46px;
            font-weight: 800;
            color: #F8FAFC;
            letter-spacing: -1px;
        }        


        .hero-subtitle {

            font-size: 18px;

            color: #cbd5e1;

            line-height: 1.6;

}


        /* Cards */

        .section-card {

            background:

            rgba(
                30,
                41,
                59,
                0.75
            );

            border-radius:18px;

            padding:25px;

            border:

            1px solid #334155;

            margin-top:25px;

        }



        .section-title {

            font-size:20px;

            font-weight:700;

            color:#60A5FA;

            margin-bottom:15px;

        }



        /* Input */

        textarea {

            background-color:#111827 !important;

            border-radius:12px !important;

        }



        /* Button */

        .stButton button {

            width:100%;

            height:45px;

            border-radius:12px;

            background:

            linear-gradient(
                90deg,
                #2563EB,
                #3B82F6
            );

            color:white;

            font-weight:700;

            border:none;

        }


        .stButton button:hover {

            background:

            linear-gradient(
                90deg,
                #1D4ED8,
                #2563EB
            );

        }



        /* Metrics */

        div[data-testid="metric-container"] {

            background:#111827;

            border-radius:14px;

            padding:15px;

            border:

            1px solid #334155;

        }



        </style>

        """,
        unsafe_allow_html=True,
    )


def render_header():

    st.markdown(
        """
        <div class="hero">
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-title">
            🛡️ PolicyBuddy
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-subtitle">
            AI-powered Corporate Compliance Assistant
            <br><br>
            Ask questions about corporate policies
            and receive evidence-based answers.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_user_question():

    return st.text_area(

        "Ask your policy question:",

        placeholder=

        """
Example:

Can I share confidential company data
with external partners?
        """,

        height=120,

    )


def render_answer(answer):

    st.markdown(
        "### 🤖 PolicyBuddy Answer"
    )


    with st.container():

        st.markdown(
            """
            <div class="section-card">
            """,
            unsafe_allow_html=True,
        )


        st.markdown(
            answer
        )


        st.markdown(
            """
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_metadata(

    confidence,

    status,

    score,

):

    st.markdown(
        "### 📊 Evidence Analysis"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(

            "Confidence",

            confidence.upper()

        )


    with col2:

        st.metric(

            "Retrieval",

            status.upper()

        )


    with col3:

        st.metric(

            "Best Score",

            f"{score:.3f}"

            if score is not None

            else "-"

        )


def render_sources(sources):

    if not sources:

        return


    st.markdown(
        "### 📚 Sources Used"
    )


    for index, source in enumerate(
        sources,
        start=1
    ):
        st.markdown(
            f"""
            **Document {index}**

            {source.content[:500]}...
            """              
            )

        st.divider()
