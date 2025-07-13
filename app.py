import streamlit as st
import math

# Set page config
st.set_page_config(
    page_title="Calculator App",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
.calculator-title {
    text-align: center;
    color: #2E86AB;
    font-size: 2.5rem;
    margin-bottom: 2rem;
}

.result-display {
    background-color: #"#000000";
    padding: 20px;
    border-radius: 10px;
    font-size: 1.5rem;
    font-weight: bold;
    text-align: right;
    margin-bottom: 20px;
    border: 2px solid #ddd;
}

.stButton > button {
    width: 100%;
    height: 60px;
    font-size: 1.2rem;
    font-weight: bold;
    border-radius: 8px;
    border: none;
    margin: 2px;
}

.stButton > button:hover {
    background-color: #2E86AB;
    color: white;
}

.operation-button {
    background-color: #A23B72 !important;
    color: white !important;
}

.clear-button {
    background-color: #F18F01 !important;
    color: white !important;
}

.equals-button {
    background-color: #C73E1D !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="calculator-title">🧮 Calculator App</h1>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'display' not in st.session_state:
        st.session_state.display = "0"
    if 'previous_input' not in st.session_state:
        st.session_state.previous_input = ""
    if 'operation' not in st.session_state:
        st.session_state.operation = ""
    if 'waiting_for_number' not in st.session_state:
        st.session_state.waiting_for_number = False

    # Display screen
    st.markdown(f'<div class="result-display">{st.session_state.display}</div>', unsafe_allow_html=True)
    
    # Create calculator layout
    col1, col2, col3, col4 = st.columns(4)
    
    # Row 1: Clear, operations
    with col1:
        if st.button("C", key="clear"):
            clear_all()
    
    with col2:
        if st.button("⌫", key="backspace"):
            backspace()
    
    with col3:
        if st.button("√", key="sqrt"):
            calculate_sqrt()
    
    with col4:
        if st.button("÷", key="divide"):
            set_operation("÷")
    
    # Row 2: 7, 8, 9, ×
    with col1:
        if st.button("7", key="7"):
            input_number("7")
    
    with col2:
        if st.button("8", key="8"):
            input_number("8")
    
    with col3:
        if st.button("9", key="9"):
            input_number("9")
    
    with col4:
        if st.button("×", key="multiply"):
            set_operation("×")
    
    # Row 3: 4, 5, 6, −
    with col1:
        if st.button("4", key="4"):
            input_number("4")
    
    with col2:
        if st.button("5", key="5"):
            input_number("5")
    
    with col3:
        if st.button("6", key="6"):
            input_number("6")
    
    with col4:
        if st.button("−", key="subtract"):
            set_operation("−")
    
    # Row 4: 1, 2, 3, +
    with col1:
        if st.button("1", key="1"):
            input_number("1")
    
    with col2:
        if st.button("2", key="2"):
            input_number("2")
    
    with col3:
        if st.button("3", key="3"):
            input_number("3")
    
    with col4:
        if st.button("+", key="add"):
            set_operation("+")
    
    # Row 5: 0, ., =
    with col1:
        if st.button("0", key="0"):
            input_number("0")
    
    with col2:
        if st.button(".", key="decimal"):
            input_decimal()
    
    with col3:
        if st.button("±", key="plus_minus"):
            toggle_sign()
    
    with col4:
        if st.button("=", key="equals"):
            calculate_result()
    
    # Scientific functions section
    st.markdown("### Scientific Functions")
    sci_col1, sci_col2, sci_col3, sci_col4 = st.columns(4)
    
    with sci_col1:
        if st.button("sin", key="sin"):
            calculate_trig("sin")
    
    with sci_col2:
        if st.button("cos", key="cos"):
            calculate_trig("cos")
    
    with sci_col3:
        if st.button("tan", key="tan"):
            calculate_trig("tan")
    
    with sci_col4:
        if st.button("log", key="log"):
            calculate_log()
    
    # Additional functions
    func_col1, func_col2, func_col3, func_col4 = st.columns(4)
    
    with func_col1:
        if st.button("x²", key="square"):
            calculate_square()
    
    with func_col2:
        if st.button("x³", key="cube"):
            calculate_cube()
    
    with func_col3:
        if st.button("1/x", key="reciprocal"):
            calculate_reciprocal()
    
    with func_col4:
        if st.button("π", key="pi"):
            input_pi()

def clear_all():
    st.session_state.display = "0"
    st.session_state.previous_input = ""
    st.session_state.operation = ""
    st.session_state.waiting_for_number = False

def backspace():
    if st.session_state.display != "0" and len(st.session_state.display) > 1:
        st.session_state.display = st.session_state.display[:-1]
    else:
        st.session_state.display = "0"

def input_number(number):
    if st.session_state.waiting_for_number or st.session_state.display == "0":
        st.session_state.display = number
        st.session_state.waiting_for_number = False
    else:
        st.session_state.display += number

def input_decimal():
    if st.session_state.waiting_for_number:
        st.session_state.display = "0."
        st.session_state.waiting_for_number = False
    elif "." not in st.session_state.display:
        st.session_state.display += "."

def toggle_sign():
    if st.session_state.display != "0":
        if st.session_state.display.startswith("-"):
            st.session_state.display = st.session_state.display[1:]
        else:
            st.session_state.display = "-" + st.session_state.display

def set_operation(op):
    if st.session_state.operation and not st.session_state.waiting_for_number:
        calculate_result()
    
    st.session_state.previous_input = st.session_state.display
    st.session_state.operation = op
    st.session_state.waiting_for_number = True

def calculate_result():
    if st.session_state.operation and st.session_state.previous_input:
        try:
            prev_num = float(st.session_state.previous_input)
            current_num = float(st.session_state.display)
            
            if st.session_state.operation == "+":
                result = prev_num + current_num
            elif st.session_state.operation == "−":
                result = prev_num - current_num
            elif st.session_state.operation == "×":
                result = prev_num * current_num
            elif st.session_state.operation == "÷":
                if current_num == 0:
                    st.session_state.display = "Error"
                    return
                result = prev_num / current_num
            
            # Format result
            if result == int(result):
                st.session_state.display = str(int(result))
            else:
                st.session_state.display = str(round(result, 10))
            
            st.session_state.operation = ""
            st.session_state.previous_input = ""
            st.session_state.waiting_for_number = True
            
        except ValueError:
            st.session_state.display = "Error"

def calculate_sqrt():
    try:
        num = float(st.session_state.display)
        if num < 0:
            st.session_state.display = "Error"
        else:
            result = math.sqrt(num)
            st.session_state.display = str(round(result, 10))
    except ValueError:
        st.session_state.display = "Error"

def calculate_trig(func):
    try:
        num = float(st.session_state.display)
        radians = math.radians(num)  # Convert degrees to radians
        
        if func == "sin":
            result = math.sin(radians)
        elif func == "cos":
            result = math.cos(radians)
        elif func == "tan":
            result = math.tan(radians)
        
        st.session_state.display = str(round(result, 10))
    except ValueError:
        st.session_state.display = "Error"

def calculate_log():
    try:
        num = float(st.session_state.display)
        if num <= 0:
            st.session_state.display = "Error"
        else:
            result = math.log10(num)
            st.session_state.display = str(round(result, 10))
    except ValueError:
        st.session_state.display = "Error"

def calculate_square():
    try:
        num = float(st.session_state.display)
        result = num ** 2
        st.session_state.display = str(round(result, 10))
    except ValueError:
        st.session_state.display = "Error"

def calculate_cube():
    try:
        num = float(st.session_state.display)
        result = num ** 3
        st.session_state.display = str(round(result, 10))
    except ValueError:
        st.session_state.display = "Error"

def calculate_reciprocal():
    try:
        num = float(st.session_state.display)
        if num == 0:
            st.session_state.display = "Error"
        else:
            result = 1 / num
            st.session_state.display = str(round(result, 10))
    except ValueError:
        st.session_state.display = "Error"

def input_pi():
    st.session_state.display = str(math.pi)

if __name__ == "__main__":
    main()