import streamlit as st

from policybuddy.service.service import answer_question
from policybuddy.ui.ui import (
    get_user_question,
    render_answer,
    render_header,
    render_metadata,
    render_sources,
    setup_page,
)

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