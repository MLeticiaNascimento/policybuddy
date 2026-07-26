import streamlit as st

from policybuddy.ui import (
    setup_page,
    render_header,
    get_user_question,
    render_answer,
    render_metadata,
    render_sources,
)

from policybuddy.service import answer_question


setup_page()

render_header()


question = get_user_question()


if st.button("Analyze Policy"):

    if not question:

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Analyzing policies..."
        ):

            response = answer_question(
                question
            )


        render_answer(
            response.answer
        )


        render_metadata(
            confidence=response.confidence,
            status=response.retrieval_status,
            score=response.best_score,
        )


        render_sources(response.sources)