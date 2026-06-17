import speech_recognition as sr
import os
import webbrowser
from openai import OpenAI

# =====================================================
# OLLAMA CLIENT
# =====================================================

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

WAKE_WORD = "hey buddy"

# =====================================================
# SYSTEM PROMPT
# =====================================================

SYSTEM_PROMPT = """
You are a personal study assistant for a final-year B.Tech CSE student preparing for placements.

His preferences:
- Explain using real-world analogies
- Keep responses short unless asked to elaborate
- Ask one MCQ at a time if quizzing
- Topics: Python, SQL, DBMS, DSA, Machine Learning, Data Analytics
- Dense structured answers preferred
- If user says 'next', move to next question
- If user says 'explain', go deeper
- No unnecessary filler

When explaining DSA:
- Intuition first
- Algorithm second
- Complexity third

When explaining SQL:
- Explain mentally first
- Query second

When explaining interview questions:
- Answer in interview style

Respond in plain text only.
"""

# =====================================================
# CONVERSATION MEMORY
# =====================================================

conversation_history = []

# =====================================================
# SPEAK
# =====================================================

def speak(text):
    clean = (
        text.replace("", "")
            .replace("#", "")
            .replace("-", "")
            .replace("`", "")
            .replace("'", "")
    )

    print(f"\nAssistant: {clean}\n")
    os.system(f"say '{clean}'")

# =====================================================
# LISTEN
# =====================================================

recognizer = sr.Recognizer()

def listen(timeout=1, phrase_limit=5):

    with sr.Microphone() as source:

        recognizer.adjust_for_ambient_noise(
            source,
            duration=0.5
        )

        print("Listening...")

        try:
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_limit
            )

            text = recognizer.recognize_google(audio)

            print(f"You: {text}")

            return text.lower()

        except sr.WaitTimeoutError:
            return ""

        except sr.UnknownValueError:
            return ""

        except Exception as e:
            print(f"Listen error: {e}")
            return ""

# =====================================================
# OLLAMA LLM CALL
# =====================================================

def ask_ai(user_input):

    conversation_history.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Keep only recent memory
    conversation_history[:] = conversation_history[-20:]

    response = client.chat.completions.create(
        model="qwen2.5:1.5b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ] + conversation_history,
        max_tokens=300,
        temperature=0.7
    )

    reply = response.choices[0].message.content

    conversation_history.append(
        {
            "role": "assistant",
            "content": reply
        }
    )

    return reply

# =====================================================
# COMMAND HANDLER
# =====================================================

def process_command(command):

    # -------------------------
    # Browser Commands
    # -------------------------

    if "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
        return

    if "open github" in command:
        webbrowser.open("https://github.com")
        speak("Opening GitHub")
        return

    if "open leetcode" in command:
        webbrowser.open("https://leetcode.com")
        speak("Opening LeetCode")
        return

    if "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google")
        return
    if "open facebook" in command:
        webbrowser.open("https://facebook.com")
        speak("Opening facebook")
        return
    if "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
        speak("Opening linkedin")
        return

    # -------------------------
    # Study Commands
    # -------------------------

    if command == "next":
        command = "Ask the next question."

    elif command == "explain":
        command = "Explain the previous answer in more detail."

    elif "quiz me" in command:
        command = "Quiz me on Python. Ask one MCQ only."

    elif "interview me" in command:
        command = "Take a placement interview for Python."

    elif "revise sql" in command:
        command = "Give me a quick SQL revision."

    elif "revise dbms" in command:
        command = "Give me a quick DBMS revision."

    elif "revise dsa" in command:
        command = "Give me a quick DSA revision."

    # -------------------------
    # Send To Ollama
    # -------------------------

    reply = ask_ai(command)
    speak(reply)

# =====================================================
# MAIN PROGRAM
# =====================================================

if __name__ == "__main__":

    speak(
        "Hello hannan your assistant is ready. Say hey buddy to start."
    )

    print(
        "Say 'hey buddy' to activate."
    )

    print(
        "Say 'quit' or 'exit' to stop.\n"
    )

    while True:

        # Wait for wake word
        wake = listen(
            timeout=4,
            phrase_limit=3
        )

        if not wake:
            continue

        # Exit
        if (
            "quit" in wake
            or "exit" in wake
            or "bye" in wake
        ):
            speak(
                "Closing. Good luck with placements."
            )
            break

        # Wake Word
        if "buddy" in wake:

            speak("Yeah?")

            command = listen(
                timeout=6,
                phrase_limit=15
            )

            if not command:
                speak("Didn't catch that.")
                continue

            if (
                "quit" in command
                or "exit" in command
                or "bye" in command
            ):
                speak(
                    "Closing. Good luck with placements."
                )
                break

            process_command(command)