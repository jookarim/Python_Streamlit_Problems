import streamlit as st

# Display app title
st.title("Smart Quiz Master")

# Create 3 tabs (Quiz, Results, Review Answers)
tab1, tab2, tab3 = st.tabs(['Quiz', 'Results', 'Review Answers'])

# Total number of quiz questions
TOTAL_QUESTIONS = 5

# Create session state variables
# (Data stored until the page is refreshed)

if 'questions' not in st.session_state:
    st.session_state.questions = []

if 'curr_ques' not in st.session_state:
    st.session_state.curr_ques = 0

if 'curr_score' not in st.session_state:
    st.session_state.curr_score = 0

if 'show_results' not in st.session_state:
    st.session_state.show_results = False

if 'student_name' not in st.session_state:
    st.session_state.student_name = ""

if 'student_answers' not in st.session_state:
    st.session_state.student_answers = []

if 'difficulty_level' not in st.session_state:
    st.session_state.difficulty_level = ""
    
def display_sidebar():
    """Display quiz rules and quiz information."""
    with st.sidebar:
        st.header("Quiz Rules")
        st.write("Do not cheat")

        st.write(f"Total Questions: {TOTAL_QUESTIONS}")
        st.write("Passing Score: 60%")


def add_question(question, choices, correct_answer, difficulty_level):
    """Add one question to the quiz."""
    st.session_state.questions.append( {difficulty_level :{
        'Question': question,
        'Choices': choices,
        'Correct Answer': correct_answer
    }})


def add_questions(questions, choices, correct_answers, difficulty_level):
    """Add all quiz questions."""
    for i in range(TOTAL_QUESTIONS):
        add_question(questions[i], choices[i], correct_answers[i], difficulty_level)


def valid_name(student_name):
    """Return True if the student entered a name."""
    return len(student_name) > 0


def create_quiz():
    """Display the quiz interface."""
    col1, col2 = st.columns(2)

    with col1:

        # Get student's name
        st.session_state.student_name = st.text_input("Enter Student Name:")
      
        st.session_state.difficulty_level = st.selectbox("Difficulty Level", [
            'Easy', 'Medium', 'Hard'
        ])
        
        submit_button = False
        next_ques_button = False

        # Start quiz only after entering a valid name
        if valid_name(st.session_state.student_name):

            # Calculate Index Shift
            if st.session_state.difficulty_level == "Medium":
                global_idx = st.session_state.curr_ques + 5
            elif st.session_state.difficulty_level == "Hard":
                global_idx = st.session_state.curr_ques + 10
            else:
                global_idx = st.session_state.curr_ques

            # Get current question data using the shifted global index
            question = st.session_state.questions[global_idx][st.session_state.difficulty_level]["Question"]
            choices = st.session_state.questions[global_idx][st.session_state.difficulty_level]["Choices"]
            correct_answer = st.session_state.questions[global_idx][st.session_state.difficulty_level]["Correct Answer"]

            # Let student choose an answer (added a simple key to prevent selectbox reset issues)
            answer = st.selectbox(question, choices, key=f"q_{st.session_state.curr_ques}")

            # Quiz buttons
            submit_button = st.button("Submit")
            next_ques_button = st.button("Next Question")

            ans_correct = False

            # Check submitted answer
            if submit_button:

                # Save student's answer if they haven't submitted one for this step yet
                if len(st.session_state.student_answers) <= st.session_state.curr_ques:
                    st.session_state.student_answers.append(answer)

                    # Increase score if correct
                    if answer == correct_answer:
                        st.session_state.curr_score += 1
                        ans_correct = True

            # Move to the next question
            if next_ques_button:

                # Still have questions remaining
                if st.session_state.curr_ques < TOTAL_QUESTIONS - 1:
                    st.session_state.curr_ques += 1
                    st.rerun()

                # Quiz finished
                else:
                    st.session_state.show_results = True
                    st.rerun()

    with col2:

        # Display current quiz statistics
        st.write(f"Current Score: {st.session_state.curr_score}")
        st.write(f"Remaining Questions: {TOTAL_QUESTIONS - st.session_state.curr_ques - 1}")

        # Show whether the answer was correct
        if submit_button:
            # We look up the exact item in student_answers safely
            if len(st.session_state.student_answers) > st.session_state.curr_ques:
                current_student_ans = st.session_state.student_answers[st.session_state.curr_ques]
                
                if st.session_state.difficulty_level == "Medium":
                    g_idx = st.session_state.curr_ques + 5
                elif st.session_state.difficulty_level == "Hard":
                    g_idx = st.session_state.curr_ques + 10
                else:
                    g_idx = st.session_state.curr_ques
                    
                actual_correct = st.session_state.questions[g_idx][st.session_state.difficulty_level]["Correct Answer"]
                
                if current_student_ans == actual_correct:
                    st.success("Correct")
                else:
                    st.error("Incorrect")


def show_results():
    """Display final quiz results."""

    if st.session_state.show_results:

        # Student summary
        st.write(f"Student Name: {st.session_state.student_name}")
        st.write(f"Difficulty Level: {st.session_state.difficulty_level}")
        st.write(f"Total Questions: {TOTAL_QUESTIONS}")
        st.write(f"Correct Answers: {st.session_state.curr_score}")
        st.write(f"Wrong Answers: {TOTAL_QUESTIONS - st.session_state.curr_score}")

        # Display percentage score
        st.write(
            f"Total Score: {st.session_state.curr_score} / {TOTAL_QUESTIONS} "
            f"({st.session_state.curr_score / TOTAL_QUESTIONS * 100}%)"
        )

        # Pass or fail message
        if st.session_state.curr_score >= 3:
            st.success("Passed")
            st.write("Keep Going")
        else:
            st.error("Failed")
            st.write("Study and Retry")


def review_answers():
    """Display every question with the student's answer."""

    if st.session_state.show_results:

        for i in range(TOTAL_QUESTIONS):

            # --- Calculate Index Shift for Review ---
            if st.session_state.difficulty_level == "Medium":
                global_idx = i + 5
            elif st.session_state.difficulty_level == "Hard":
                global_idx = i + 10
            else:
                global_idx = i

            correct_answer = st.session_state.questions[global_idx][st.session_state.difficulty_level]["Correct Answer"]
            student_answer = st.session_state.student_answers[i]

            # Display question and answers
            st.write(f"Question {i + 1}: {st.session_state.questions[global_idx][st.session_state.difficulty_level]['Question']}")
            st.write(f"Student's Answer: {student_answer}")
            st.write(f"Correct Answer: {correct_answer}")

            # Show if the answer was correct
            if correct_answer == student_answer:
                st.success("Correct Answer")
            else:
                st.error("Wrong Answer")


# Add quiz questions only once
if len(st.session_state.questions) == 0:
    # EASY QUESTIONS
    add_questions(
        [
            "What is Egypt's capital?",
            "What is 4x4?",
            "What is Python?",
            "Where does Real Madrid play?",
            "What is the continent that Egypt is in?"
        ],
        [
            ['Cairo', 'Madrid', 'Paris', 'Giza'],
            ['16', '25', '34', '26'],
            ['Programming language', 'Database', 'Playground', 'Operating system'],
            ['Spain', 'France', 'Italy', 'Germany'],
            ['Africa', 'Asia', 'Europe', 'South America']
        ],
        ['Cairo', '16', 'Programming language', 'Spain', 'Africa'], 
        "Easy"
    )

    # MEDIUM QUESTIONS
    add_questions(
        [
            "Which planet is known as the Red Planet?",
            "What is the square root of 144?",
            "In Python, which keyword is used to define a function?",
            "How many players are on the field for one team in a standard soccer match?",
            "Which ocean is the largest in the world?"
        ],
        [
            ['Mars', 'Venus', 'Jupiter', 'Saturn'],
            ['12', '14', '10', '16'],
            ['def', 'func', 'function', 'define'],
            ['11', '10', '9', '12'],
            ['Pacific Ocean', 'Atlantic Ocean', 'Indian Ocean', 'Arctic Ocean']
        ],
        ['Mars', '12', 'def', '11', 'Pacific Ocean'], 
        "Medium"
    )

    # HARD QUESTIONS
    add_questions(
        [
            "What is the chemical symbol for Gold?",
            "Solve for x: 2x + 7 = 19",
            "What is the time complexity of searching in a balanced Binary Search Tree (BST)?",
            "Which country won the very first FIFA World Cup in 1930?",
            "What is the capital city of Australia?"
        ],
        [
            ['Au', 'Ag', 'Gd', 'Go'],
            ['6', '5', '12', '7'],
            ['O(log n)', 'O(n)', 'O(n log n)', 'O(1)'],
            ['Uruguay', 'Argentina', 'Brazil', 'Italy'],
            ['Canberra', 'Sydney', 'Melbourne', 'Brisbane']
        ],
        ['Au', '6', 'O(log n)', 'Uruguay', 'Canberra'], 
        "Hard"
    )
# Display sidebar
display_sidebar()

# Quiz tab
with tab1:
    create_quiz()

# Results tab
with tab2:
    show_results()

# Review Answers tab
with tab3:
    review_answers()